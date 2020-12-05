from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import os, time, socket, re
from utils import checkInternetConnectivity
from django.conf import settings
from selenium.common.exceptions import TimeoutException

config = settings.CONFIG

class linkedInScraper:

    def __init__(self, website='linkedIn', driver = 'geckoDriver'):
        #website specific details
        self.url = config.get(website).get('url')
        self.email = config.get(website).get('email')
        self.password = config.get(website).get('password')


        #firefox specific details
        options = Options()
        options.add_argument("--headless")
        # options.add_argument('--no-sandbox')
        options.binary_location = "/usr/bin/firefox"


        #Firefox driver
        self.driver =  webdriver.Firefox(executable_path = config.get(driver).get('path'), firefox_options = options)

    def addDelay(self,timeInSeconds = 1):
        time.sleep(timeInSeconds)

    def login(self):
        if not checkInternetConnectivity:
            return
        self.driver.get(self.url)
        email = self.driver.find_element_by_name("session_key")
        password = self.driver.find_element_by_name("session_password")

        email.send_keys(self.email)
        self.addDelay(3)
        password.send_keys(self.password)
        self.addDelay(3)
        password.send_keys(Keys.ENTER)

    def getNotifications(self):
        notifications = []
        if not checkInternetConnectivity:
            return notifications
        self.login()
        self.addDelay(8)
        self.driver.get(self.url + 'notifications')
        self.addDelay(4)
        element = self.driver.find_element_by_class_name('core-rail')
        html = element.get_attribute('innerHTML')
        soup = BeautifulSoup(html, 'html.parser')
        soup = soup.find('section')
        html = soup.findAll('div', id = re.compile('^ember\d+'), recursive = False)
        for element in html:
            if element.article is None or element.article.div is None:
                continue
            div = element.article.div
            divs = div.findAll('div', recursive = False)

            imageDiv = divs[0]
            img = imageDiv.find('img')
            if img == None:
                img = imageDiv.find('div',{'class': 'EntityPhoto-circle-4-ghost-person'})
                if img == None:
                    continue
                else :
                    img = ""
            else :
                img = img['src']
            contentDiv = divs[1]
            a = contentDiv.find('a', recursive = False)
            content = a.find('span', recursive = False).next_sibling.get_text(strip = True)

            date = divs[2].findAll('p')[-1]
            date = date.get_text(strip = True)
            notifications.append({'image': img, 'body':content, 'created':date, 'url': a['href']})

        self.driver.quit()
        return notifications