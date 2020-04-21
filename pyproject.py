from selenium import webdriver
import selenium
from bs4 import BeautifulSoup
import requests
import time
#import re



def iq_game(name):
    r = requests.get('https://iqga.me/base/')     #заходим на сайт
    soup = BeautifulSoup(r.content, 'html.parser')
    
    links = soup.find_all("a")       #ищем <a>

    for link in links:                #ищем ссылку на турнир(root_url)
        if name in link:
            root_url = 'https://iqga.me'+link.get("href")

    r = requests.get(root_url)        #ищем вопросы по очереди
    soup = BeautifulSoup(r.content, 'html.parser')
    k = 1
    f = 1
    a = ' '
    
    while f != 0:
        r = requests.get(root_url)        #ищем вопросы по очереди
        soup = BeautifulSoup(r.content, 'html.parser')
        links = soup.find_all("a")
        for link in links:
            if 'Вопрос ' + str(k) in link and 'Вопрос ' + str(k) + '1' not in link and 'Вопрос ' + str(k) + '2' not in link and 'Вопрос ' + str(k) + '3' not in link and 'Вопрос ' + str(k) + '4' not in link and 'Вопрос ' + str(k) + '5' not in link and 'Вопрос ' + str(k) + '6' not in link and 'Вопрос ' + str(k) + '7' not in link and 'Вопрос ' + str(k) + '8' not in link and 'Вопрос ' + str(k) + '9' not in link and 'Вопрос ' + str(k) + '0' not in link:
                y = link.get("href")
        if a == y:
            f = 0

        a = y
        new_root = 'https://iqga.me'+y
        qwest = requests.get(new_root)     #идем по ссылке вопроса  
        soup = BeautifulSoup(qwest.content, 'html.parser')
        t = soup.find_all("p")[3]
        print(t, end='\n')
        p = soup.find_all("p")[4]
        k += 1
        print(p, end='\n')
        
    
def db_cgk(name):
    driver = webdriver.Safari()                      #
    driver.get('https://db.chgk.info/search/tours')
    id_box = driver.find_element_by_name("keys")
    id_box.send_keys(name)
    search_button = driver.find_element_by_id("edit-submit-1")
    search_button.click()
    time.sleep(7)
    url = driver.current_url
    print(url)

    answ = requests.get(url)                          #
    driver.quit()
    soup = BeautifulSoup(answ.content, 'html.parser')
    links = soup.find_all("a")
    for link in links:
        if '/tour/' in link.get("href"):
            root_url = 'https://db.chgk.info' + link.get("href")
            print(root_url)


    
    
    
    
    





    
#iq_game('Лига вузов. V тур')
db_cgk('Синхронный турнир «Вторая октава: Игра в стиле блюз»')


    
