from selenium import webdriver
import selenium
from bs4 import BeautifulSoup
import requests
import re
#multiproc для одновременного выполнения поиска пакета

def iq_game(name):
    w = []
    w_1 = []
    e = 1
    r = requests.get('https://iqga.me/base/')     #заходим на сайт
    soup = BeautifulSoup(r.content, 'html.parser')
    
    links = soup.find_all("a") #ищем <a>
    
    while True:
        h = 1
        for link in links: #ищем ссылку на турнир(root_url)
            if name in link:
                root_url = 'https://iqga.me'+link.get("href")
                e = 0
            if 'Вперед' in link:     #проверка других страниц
                new_url = 'https://iqga.me'+link.get("href")
                h = 0
        if e == 0:
            break
        r = requests.get(new_url)
        soup = BeautifulSoup(r.content, 'html.parser')
        links = soup.find_all("a")
        if h == 0:
            continue
        else:
            return w

    r = requests.get(root_url)        #ищем вопросы по очереди
    soup = BeautifulSoup(r.content, 'html.parser')
    k = 1
    f = 1
    a = ' '
    
    while f != 0:
        u = 0
        r = requests.get(root_url)        #ищем вопросы по очереди
        soup = BeautifulSoup(r.content, 'html.parser')
        links = soup.find_all("a")
        for link in links:
            if 'Вопрос ' + str(k) in link and 'Вопрос ' + str(k) + '1' not in link and 'Вопрос ' + str(k) + '2' not in link and 'Вопрос ' + str(k) + '3' not in link and 'Вопрос ' + str(k) + '4' not in link and 'Вопрос ' + str(k) + '5' not in link and 'Вопрос ' + str(k) + '6' not in link and 'Вопрос ' + str(k) + '7' not in link and 'Вопрос ' + str(k) + '8' not in link and 'Вопрос ' + str(k) + '9' not in link and 'Вопрос ' + str(k) + '0' not in link:
                y = link.get("href")
        if a == y:
            f = 0

        a = y
        new_root = 'https://iqga.me' + y
        qwest = requests.get(new_root)     #идем по ссылке вопроса  
        soup = BeautifulSoup(qwest.content, 'html.parser')
        t = soup.find_all("p")[3]
        if 'Раздаточный материал'in t.text:      #ищем ссылку на раздатку
            o = soup.find_all("p")[4]
            png_url = 'https://iqga.me' + o.a['href']
            t = soup.find_all("p")[5]
            p = soup.find_all("p")[6]
            quest = re.search(r'(\[.+?\]\n)?(.+)', t.text)
            w_1.append('Раздаточный материал')
            w_1.append(png_url)
            if quest.group(1) is True :
                w_1.append(quest.group(1))
            else:
                w_1.append(quest.group(0))
            w_1.append(p.text)
            w.append(w_1)
        else:
            p = soup.find_all("p")[4]
            quest = re.search(r'(\[.+?\]\n)?(.+)', t.text)
            if quest.group(1) is True :
                w_1.append(quest.group(1))
            else:
                w_1.append(quest.group(0))
            w_1.append(p.text)
            w.append(w_1)
        k += 1
        w_1 = []
    return w
            
def db_cgk(name):
    driver = webdriver.Safari()                      #заходим на сайт бд чгк и вбиваем название пакета в поиск
    driver.get('https://db.chgk.info/search/tours')
    id_box = driver.find_element_by_name("keys")
    id_box.send_keys(name)
    search_button = driver.find_element_by_id("edit-submit-1")
    search_button.click()
    time.sleep(7)
    url = driver.current_url
    #print(url)

    answ = requests.get(url)                          #вытаскиваем ссылку на пакет
    driver.quit()
    soup = BeautifulSoup(answ.content, 'html.parser')
    links = soup.find_all("a")
    for link in links:
        if '/tour/' in link.get("href"):
            root_url = 'https://db.chgk.info' + link.get("href")
            #print(root_url)


#def rand_q():
#def rating():
#def db_acc():
 
q = iq_game('Лига Сибири. V тур')
#db_cgk('Синхронный турнир «Вторая октава: Игра в стиле блюз»')
