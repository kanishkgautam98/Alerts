from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import os, time, socket
from utils import checkInternetConnectivity
from django.conf import settings
from selenium.common.exceptions import TimeoutException


config = settings.CONFIG
class ScraperPersonal:
    
    def __init__(self, website='medium', driver = 'geckoDriver'):
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
        if not checkInternetConnectivity():
            self.driver.quit()
            return
        try:
            self.driver.set_page_load_timeout(20)
            self.driver.get(self.url)
        except TimeoutException as e:
            self.driver.close()
        self.driver.find_element_by_link_text("Sign in").click()
        self.addDelay(5)
        signInUsingGmailButton = self.driver.find_elements_by_class_name("button-label")
        if len(signInUsingGmailButton) == 0:
            signInUsingGmailButton = self.driver.find_element_by_link_text("Sign in with Google")
        else :
            signInUsingGmailButton = signInUsingGmailButton[0]
        
        signInUsingGmailButton.click()
        self.addDelay(5)
        email = self.driver.find_element_by_name("identifier")
        email.send_keys(self.email)
        email.send_keys(Keys.ENTER)
        
        self.addDelay(4)

        password = self.driver.find_element_by_name("password")
        password.send_keys(self.password)
        password.send_keys(Keys.ENTER)

        
    def getNotifications(self):
        if not checkInternetConnectivity():
            self.driver.quit()
            return        
        self.login()
        self.addDelay(10)
        self.driver.find_element_by_xpath('//*[@title="Notifications"]').click()
        self.addDelay(5)

        notifications = self.driver.find_element_by_class_name("notificationsList").find_elements_by_tag_name('li')
        notificationsList = []
        for li in notifications:
            self.driver.execute_script("arguments[0].scrollIntoView();", li)
            html = li.get_attribute('innerHTML')
            html = BeautifulSoup(html, 'html.parser')
            image = html.find('img', {'class' : 'avatar-image'})
            if image == None:
                break
            else :
                image = image['src']
            text = html.find('a', {'class': 'notificationsList-button'}).findAll(text=True)
            date = text.pop()
            text = "".join(text)
            notificationsList.append({
                'description' : text,
                'image': image,
                'date' : date
                })
        self.driver.quit()
        return notificationsList