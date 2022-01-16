from selenium import webdriver
from time import time, sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver import ActionChains as A
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
import const_hack



def to_do():

    def move_back(times):
        for _ in range(times):
            driver.back()
    #clicker a partir d'un link
    def click_link(link_text):
            try:
                link = wait.until(ec.presence_of_element_located((By.LINK_TEXT,link_text)))
                link.click()
            except Exception:
                link = wait.until(ec.presence_of_element_located((By.LINK_TEXT,link_text)))
                link.click()
    #sectionner une valeur
    def get_dropdown_value(dropdown_id,index_value):
            try:
                dropdown = Select(wait.until(ec.presence_of_element_located((By.ID,dropdown_id))))
                dropdown_value = dropdown.select_by_index(index_value)
            except Exception:
                try:
                    dropdown = Select(wait.until(ec.presence_of_element_located((By.ID,dropdown_id))))
                    dropdown_value = dropdown.select_by_index(index_value)
                except Exception:
                    print('u should click the button first')
                return dropdown_value

    def click_button_id(button_id):
            try:
                button = wait.until(ec.presence_of_element_located((By.ID,button_id)))
                button.click()
            except Exception:
                try:
                    button = wait.until(ec.presence_of_element_located((By.ID,button_id)))
                    button.click()
                except Exception:
                    print('enable to click button id')

    # Write in field
    def write_value(field_id,value):
        try:
            field = wait.until(ec.presence_of_element_located((By.ID,field_id)))
            field.send_keys(value)
        except Exception:
            try:
                field = wait.until(ec.presence_of_element_located((By.ID,field_id)))
                field.send_keys(value)
            except Exception:
                print('enable to write value')

    
    def Studium_log_in():
        try:
            driver.get(const_hack.STUDIUM_LINK)
        except Exception:
            print('error')
        click_link('Accéder à votre StudiUM')
        sleep(1)
        try:
            username=wait.until(ec.presence_of_element_located((By.ID, "username")))
            username.clear()
            username.send_keys(const_hack.username)
        except Exception:
            username=wait.until(ec.presence_of_element_located((By.ID, "username")))
            username.clear()
            username.send_keys(const_hack.username)

        try:
            password=wait.until(ec.presence_of_element_located((By.ID, "password")))
            password.clear()
            password.send_keys(const_hack.password)
        except Exception:
            password=wait.until(ec.presence_of_element_located((By.ID, "password")))
            password.clear()
            password.send_keys(const_hack.password)
        #click se connecter button
        driver.find_element_by_css_selector("input[autocomplete='off'][type='submit'][class='apmui-button apmui-button-submit'][value='Se connecter']").click()

    def tasks_to_do():
        dict_todo={}
        click_button_id('groupingdropdown')
        click_link('Mes cours')
        val=driver.find_elements(By.XPATH, "//div[@class='dropdown-menu show']/a[@class='dropdown-item']")
        val[1].click()
        header=driver.find_element_by_id('page-header').text
        cour=(header.split(' '))[0]
        session=(cour.split('-'))[-1]
        cours=(cour.split('-'))[0]
        courses={}
        txt={}
        courses.update({'cours_0':cours}) 
        dict_todo.update({'session':session})
        texte=driver.find_element_by_id('section-2').text
        texte=texte.split('\n')
        texte = list(filter(lambda txt: (txt not in ['','Fichier','Cours','Démo','URL','Zoom']), texte))
        tab=[]
        for i in texte:
            if 'Zoom' and 'Janvier' in i:
                tab.append(texte.index(i))
        for j in tab:
            del texte[j]
            
        
        
                
        
        txt.update({'cours_0':texte})
        move_back(1)       
        for i in range(2,len(val)):
            click_link('Mes cours')
            sleep(1)
            val=driver.find_elements(By.XPATH, "//div[@class='dropdown-menu show']/a[@class='dropdown-item']")
            val[i].click()
            header=driver.find_element_by_id('page-header').text
            cour=(header.split(' '))[0]
            sess=(cour.split('-'))[-1]
            cours=cour.split('-')[0]
            if sess == session:
                courses.update({'cours_'+str(i):cours})
                try:
                    texte=driver.find_element_by_id('section-2').text
                    texte=texte.split('\n')

                    texte = list(filter(lambda txt: (txt not in ['','Fichier','Cours','Démo','URL']), texte))
                    tab=[]
                    for i in texte:
                        if 'Zoom' and 'janvier' in i:
                            tab.append(texte.index(i))
                    for j in tab:
                        del texte[j]

                    txt.update({'cours_'+str(i):texte})
                except Exception:
                    texte='vide'    
            else:
                break       
            move_back(1)
        
        dict_todo.update({'cours':courses})
        dict_todo.update({'texte':txt})
        driver.find_element_by_css_selector("span[class='userbutton']").click()
        click_link('Déconnexion')
        return dict_todo
    
    def write_tab(dict):
        i=1
        j=1
        try:
            driver.get(const_hack.TO_DO_LINK)
        except Exception:
            print('error')

        write_value('semester',dict['session'])

        for key in dict['cours'].keys():
            write_value('c'+str(i),dict['cours'][key])
            i+=1
        for key in dict['texte'].keys():
            for ligne in dict['texte'][key]:
                write_value('w'+str(j),'- '+ligne+'\n')
            j+=1
        
        write_value('w1','value')
        sleep(1)
    driver = webdriver.Chrome(const_hack.DRIVER_PATH,options=chrome_options)
    wait = WebDriverWait(driver,30)
    Studium_log_in()
    dict_todo=tasks_to_do()
    
    write_tab(dict_todo)
    
    driver.quit()

to_do()

sleep(1)



