from typing import List


class WordCounter:
    __relatedWords: List[str]
    __keyWord: str

    def __init__(self, keyWord: str):
        self.__keyWord = keyWord
        self.__relatedWords = []

    def addRelatedWord(self, word: str):
        self.__relatedWords.append(word)

    def getLenRelatedWords(self):
        return len(self.__relatedWords)

    def getKeyWord(self):
        return self.__keyWord

    def getRelatedWords(self):
        return self.__relatedWords
