from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import os, time, socket, re
from selenium.common.exceptions import TimeoutException
from django.conf import settings
from utils import checkInternetConnectivity


config = settings.CONFIG

class youtubeScraper:

    def __init__(self, website='youtube', driver = 'geckoDriver'):
        #website specific details
        self.url = config.get(website).get('url')
        self.alternateUrl = config.get(website).get('alternateUrl')
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

    def alternateLogin(self, website = 'stackoverflow'):
        self.driver.get(self.alternateUrl)
        self.driver.find_element_by_link_text("Log in").click()
        self.addDelay(5)
        self.driver.find_element_by_xpath('//*[@id="openid-buttons"]/button[1]').click()
        self.addDelay(5)
        email = self.driver.find_element_by_xpath('//*[@id="identifierId"]')
        print(email.get_attribute('innerHTML'))
        email.send_keys(self.email)
        email.send_keys(Keys.ENTER)
        self.addDelay(4)
        password = self.driver.find_element_by_name("password")
        password.send_keys(self.password)
        password.send_keys(Keys.ENTER)
        self.addDelay(10)

    def login(self):
        if not checkInternetConnectivity():
            return
        self.alternateLogin()
        self.driver.get(self.url)
        self.addDelay(5)

    def getNotifications(self):
        if not checkInternetConnectivity():
            return
            
        self.login()
        self.driver.find_element_by_class_name("ytd-notification-topbar-button-renderer").click()
        self.addDelay(5)
        htmlElements = self.driver.find_elements_by_tag_name("ytd-notification-renderer")
        notifications = []

        for html in htmlElements:
            self.driver.execute_script("arguments[0].scrollIntoView();", html)
            html = html.get_attribute('innerHTML')
            soup = BeautifulSoup(html, 'html.parser')
            a = soup.find('a')
            videoLink = a['href']
            newDiv = a.find("div", {"id" : "new"})
            read = False
            if newDiv is None:
                read = True

            image = a.find("yt-img-shadow").find("img")["src"]
            time = a.find("div", {"class" :"text"}).find("div", {"class" : "metadata"}).findAll("yt-formatted-string",recursive = False)[-1].get_text()
            text = a.find("div", {"class" :"text"}).find("yt-formatted-string").get_text()
            thumbnail = a.find("div",{"class": "thumbnail-container"}).find("img")['src']
            print(time)
            notifications.append({

                'videoLink': videoLink,
                'read': read,
                'image': image,
                'time': time,
                'description': text,
                'thumbnail': thumbnail

            })
        self.driver.quit()
        return notifications