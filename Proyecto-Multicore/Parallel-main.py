from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import concurrent.futures
import time

import threading

import json


#Se puede implementar mediante el threading que corra las funciones en forma paralela, creando funciones que ocupen los links de la lista pero que no dependan una de otra y mediante 
#la obtención de las listas (listadetítulos,precios de steam, precios de amazon, score de metacritic, horas de how long to beat) se utilicen en una función para almacernalos
#mediante un for secuencial todos los datos en orden en un .json

#x = open('Proyecto-Multicore\games.txt','r')
#s = x.readlines()

#print(s)
#for i in lista:
#    print(i)



# The idea is to create a function that travels by a loop to get the txt file information to generate web scraping with the respective information by order...

#1: Title of the game
#2: Amazon link index+1
#3: Steam link index+2
#4: Metacritic link index+3
#5: Howlongtobeat link index+4
#Then the another game with the same order...
#Then with the obtainable information, it will allow to generate a .json file to start developing the web page with the help of HTML.
path = 'Proyecto-Multicore\chromedriver.exe'    
driver1 = webdriver.Chrome(path)
driver2 = webdriver.Chrome(path)
driver3 = webdriver.Chrome(path)
driver4 = webdriver.Chrome(path)

def Obtain_amazonprice(link):
    #amaprices = list()
    #for indexlink in range(1,len(links),5):
#    link = links[indexlink]
    driver1.get(link)
    try:
        amasearch = WebDriverWait(driver1,10).until(EC.presence_of_element_located((By.ID,"priceblock_ourprice")))   
        #amasearch = driver.find_element_by_id('priceblock_ourprice') #Its where is located the price of the game.
        amaprice= amasearch.text #It converts the object to a string
        #amaprices.append(amaprice)
    except:
        amaprice = 'Juego no disponible. '
        #amaprices.append(amaprice)
    print(amaprice)    
    return amaprice

def age_ver(link): #When age verification in steam appears the this function will pass the age verification to get the price of the game
    driver2.get(link)
    agemess = driver2.find_element_by_class_name('agegate_birthday_desc')
    y= driver2.find_element_by_xpath('//option[@value="1900"]')
    y.click()
    seepage= driver2.find_element_by_xpath('//a[@onclick="ViewProductPage()"]')
    seepage.click()
    try: #When the url changes we need to use wait method to search for the another values
        element= WebDriverWait(driver2,10).until(EC.presence_of_element_located((By.XPATH,"//div[@class='game_purchase_price price']")))   
        price = element.text            
        print(f'{price} sol1')
    except:
        element= WebDriverWait(driver2,10).until(EC.presence_of_element_located((By.CLASS_NAME,'discount_final_price')))
        price= element.text
        print(f'{price} sol2') 
    
    return price

def Obtain_steamprice(link): 
    
    
#for indexlink in range(2,len(links),5):
    #link = links[indexlink]
    agever = link.split('/') #This will convert the link in a list where the position will be divided for '/'
    if agever[3] == 'agecheck': 
        price = age_ver(link)

    else:
        driver2.get(link)
        try:    #This is implemented because if a variable called self.find_element... does not appear will raise an error
            stsearch= driver2.find_element_by_xpath('//div[@class="game_purchase_price price"]')
            price= stsearch.text

            print(f'{price} sol3')


             
        except:
            stsearch = driver2.find_elements_by_xpath("//div[@id='game_area_purchase']")
            disc_element = stsearch[0].find_element_by_class_name('discount_final_price') #In this position is located the string that the function needs
            price = disc_element.text

            print(f'{price} sol4')
           
    return price

def Obtain_Metascore(link): #tag a, tag span
    driver3.get(link)
    
    mtsearch = driver3.find_elements_by_class_name('metascore_anchor')
    score=mtsearch[0].text #The position 0 where is located the Metascore.
    print(score)
    return score

def Obtain_HLongtobeat(link):
    driver4.get(link)

    HLTBsearch = driver4.find_elements_by_class_name('game_times')
    hlong =HLTBsearch[0].text
    print(hlong)
    return hlong




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

            #title = sites[site]                         #It will be a function to save the titles of the games
            #amazon_price = Obtain_amazonprice(sites[site+1])   #Another idea to storage the content of this function could be that all the functions return the value we want
            #steam_price = Obtain_steamprice(sites[site+2])    #so all the content could be storage in a .json file by creating a way to insert them
            #metascore = Obtain_Metascore(sites[site+3])
            #hlong = Obtain_HLongtobeat(sites[site+4])

            #titles.append(title)
            #amazon.append(amazon_price)
            #steam.append(steam_price)
            #meta.append(metascore)
            #hwlong.append(hlong)
        file1.close()
    return titles, amazon, steam, meta, hwlong


def Generate_info(list1,list2,list3,list4,list5):
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        
        r1 = [executor.submit(Obtain_amazonprice,amazon_ind) for amazon_ind in list2]
            
        r2 = [executor.submit(Obtain_steamprice,steam_prices) for steam_prices in list3]
            
        r3 = [executor.submit(Obtain_Metascore,score) for score in list4]

        r4 = [executor.submit(Obtain_HLongtobeat,ti) for ti in list5]
          
    for i in range(0,len(list1)):
        print(f'\n{list1[i]":"}\n\n{r1[i].result()}{r2[i].result()}{r3[i].result()}{r4[i].result()}')
    driver1.quit()
    driver2.quit()
    driver3.quit()
    driver4.quit()      

    return
#Sort_info()

title_list, amazon_list, steam_list, meta_list, hlong_list  = Sort_info()
Generate_info(title_list, amazon_list, steam_list, meta_list, hlong_list)
