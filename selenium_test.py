from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def login_OFD(logn, pas):
    driver = webdriver.Chrome()
    driver.get("https://lk.platformaofd.ru/web/login")

    login = driver.find_element_by_name("j_username")
    login.send_keys(logn)
    pwd = driver.find_element_by_name("j_password")
    pwd.send_keys(pas)
    pwd.send_keys(Keys.RETURN)
