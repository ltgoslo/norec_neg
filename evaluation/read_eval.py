import re
import numpy as np
# import itertools as it
from tabulate import tabulate


name_map = {"point_to_root": "Point-to-root",
            "head_first": "Head-first",
            "head_first-inside_label": "+inlabel",
            "head_final": "Head-final",
            "head_final-inside_label": "+inlabel",
            "head_final-inside_label-dep_edges": "Dep. edges",
            "head_final-inside_label-dep_edges-dep_labels": "Dep. labels"
            }

categories = ("Cues",
              "Scopes(cue match)",
              "Scopes(no cue match)",
              "Scope tokens(no cue match)",
              "Full negation"
              )

experiments = ["point_to_root", "head_first", "head_first-inside_label",
               "head_final", "head_final-inside_label",
               "head_final-inside_label-dep_edges",
               "head_final-inside_label-dep_edges-dep_labels"]


def precision(tp: int, fp: int) -> float:
    return tp / (tp + fp + float(1e-6))


def recall(tp: int, fn: int) -> float:
    return tp / (tp + fn + float(1e-6))


def fscore(p: float, r: float) -> float:
    return (2 * p * r) / (p + r + float(1e-6))


def read_eval_output(fn: str):
    results = {}
    with open(fn) as fh:
        for _line in fh:
            line = _line.split(":")
            category = line[0]
            if category in categories:
                numbers = [int(x.group(0)) for x in re.finditer(r"\d+", _line)][:5]
                gold, system, tp, fp, fn = numbers
                results[category] = {"gold": gold,
                                     "system": system,
                                     "tp": tp,
                                     "fp": fp,
                                     "fn": fn}
                if category == "Full negation":
                    return results


def main(folder: str, devtest: str):
    metrics = []
    for setup in experiments:
        print(setup)
        metric = []
        metric.append("")
        metric.append(name_map[setup])

        # sub_metrics = {m: [] for m in it.product(categories, ["Prec", "Rec", "F1"])}
        sub_metrics = {m: [] for m in categories}
        for i in [1, 2, 3, 4, 5]:
            results = read_eval_output(f"{folder}/{setup}/{devtest}.run_{i}.eval")
            for k, v in results.items():
                p = precision(v["tp"], v["fp"])
                r = recall(v["tp"], v["fn"])
                f = fscore(p, r)
                # sub_metrics[(k, "Prec")].append(p)
                # sub_metrics[(k, "Rec")].append(r)
                # sub_metrics[(k, "F1")].append(f)
                sub_metrics[k].append(f)
        # for m in categories:
        for m in sub_metrics.keys():
            arr = np.array(sub_metrics[m]) * 100
            # print("{:<40}\t{:.2f}\t{:.2f}\t{:.2f}\t{:.2f}".format(str(m), arr.max(), arr.min(), arr.mean(), arr.std()))
            mean = arr.mean()
            # print(arr)
            sd = arr.std()
            metric.append("{0:.1f} ({1:.1f})".format(mean, sd))
        metrics.append(metric)
        print()
    print(tabulate(metrics, headers=categories, tablefmt="latex", floatfmt="0.1f"))


if __name__ == "__main__":
    import sys
    main(sys.argv[1], sys.argv[2])
