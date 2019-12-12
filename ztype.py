from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from string import ascii_lowercase

b = webdriver.Chrome()
b.get('https://zty.pe/')

actions = ActionChains(b)

input('Click START GAME in the browser, then press any key to begin...:')

# actions.key_down(Keys.ENTER).perform()

while True:
  for letter in ascii_lowercase:
    actions.key_down(letter).perform()
