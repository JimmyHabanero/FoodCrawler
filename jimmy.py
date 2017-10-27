import requests
from bs4 import BeautifulSoup
import ItemClass
import sqlite3

def prepare_soup(href):
    source_code = requests.get(href)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    return soup

def spider(max_pages):
    # find every link of the product groups
    page = 1
    while page <= max_pages:
        url = 'http://www.dobradieta.pl/tabele.php'
        soup = prepare_soup(url)
        table_soup = BeautifulSoup(str(soup.findAll('div', {'class':'content content-font'})), 'html.parser')
        for link in table_soup.findAll('a'):
            href = "http://www.dobradieta.pl/" +  link.get('href')
            get_group_data(href)
        page +=1

def get_group_data(item_url):
    # collect each link for products
    soup = prepare_soup(item_url)
    data_soup = BeautifulSoup(str(soup.findAll('div', {'class':'contentbox-container-full'})), 'html.parser')
    for link in data_soup.findAll('a'):
        name = str(link.text)
        href = "http://www.dobradieta.pl/" +  link.get('href')
        get_single_item_data(name, href)

def get_single_item_data(name, href):
    # collect each item
    soup = prepare_soup(href)
    data_soup = BeautifulSoup(str(soup.findAll('table')), 'html.parser')
    table_items = data_soup.findAll('td')
    # something corrupts encoding so hard coding polish letters in name is necessary
    intab = '¿³ê¦¶¯¼±ñæ'
    outtab = 'żłęśśżźąńć'
    name = name.translate({ord(x): y for (x, y) in zip(intab, outtab)})
    item = ItemClass.FoodItem(name,
                     float(str(table_items[5].text)),
                     float(str(table_items[6].text)),
                     float(str(table_items[7].text)),
                     int(str(table_items[9].text)))
    serialize_data(item)
    print(name)

def serialize_data(data):
    conn = sqlite3.connect('food_database.db')
    c = conn.cursor()
    c.execute("INSERT INTO food_database VALUES (:name, :protein, :fat, :carbs, :kcal)",
              {'name':data.name,'protein':data.protein,'fat':data.fat,'carbs':data.carbs,'kcal':data.kcal})
    conn.commit()

spider(1)

