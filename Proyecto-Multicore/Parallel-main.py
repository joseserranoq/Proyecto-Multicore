from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import concurrent.futures
import time

from selenium.webdriver.chrome.options import Options

import json


#Se puede implementar mediante el threading que corra las funciones en forma paralela, creando funciones que ocupen los links de la lista pero que no dependan una de otra y mediante 
#la obtención de las listas (listadetítulos,precios de steam, precios de amazon, score de metacritic, horas de how long to beat) se utilicen en una función para almacernalos
#mediante un for secuencial todos los datos en orden en un .json


# The idea is to create a function that travels by a loop to get the txt file information to generate web scraping with the respective information by order...

#1: Title of the game
#2: Amazon link index+1
#3: Steam link index+2
#4: Metacritic link index+3
#5: Howlongtobeat link index+4
#Then the another game with the same order...
#Then with the obtainable information, it will allow to generate a .json file to start developing the web page with the help of HTML.
path = 'Proyecto-Multicore\chromedriver.exe'   
chrome_options = Options()
chrome_options.add_argument("--headless")
driver1 = webdriver.Chrome(path,options=chrome_options)
driver2 = webdriver.Chrome(path,options=chrome_options)
driver3 = webdriver.Chrome(path,options=chrome_options)
driver4 = webdriver.Chrome(path,options=chrome_options)


def Obtain_amazonprice(links):

    driver1.get(links)
    try:
        
        amasearch = driver1.find_element_by_id('priceblock_ourprice') #Its where is located the price of the game.
        amaprice= amasearch.text #It converts the object to a string
    except:
        amaprice = 'Juego no disponible. '

    print(amaprice)
    return amaprice

def st_price():
    #driver.get(link)
    try:    #The try is implemented because if a variable called self.find_element... does not appear will raise an error
        stsearch= driver2.find_element_by_xpath('//div[@class="game_purchase_price price"]')
        price= stsearch.text
        print(f'{price} Price')

             
    except:
        stsearch= driver2.find_elements_by_xpath("//div[@id='game_area_purchase']")
        disc_element = stsearch[0].find_element_by_class_name('discount_final_price') #In this position is located the string that the function needs
        price = disc_element.text
        print(f'{price} Discount')
    return price

def agecheck_prices():
    try:
                #When the url changes we need to use wait method to search for the another values
        element= WebDriverWait(driver2,10).until(EC.presence_of_element_located((By.XPATH,"//div[@class='game_purchase_price price']")))   
        price = element.text            
        print(f'{price} Wait.price')
    except:
        element= WebDriverWait(driver2,10).until(EC.presence_of_element_located((By.CLASS_NAME,'discount_final_price')))
        price= element.text
        print(f'{price} Wait.discount')
    return price

def age_verification(): #When age verification in steam appears the this function will pass the age verification to get the price of the game
    #driver.get(link)
    try:
        
        agemess = driver2.find_element_by_class_name('agegate_birthday_desc')
        y= driver2.find_element_by_xpath('//option[@value="1900"]')
        y.click()
        seepage= driver2.find_element_by_xpath('//a[@onclick="ViewProductPage()"]')
        seepage.click()
        
        price =agecheck_prices()
    
    except: #When selenium entered the year it will not appear again, so only the button needs to be clicked
        seepage= driver2.find_element_by_xpath('//a[@onclick="ViewProductPage()"]')
        seepage.click()
        price=agecheck_prices()

    return price

def Obtain_steamprice(link):
    driver2.get(link)
    #agever = link.split('/') #This will convert the link in a list where the position will be divided for '/'
    #if agever[3] == 'agecheck': 
    #    price = age_verification(link)
    try:
        agever = driver2.find_element_by_xpath("//div[@id='app_agegate']") #If It does not raise an exeption is because this id is only in the pages with age verification
    
        price =age_verification()
    except:
        price = st_price()


    return price

def Obtain_Metascore(link): #tag a, tag span
    driver3.get(link)
    
    mtsearch = driver3.find_elements_by_class_name('metascore_anchor')
    print(mtsearch[0].text) #The position 0 where is located the Metascore.
    score = mtsearch[0].text
    return score

def Obtain_HLongtobeat(link):
    driver4.get(link)

    HLTBsearch = driver4.find_elements_by_class_name('game_times')
    element= HLTBsearch[0].text
    l_hwtime = element.split('\n')
    
    print(l_hwtime)
    return l_hwtime



def Sort_info(): #It has some limitations like adult verification by steam, so the function will get content from games below that category
    
    titles = list() 
    amazon = list() 
    steam = list() 
    meta = list() 
    hwlong = list()
    
    with open('Proyecto-Multicore\games.txt','r') as file1:
        sites = file1.readlines()

        for site in range(0,len(sites),5): #It creates indexes for the games, each game has information in 4 positions after the chose index in the loop,
            titles.append(sites[site])
            amazon.append(sites[site+1])
            steam.append(sites[site+2])
            meta.append(sites[site+3])
            hwlong.append(sites[site+4])

        file1.close()
    return titles, amazon, steam, meta, hwlong


def Generate_info():
    list1,list2,list3,list4,list5  = Sort_info()
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        
        r1 = [executor.submit(Obtain_amazonprice,amazon_ind) for amazon_ind in list2]
            
        r2 = [executor.submit(Obtain_steamprice,steam_prices) for steam_prices in list3]
            
        r3 = [executor.submit(Obtain_Metascore,score) for score in list4]

        r4 = [executor.submit(Obtain_HLongtobeat,ti) for ti in list5]
    
    with open('Proyecto-Multicore\\templates\game_data.txt','w',encoding="utf-8") as file2:
        for i in range(0,len(list1)):
            print(f'{list1[i]}{r1[i].result()}\n{r2[i].result()}\n{r3[i].result()}\n{r4[i].result()[0]}-{r4[i].result()[1]}')
            file2.write(f'{list1[i]}{r1[i].result()}\n{r2[i].result()}\n{r3[i].result()}\n{r4[i].result()[0]}-{r4[i].result()[1]}\n')
        file2.close()
    driver1.quit()
    driver2.quit()
    driver3.quit()
    driver4.quit()      

    return


Generate_info()
