# PPLG.lib.Generate.py
# CodeWriter21

from typing import Iterable as _Iterable
from PPLG.lib.Generate_cy import extend_words, generate, change_case, replace

__all__ = ['extend_words', 'extend_words_iter', 'generate']


def extend_words_iter(words: _Iterable[str]):
    """
    Takes a sequence of words and extend them. Yields each of the words.

    :param words: Iterable[str]: A sequence of words to extend
    :return: Iterable[str]
    """
    output = set(words)
    for word in output:
        yield word
    for word in words:
        tmp = set()
        change_case(tmp, word)
        for w in tmp:
            if w not in output:
                output.add(w)
                yield w
    for word in output.copy():
        new_words = set()
        replace(new_words, word)
        for w in new_words:
            if w not in output:
                output.add(w)
                yield w
