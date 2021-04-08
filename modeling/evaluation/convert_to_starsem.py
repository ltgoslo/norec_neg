import re
import json
import argparse
import numpy as np
from col_data import Sentence, read_col_data
from typing import Tuple, List, Iterable, Dict


prefixes = ['U', 'ikke-', 'in', 'mis', 'utenom', 'u']
suffixes = ['frie', 'fritt', 'fri', 'løse', 'løst', 'løs', 'tomme']
no_affix = ['Unntaket', 'Uten', 'fri', 'inga', 'ingen', 'ingenting', 'inget',
            'intet', 'mister', 'mistet', 'unngå', 'unngår', 'unntak',
            'unntaket', 'unntatt', 'utan', 'uteble', 'uteblir', 'uten']


def flatten(lst):
    return [item for sublist in lst for item in sublist]


def read_span(span_string: str) -> Tuple[int, int]:
    s, e = span_string.split(":")
    return int(s), int(e)


def multiword_span_to_idx(words: List[str],
                          spans: List[Tuple[int, int]],
                          span: Tuple[int, int]
                          ) -> Tuple[List[int], List[str]]:
    mws_idx = []
    mws_str = []
    words_str = " ".join(words)
    for i, (word, (start, end)) in enumerate(zip(words, spans)):
        # print(i, word, start, end, span)
        # normal scope
        if (start >= span[0] and end <= span[1]):
            mws_idx.append(i)
            mws_str.append(word)
        # scope is prefixed by cue
        elif (span[0] >= start and span[0] <= end):
            # print("yay", i, word, start, end, span)
            mws_idx.append(i)
            mws_str.append(words_str[span[0]:end])
        # scope is suffixed by cue
        elif (start >= span[0] and start <= span[1]):
            # print("wow", i, word, start, end, span)
            mws_idx.append(i)
            mws_str.append(words_str[start:span[1]])
    # print(mws_idx)
    return mws_idx, mws_str


def subword_span_to_idx(words: List[str],
                        spans: List[Tuple[int, int]],
                        span: Tuple[int, int]
                        ) -> int:
    for i, (word, (start, end)) in enumerate(zip(words, spans)):
        if start == span[0] or end == span[1]:
            return i
    raise IndexError("the given spans did not match to find an index")


def read_json(sen):
    sid = sen["sent_id"]
    # read the words and negations
    pattern = r"\S+"  # whitespace split
    words, spans = zip(*[(m.group(0), (m.start(0), m.end(0))) for m in
                         re.finditer(pattern, sen["text"])])
    negations = []
    for neg in sen["negations"]:
        cue_indices = [subword_span_to_idx(words, spans, read_span(x)) for x in
                       neg["Cue"][1]]
        cue_strings = neg["Cue"][0]
        cue_map = {}
        for i, c in zip(cue_indices, cue_strings):
            if len(c.split()) > 1:
                for ci, cx in enumerate(c.split()):
                    cue_map[i + ci] = cx
            else:
                cue_map[i] = c

        # cue_map = {i: c for i, c in zip(cue_indices, cue_strings)}
        try:
            # empty scopes
            inds, strs = zip(*[multiword_span_to_idx(words, spans,
                                                     read_span(x)) for x in
                               neg["Scope"][1]])
        except ValueError:
            inds, strs = [], []
        scope_indices = flatten(inds)
        scope_strs = flatten(strs)
        negations.append({"cue_map": cue_map,
                          "scope_indices": scope_indices,
                          "scope_strs": scope_strs
                          })
    return sid, words, negations


def json_dict_to_starsem(sen, stream=None) -> str:
    sid, words, negations = read_json(sen)
    has_neg = True if sen["negations"] else False
    out = []
    for i, tok in enumerate(sen["text"].split()):
        out.append(f"_\t{sid}\t{i}\t{tok}\t_\t_\t_\t")
        if not has_neg:
            out.append("***\n")
        else:
            # print(sen["negations"])
            for neg in negations:
                out.append(neg["cue_map"].get(i, "_") + "\t")
                if i in neg["scope_indices"]:
                    j = neg["scope_indices"].index(i)
                    ###
                    # affix
                    if i in neg["cue_map"] and tok not in no_affix:
                        form, (start, end) = affixer(tok)
                        if start == 0 and end != len(tok):  # prefix
                            # print(sentence.id, end="\t")
                            # print("prefix", tok, form, start, end, neg)
                            # print([(t.id, t.form) for t in sentence])
                            form = tok[end:]
                        elif start != 0 and end == len(tok):  # suffix
                            # print(sentence.id, end="\t")
                            # print("suffix", tok, form, start, end, neg)
                            # print([(t.id, t.form) for t in sentence])
                            form = tok[:start]
                        out.append(form + "\t")
                    ###
                    else:
                        out.append(neg["scope_strs"][j] + "\t")
                else:
                    out.append("_\t")
                out.extend(("_", "\t"))  # event remnant
            out[-1] = "\n"  # exchange last tab with newline
    return "".join(out)


def json_file_to_starsem(fn_in: str, fn_out: str) -> None:
    with open(fn_in) as fh_in, open(fn_out, "w") as fh_out:
        for line in json.load(fh_in):
            print(json_dict_to_starsem(line), file=fh_out)


def negation_matrix(sentence: Sentence) -> np.array:
    n = len(sentence) + 1
    matrix = np.empty((n, n), dtype=object)
    for token in sentence:
        dependent = token.id
        for head, label in token.scope:
            matrix[head, dependent] = label
    return matrix


def get_descendants(i: int,
                    matrix: np.array,
                    label: str,
                    visited=None
                    ) -> Iterable[int]:
    n = matrix.shape[1]
    if visited is None:
        visited = []
    else:
        yield i
        visited.append(i)
    for j in range(n):
        if j in visited:
            continue
        elif matrix[i, j] is not None and matrix[i, j].endswith(label):
            # print(f"inner: {i}-{label}>{j}")
            yield from get_descendants(j, matrix, label, visited)


def negations_from_matrix(matrix: np.array,
                          sentence: Sentence
                          ) -> Dict[int, Dict[str, List[int]]]:
    root_cues = [i for i in range(matrix.shape[1]) if matrix[0, i] == "cue"]
    negations: Dict[int, Dict[str, List[int]]] = {r: {} for r in root_cues}
    for rc in root_cues:
        cue_desc = [rc] + list(get_descendants(rc, matrix, "cue"))
        scope_desc = list(get_descendants(rc, matrix, "scope"))
        # print(scope_desc)
        negations[rc]["Cue"] = [i for i in cue_desc]
        negations[rc]["Scope"] = [i for i in scope_desc]
    return negations


def affixer(word: str) -> Tuple[str, Tuple[int, int]]:
    pref_re = re.compile("^" + "|^".join(prefixes))
    suff_re = re.compile("$|".join(suffixes) + "$")
    pref = re.search(pref_re, word)
    if pref:
        return pref.group(0), pref.span()
    suff = re.search(suff_re, word)
    if suff:
        return suff.group(0), suff.span()
    return word, (0, len(word))


def coldata_to_starsem(fn_in: str, fn_out: str) -> None:
    with open(fn_out, "w") as fh_out:
        for sentence in read_col_data(fn_in):
            # print(sentence, file=fh_out)
            negs = negations_from_matrix(negation_matrix(sentence), sentence)
            out = []
            for token in sentence:
                out.append(
                    f"_\t{sentence.id}\t{token.id-1}\t{token.form}\t_\t_\t_\t"
                          )
                if not negs:
                    out.append("***\n")
                else:
                    out_neg = []
                    for neg in negs.values():
                        if token.id in neg["Cue"]:
                            if token.form not in no_affix:
                                form, span = affixer(token.form)
                            else:
                                form = token.form
                            out_neg.append(form)
                        else:
                            out_neg.append("_")
                        if token.id in neg["Scope"] and \
                           token.id not in neg["Cue"]:  # cue in other negation's scope
                            form = token.form
                            out_neg.append(form)
                        elif token.id in neg["Cue"]:
                            form, (start, end) = affixer(token.form)
                            if token.form in no_affix:
                                form = "_"
                            elif start == 0 and end != len(token.form):  # prefix
                                # print(sentence.id, end="\t")
                                # print("prefix", token.form, form, span, neg)
                                # print([(t.id, t.form) for t in sentence])
                                form = token.form[end:]
                            elif start != 0 and end == len(token.form):  # suffix
                                # print(sentence.id, end="\t")
                                # print("suffix", token.form, form, span, neg)
                                # print([(t.id, t.form) for t in sentence])
                                form = token.form[:start]
                            else:
                                form = "_"
                            out_neg.append(form)
                        else:
                            out_neg.append("_")
                        out_neg.append("_")  # event remnant
                    out.append("\t".join(out_neg))
                    out.append("\n")

            print("".join(out), file=fh_out)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Convert to starsem.')
    parser.add_argument('--in_file', type=str, help='file to read in')
    parser.add_argument('--out_file', type=str, help='file to  write to')
    parser.add_argument("--format", type=str, choices=["json", "conllu"],
                        help="original format (json|conllu)")

    args = parser.parse_args()

    return args


def main():
    _args = parse_args()
    args = vars(_args)
    if args["format"] == "json":
        json_file_to_starsem(args["in_file"], args["out_file"])
    elif args["format"] == "conllu":
        coldata_to_starsem(args["in_file"], args["out_file"])
    else:
        raise Exception("No such format known")


if __name__ == "__main__":
    main()
