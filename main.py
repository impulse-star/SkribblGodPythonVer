from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.wait import WebDriverWait
import PySimpleGUI as sg

from GamePlayer import GamePlayer

def main():
    layout = [
        [
            sg.Text("URL")
        ],
        [
            sg.In(size=(25, 1), enable_events=True, key="-LABEL1-")
        ],
        [
            sg.Button(button_text="Join", key="-BUTTON1-"),
        ]
    ]

    window = sg.Window("SkribblGod", layout)

    while True:
        event, values = window.read()
        if event == "-LABEL1-":
            pass
        if event == "-BUTTON1-":
            print("Skribblbot Starting")
            service: Service = Service(executable_path='./ExternalDependencies/geckodriver.exe')
            driver: webdriver = webdriver.Firefox(service=service)
            url: str = values["-LABEL1-"]
            wordFilePath: str = "./WordList.txt"
            driver.get(url)
            driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[2]/div[1]/form/button[1]").click()
            driver.implicitly_wait(5)
            WebDriverWait(driver, 5)
            gameplayer: GamePlayer = GamePlayer(driver, wordFilePath)
        if event == sg.WIN_CLOSED:
            break

    window.close()


if __name__ == '__main__':
    main()
