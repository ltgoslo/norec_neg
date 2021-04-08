#!/usr/bin/env python
# coding: utf-8

import numpy as np
import time
import subprocess
from typing import Iterable, List
from read_eval import read_eval_output
from tqdm import tqdm


def shell_command(command):
    peval = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
    stdout, stderr = peval.communicate()
    return stdout.decode("utf-8")


def read_starsem(fn: str) -> Iterable[List[str]]:
    sentence = []
    with open(fn) as fh:
        for line in fh:
            if line == "\n":
                yield sentence
                sentence = []
            else:
                sentence.append(line.split())


def eval_singles(gold: Iterable[str], pred: Iterable[str]):
    tpfpfns = []
    for g, p in tqdm(zip(gold, pred), total=len(gold)):
        with open("g.tmp", "w") as gh, open("p.tmp", "w") as ph:
            print("\n".join(["\t".join(x) for x in g]), end="\n\n", file=gh)
            print("\n".join(["\t".join(x) for x in p]), end="\n\n", file=ph)
        peval = shell_command("perl eval.cd-sco.pl -g g.tmp -s p.tmp".split())
        results = read_eval_output(peval.split("\n"))
        tpfpfns.append(np.array([[v["tp"], v["fp"], v["fn"]] for v in
                                 results.values()]
                                )
                       )
    return np.array(tpfpfns)


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def prec(x, i, j):
    return np.divide(x[..., i], (x[..., i] + x[..., j] + 1e-6))


def rec(x, i, j):
    return np.divide(x[..., i], (x[..., i] + x[..., j] + 1e-6))


def fscore(p, r):
    return np.divide(2 * p * r, (p + r + 1e-6))


def compute_scores(scores, counts, p, r, x):
    scores[:, x] = fscore(p, r)
    return scores


def fill_scores(scores, evals, debug=False):
    eval_cnts = evals.shape[0] if len(evals.shape) > 2 else 1
    if eval_cnts == 1:
        a, b = evals.shape
        evals = np.reshape(evals, (1, a, b))
    for i in range(eval_cnts):
        scores[i, ..., 0] = prec(evals[i], 0, 1)
        scores[i, ..., 1] = rec(evals[i], 0, 2)
        scores[i, ..., 2] = fscore(scores[i, ..., 0], scores[i, ..., 1])

        if debug:
            print(scores[i, ..., 0])
            print(scores[i, ..., 1])
            print(scores[i, ..., 2])
    return scores


def main(b, folder, devtest, setup1, setup2, debug=False):

    if debug:
        s = time.time()

    r = 5
    gold = list(read_starsem(f"{folder}/neg_{devtest}.starsem"))
    pred1 = []
    pred2 = []
    for i in range(1, r+1):
        print(f"Run: {i}")
        p1_fn = f"{folder}/{setup1}/{devtest}.starsem.{i}.pred"
        p2_fn = f"{folder}/{setup2}/{devtest}.starsem.{i}.pred"
        p1 = read_starsem(p1_fn)
        p2 = read_starsem(p2_fn)
        pred1.extend(eval_singles(gold, p1))
        pred2.extend(eval_singles(gold, p2))

    # number of runs
    n = len(gold)
    b = int(b)

    M1 = np.array(pred1)
    M2 = np.array(pred2)

    if debug:
        print(f"reading in data {time.time() - s}")
        s = time.time()

    # sample 'b' ids for a test set of size 'n' with 'r' runs
    # np.random.choice(n * r, n*b).reshape(b, n)

    if debug:
        print(f"data as matrix {time.time() - s}")
        s = time.time()

    # sample_ids samples b datasets of size n with indices ranging the five
    # runs creating a sample out of all runs
    sample_ids = np.random.choice(n * r, n*b).reshape(b, n)

    # fill a zero matrix with how often each sentence was drawn in one sample
    samples = np.zeros((n*r, b))
    for j in range(b):
        for i in range(n):
            samples[sample_ids[j, i], j] += 1

    if debug:
        print(f"get samples {time.time() - s}")
        s = time.time()

    # get the counts for the sample
    # Mx has the counts per sentence and samples chooses how often each sample
    # is taken resulting in a matrix of b rows with sums of tp, fp, fn etc.
    evals1 = (np.einsum('ijk,il->ljk', M1, samples))
    evals2 = (np.einsum('ijk,il->ljk', M2, samples))

    if debug:
        print(f"extract sample counts {time.time() - s}")
        s = time.time()

    # compute the eval measures for each row/sample
    sample_scores1 = fill_scores(np.zeros((b, M1.shape[1], M1.shape[2])), evals1, False)
    sample_scores2 = fill_scores(np.zeros((b, M2.shape[1], M2.shape[2])), evals2, False)

    if debug:
        print(f"compute scores {time.time() - s}")
        s = time.time()
        print(np.sum(M1, axis=0))

    # scores for the dataset across all runs
    true_scores1 = fill_scores(np.zeros((1, M1.shape[1], M1.shape[2])), np.sum(M1, axis=0))
    true_scores2 = fill_scores(np.zeros((1, M2.shape[1], M2.shape[2])), np.sum(M2, axis=0))

    # bootstrap scores
    deltas = true_scores1 - true_scores2
    deltas *= 2

    diffs = sample_scores1 - sample_scores2
    diffs_plus = np.where(diffs >= 0, diffs, 0)
    diffs_minus = np.where(diffs < 0, diffs, 0)

    if debug:
        print("sample_scores1")
        print(sample_scores1)
        print("sample_scores2")
        print(sample_scores2)
        print("diffs")
        print(diffs)
        print("diffs_plus")
        print(diffs_plus)
        print("diffs_minus")
        print(diffs_minus)

    deltas_plus = np.where(deltas > 0, deltas, np.float("inf"))

    deltas_minus = np.where(deltas < 0, deltas, -np.float("inf"))
    s1 = np.sum(diffs_plus > deltas_plus, axis=0)
    s2 = np.sum(diffs_minus < deltas_minus, axis=0)

    if debug:
        print(f"the rest {time.time() - s}")

        print(true_scores1)
        print(true_scores2)

        print(s1 / b)
        print(s2 / b)

        print()
    s1 = s1 / b
    s2 = s2 / b
    end = color.END

    print(f"{color.BOLD}{color.BLUE}{setup1} || {color.RED}{setup2}{color.END}")
    _m, _p, _r, _f = "Measure Precision Recall Fscore".split()
    print(f"{_m:<15}{_p:<21}\t{_r:<21}\t{_f:<21}")
    for i, name in enumerate("CUE SM ST FN".split()):
        print(f"{name:<13}:", end=" ") 
        for j, mea in enumerate("Prec. Rec. Fscore".split()):
            x = true_scores1[0][i][j]
            y = true_scores2[0][i][j]
            z = s1[i][j] if x > y else s2[i][j]
            if z < 0.05 and x > y:
                bold = color.BLUE
            elif z < 0.05 and y > x:
                bold = color.RED
            else:
                bold = color.END
            # print(f"{bold}{name:<13}: {x:.2%}\t{y:.2%}\t{z:.4f}{end}", end="\t")
            print(f"{bold}{x:.2%}\t{y:.2%}\t{z:.4f}{end}", end="\t")
        print()

    print()
    if debug:
        for r_i in [1, 2, 3, 4, 5]:
            print(r_i)
            # scores for the dataset across all runs (i-1)*int(n/5):int(n/5)*i
            print(M1.shape)
            m1 = M1[(r_i-1)*int(n):int(n)*r_i, ...]
            m2 = M2[(r_i-1)*int(n):int(n)*r_i, ...]
            print(m1.shape)
            print(np.sum(m1, axis=0))
            print(np.sum(m2, axis=0))
            true_scores1 = fill_scores(np.zeros((1, m1.shape[1], m1.shape[2])), np.sum(m1, axis=0))
            true_scores2 = fill_scores(np.zeros((1, m2.shape[1], m2.shape[2])), np.sum(m2, axis=0))
            # true_scores1 = fill_scores(np.zeros((1, 8)), np.sum(M1[(r_i-1)*int(N/r):int(N/r)*r_i, :], axis=0))
            # true_scores2 = fill_scores(np.zeros((1, 8)), np.sum(M2[(r_i-1)*int(N/r):int(N/r)*r_i, :], axis=0))
            print(true_scores1)
            print(true_scores2)


if __name__ == "__main__":
    import sys
    b = 10e5
    debug = True
    folder = sys.argv[1]
    devtest = sys.argv[2]
    setup1 = sys.argv[3]
    setup2 = sys.argv[4]

    main(b, folder, devtest, setup1, setup2, debug=debug)
