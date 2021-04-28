from selenium import webdriver
from selenium.webdriver.common.keys import Keys #Sirve para encontrar los resultados que busco en alguna barra de búsqueda
import time

    #PATH = "C:\\Users\\Lenovo\\Desktop\\Selenium examples\\chromedriver.exe"
driver = webdriver.Chrome()
def ejemplo1(driver1):



    #*****


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
    return

def ejemplo2(driver2):
    #SIRVE PARA ENCONTRAR EL TEXTO DE LOS TÍTULOS RELACIONADOS CON EL TEMA PYCON
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys #Sirve para encontrar los resultados que busco en alguna barra de búsqueda
    import time
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC


    #path = "C:\\Users\\Lenovo\\Desktop\\Selenium examples\\chromedriver.exe"
    driver = webdriver.Chrome()

    driver.get("http://www.python.org")

    searchbar = driver.find_element_by_id("id-search-field")
    searchbar.send_keys("pycon")
    button = driver.find_element_by_id("submit")
    button.click()

    try:
        #funciona para encontrar un elemento que se encuentre en la página.
        element= WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.TAG_NAME,'ul')))
        for header in element:
            hli = header.find_elements_by_tag_name("li")
            for header3 in hli:
                #print(header3.text)   
                hrefs = header3.find_elements_by_tag_name('h3')
                for href in hrefs:
                    print(href.text)
    finally:                                                                                
        driver.quit()

    return
#LLAMADAS DE LAS FUNCIONES
#ejemplo1(driver)
#ejemplo2(driver)