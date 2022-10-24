from typing import Dict, Set, List
import logging
from WordInteractors.WordCollection import WordCollection


class WordDictionary:
    __wordCollections: Dict[int, WordCollection]
    __wordsInWordCollections: Set[str]
    __wordFile: str
    
    def __init__(self, wordFile: str):
        self.__wordFile = wordFile
        self.__parseData(self.__wordFile)

    def GetBestRandomGuess(self, hint: str) -> List[str]:
        hintLength: int = len(hint)
        if hintLength in self.__wordCollections and\
            self.__wordCollections[hintLength] is not None:
            # sanity check
            if self.__wordCollections[hintLength].getLenWords() != len(hint):
                raise Exception("List of word collection array improperly formed. "\
                                + f"Detected when broad indexing {hint}")
            return self.__wordCollections[hintLength].GetBroadGuessWords()
        return []

    def GetSpecificGuess(self, hint: str) -> List[str]:
        hintLength: int = len(hint)
        if hintLength in self.__wordCollections and \
                self.__wordCollections[hintLength] is not None:
            # sanity check
            if self.__wordCollections[hintLength].getLenWords() != len(hint):
                raise Exception("List of word collection array improperly formed. " \
                                + f"Detected when narrow indexing {hint}")
            return self.__wordCollections[hintLength].GetNarrowGuessWords(hint)
        return []

    def UpdateWordDictionary(self, newWord: str) -> None:
        if newWord.lower() in self.__wordsInWordCollections:
            word: str
            with open(self.__wordFile, 'a') as f:
                f.write(newWord)
        self.__parseData(self.__wordFile)

    def __parseData(self, wordFile: str) -> None:
        self.__wordsInWordCollections = set()
        self.__wordCollections = {}

        lengthWords: Dict[int, List[str]] = {}
        words: List[str] = []

        with open(self.__wordFile, 'r') as f:
            words = f.readline().split(',')

        for word in words:
            if word == '':
                continue
            newWord: str = word.lower()
            self.__wordsInWordCollections.add(newWord)
            wordLength: int = len(newWord)
            if wordLength not in lengthWords:
                lengthWords[wordLength] = []
            lengthWords[wordLength].append(newWord)

        for key, value in lengthWords.items():
            self.__wordCollections[key] = WordCollection(value)
            if key != self.__wordCollections[key].getLenWords():
                raise Exception("Sanity check failed, word Dictionary not constructed properly for"
                                + f" words of length {key}")
