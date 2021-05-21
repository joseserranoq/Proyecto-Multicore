from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import concurrent.futures
import time
from selenium.webdriver.chrome.options import Options



# The idea is to create a function that travels by a loop to get the txt file information to generate web scraping with the respective information by order...

#1: Title of the game
#2: Amazon link index+1
#3: Steam link index+2
#4: Metacritic link index+3
#5: Howlongtobeat link index+4

path = 'Proyecto-Multicore\chromedriver.exe'   
chrome_options = Options()
chrome_options.add_argument("--headless")
driver1 = webdriver.Chrome(path,options=chrome_options)
driver2 = webdriver.Chrome(path,options=chrome_options)
driver3 = webdriver.Chrome(path,options=chrome_options)
driver4 = webdriver.Chrome(path,options=chrome_options)


def Obtain_amazonprice(links): #it finds the price in the amazon web page 

    driver1.get(links)
    try:
        
        amasearch = driver1.find_element_by_id('priceblock_ourprice') #Its where is located the price of the game.
        amaprice= amasearch.text #It converts the object to a string
    except:
        amaprice = 'Juego no disponible. '

    print(amaprice)
    return amaprice

def st_price(): #It finds the price of the games in steam but only if the games does not have adult restriction.
 
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

def agecheck_prices():  #It finds the games that has age restriction in web page steam
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

def age_verification(): #By try and except it will skip the age verification page in steam web page

    try:    #It will enter a year 1900 to skip the age verification
        
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

def Obtain_steamprice(link):    #It is the main function to return the price of a game in steam web page, 
    driver2.get(link)           #by a try it sees if the web page has a particular element that is only found in age verification pages in steam
                                #The except contains a function that will return the price of amazon, games that does not have age restriction
    try:
        agever = driver2.find_element_by_xpath("//div[@id='app_agegate']") #If It does not raise an exeption is because this id is only in the pages with age verification
    
        price =age_verification()
    except:
        price = st_price()


    return price

def Obtain_Metascore(link): #It obtains the score of the games 
    driver3.get(link)
    
    mtsearch = driver3.find_elements_by_class_name('metascore_anchor')
    print(mtsearch[0].text) #The position 0 where is located the Metascore.
    score = mtsearch[0].text
    return score

def Obtain_HLongtobeat(link):   #It obtains the main hour playtime of a game
    driver4.get(link)

    HLTBsearch = driver4.find_elements_by_class_name('game_times')
    element= HLTBsearch[0].text
    l_hwtime = element.split('\n')
    
    print(l_hwtime)
    return l_hwtime



def Sort_info(): #It will create lists that will contain the data of the games.txt file 
    
    titles = list() 
    amazon = list() 
    steam = list() 
    meta = list() 
    hwlong = list()
    
    with open('Proyecto-Multicore\games.txt','r') as file1:
        sites = file1.readlines()

        for site in range(0,len(sites),5): #Each 5 position a title appears then i+1 amazon link, i+2 steam link, i+3 metacritic link, i+4 Howlongtobeat link
            titles.append(sites[site])
            amazon.append(sites[site+1])
            steam.append(sites[site+2])
            meta.append(sites[site+3])
            hwlong.append(sites[site+4])

        file1.close()
    return titles, amazon, steam, meta, hwlong


def Generate_info():
    list1,list2,list3,list4,list5  = Sort_info() #It is used inside this function to make a loop that travels this lists by concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor: #It is used like a way of parallelism the variables will return a list of objects
        
        r1 = [executor.submit(Obtain_amazonprice,amazon_ind) for amazon_ind in list2]
            
        r2 = [executor.submit(Obtain_steamprice,steam_prices) for steam_prices in list3]
            
        r3 = [executor.submit(Obtain_Metascore,score) for score in list4]

        r4 = [executor.submit(Obtain_HLongtobeat,ti) for ti in list5]
    
    with open('Proyecto-Multicore\\templates\game_data.txt','w',encoding="utf-8") as file2: #It will be written the content of the variables r1,r2,r3,r4 and the list1 that contains the titles of the games
        for i in range(0,len(list1)):                                                       #It need the variable enconding because it does not recognize the data in the lists produced by the parallel method
            print(f'{list1[i]}{r1[i].result()}\n{r2[i].result()}\n{r3[i].result()}\n{r4[i].result()[0]}-{r4[i].result()[1]}') 
            file2.write(f'{list1[i]}{r1[i].result()}\n{r2[i].result()}\n{r3[i].result()}\n{r4[i].result()[0]}-{r4[i].result()[1]}\n') #The lists produced by the parallel method will be accesed with .result()
        file2.close()
    driver1.quit()
    driver2.quit()
    driver3.quit()
    driver4.quit()      

    return


Generate_info()
