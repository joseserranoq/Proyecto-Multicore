from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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
driver = webdriver.Chrome(path)
#It will allow to obtain the information that goes to .json's file
def Generate_info(): #It has some limitations like adult verification by steam, so the function will get content from games below that category
    
    with open('Proyecto-Multicore\games.txt','r') as file1:
        sites = file1.readlines()
        for site in range(0,len(sites),5): #It creates indexes for the games, each game has information in 4 positions after the chose index in the loop,
            print(sites[site])                         #It will be a function to save the titles of the games
            Obtain_amazonprice(sites[site+1])   #Another idea to storage the content of this function could be that all the functions return the value we want
            Obtain_steamprice(sites[site+2])    #so all the content could be storage in a .json file by creating a way to insert them
            Obtain_Metascore(sites[site+3])
            Obtain_HLongtobeat(sites[site+4])
    driver.quit()
    return

def Obtain_amazonprice(link):

    driver.get(link)

    amasearch = driver.find_element_by_id('priceblock_ourprice') #Its where is located the price of the game.
    print(amasearch.text) #It converts the object to a string
    return

def age_ver(link): #When age verification in steam appears the this function will pass the age verification to get the price of the game
    driver.get(link)
    agemess = driver.find_element_by_class_name('agegate_birthday_desc')
    y= driver.find_element_by_xpath('//option[@value="1900"]')
    y.click()
    seepage= driver.find_element_by_xpath('//a[@onclick="ViewProductPage()"]')
    seepage.click()
    try: #When the url changes we need to use wait method to search for the another values
        element= WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//div[@class='game_purchase_price price']")))   
        price = element.text            
        print(f'{price} sol1')
    except:
        element= WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,'discount_final_price')))
        price= element.text
        print(f'{price} sol2') 
    return price

def Obtain_steamprice(link): 
    agever = link.split('/') #This will convert the link in a list where the position will be divided for '/'
    if agever[3] == 'agecheck': 
        price = age_ver(link)
    else:
        driver.get(link)
        try:    #This is implemented because if a variable called self.find_element... does not appear will raise an error
            stsearch= driver.find_element_by_xpath('//div[@class="game_purchase_price price"]')
            price= stsearch.text
            print(f'{price} sol3')

             
        except:
            stsearch= driver.find_elements_by_xpath("//div[@id='game_area_purchase']")
            disc_element = stsearch[0].find_element_by_class_name('discount_final_price') #In this position is located the string that the function needs
            price = disc_element.text
            print(f'{price} sol4')
    return price

def Obtain_Metascore(link): #tag a, tag span
    driver.get(link)
    
    mtsearch = driver.find_elements_by_class_name('metascore_anchor')
    print(mtsearch[0].text) #The position 0 where is located the Metascore.
    return

def Obtain_HLongtobeat(link):
    driver.get(link)

    HLTBsearch = driver.find_elements_by_class_name('game_times')
    print(HLTBsearch[0].text)

Generate_info()