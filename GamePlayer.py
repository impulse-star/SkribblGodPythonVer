from typing import List
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox import webdriver
from selenium.webdriver.remote.webelement import WebElement

from Enum.Status import Status
from WordInteractors.WordGuesser import WordGuesser


class GamePlayer:
    __driver: webdriver
    __wordGuesser: WordGuesser
    __basicDrawer: None
    __playerIdentifier: str = "\w*\(You\)\w*"

    def __init__(self, driver: webdriver, wordFile: str):
        self.__driver = driver
        self.__wordGuesser = WordGuesser(self, driver, wordFile)
        # todo make this a real class! :)
        self.__basicDrawer = None
        self.__runGamePlayer()

    def GetStatus(self) -> Status:
        print("proceeding to find status")
        if self.__driver.find_element(By.ID, "overlay").is_displayed():
            print("were between rounds")
            self.__wordGuesser.exaustedGuesses = False
            return Status.BetweenRounds
        print("not between rounds")
        if not self.__driver.find_element(By.ID, "screenGame").is_displayed():
            print("were not playing")
            return Status.NotPlaying
        print("not avoiding playing")
        if self.__driver.find_element(By.CLASS_NAME, "containerToolbar").is_displayed():
            print("were drawing")
            return Status.Drawing
        print("not drawing.")
        elements: List[WebElement] = self.__driver.find_elements(
            By.CSS_SELECTOR, ".player.guessedWord")
        print("time to iterate through the elements")

        for element in elements:
            print(f"searching through element: element")
            if re.search(self.__playerIdentifier,
                         element.find_element(By.CLASS_NAME, "name").get_attribute("textContent")):
                print("were idle")
                return Status.Idle
        print("not idle")
        return Status.Guessing

    def __runGamePlayer(self) -> None:
        print("skribblgod now running")
        while True:
            status: Status = self.GetStatus()
            print(f"status is: {status}")

            if status == Status.Drawing:
                # not implemented
                pass
            elif status == Status.Guessing:
                self.__wordGuesser.Guess()
            elif status == Status.Idle:
                # dont do anything
                pass
            elif status == Status.NotPlaying:
                # dont do anything
                pass
            elif status == Status.BetweenRounds:
                # todo collect words maybe here
                pass
            else:
                raise Exception("Error, Invalid GamePlayer status obtained.")
            self.__wordGuesser.exaustedGuesses = False

    def __pullNewWords(self) -> None:
        # this is todo in the codebase
        pass