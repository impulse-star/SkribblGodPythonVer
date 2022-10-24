from typing import List

from copy import deepcopy
from .WordCounter import *


class WordCollection:
    __lengthOfWords: int
    __words: List[List[str]]

    def __init__(self, words: List[str]):
        self.__words = []
        if len(words) == 0:
            raise Exception("Invalid list of words given.")
        self.__lengthOfWords = len(words[0])
        self.__ProperlyProcessWords(words[:])

    def GetBroadGuessWords(self) -> List[str]:
        words = deepcopy(self.__words)
        returnWords: List[str] = list(map(lambda word: word[0], words))
        return returnWords

    def GetNarrowGuessWords(self, word: str) -> List[str]:
        for listOfWord in self.__words:
            if listOfWord[0] == word:
                return listOfWord[1:]
        raise Exception(f"Error, given word \"{word}\" is not located in WordCollection")

    def __ProperlyProcessWords(self, listOfWords: List[str]) -> None:
        if len(listOfWords) == 0:
            return
        words2: List[str] = deepcopy(listOfWords)
        temp: List[WordCounter] = []

        for word in listOfWords:
            wordCounter: WordCounter = WordCounter(word)
            for otherWord in listOfWords:
                if word != otherWord and self.__isWordSimilar(word, otherWord):
                    wordCounter.addRelatedWord(otherWord)
            temp.append(wordCounter)

        best: WordCounter = temp[0]
        for wordcounter in temp:
            if wordcounter.getLenRelatedWords() > best.getLenRelatedWords():
                best = wordcounter

        final: List[str] = [best.getKeyWord()]
        final.extend(best.getRelatedWords())
        self.__words.append(final)
        for word in final:
            if word in words2:
                words2.remove(word)
        self.__ProperlyProcessWords(words2)

    def __isWordSimilar(self, word1: str, word2: str) -> bool:
        diffCount = 0
        for i in range(len(word1)):
            if word1[i] != word2[i]:
                diffCount += 1

            if diffCount > 1:
                return False

        return True

    def getLenWords(self):
        return self.__lengthOfWords
