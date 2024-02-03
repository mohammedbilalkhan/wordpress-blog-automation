import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, UnexpectedAlertPresentException, WebDriverException
from tkinter import *
from tkinter import messagebox
import pandas as pd
import time, datetime, os
import csv
import urllib.request as ur
import threading


def delay(wait_time = 0):
    time.sleep(3 + wait_time)

# current time
currentDateTime = datetime.datetime.now()
currenthour = currentDateTime.hour
currentminute = currentDateTime.minute
currentday = currentDateTime.day
currentyear = currentDateTime.year
currentmonth = currentDateTime.strftime("%b") 



## uc chrome options
opts = uc.ChromeOptions()
opts.add_argument("--start-maximized")
opts.add_argument('--no-sandbox')

def check_connection():
    host = "https://www.google.com"
    try:
        ur.urlopen(host)
        return True
    except:
        return False

def writefile(scriptlinkpathlist):
    global length_scriptlist
    length_scriptlist = len(scriptlinkpathlist)
    print('Scripts found:', length_scriptlist)
    with open(f'{logpath}/{file_name}', 'a', newline='\n') as link_file2:
        link_writer2 = csv.DictWriter(link_file2, fieldnames=["Links"])
        for scriptlinkhref in scriptlinkpathlist:
            scriptlink = scriptlinkhref.get_attribute("href")
            link_writer2.writerow({'Links' : str(scriptlink)})      # saving links

        print('Scannig Finished.')
    link_file2.close()


def runcommand(name, email, website, atpage, noofpage, comment):
    global links_writer, link_file, logpath, file_name
    # log path
    getpwd = os.getcwd()
    gpwd = getpwd.replace('\\','/')
    logname = f'/Log/{currentday}-{currentmonth}-{currentyear}'
    logpath = gpwd + logname
    if os.path.exists(logpath):
        print('Log Folder Exists.')
        
    else :
        os.makedirs(logpath)
        print("Log Folder Created.")   
    
    # reading websites
    df0 = pd.read_csv('sites.csv')
    websiteslist = df0["Links"].to_list()

    try:
        driver = uc.Chrome(options=opts)
    except WebDriverException:
        messagebox.showerror('Chromedriver Version not up to date.', 'Download Chromedriver that meets your Chrome Versions. \nDownload from here: https://chromedriver.chromium.org/downloads')
        pass

    file_name = f"links.csv"
    success_filename = f"success_file.csv"
    if os.path.exists(f"{logpath}/{file_name}") and os.path.exists(f"{logpath}/{success_filename}"):
        expand = 1
        while True:
            expand += 1
            new_file_name = file_name.split(".csv")[0] + str(expand) + ".csv"
            new_filename2 = success_filename.split(".csv")[0] + str(expand) + ".csv"
            if os.path.exists(f"{logpath}/{new_file_name}") and os.path.exists(f"{logpath}/{new_filename2}"):
                continue
            else:
                file_name = new_file_name
                success_filename = new_filename2
                break

    # opening file
    with open(f'{logpath}/{file_name}', 'a', newline='\n') as link_file, open(f'{logpath}/{success_filename}', 'a', newline='\n') as success_file:
        linkheader = ['Links']
        links_writer = csv.DictWriter(link_file, fieldnames=linkheader)
        links_writer.writeheader()

        successheader = ['success_links']
        success_writer = csv.DictWriter(success_file, fieldnames=successheader)
        success_writer.writeheader()

        link_file.close()

        length_list = []
        m = -1
        while m in range(m, len(websiteslist)-1):
            m += 1
            indivi_website = websiteslist[m]
            print(indivi_website)

            atpage = int(atpage)
            noofpage = int(noofpage)
     
            i = -1
            while i < noofpage:
                i += 1
                if i == noofpage:
                    break

                getwebsite = f'{indivi_website}/page/{atpage + i}'
                driver.get(getwebsite)
                # print(getwebsite)
                delay()
                
                sectionpathlist = ["//article/div/div/header/h2/a", "//article/header/h2/a", "//article/div/div/h3/a",  "//article/div/header/h3/a", "//article/div/header/h2/a", 
                                    "//article/header/h1/a", "//article/div/a", "//article/div/div/div/div/a", "//article/div[2]/h2/a", "//article/div[2]/h3/a",
                                    "//div/div/h3/a", "//div/div/a", "//article/h2/a", "//article/div[2]/header/h2/a"] 
                for sectionpath in sectionpathlist:
                    try:
                        driver.find_element(By.XPATH, f"{sectionpath}")
                        scriptlinkpathlist = driver.find_elements(By.XPATH, f"{sectionpath}")
                        print('1')
                        writefile(scriptlinkpathlist)
                        break
                    except NoSuchElementException:     
                        pass


            length_list.append(len(scriptlinkpathlist))

            df = pd.read_csv(f'{logpath}/{file_name}', error_bad_lines=False)
            linklist = df["Links"].to_list()
            
            total = sum(length_list)
            current_index = total - length_scriptlist
            n = current_index - 1
            print(n)             
            while n in range(0, len(linklist)):
                n += 1
                print(f'\n{n}')
                try:
                    link = linklist[n]
                except IndexError:
                    break
                print(link)
                driver.get(link)            
                delay(-1)

                 # comment
                try:
                    commentpath = driver.find_element(By.XPATH, "//textarea[@id='comment']")       
                except NoSuchElementException:
                    try:
                        commentpath = driver.find_element(By.XPATH, "//textarea[@id='wc-textarea-0_0']")    
                    except NoSuchElementException:
                        print('Comment Section not open/available. Skipping this page.')
                        continue   
                    pass
                except UnexpectedAlertPresentException:
                    continue
                try:
                    commentpath.click()
                except ElementClickInterceptedException:
                    print('Comment Box not clickable.')
                    continue
                commentpath.send_keys(comment)
                
                 # Author Name
                try:
                    delay(-1)
                    authorpath = driver.find_element(By.XPATH, "//input[@id='author']")            
                except NoSuchElementException:
                    authorpath = driver.find_element(By.XPATH, "//input[@id='wc_name-0_0']")            
                    pass
                authorpath.send_keys(name)
                    
                # Email    
                try:
                    emailpath = driver.find_element(By.XPATH, "//input[@id='email']")               
                except NoSuchElementException:
                    emailpath = driver.find_element(By.XPATH, "//input[@id='wc_email-0_0']")              
                    pass
    
                emailpath.send_keys(email)

                # Website
                try:
                    websitepath = driver.find_element(By.XPATH, "//input[@id='url']")               
                except NoSuchElementException:
                    websitepath = driver.find_element(By.XPATH, "//input[@id='wc_website-0_0']")              
                    pass
                websitepath.send_keys(website)
                delay()

                # Posting a comment
                try:
                    driver.find_element(By.XPATH, "//input[@id='submit']").click()                  
                    print('Sent.')
                    success_writer.writerow({'success_links' : str(link)})
                except ElementClickInterceptedException:
                    driver.find_element(By.XPATH, "//input[@value='Post Comment']").click()
                    print('Sent.')
                    success_writer.writerow({'success_links' : str(link)})
                    pass
                except NoSuchElementException:
                    driver.find_element(By.XPATH, "//input[@id='wpd-field-submit-0_0']").click()
                    print('Sent.')
                    success_writer.writerow({'success_links' : str(link)})

                delay(5)
            
                print('Next Link')
            print('\n Next Website.')

    messagebox.showinfo('Completed !', 'Finished.')

def getfieldscommand():
    getname = entrybox_authorname.get()
    getemail = entrybox_email.get()
    getwebsite = entrybox_website.get()
    getatpage = entrybox_atpage.get()
    getnoofpage = entrybox_noofpage.get()
    getcomment = commentTextarea.get(1.0, END)

    if getname == '' or getemail == '' or getwebsite =='' or getatpage == '' or getnoofpage == '' or getcomment == '':
        messagebox.showerror('Incomplete Fields !!!', 'Fill all the fields.')
    else:
        runthreadcommand(getname, getemail, getwebsite, getatpage, getnoofpage, getcomment)


def clearcommand():
    entrybox_authorname.delete(0, END)
    entrybox_email.delete(0, END)
    entrybox_website.delete(0, END)
    entrybox_atpage.delete(0, END)
    entrybox_noofpage.delete(0, END)
    commentTextarea.delete(1.0, END)


def runthreadcommand(getname, getemail, getwebsite, getatpage, getnoofpage, getcomment):
    threading.Thread(target=runcommand, args=(getname, getemail, getwebsite, getatpage, getnoofpage, getcomment,)).start()


def mainwindow():                                                             # window body
    global  window, entrybox_authorname, entrybox_email, entrybox_website, entrybox_atpage, entrybox_noofpage, commentTextarea

    window = Tk()
    window.geometry('620x550')
    window.title('Wordpress Comment Automation')

    # validate only numbers
    def only_numbers(char):
        return char.isdigit()
    validation = window.register(only_numbers)

    # author name
    label_authorname = Label(window, text='Author Name', font=('Times New Roman', 11))
    label_authorname.place(relx=0.03, rely=0.07, anchor='nw')
    entrybox_authorname = Entry(window)
    entrybox_authorname.place(relx=0.22, rely=0.07, anchor='nw')

    # email
    label_email = Label(window, text='Email', font=('Times New Roman', 11))
    label_email.place(relx=0.03, rely=0.16, anchor='nw')
    entrybox_email = Entry(window)
    entrybox_email.place(relx=0.22, rely=0.16, anchor='nw')

    # website
    label_website = Label(window, text='Website', font=('Times New Roman', 11))
    label_website.place(relx=0.03, rely=0.25, anchor='nw')
    entrybox_website = Entry(window)
    entrybox_website.place(relx=0.22, rely=0.25, anchor='nw')

    # atpage
    label_atpage = Label(window, text='At Page', font=('Times New Roman', 11))
    label_atpage.place(relx=0.03, rely=0.34, anchor='nw')
    entrybox_atpage = Entry(window, validate="key",validatecommand=(validation, '%S'))
    entrybox_atpage.place(relx=0.22, rely=0.34, anchor='nw')

    # no.of page
    label_noofpage = Label(window, text='No of page', font=('Times New Roman', 11))
    label_noofpage.place(relx=0.03, rely=0.43, anchor='nw')
    entrybox_noofpage = Entry(window, validate="key",validatecommand=(validation, '%S'))
    entrybox_noofpage.place(relx=0.22, rely=0.43, anchor='nw')

    # comment
    label_comment = Label(window, text='Comment', font=('Times New Roman', 11))
    label_comment.place(relx=0.03, rely=0.52, anchor='nw')
    commentTextarea = Text(window, font=('Times New Roman', 10), width=49, height=13)
    commentTextarea.place(relx=0.22, rely=0.52, anchor='nw')
    commentTextarea.config(padx=5, pady=5)

    generate_button = Button(window, text='Run', command=getfieldscommand, font=('Times New Roman', 11))
    generate_button.place(relx=0.6, rely=0.20, anchor='nw')
    
    clear_button = Button(window, text='Clear', command=clearcommand, font=('Times New Roman', 11))
    clear_button.place(relx=0.6, rely=0.30, anchor='nw')
    
    window.mainloop()

if __name__ == '__main__':
    # runcommand()
    mainwindow()


