#! python3
# Standard 1 volume German anonymous checkout

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

print('Running checkout with standard product, one volume, anonymous Austrian user, Credit Card...')
docs_dir = 'C:\\Users\\pzakharevich\\Desktop\\Image attachments\\Testdata\\'
pdf_docs = []
for item in os.listdir(docs_dir):
    if item.endswith('.pdf'):
        pdf_docs.append(item)
    else:
        pass
for pdf in pdf_docs:
    print(str(pdf_docs.index(pdf)) + ' ' + pdf)
print('\nType number of the document you want to print.\n')
pdf_number_1 = int(input('Document: '))
pdf_number_2 = int(input('Document: '))
pdf_number_3 = int(input('Document: '))

# Create instance and go to landing page:

browser = webdriver.Chrome('C:\ChromeDriver\chromedriver.exe')
browser.get('https://staging.pluspeter.com')
browser.maximize_window()

# Open standard wizard:


def add_standard_flow():

    WebDriverWait(browser, 5).until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
    browser.find_element_by_xpath("//div[@class='button-bottom-holder']/button[@id='print_europe']").click()


add_standard_flow()

# Add document:


WebDriverWait(browser, 7).until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.NAME, 'file-input')))
browser.find_element_by_name('file-input').send_keys(docs_dir + pdf_docs[pdf_number_1])

# Select and accept document orientation:

WebDriverWait(browser, 7).until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
try:
    orientation_options = browser.find_elements_by_xpath("//span[@class='input-radio']")
    orientation_options[1].click()
    browser.find_element_by_xpath("//button[@type='submit']").click()
except IndexError:
    print('Document is portrait. Skipping document orientation flow...')

# Set volume options:

WebDriverWait(browser, 7).until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
volume_options = browser.find_elements_by_xpath("//div[@class='profil-select select-search-input div-as-input']")
volume_options[0].click()
browser.find_element_by_xpath("//div[@value='1c']").click()
WebDriverWait(browser, 7).until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
# volume_options[1].click()
# browser.find_element_by_xpath("//div[@value='punched']").click()
# WebDriverWait(browser, 7).until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
volume_options[2].click()
browser.find_element_by_xpath("//div[@value='dark_blue']").click()
WebDriverWait(browser, 7).until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
browser.find_element_by_xpath("//input[@placeholder='Titel']").send_keys('Stan/dard-by bot!')
browser.find_element_by_id('wizard').click()
WebDriverWait(browser, 7).until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

# Fill profile:

browser.find_element_by_xpath("//a[@class='letter-file']").click()
WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, "//form[@id='user_profile_form_wizard']")))
profile_selectors = browser.find_elements_by_xpath("//form[@id='user_profile_form_wizard']"
                                                   "/div/div/div[@class='fields-block']/div"
                                                   "/div[@class='field-group fields-row__item']")
profile_selectors[0].click()
browser.find_element_by_xpath("//div[@value='f']").click()
profile_selectors[1].click()
browser.find_element_by_xpath("//div[@value='at']").click()
browser.find_element_by_id('vorname').send_keys('Magdalena')
browser.find_element_by_id('name').send_keys('Baumgartner')
browser.find_element_by_id('email').send_keys('magda2000@subdomain.domain.com.de')
browser.find_element_by_id('Handynummer').send_keys('+436234567890')
browser.find_element_by_id('Adresse').send_keys('Dorotheergasse')
browser.find_element_by_id('Hausnummer').send_keys('551fsT')
# browser.find_element_by_id('Zusatz').send_keys('45/66-B d. 9')
browser.find_element_by_id('Stadt').send_keys('Sankt Pölten')
browser.find_element_by_id('zip_code').send_keys('2431')
browser.find_element_by_id('wizard_profile_update_btn').click()

# Add second Standard volume and add two documents:

WebDriverWait(browser, 5).until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
browser.find_element_by_xpath("//a[@href='#']").click()
add_standard_flow()
WebDriverWait(browser, 7).until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
browser.execute_script('window.scrollTo(0, 900)')
file_input = browser.find_elements(By.NAME, 'file-input')
file_input[1].send_keys(docs_dir + pdf_docs[pdf_number_2])
try:
    WebDriverWait(browser, 7).until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
    browser.find_element_by_xpath("//button[@type='submit']").click()
except NoSuchElementException:
    print('Document is portrait. Skipping document orientation flow...')
WebDriverWait(browser, 7).until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
file_input[1].send_keys(docs_dir + pdf_docs[pdf_number_3])
try:
    WebDriverWait(browser, 7).until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
    browser.find_element_by_xpath("//button[@type='submit']").click()
except NoSuchElementException:
    print('Document is portrait. Skipping document orientation flow...')

# Remove document, change orientation, remove volume:

WebDriverWait(browser, 15).until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
volume_documents = browser.find_elements_by_xpath("//div[@class='pdf-placer']")
document_remove = browser.find_elements_by_xpath("//button[@class='closer closer--dark "
                                                 "delete-func closer-volumes']")
ActionChains(browser).move_to_element(volume_documents[2]).move_to_element(document_remove[2]).click(
    document_remove[2]).perform()
WebDriverWait(browser, 7).until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
orientation_options_volume = browser.find_elements_by_xpath("//span[@class='big']")
try:
    orientation_options_volume[1].click()
except IndexError:
    print('Document is portrait. Skipping document orientation flow...')
WebDriverWait(browser, 7).until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
volume_remove = browser.find_elements_by_xpath("//button[@class='closer closer--red closer--small']")
volume_remove[1].click()

# Mark checkboxes and open Stripe:

WebDriverWait(browser, 12).until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, 'paypal3'))).click()
browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
browser.find_element_by_xpath("//label[@for='checkbox-3']").click()
browser.find_element_by_id('paypalPayment').click()
# WebDriverWait(browser, 10).until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
# WebDriverWait(browser, 10).until(EC.url_contains('www.sandbox.paypal.com'))

# PayPal checkout:

# WebDriverWait(browser, 25).until(EC.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
# try:
#     browser.find_element_by_xpath("//a[@class='btn full ng-binding']").click()
# except NoSuchElementException:
#     print("Log in button not found. Trying to find email field...")
# WebDriverWait(browser, 25).until(EC.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
# WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'login_email'))).send_keys(
#     'info-buyer@printpeter.de')
# WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, 'btnNext'))).click()
# WebDriverWait(browser, 25).until(EC.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
# WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, 'password'))).send_keys('fdjkru12')
# browser.find_element_by_id('btnLogin').click()
# WebDriverWait(browser, 30).until(EC.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
# browser.find_element_by_id('confirmButtonTop').click()
# WebDriverWait(browser, 25).until(EC.invisibility_of_element_located((By.ID, 'preloaderSpinner')))

# Switch to stripe and finish checkout:

WebDriverWait(browser, 20).until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
WebDriverWait(browser, 15).until(EC.frame_to_be_available_and_switch_to_it('stripe_checkout_app'))
browser.find_element_by_xpath("//input[@placeholder='Card number']").send_keys('5105105105105100')
browser.find_element_by_xpath("//input[@placeholder='MM / YY']").send_keys('624')
browser.find_element_by_xpath("//input[@placeholder='CVC']").send_keys('518')
browser.find_element_by_xpath("//input[@placeholder='ZIP Code']").send_keys('8756')
browser.find_element_by_xpath("//button[@type='submit']").click()
browser.switch_to.default_content()

# Go to landing:

WebDriverWait(browser, 5).until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@class='closer']"))).click()

# Quit:

# WebDriverWait(browser, 12).until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
# WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.LINK_TEXT, "Abmelden"))).click()
WebDriverWait(browser, 12).until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
browser.quit()
