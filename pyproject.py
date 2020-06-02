from selenium import webdriver
import selenium, requests, re, random, time
from bs4 import BeautifulSoup
import random
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)
import socks

TOKEN = 'Token'

def main():
    proxy_settings = {
        'proxy_url': 'socks5://orbtl.s5.opennetwork.cc:999',
        'urllib3_proxy_kwargs': {
            'username': '3571087',
            'password': 'iyyXSuti'
        }
    }
    updater = Updater(TOKEN, use_context=True, request_kwargs=proxy_settings)
    dp = updater.dispatcher  
    dp.add_handler(CommandHandler('start', command_start))
    dp.add_handler(CommandHandler('rand', command_rand))
    dp.add_handler(MessageHandler(Filters.text, search))
    updater.start_polling()
    updater.idle()

def command_start(update, context):
    update.message.reply_text('Привет!\nЯ бот, можешь попробовать команды\nЯ бы советовал попробовать написать "Лига Сибири. V тур" или /rand')

def search(update, context):
    message =  update.message.text
    a = iq_game(message)
    b = db_cgk(message)
    if a == [] and b == []:
        update.message.reply_text('такого пакета нет')
    elif a != []:
        for i in len(a):
            for y in len(a[i]):
                update.message.reply_text(a[i][y])
    elif a != []:
        for i in len(a):
            for y in len(a[i]):
                if y == len(a[i]-1):
                    time.sleep(20)
                update.message.reply_text(a[i][y])

def command_rand(update, context):
    a = rand_1()
    for i in range(0, len(a)):
        for y in range(0, len(a[i])):
            update.message.reply_text(a[i][y])

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
    k = 1
    f = 1
    a = ' ' 
    while f != 0:
        u = 0
        r = requests.get(root_url)  #ищем вопросы по очереди
        soup = BeautifulSoup(r.content, 'html.parser')
        link_1 = soup.find_all("b")
        #links = link_1.find("a")
        for link in link_1:
            if (link.a != None) and ('Вопрос ' + str(k) == link.a.text):
                y = link.a.get("href")
                break
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
    w = []
    w_1 = []
    root_url = ''
    driver = webdriver.Safari()                      #заходим на сайт бд чгк и вбиваем название пакета в поиск
    driver.get('https://db.chgk.info/search/tours')
    id_box = driver.find_element_by_name("keys")
    id_box.send_keys(name)
    search_button = driver.find_element_by_id("edit-submit-1")
    search_button.click()
    time.sleep(4)
    url = driver.current_url
    answ = requests.get(url)                          #вытаскиваем ссылку на пакет
    driver.quit()
    soup = BeautifulSoup(answ.content, 'html.parser')
    links = soup.find_all("a")
    for link in links:
        if '/tour/' in link.get("href"):
            root_url = 'https://db.chgk.info' + link.get("href")
            break
    if root_url == '':
        return w
    db = requests.get(root_url)
    soup = BeautifulSoup(db.content, 'html.parser')
    an_links = soup.find_all("strong", class_="Question")  #ищем вопросы по классу
    l = 1
    f = 1
    a = ' '
    y = 'k'
    while f != 0:
        k = 1
        db = requests.get(root_url)
        soup = BeautifulSoup(db.content, 'html.parser')
        links = soup.find_all("strong", class_="Question")   #ищем вопросы по классу
        for link in links:
            if 'Вопрос ' + str(l) + ':' == link.text:
                y = links[k-1].a.get("href")
                break
            k += 1
            if k > len(links):
                break
        if a == y:
            f = 0
        a = y
        new_root = 'https://db.chgk.info' + y    #идем на страницу вопроса
        r = requests.get(new_root)
        soup = BeautifulSoup(r.content, 'html.parser')
        b = soup.find("div", class_="razdatka")
        t_1 = soup.find_all("p")
        qw = t_1[1].text
        answ = t_1[2].text + t_1[3].text + t_1[4].text
        if b != None:
            razd = b.img['src']
            w_1.append('Раздаточный материал')
            w_1.append(razd)
        w_1.append(qw)
        w_1.append(answ)
        w.append(w_1)
        w_1 = []
        l += 1
    return w

def rand_1():
    w = [] 
    r = requests.get('https://iqga.me/base/')
    soup = BeautifulSoup(r.content, 'html.parser')
    link = soup.find("div", class_="pages")
    links = link.find_all("a")
    a = random.randint(0, len(links)-1)
    root = 'https://iqga.me' + links[a].get("href")
    r = requests.get(root)
    soup = BeautifulSoup(r.content, 'html.parser')
    link = soup.find_all("div", class_="l-cell-4 l-mobile-cell-12")
    a = random.randint(0, len(link)-1)
    name = link[a].a.text
    w = iq_game(name)
    return w


if __name__ == '__main__':
    main()
    
    
