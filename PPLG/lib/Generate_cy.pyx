# PPLG.lib.Generate.py
# CodeWriter21

from typing import Iterable as _Iterable, Set as _Set, Tuple as _Tuple, Union as _Union
from threading import Thread as _Thread

__all__ = ['extend_words', 'generate', 'change_case', 'replace']

_chs = {"a": "@4", "A": "@4", "s": "$5S", "S": "$5s", "i": "!1lI", "I": "!1li", "l": "!1iI", "1": "!ilI", "g": "9",
       "G": "6", "o": "0", "O": "0", "E": "3", "e": "3", "0": "Oo", "3": "E", "4": "Aa"}

cpdef void change_case(output: _Set[str], str word):
    """
    Changes a word's case and add it to an output set.
    
    :param output: Set[str]: A set to add words to
    :param word: str: The word to be changed and added to the output set.
    :return: None
    """
    cdef str ch
    output.add(word.lower())
    output.add(word.upper())
    output.add(word.swapcase())
    output.add(word.capitalize())

cpdef void replace(output: _Set[str], str word):
    """
    Takes a word and replaces some of its characters with some other characters using `_chs` dictionary
    
    :param output: Set[str]: A set to add words to
    :param word: str: The word to use in the function
    :return: None
    """
    cdef str ch
    for ch in _chs:
        for ch2 in _chs[ch]:
            output.add(word.replace(ch, ch2))

cpdef extend_words(words: _Iterable[str], int max_threads = 1):
    """
    Takes a sequence of words and extend them.
    
    :param words: Iterable[str]: A sequence of words to extend
    :param max_threads: int = 1: Maximum number of threads you want to use
    :return: Set[str]
    """
    output = set(words)
    cdef str word
    cdef int i = 0

    if max_threads < 2:
        for word in words:
            change_case(output, word)
        for word in output.copy():
            replace(output, word)
    else:
        threads = []
        for word in words:
            i = 0
            while max_threads <= len(threads):
                if i == len(threads):
                    i = 0
                if not threads[i].is_alive():
                    threads.pop(i)
                    break
                i += 1

            thread = _Thread(target=change_case, args=(output, word))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        threads.clear()
        for word in words:
            i = 0
            while max_threads <= len(threads):
                if i == len(threads):
                    i = 0
                if not threads[i].is_alive():
                    threads.pop(i)
                    break
                i += 1

            thread = _Thread(target=replace, args=(output, word))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
    return output

def _generate(str word, output: _Set[str], methods1: _Iterable[str], methods2: _Iterable[str],
              int max_count = 0) -> _Union[None, Exception]:
    """
    Takes a word and two method-lists and generate passwords using the word and methods.

    :param word: str: A word for password generation.
    :param output: Set[str]: A set to add words to
    :param methods1: Iterable[str]: A sequence of methods
    :param methods2: Iterable[str]: A sequence of methods
    :param max_count: int = 0: Maximum number of passwords to generate.(Unlimited: 0)
    :return: Union[None, Exception]
    """
    cdef str m1, m2
    methods1 = set(methods1)
    methods2 = set(methods2)
    try:
        for m1 in methods1:
            output.add(word)
            output.add(word + m1)
            output.add(m1 + word)
            for m2 in methods2:
                output.add(word + m1 + m2)
                output.add(word + m2 + m1)
                output.add(m1 + word + m2)
                output.add(m1 + m2 + word)
                output.add(m2 + word + m1)
                output.add(m2 + m1 + word)
                output.add(word + m2)
                output.add(m2 + word)
            if 0 < max_count <= len(output):
                break
        return None
    except Exception as e:
        return e

def generate(words: _Iterable[str], methods1: _Iterable[str], methods2: _Iterable[str], int max_threads = 3,
             int max_count = 0) -> _Tuple[_Union[Exception, None], _Iterable[str]]:
    """
    Takes a list of words and two method-lists and generate passwords using the wordlist and methods.

    :param words: Iterable[str]: A list of words to generate passwords from
    :param methods1: Iterable[str]: A sequence of methods
    :param methods2: Iterable[str]: A sequence of methods
    :param max_threads: int = 3: Maximum number of threads you want to use
    :param max_count: int = 0: Maximum number of passwords to generate.(Unlimited: 0)
    :return: Tuple[Union[Exception, None], Iterable[str]]
    """
    words = set(words)
    methods1 = set(methods1)
    methods2 = set(methods2)
    output = set()
    cdef str word
    cdef int i = 0
    if max_threads < 2:
        try:
            for word in words:
                e = _generate(word, output, methods1, methods2, max_count)
                if e:
                    return e, output
                if 0 < max_count <= len(output):
                    break
        except MemoryError as e:
            return e, output
    else:
        threads = []
        try:
            for word in words:
                i = 0
                while max_threads < len(threads):
                    if i == len(threads):
                        i = 0
                    if not threads[i].is_alive():
                        threads.pop(i)
                        break
                    i += 1

                thread = _Thread(target=_generate, args=(word, output, methods1, methods2, max_count))
                threads.append(thread)
                thread.start()
            for thread in threads:
                thread.join()
        except MemoryError as e:
            return e, output

    if max_count > 0:
        return None, set(list(output)[:max_count])
    return None, output
