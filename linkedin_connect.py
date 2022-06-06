# Time      :   18/05/2022 8:01 PM
# Author    :   Vladimir Vasilenko
# File      :   linkedin_connect.py
import argparse
import time
from selenium import webdriver
import random
from selenium.webdriver.common.by import By

sign_in_url = 'https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin'


class SignInLocators:
    USERNAME_FIELD = (By.XPATH, '//input[@id="username"]')
    PWD_FIELD = (By.XPATH, '//input[@id="password"]')
    SIGN_IN_BUTTON = (By.XPATH, '//button[@class="btn__primary--large from__button--floating"]')
    USERNAME_ERROR = (By.XPATH, '//div[@error-for="username"]')
    PASSWORD_ERROR = (By.XPATH, '//div[@error-for="password"]')


class SearchPageLocators:
    CONNECT_BUTTON = (By.XPATH, '//span[@class="artdeco-button__text" and text()="Connect"]')
    SEND_BUTTON = (By.XPATH, '//span[@class="artdeco-button__text" and text()="Send"]')
    NEXT_BUTTON = (By.XPATH, '//button[@aria-label="Next"]')
    ONLY_EMAIL = (By.XPATH, '//label[@for="email"]')
    CLOSE_BUTTON = (By.XPATH, '//button[@data-test-modal-close-btn]')


class Linkedin:

    def __init__(self, login, password, connections, search_url, webdriver_path):
        self.login = login
        self.password = password
        self.connections = connections
        self.search_url = search_url
        self.webdriver_path = webdriver_path
        self.browser = webdriver.Chrome(webdriver_path)
        self.browser.implicitly_wait(5)
        self.sent_connections = 0

    def open_browser(self):
        self.browser.get(sign_in_url)
        return self

    def fill_creds(self):
        self.browser.find_element(*SignInLocators.USERNAME_FIELD).send_keys(self.login)
        self.browser.find_element(*SignInLocators.PWD_FIELD).send_keys(self.password)
        return self

    def click_sign_in(self):
        self.browser.find_element(*SignInLocators.SIGN_IN_BUTTON).click()
        if self.is_displayed(*SignInLocators.USERNAME_ERROR):
            print('>>> Couldn’t find a LinkedIn account associated with this email. Please try again.')
            self.browser.quit()
            exit(0)
        if self.is_displayed(*SignInLocators.PASSWORD_ERROR):
            print(">>> That's not the right password.")
            self.browser.quit()
            exit(0)
        time.sleep(random.randint(10, 15))
        self.browser.get(self.search_url)
        return self

    def is_displayed(self, *element):
        if self.is_present(*element):
            return self.browser.find_element(*element) \
                .is_displayed()
        else:
            return False

    def is_present(self, *element):
        return len(self.browser.find_elements(*element)) > 0

    def send_connect(self, connect_buttons):
        index = 0
        for button in connect_buttons:
            button.click()
            time.sleep(random.randint(1, 2))
            if self.is_displayed(*SearchPageLocators.ONLY_EMAIL):
                self.browser.find_element(*SearchPageLocators.CLOSE_BUTTON).click()
                continue
            self.browser.find_element(*SearchPageLocators.SEND_BUTTON).click()
            index += 1
            self.sent_connections += 1
            time.sleep(random.randint(1, 3))
        return index

    def connect_people(self):
        print('>>> Adding people...')
        index = 0

        while index < self.connections:
            connect_buttons = self.browser.find_elements(*SearchPageLocators.CONNECT_BUTTON)
            if len(connect_buttons) > self.connections - index:

                if index == 0:
                    index += self.send_connect(connect_buttons[:self.connections])
                else:
                    index += self.send_connect(connect_buttons[:self.connections - index])

            else:
                index += self.send_connect(connect_buttons)

            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)
            self.browser.find_element(*SearchPageLocators.NEXT_BUTTON).click()

        print(f'>>> {self.sent_connections} connections sent successfully')
        self.browser.quit()
        return self


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--login', help='Your LinkedIn login', type=str, required=True)
    parser.add_argument('--password', help='Your LinkedIn password', type=str, required=True)
    parser.add_argument('--connections', help='Count of needed connections per run', type=int, required=True)
    parser.add_argument('--search_url', help='Search url', type=str, required=True)
    parser.add_argument('--webdriver_path', help='Path to Webdriver', type=str, required=True)
    args = parser.parse_args()

    Linkedin(args.login, args.password, args.connections, args.search_url, args.webdriver_path).open_browser()\
        .fill_creds()\
        .click_sign_in()\
        .connect_people()
