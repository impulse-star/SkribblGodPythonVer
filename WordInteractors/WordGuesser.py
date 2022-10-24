import logging
import os
from time import sleep
from typing import Any, List, Set
import re

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox import webdriver
from selenium.webdriver.remote.webelement import WebElement

from Enum.Status import Status
from WordInteractors.WordDictionary import WordDictionary


class WordGuesser:
    __wordDictionary: WordDictionary
    __driver: webdriver
    __wordFilePath: str
    __hasNoHints: str = "[a-z]+"
    __isCloseGuessMessage: str = "color: rgb\(204, 204, 0\); font-weight: bold;"
    __gamePlayer = None

    __chars: List[chr] = [' ', '-', '\'']
    __autoHints: Set[chr] = set(__chars)

    exaustedGuesses: bool

    def __init__(self, gameplayer, driver: webdriver, wordFile: str):
        from Enum.Status import Status

        self.__gamePlayer = gameplayer
        self.__driver = driver
        self.__wordFilePath = wordFile
        self.__wordDictionary = WordDictionary(wordFile)
        self.exaustedGuesses = False

    def Guess(self) -> None:
        print("time to guess.")
        if self.exaustedGuesses:
            return
        numHints: int = 0
        wordToGuess: str = self.__getHint()
        guesses: List[str] = self.__wordDictionary.GetBestRandomGuess(wordToGuess)
        # TODO maybe this breaks because i pass wordTOGuess as value not ref
        self.__cleanGuesses(guesses, wordToGuess)
        print(f"guessing with list of words with length {len(guesses)}")
        print(self.__gamePlayer.GetStatus() == Status.Guessing and len(guesses) != 0)
        while (self.__gamePlayer.GetStatus() == Status.Guessing and len(guesses) != 0):
            wordToGuess = self.__getHint()
            hintsInWord: int = len(wordToGuess) - wordToGuess.count('_')
            print(f"word to guess: {wordToGuess}")
            if (numHints != hintsInWord):
                numHints = hintsInWord
                self.__filterGuesses(guesses, wordToGuess)
            print(f"time to guess: {wordToGuess} with {len(guesses)} possibilities")
            if len(guesses) != 0:
                print(f"submitting guess {guesses[0]}")
                guess: str = guesses[0]
                self.__submitGuess(guess)
                if (self.__isNarrowGuess(guess)):
                    self.__narrowGuess(guess)
                    self.exaustedGuesses = True
                    return
            guesses.remove(guesses[0])

        # todo check if bot is alive and if so set exaustedguesses to true


    def __cleanGuesses(self, guesses: List[str], wordToGuess: str) -> None:
        for guess in guesses:
            if self.__guessNotMatchesHint(guess, wordToGuess):
                guesses.remove(guess)

    def __guessNotMatchesHint(self, guess: str, wordToGuess: str) -> bool:
        for char in wordToGuess:
            if char == '_' and char in self.__autoHints:
                return True
        return False

    def __filterGuesses(self, guesses: List[str], wordToGuess: str) -> None:
        for guess in guesses:
            if self.__invalidGuessableWord(wordToGuess, guess):
                guesses.remove(guess)

    def __invalidGuessableWord(self, mainWord: str, possibleWord: str) -> bool:
        for index in range(len(mainWord)):
            if mainWord[index] != '_' and (possibleWord[index] != mainWord[index]):
                return True
        return False

    def __isNarrowGuess(self, guess: str) -> bool:
        messages: List[WebElement] = self.__driver.find_elements(By.TAG_NAME, "p")
        messages = messages[min(-10, len(messages) - 10):len(messages):1]
        narrowGuessConfirm: str = f"'{guess}' is close!"

        for element in messages:
            if re.search(self.__isCloseGuessMessage, element.get_attribute("style")):
                logging.info(element.find_element(By.TAG_NAME, "span").get_attribute("textContent"))
                if re.search(narrowGuessConfirm,
                             element.find_element(By.TAG_NAME, "span").get_attribute("textContent")):
                    return True

        return False

    def __narrowGuess(self, guess: str) -> None:
        wordToGuess: str = self.__getHint()
        guesses: List[str] = self.__wordDictionary.GetSpecificGuess(guess)
        self.__filterGuesses(guesses, wordToGuess)
        one: int = len(guesses)
        zero: str = self.__getHint()
        logging.info(f"{zero} was considered a guessed word, our dictionary found "
                     + str(one) + " similar word to it.")
        while (self.__gamePlayer.GetStatus() == Status.Guessing and len(guesses) != 0):
            self.__submitGuess(guesses[0])
            guesses.remove(guesses[0])

    def __submitGuess(self, guess: str) -> None:
        print("i am sending a guess.")
        sleep(1)
        self.__driver.find_element(By.ID, "inputChat").send_keys(guess)
        self.__driver.find_element(By.ID, "inputChat").send_keys(Keys.ENTER)
        sleep(1)

    def __getHint(self) -> str:
        return self.__driver.find_element(By.ID, "currentWord").get_attribute("textContent")

