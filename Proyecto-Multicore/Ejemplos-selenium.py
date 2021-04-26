from selenium import webdriver
from selenium.webdriver.common.keys import Keys #Sirve para encontrar los resultados que busco en alguna barra de búsqueda
import time


'''
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
try:
    element= WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,''))) #funciona para encontrar un elemento que se encuentre 
finally:                                                                                #en la página.
    driver.quit()
'''


#*****
PATH = "C:\\Users\\Lenovo\\Desktop\\Selenium examples\\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get('https://www.amazon.com/-/es/')
#print(driver.title) #Sirve para imprimir el título de la página
#print(driver.page_source) #Sirve para ver los el código de la página

search = driver.find_element_by_id("twotabsearchtextbox")
search.send_keys('Lapicero') #Escribe el texto en la barra de búsqueda
search.send_keys(Keys.RETURN)
#search.clear() #Limpia el texto para poder escribir otra palabra


#*******
#presionar = driver.find_element_by_id("nav-search-submit-button") #Sirve para darle click a un botón
#presionar.click()
#*******

#time.sleep(5) Sirve para que la página se mantenga abierta por segundos
driver.quit()
