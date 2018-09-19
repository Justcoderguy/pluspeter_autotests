import unittest
import random
import os
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import WebDriverException, NoSuchElementException


# IMPORTANT: before running these tests make sure daily print limit is not reached;
# full stop print is not activated, and user is able to make free Freemium+ order.

# Project documents are located here:
docs_dir = 'C:\\Users\\pzakharevich\\Desktop\\Education\\PlusPeter\\docs'
# Test documents are located here:
test_docs_dir = 'C:\\Users\\pzakharevich\\Desktop\\Image attachments\\Testdata\\'
# Credit card credentials
card_numbers = ['4242424242424242', '4000056655665556', '5555555555554444', '2223003122003222',
                '5200828282828210', '5105105105105100', '378282246310005', '371449635398431']
selected_card_number = random.choice(card_numbers)


class StandardFlow(unittest.TestCase):

    def setUp(self):

        self.browser = webdriver.Chrome('C:\ChromeDriver\chromedriver.exe')

    def test_4c_wireo_blau(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_4c_wireo_blau.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Create list of available test documents
        print('Running checkout with freemium or freemium plus product.')
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have more than 25, but less than 170 pages for this test
        pdf_number = 0
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Go to login page and sign in:
        logging.debug('Clicking on login button.')
        browser.find_element_by_link_text('Login').click()
        logging.debug('Typing login.')
        browser.find_element_by_id('id_username').send_keys(login)
        logging.debug('Typing password.')
        browser.find_element_by_id('id_password').send_keys(password)
        logging.debug('Submitting login form.')
        browser.find_element_by_id('id_password').submit()

        # Profile page opens:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to products page:
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Open Standard volume:
        logging.debug('Clicking on "Print now" button for Standard.')
        browser.find_element_by_id('print_europe').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document:
        logging.debug('Uploading document ' + pdf_docs[pdf_number])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        try:
            logging.debug('Submitting document pages orientation.')
            browser.find_element_by_xpath("//button[@type='submit']").click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
        except WebDriverException:
            logging.debug('Document has no landscape pages.')

        # Typing Standard volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[2]/div/div/div[2]/input').send_keys(
            'Stan/dard by-b0t! vol1 blue cover')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Select Credit Card payment method:
        browser.find_element_by_id('paypal3').click()
        logging.debug('Clicked on "Credit card" radiobutton')
        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-3']").click()
        # Initiate payment
        logging.debug('Clicking on "Print now" button.')
        browser.find_element_by_id('paypalPayment').click()

        # Switch to stripe frame
        logging.debug('Switching to stripe frame.')
        WebDriverWait(browser, 60).until(ec.frame_to_be_available_and_switch_to_it('stripe_checkout_app'))
        logging.debug('Typing card number (Stripe).')
        # Type card number
        browser.find_element_by_xpath("//input[@placeholder='Card number']").send_keys(selected_card_number)
        # Type card month/year
        logging.debug('Typing month/year (Stripe).')
        browser.find_element_by_xpath("//input[@placeholder='MM / YY']").send_keys('0123')
        # Type card CVC
        logging.debug('Typing CVC (Stripe)')
        browser.find_element_by_xpath("//input[@placeholder='CVC']").send_keys('456')
        # Type card zip code
        logging.debug('Typing zip code (Stripe).')
        try:
            browser.find_element_by_xpath("//input[@placeholder='ZIP Code']").send_keys('7890')
        except NoSuchElementException:
            # Not all card types require zip code
            logging.debug('Zip code field was not located.')
        # Submit Stripe form
        logging.debug('Submitting Stripe.')
        browser.find_element_by_xpath("//button[@type='submit']").click()
        # Switch back from frame
        logging.debug('Switching to default content.')
        browser.switch_to.default_content()

        # Successful upload page opens
        logging.debug('Successful upload page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to profile page
        logging.debug('Clicking on "Close" button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH, "//a[@class='closer']"))).click()

        # Logout:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on Logout button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.LINK_TEXT, "Abmelden"))).click()
        logging.debug('Landing page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        browser.quit()

    def test_4c_wireo_grun(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_4c_wireo_blau.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Set Paypal credentials:
        paypal_login = 'info-buyer@printpeter.de'
        paypal_password = 'fdjkru12'

        # Create list of available test documents
        print('Running checkout with freemium or freemium plus product.')
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have more than 25, but less than 170 pages for this test
        pdf_number = 4
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Go to login page and sign in:
        logging.debug('Clicking on login button.')
        browser.find_element_by_link_text('Login').click()
        logging.debug('Typing login.')
        browser.find_element_by_id('id_username').send_keys(login)
        logging.debug('Typing password.')
        browser.find_element_by_id('id_password').send_keys(password)
        logging.debug('Submitting login form.')
        browser.find_element_by_id('id_password').submit()

        # Profile page opens:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to products page:
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Open Standard volume:
        logging.debug('Clicking on "Print now" button for Standard.')
        browser.find_element_by_id('print_europe').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document:
        logging.debug('Uploading document ' + pdf_docs[pdf_number])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        try:
            logging.debug('Submitting document pages orientation.')
            browser.find_element_by_xpath("//button[@type='submit']").click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
        except WebDriverException:
            logging.debug('Document has no landscape pages.')

        # Set volume options:
        volume_options = browser.find_elements_by_xpath(
            "//div[@class='profil-select select-search-input div-as-input']")
        volume_options[2].click()
        browser.find_element_by_xpath("//div[@value='green']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))

        # Typing Standard volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[2]/div/div/div[2]/input').send_keys(
            'Stan/dard by-b0t! vol1 green cover')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-3']").click()
        logging.debug('Clicking on "Print now" button.')
        browser.find_element_by_id('paypalPayment').click()
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Wizard page rendered.')
        # Make sure URL changed to Paypal
        logging.debug('Waiting for URL to be changed to "www.sandbox.paypal.com"')
        WebDriverWait(browser, 60).until(ec.url_contains('www.sandbox.paypal.com'))

        # PayPal checkout:
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        try:
            # Open log in page
            logging.debug('Clicking on login button (Paypal).')
            browser.find_element_by_xpath("//a[@class='btn full ng-binding']").click()
        except NoSuchElementException:
            logging.debug('Login button was not located.')
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Type Paypal login
        logging.debug('Typing Paypal login.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.NAME,
                                                                           'login_email'))).send_keys(paypal_login)
        # Send Paypal login
        logging.debug('Clicking on "Next" button.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.ID, 'btnNext'))).click()
        logging.debug('Paypal page rendring.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Type Paypal password
        logging.debug('Typing Paypal password.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.ID,
                                                                           'password'))).send_keys(paypal_password)
        # Send Paypal password
        logging.debug('Clicking on Login button.')
        browser.find_element_by_id('btnLogin').click()
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Confirm Paypal payment
        logging.debug('Clicking on "Continue" button.')
        browser.find_element_by_id('confirmButtonTop').click()
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))

        # Successful upload page opens:
        logging.debug('Successful upload page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to profile:
        logging.debug('Clicking on "Close" button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH, "//a[@class='closer']"))).click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Profile page rendered.')

        # Logout and quit:
        logging.debug('Clicking on Logout button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.LINK_TEXT, "Abmelden"))).click()
        logging.debug('Landing page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        browser.quit()

    def test_4c_wireo_violett(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_4c_wireo_blau.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Create list of available test documents
        print('Running checkout with freemium or freemium plus product.')
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have more than 25, but less than 170 pages for this test
        pdf_number = 4
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Go to login page and sign in:
        logging.debug('Clicking on login button.')
        browser.find_element_by_link_text('Login').click()
        logging.debug('Typing login.')
        browser.find_element_by_id('id_username').send_keys(login)
        logging.debug('Typing password.')
        browser.find_element_by_id('id_password').send_keys(password)
        logging.debug('Submitting login form.')
        browser.find_element_by_id('id_password').submit()

        # Profile page opens:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to products page:
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Open Standard volume:
        logging.debug('Clicking on "Print now" button for Standard.')
        browser.find_element_by_id('print_europe').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document:
        logging.debug('Uploading document ' + pdf_docs[pdf_number])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        try:
            logging.debug('Submitting document pages orientation.')
            browser.find_element_by_xpath("//button[@type='submit']").click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
        except WebDriverException:
            logging.debug('Document has no landscape pages.')

        # Set volume options:
        volume_options = browser.find_elements_by_xpath(
            "//div[@class='profil-select select-search-input div-as-input']")
        volume_options[2].click()
        browser.find_element_by_xpath("//div[@value='purple']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))

        # Typing Standard volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[2]/div/div/div[2]/input').send_keys(
            'Stan/dard by-b0t! vol1 purple cover')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Select Credit Card payment method:
        browser.find_element_by_id('paypal3').click()
        logging.debug('Clicked on "Credit card" radiobutton')
        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-3']").click()
        # Initiate payment
        logging.debug('Clicking on "Print now" button.')
        browser.find_element_by_id('paypalPayment').click()

        # Switch to stripe frame
        logging.debug('Switching to stripe frame.')
        WebDriverWait(browser, 60).until(ec.frame_to_be_available_and_switch_to_it('stripe_checkout_app'))
        logging.debug('Typing card number (Stripe).')
        # Type card number
        browser.find_element_by_xpath("//input[@placeholder='Card number']").send_keys(selected_card_number)
        # Type card month/year
        logging.debug('Typing month/year (Stripe).')
        browser.find_element_by_xpath("//input[@placeholder='MM / YY']").send_keys('0123')
        # Type card CVC
        logging.debug('Typing CVC (Stripe)')
        browser.find_element_by_xpath("//input[@placeholder='CVC']").send_keys('456')
        # Type card zip code
        logging.debug('Typing zip code (Stripe).')
        try:
            browser.find_element_by_xpath("//input[@placeholder='ZIP Code']").send_keys('7890')
        except NoSuchElementException:
            # Not all card types require zip code
            logging.debug('Zip code field was not located.')
        # Submit Stripe form
        logging.debug('Submitting Stripe.')
        browser.find_element_by_xpath("//button[@type='submit']").click()
        # Switch back from frame
        logging.debug('Switching to default content.')
        browser.switch_to.default_content()

        # Successful upload page opens
        logging.debug('Successful upload page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to profile page
        logging.debug('Clicking on "Close" button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH, "//a[@class='closer']"))).click()

        # Logout:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on Logout button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.LINK_TEXT, "Abmelden"))).click()
        logging.debug('Landing page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        browser.quit()

    def test_4c_wireo_rot(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_4c_wireo_blau.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Set Paypal credentials:
        paypal_login = 'info-buyer@printpeter.de'
        paypal_password = 'fdjkru12'

        # Create list of available test documents
        print('Running checkout with freemium or freemium plus product.')
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have more than 25, but less than 170 pages for this test
        pdf_number = 11
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Go to login page and sign in:
        logging.debug('Clicking on login button.')
        browser.find_element_by_link_text('Login').click()
        logging.debug('Typing login.')
        browser.find_element_by_id('id_username').send_keys(login)
        logging.debug('Typing password.')
        browser.find_element_by_id('id_password').send_keys(password)
        logging.debug('Submitting login form.')
        browser.find_element_by_id('id_password').submit()

        # Profile page opens:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to products page:
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Open Standard volume:
        logging.debug('Clicking on "Print now" button for Standard.')
        browser.find_element_by_id('print_europe').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document:
        logging.debug('Uploading document ' + pdf_docs[pdf_number])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        try:
            logging.debug('Submitting document pages orientation.')
            browser.find_element_by_xpath("//button[@type='submit']").click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
        except WebDriverException:
            logging.debug('Document has no landscape pages.')

        # Set volume options:
        volume_options = browser.find_elements_by_xpath(
            "//div[@class='profil-select select-search-input div-as-input']")
        volume_options[2].click()
        browser.find_element_by_xpath("//div[@value='red']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))

        # Typing Standard volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[2]/div/div/div[2]/input').send_keys(
            'Stan/dard by-b0t! vol1 red cover')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-3']").click()
        logging.debug('Clicking on "Print now" button.')
        browser.find_element_by_id('paypalPayment').click()
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Wizard page rendered.')
        # Make sure URL changed to Paypal
        logging.debug('Waiting for URL to be changed to "www.sandbox.paypal.com"')
        WebDriverWait(browser, 60).until(ec.url_contains('www.sandbox.paypal.com'))

        # PayPal checkout:
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        try:
            # Open log in page
            logging.debug('Clicking on login button (Paypal).')
            browser.find_element_by_xpath("//a[@class='btn full ng-binding']").click()
        except NoSuchElementException:
            logging.debug('Login button was not located.')
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Type Paypal login
        logging.debug('Typing Paypal login.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.NAME,
                                                                           'login_email'))).send_keys(paypal_login)
        # Send Paypal login
        logging.debug('Clicking on "Next" button.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.ID, 'btnNext'))).click()
        logging.debug('Paypal page rendring.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Type Paypal password
        logging.debug('Typing Paypal password.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.ID,
                                                                           'password'))).send_keys(paypal_password)
        # Send Paypal password
        logging.debug('Clicking on Login button.')
        browser.find_element_by_id('btnLogin').click()
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Confirm Paypal payment
        logging.debug('Clicking on "Continue" button.')
        browser.find_element_by_id('confirmButtonTop').click()
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))

        # Successful upload page opens:
        logging.debug('Successful upload page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to profile:
        logging.debug('Clicking on "Close" button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH, "//a[@class='closer']"))).click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Profile page rendered.')

        # Logout and quit:
        logging.debug('Clicking on Logout button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.LINK_TEXT, "Abmelden"))).click()
        logging.debug('Landing page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        browser.quit()

    def test_4c_wireo_gelb(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_4c_wireo_blau.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Create list of available test documents
        print('Running checkout with freemium or freemium plus product.')
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have more than 25, but less than 170 pages for this test
        pdf_number = 11
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Go to login page and sign in:
        logging.debug('Clicking on login button.')
        browser.find_element_by_link_text('Login').click()
        logging.debug('Typing login.')
        browser.find_element_by_id('id_username').send_keys(login)
        logging.debug('Typing password.')
        browser.find_element_by_id('id_password').send_keys(password)
        logging.debug('Submitting login form.')
        browser.find_element_by_id('id_password').submit()

        # Profile page opens:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to products page:
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Open Standard volume:
        logging.debug('Clicking on "Print now" button for Standard.')
        browser.find_element_by_id('print_europe').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document:
        logging.debug('Uploading document ' + pdf_docs[pdf_number])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        try:
            logging.debug('Submitting document pages orientation.')
            browser.find_element_by_xpath("//button[@type='submit']").click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
        except WebDriverException:
            logging.debug('Document has no landscape pages.')

        # Set volume options:
        volume_options = browser.find_elements_by_xpath(
            "//div[@class='profil-select select-search-input div-as-input']")
        volume_options[2].click()
        browser.find_element_by_xpath("//div[@value='yellow']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))

        # Typing Standard volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[2]/div/div/div[2]/input').send_keys(
            'Stan/dard by-b0t! vol1 yellow cover')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Select Credit Card payment method:
        browser.find_element_by_id('paypal3').click()
        logging.debug('Clicked on "Credit card" radiobutton')
        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-3']").click()
        # Initiate payment
        logging.debug('Clicking on "Print now" button.')
        browser.find_element_by_id('paypalPayment').click()

        # Switch to stripe frame
        logging.debug('Switching to stripe frame.')
        WebDriverWait(browser, 60).until(ec.frame_to_be_available_and_switch_to_it('stripe_checkout_app'))
        logging.debug('Typing card number (Stripe).')
        # Type card number
        browser.find_element_by_xpath("//input[@placeholder='Card number']").send_keys(selected_card_number)
        # Type card month/year
        logging.debug('Typing month/year (Stripe).')
        browser.find_element_by_xpath("//input[@placeholder='MM / YY']").send_keys('0123')
        # Type card CVC
        logging.debug('Typing CVC (Stripe)')
        browser.find_element_by_xpath("//input[@placeholder='CVC']").send_keys('456')
        # Type card zip code
        logging.debug('Typing zip code (Stripe).')
        try:
            browser.find_element_by_xpath("//input[@placeholder='ZIP Code']").send_keys('7890')
        except NoSuchElementException:
            # Not all card types require zip code
            logging.debug('Zip code field was not located.')
        # Submit Stripe form
        logging.debug('Submitting Stripe.')
        browser.find_element_by_xpath("//button[@type='submit']").click()
        # Switch back from frame
        logging.debug('Switching to default content.')
        browser.switch_to.default_content()

        # Successful upload page opens
        logging.debug('Successful upload page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to profile page
        logging.debug('Clicking on "Close" button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH, "//a[@class='closer']"))).click()

        # Logout:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on Logout button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.LINK_TEXT, "Abmelden"))).click()
        logging.debug('Landing page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        browser.quit()

    def test_4c_wireo_dunkelblau(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_4c_wireo_blau.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Set Paypal credentials:
        paypal_login = 'info-buyer@printpeter.de'
        paypal_password = 'fdjkru12'

        # Create list of available test documents
        print('Running checkout with freemium or freemium plus product.')
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have more than 25, but less than 170 pages for this test
        pdf_number = 11
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Go to login page and sign in:
        logging.debug('Clicking on login button.')
        browser.find_element_by_link_text('Login').click()
        logging.debug('Typing login.')
        browser.find_element_by_id('id_username').send_keys(login)
        logging.debug('Typing password.')
        browser.find_element_by_id('id_password').send_keys(password)
        logging.debug('Submitting login form.')
        browser.find_element_by_id('id_password').submit()

        # Profile page opens:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to products page:
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Open Standard volume:
        logging.debug('Clicking on "Print now" button for Standard.')
        browser.find_element_by_id('print_europe').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document:
        logging.debug('Uploading document ' + pdf_docs[pdf_number])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        try:
            logging.debug('Submitting document pages orientation.')
            browser.find_element_by_xpath("//button[@type='submit']").click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
        except WebDriverException:
            logging.debug('Document has no landscape pages.')

        # Set volume options:
        volume_options = browser.find_elements_by_xpath(
            "//div[@class='profil-select select-search-input div-as-input']")
        volume_options[2].click()
        browser.find_element_by_xpath("//div[@value='dark_blue']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))

        # Typing Standard volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[2]/div/div/div[2]/input').send_keys(
            'Stan/dard by-b0t! vol1 dark blue cover')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-3']").click()
        logging.debug('Clicking on "Print now" button.')
        browser.find_element_by_id('paypalPayment').click()
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Wizard page rendered.')
        # Make sure URL changed to Paypal
        logging.debug('Waiting for URL to be changed to "www.sandbox.paypal.com"')
        WebDriverWait(browser, 60).until(ec.url_contains('www.sandbox.paypal.com'))

        # PayPal checkout:
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        try:
            # Open log in page
            logging.debug('Clicking on login button (Paypal).')
            browser.find_element_by_xpath("//a[@class='btn full ng-binding']").click()
        except NoSuchElementException:
            logging.debug('Login button was not located.')
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Type Paypal login
        logging.debug('Typing Paypal login.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.NAME,
                                                                           'login_email'))).send_keys(paypal_login)
        # Send Paypal login
        logging.debug('Clicking on "Next" button.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.ID, 'btnNext'))).click()
        logging.debug('Paypal page rendring.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Type Paypal password
        logging.debug('Typing Paypal password.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.ID,
                                                                           'password'))).send_keys(paypal_password)
        # Send Paypal password
        logging.debug('Clicking on Login button.')
        browser.find_element_by_id('btnLogin').click()
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Confirm Paypal payment
        logging.debug('Clicking on "Continue" button.')
        browser.find_element_by_id('confirmButtonTop').click()
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))

        # Successful upload page opens:
        logging.debug('Successful upload page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to profile:
        logging.debug('Clicking on "Close" button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH, "//a[@class='closer']"))).click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Profile page rendered.')

        # Logout and quit:
        logging.debug('Clicking on Logout button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.LINK_TEXT, "Abmelden"))).click()
        logging.debug('Landing page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        browser.quit()

    def test_4c_wireo_hellblau(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_4c_wireo_blau.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Create list of available test documents
        print('Running checkout with freemium or freemium plus product.')
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have more than 25, but less than 170 pages for this test
        pdf_number = 12
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Go to login page and sign in:
        logging.debug('Clicking on login button.')
        browser.find_element_by_link_text('Login').click()
        logging.debug('Typing login.')
        browser.find_element_by_id('id_username').send_keys(login)
        logging.debug('Typing password.')
        browser.find_element_by_id('id_password').send_keys(password)
        logging.debug('Submitting login form.')
        browser.find_element_by_id('id_password').submit()

        # Profile page opens:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to products page:
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Open Standard volume:
        logging.debug('Clicking on "Print now" button for Standard.')
        browser.find_element_by_id('print_europe').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document:
        logging.debug('Uploading document ' + pdf_docs[pdf_number])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        try:
            logging.debug('Submitting document pages orientation.')
            browser.find_element_by_xpath("//button[@type='submit']").click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
        except WebDriverException:
            logging.debug('Document has no landscape pages.')

        # Set volume options:
        volume_options = browser.find_elements_by_xpath(
            "//div[@class='profil-select select-search-input div-as-input']")
        volume_options[2].click()
        browser.find_element_by_xpath("//div[@value='light_blue']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))

        # Typing Standard volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[2]/div/div/div[2]/input').send_keys(
            'Stan/dard by-b0t! vol1 bright blue')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Select Credit Card payment method:
        browser.find_element_by_id('paypal3').click()
        logging.debug('Clicked on "Credit card" radiobutton')
        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-3']").click()
        # Initiate payment
        logging.debug('Clicking on "Print now" button.')
        browser.find_element_by_id('paypalPayment').click()

        # Switch to stripe frame
        logging.debug('Switching to stripe frame.')
        WebDriverWait(browser, 60).until(ec.frame_to_be_available_and_switch_to_it('stripe_checkout_app'))
        logging.debug('Typing card number (Stripe).')
        # Type card number
        browser.find_element_by_xpath("//input[@placeholder='Card number']").send_keys(selected_card_number)
        # Type card month/year
        logging.debug('Typing month/year (Stripe).')
        browser.find_element_by_xpath("//input[@placeholder='MM / YY']").send_keys('0123')
        # Type card CVC
        logging.debug('Typing CVC (Stripe)')
        browser.find_element_by_xpath("//input[@placeholder='CVC']").send_keys('456')
        # Type card zip code
        logging.debug('Typing zip code (Stripe).')
        try:
            browser.find_element_by_xpath("//input[@placeholder='ZIP Code']").send_keys('7890')
        except NoSuchElementException:
            # Not all card types require zip code
            logging.debug('Zip code field was not located.')
        # Submit Stripe form
        logging.debug('Submitting Stripe.')
        browser.find_element_by_xpath("//button[@type='submit']").click()
        # Switch back from frame
        logging.debug('Switching to default content.')
        browser.switch_to.default_content()

        # Successful upload page opens
        logging.debug('Successful upload page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to profile page
        logging.debug('Clicking on "Close" button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH, "//a[@class='closer']"))).click()

        # Logout:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on Logout button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.LINK_TEXT, "Abmelden"))).click()
        logging.debug('Landing page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        browser.quit()

    def test_4c_punched_blau(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_4c_punched_blau.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Create list of available test documents
        print('Running checkout with freemium or freemium plus product.')
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have more than 25, but less than 170 pages for this test
        pdf_number = 0
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Go to login page and sign in:
        logging.debug('Clicking on login button.')
        browser.find_element_by_link_text('Login').click()
        logging.debug('Typing login.')
        browser.find_element_by_id('id_username').send_keys(login)
        logging.debug('Typing password.')
        browser.find_element_by_id('id_password').send_keys(password)
        logging.debug('Submitting login form.')
        browser.find_element_by_id('id_password').submit()

        # Profile page opens:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to products page:
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Open Standard volume:
        logging.debug('Clicking on "Print now" button for Standard.')
        browser.find_element_by_id('print_europe').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document:
        logging.debug('Uploading document ' + pdf_docs[pdf_number])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        try:
            logging.debug('Submitting document pages orientation.')
            browser.find_element_by_xpath("//button[@type='submit']").click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
        except WebDriverException:
            logging.debug('Document has no landscape pages.')

        # Set volume options:
        volume_options = browser.find_elements_by_xpath(
            "//div[@class='profil-select select-search-input div-as-input']")
        volume_options[1].click()
        browser.find_element_by_xpath("//div[@value='punched']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))

        # Typing Standard volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[2]/div/div/div[2]/input').send_keys(
            'Stan/dard by-b0t! vol1 blue cover')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Select Credit Card payment method:
        browser.find_element_by_id('paypal3').click()
        logging.debug('Clicked on "Credit card" radiobutton')
        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-3']").click()
        # Initiate payment
        logging.debug('Clicking on "Print now" button.')
        browser.find_element_by_id('paypalPayment').click()

        # Switch to stripe frame
        logging.debug('Switching to stripe frame.')
        WebDriverWait(browser, 60).until(ec.frame_to_be_available_and_switch_to_it('stripe_checkout_app'))
        logging.debug('Typing card number (Stripe).')
        # Type card number
        browser.find_element_by_xpath("//input[@placeholder='Card number']").send_keys(selected_card_number)
        # Type card month/year
        logging.debug('Typing month/year (Stripe).')
        browser.find_element_by_xpath("//input[@placeholder='MM / YY']").send_keys('0123')
        # Type card CVC
        logging.debug('Typing CVC (Stripe)')
        browser.find_element_by_xpath("//input[@placeholder='CVC']").send_keys('456')
        # Type card zip code
        logging.debug('Typing zip code (Stripe).')
        try:
            browser.find_element_by_xpath("//input[@placeholder='ZIP Code']").send_keys('7890')
        except NoSuchElementException:
            # Not all card types require zip code
            logging.debug('Zip code field was not located.')
        # Submit Stripe form
        logging.debug('Submitting Stripe.')
        browser.find_element_by_xpath("//button[@type='submit']").click()
        # Switch back from frame
        logging.debug('Switching to default content.')
        browser.switch_to.default_content()

        # Successful upload page opens
        logging.debug('Successful upload page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to profile page
        logging.debug('Clicking on "Close" button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH, "//a[@class='closer']"))).click()

        # Logout:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on Logout button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.LINK_TEXT, "Abmelden"))).click()
        logging.debug('Landing page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        browser.quit()

    def test_4c_punched_grun(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_4c_punched_grun.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Set Paypal credentials:
        paypal_login = 'info-buyer@printpeter.de'
        paypal_password = 'fdjkru12'

        # Create list of available test documents
        print('Running checkout with freemium or freemium plus product.')
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have more than 25, but less than 170 pages for this test
        pdf_number = 4
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Go to login page and sign in:
        logging.debug('Clicking on login button.')
        browser.find_element_by_link_text('Login').click()
        logging.debug('Typing login.')
        browser.find_element_by_id('id_username').send_keys(login)
        logging.debug('Typing password.')
        browser.find_element_by_id('id_password').send_keys(password)
        logging.debug('Submitting login form.')
        browser.find_element_by_id('id_password').submit()

        # Profile page opens:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to products page:
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Open Standard volume:
        logging.debug('Clicking on "Print now" button for Standard.')
        browser.find_element_by_id('print_europe').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document:
        logging.debug('Uploading document ' + pdf_docs[pdf_number])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        try:
            logging.debug('Submitting document pages orientation.')
            browser.find_element_by_xpath("//button[@type='submit']").click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
        except WebDriverException:
            logging.debug('Document has no landscape pages.')

        # Set volume options:
        volume_options = browser.find_elements_by_xpath(
            "//div[@class='profil-select select-search-input div-as-input']")
        volume_options[1].click()
        browser.find_element_by_xpath("//div[@value='punched']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        volume_options[2].click()
        browser.find_element_by_xpath("//div[@value='green']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))

        # Typing Standard volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[2]/div/div/div[2]/input').send_keys(
            'Stan/dard by-b0t! vol1 green cover')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-3']").click()
        logging.debug('Clicking on "Print now" button.')
        browser.find_element_by_id('paypalPayment').click()
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Wizard page rendered.')
        # Make sure URL changed to Paypal
        logging.debug('Waiting for URL to be changed to "www.sandbox.paypal.com"')
        WebDriverWait(browser, 60).until(ec.url_contains('www.sandbox.paypal.com'))

        # PayPal checkout:
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        try:
            # Open log in page
            logging.debug('Clicking on login button (Paypal).')
            browser.find_element_by_xpath("//a[@class='btn full ng-binding']").click()
        except NoSuchElementException:
            logging.debug('Login button was not located.')
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Type Paypal login
        logging.debug('Typing Paypal login.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.NAME,
                                                                           'login_email'))).send_keys(paypal_login)
        # Send Paypal login
        logging.debug('Clicking on "Next" button.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.ID, 'btnNext'))).click()
        logging.debug('Paypal page rendring.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Type Paypal password
        logging.debug('Typing Paypal password.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.ID,
                                                                           'password'))).send_keys(paypal_password)
        # Send Paypal password
        logging.debug('Clicking on Login button.')
        browser.find_element_by_id('btnLogin').click()
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Confirm Paypal payment
        logging.debug('Clicking on "Continue" button.')
        browser.find_element_by_id('confirmButtonTop').click()
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))

        # Successful upload page opens:
        logging.debug('Successful upload page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to profile:
        logging.debug('Clicking on "Close" button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH, "//a[@class='closer']"))).click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Profile page rendered.')

        # Logout and quit:
        logging.debug('Clicking on Logout button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.LINK_TEXT, "Abmelden"))).click()
        logging.debug('Landing page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        browser.quit()

    def test_4c_punched_violett(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_4c_punched_violett.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Create list of available test documents
        print('Running checkout with freemium or freemium plus product.')
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have more than 25, but less than 170 pages for this test
        pdf_number = 4
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Go to login page and sign in:
        logging.debug('Clicking on login button.')
        browser.find_element_by_link_text('Login').click()
        logging.debug('Typing login.')
        browser.find_element_by_id('id_username').send_keys(login)
        logging.debug('Typing password.')
        browser.find_element_by_id('id_password').send_keys(password)
        logging.debug('Submitting login form.')
        browser.find_element_by_id('id_password').submit()

        # Profile page opens:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to products page:
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Open Standard volume:
        logging.debug('Clicking on "Print now" button for Standard.')
        browser.find_element_by_id('print_europe').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document:
        logging.debug('Uploading document ' + pdf_docs[pdf_number])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        try:
            logging.debug('Submitting document pages orientation.')
            browser.find_element_by_xpath("//button[@type='submit']").click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
        except WebDriverException:
            logging.debug('Document has no landscape pages.')

        # Set volume options:
        volume_options = browser.find_elements_by_xpath(
            "//div[@class='profil-select select-search-input div-as-input']")
        volume_options[1].click()
        browser.find_element_by_xpath("//div[@value='punched']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        volume_options[2].click()
        browser.find_element_by_xpath("//div[@value='purple']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))

        # Typing Standard volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[2]/div/div/div[2]/input').send_keys(
            'Stan/dard by-b0t! vol1 purple cover')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Select Credit Card payment method:
        browser.find_element_by_id('paypal3').click()
        logging.debug('Clicked on "Credit card" radiobutton')
        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-3']").click()
        # Initiate payment
        logging.debug('Clicking on "Print now" button.')
        browser.find_element_by_id('paypalPayment').click()

        # Switch to stripe frame
        logging.debug('Switching to stripe frame.')
        WebDriverWait(browser, 60).until(ec.frame_to_be_available_and_switch_to_it('stripe_checkout_app'))
        logging.debug('Typing card number (Stripe).')
        # Type card number
        browser.find_element_by_xpath("//input[@placeholder='Card number']").send_keys(selected_card_number)
        # Type card month/year
        logging.debug('Typing month/year (Stripe).')
        browser.find_element_by_xpath("//input[@placeholder='MM / YY']").send_keys('0123')
        # Type card CVC
        logging.debug('Typing CVC (Stripe)')
        browser.find_element_by_xpath("//input[@placeholder='CVC']").send_keys('456')
        # Type card zip code
        logging.debug('Typing zip code (Stripe).')
        try:
            browser.find_element_by_xpath("//input[@placeholder='ZIP Code']").send_keys('7890')
        except NoSuchElementException:
            # Not all card types require zip code
            logging.debug('Zip code field was not located.')
        # Submit Stripe form
        logging.debug('Submitting Stripe.')
        browser.find_element_by_xpath("//button[@type='submit']").click()
        # Switch back from frame
        logging.debug('Switching to default content.')
        browser.switch_to.default_content()

        # Successful upload page opens
        logging.debug('Successful upload page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to profile page
        logging.debug('Clicking on "Close" button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH, "//a[@class='closer']"))).click()

        # Logout:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on Logout button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.LINK_TEXT, "Abmelden"))).click()
        logging.debug('Landing page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        browser.quit()

    def test_4c_punched_rot(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_4c_punched_rot.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Set Paypal credentials:
        paypal_login = 'info-buyer@printpeter.de'
        paypal_password = 'fdjkru12'

        # Create list of available test documents
        print('Running checkout with freemium or freemium plus product.')
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have more than 25, but less than 170 pages for this test
        pdf_number = 11
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Go to login page and sign in:
        logging.debug('Clicking on login button.')
        browser.find_element_by_link_text('Login').click()
        logging.debug('Typing login.')
        browser.find_element_by_id('id_username').send_keys(login)
        logging.debug('Typing password.')
        browser.find_element_by_id('id_password').send_keys(password)
        logging.debug('Submitting login form.')
        browser.find_element_by_id('id_password').submit()

        # Profile page opens:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to products page:
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Open Standard volume:
        logging.debug('Clicking on "Print now" button for Standard.')
        browser.find_element_by_id('print_europe').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document:
        logging.debug('Uploading document ' + pdf_docs[pdf_number])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        try:
            logging.debug('Submitting document pages orientation.')
            browser.find_element_by_xpath("//button[@type='submit']").click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
        except WebDriverException:
            logging.debug('Document has no landscape pages.')

        # Set volume options:
        volume_options = browser.find_elements_by_xpath(
            "//div[@class='profil-select select-search-input div-as-input']")
        volume_options[1].click()
        browser.find_element_by_xpath("//div[@value='punched']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        volume_options[2].click()
        browser.find_element_by_xpath("//div[@value='red']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))

        # Typing Standard volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[2]/div/div/div[2]/input').send_keys(
            'Stan/dard by-b0t! vol1 red cover')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-3']").click()
        logging.debug('Clicking on "Print now" button.')
        browser.find_element_by_id('paypalPayment').click()
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Wizard page rendered.')
        # Make sure URL changed to Paypal
        logging.debug('Waiting for URL to be changed to "www.sandbox.paypal.com"')
        WebDriverWait(browser, 60).until(ec.url_contains('www.sandbox.paypal.com'))

        # PayPal checkout:
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        try:
            # Open log in page
            logging.debug('Clicking on login button (Paypal).')
            browser.find_element_by_xpath("//a[@class='btn full ng-binding']").click()
        except NoSuchElementException:
            logging.debug('Login button was not located.')
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Type Paypal login
        logging.debug('Typing Paypal login.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.NAME,
                                                                           'login_email'))).send_keys(paypal_login)
        # Send Paypal login
        logging.debug('Clicking on "Next" button.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.ID, 'btnNext'))).click()
        logging.debug('Paypal page rendring.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Type Paypal password
        logging.debug('Typing Paypal password.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.ID,
                                                                           'password'))).send_keys(paypal_password)
        # Send Paypal password
        logging.debug('Clicking on Login button.')
        browser.find_element_by_id('btnLogin').click()
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Confirm Paypal payment
        logging.debug('Clicking on "Continue" button.')
        browser.find_element_by_id('confirmButtonTop').click()
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))

        # Successful upload page opens:
        logging.debug('Successful upload page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to profile:
        logging.debug('Clicking on "Close" button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH, "//a[@class='closer']"))).click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Profile page rendered.')

        # Logout and quit:
        logging.debug('Clicking on Logout button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.LINK_TEXT, "Abmelden"))).click()
        logging.debug('Landing page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        browser.quit()

    def test_4c_punched_gelb(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_4c_punched_gelb.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Create list of available test documents
        print('Running checkout with freemium or freemium plus product.')
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have more than 25, but less than 170 pages for this test
        pdf_number = 11
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Go to login page and sign in:
        logging.debug('Clicking on login button.')
        browser.find_element_by_link_text('Login').click()
        logging.debug('Typing login.')
        browser.find_element_by_id('id_username').send_keys(login)
        logging.debug('Typing password.')
        browser.find_element_by_id('id_password').send_keys(password)
        logging.debug('Submitting login form.')
        browser.find_element_by_id('id_password').submit()

        # Profile page opens:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to products page:
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Open Standard volume:
        logging.debug('Clicking on "Print now" button for Standard.')
        browser.find_element_by_id('print_europe').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document:
        logging.debug('Uploading document ' + pdf_docs[pdf_number])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        try:
            logging.debug('Submitting document pages orientation.')
            browser.find_element_by_xpath("//button[@type='submit']").click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
        except WebDriverException:
            logging.debug('Document has no landscape pages.')

        # Set volume options:
        volume_options = browser.find_elements_by_xpath(
            "//div[@class='profil-select select-search-input div-as-input']")
        volume_options[1].click()
        browser.find_element_by_xpath("//div[@value='punched']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        volume_options[2].click()
        browser.find_element_by_xpath("//div[@value='yellow']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))

        # Typing Standard volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[2]/div/div/div[2]/input').send_keys(
            'Stan/dard by-b0t! vol1 yellow cover')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Select Credit Card payment method:
        browser.find_element_by_id('paypal3').click()
        logging.debug('Clicked on "Credit card" radiobutton')
        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-3']").click()
        # Initiate payment
        logging.debug('Clicking on "Print now" button.')
        browser.find_element_by_id('paypalPayment').click()

        # Switch to stripe frame
        logging.debug('Switching to stripe frame.')
        WebDriverWait(browser, 60).until(ec.frame_to_be_available_and_switch_to_it('stripe_checkout_app'))
        logging.debug('Typing card number (Stripe).')
        # Type card number
        browser.find_element_by_xpath("//input[@placeholder='Card number']").send_keys(selected_card_number)
        # Type card month/year
        logging.debug('Typing month/year (Stripe).')
        browser.find_element_by_xpath("//input[@placeholder='MM / YY']").send_keys('0123')
        # Type card CVC
        logging.debug('Typing CVC (Stripe)')
        browser.find_element_by_xpath("//input[@placeholder='CVC']").send_keys('456')
        # Type card zip code
        logging.debug('Typing zip code (Stripe).')
        try:
            browser.find_element_by_xpath("//input[@placeholder='ZIP Code']").send_keys('7890')
        except NoSuchElementException:
            # Not all card types require zip code
            logging.debug('Zip code field was not located.')
        # Submit Stripe form
        logging.debug('Submitting Stripe.')
        browser.find_element_by_xpath("//button[@type='submit']").click()
        # Switch back from frame
        logging.debug('Switching to default content.')
        browser.switch_to.default_content()

        # Successful upload page opens
        logging.debug('Successful upload page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to profile page
        logging.debug('Clicking on "Close" button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH, "//a[@class='closer']"))).click()

        # Logout:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on Logout button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.LINK_TEXT, "Abmelden"))).click()
        logging.debug('Landing page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        browser.quit()

    def test_4c_punched_dunkelblau(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_4c_punched_dunkelblau.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Set Paypal credentials:
        paypal_login = 'info-buyer@printpeter.de'
        paypal_password = 'fdjkru12'

        # Create list of available test documents
        print('Running checkout with freemium or freemium plus product.')
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have more than 25, but less than 170 pages for this test
        pdf_number = 11
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Go to login page and sign in:
        logging.debug('Clicking on login button.')
        browser.find_element_by_link_text('Login').click()
        logging.debug('Typing login.')
        browser.find_element_by_id('id_username').send_keys(login)
        logging.debug('Typing password.')
        browser.find_element_by_id('id_password').send_keys(password)
        logging.debug('Submitting login form.')
        browser.find_element_by_id('id_password').submit()

        # Profile page opens:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to products page:
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Open Standard volume:
        logging.debug('Clicking on "Print now" button for Standard.')
        browser.find_element_by_id('print_europe').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document:
        logging.debug('Uploading document ' + pdf_docs[pdf_number])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        try:
            logging.debug('Submitting document pages orientation.')
            browser.find_element_by_xpath("//button[@type='submit']").click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
        except WebDriverException:
            logging.debug('Document has no landscape pages.')

        # Set volume options:
        volume_options = browser.find_elements_by_xpath(
            "//div[@class='profil-select select-search-input div-as-input']")
        volume_options[1].click()
        browser.find_element_by_xpath("//div[@value='punched']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        volume_options[2].click()
        browser.find_element_by_xpath("//div[@value='dark_blue']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))

        # Typing Standard volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[2]/div/div/div[2]/input').send_keys(
            'Stan/dard by-b0t! vol1 dark blue cover')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-3']").click()
        logging.debug('Clicking on "Print now" button.')
        browser.find_element_by_id('paypalPayment').click()
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Wizard page rendered.')
        # Make sure URL changed to Paypal
        logging.debug('Waiting for URL to be changed to "www.sandbox.paypal.com"')
        WebDriverWait(browser, 60).until(ec.url_contains('www.sandbox.paypal.com'))

        # PayPal checkout:
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        try:
            # Open log in page
            logging.debug('Clicking on login button (Paypal).')
            browser.find_element_by_xpath("//a[@class='btn full ng-binding']").click()
        except NoSuchElementException:
            logging.debug('Login button was not located.')
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Type Paypal login
        logging.debug('Typing Paypal login.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.NAME,
                                                                           'login_email'))).send_keys(paypal_login)
        # Send Paypal login
        logging.debug('Clicking on "Next" button.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.ID, 'btnNext'))).click()
        logging.debug('Paypal page rendring.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Type Paypal password
        logging.debug('Typing Paypal password.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.ID,
                                                                           'password'))).send_keys(paypal_password)
        # Send Paypal password
        logging.debug('Clicking on Login button.')
        browser.find_element_by_id('btnLogin').click()
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Confirm Paypal payment
        logging.debug('Clicking on "Continue" button.')
        browser.find_element_by_id('confirmButtonTop').click()
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))

        # Successful upload page opens:
        logging.debug('Successful upload page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to profile:
        logging.debug('Clicking on "Close" button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH, "//a[@class='closer']"))).click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Profile page rendered.')

        # Logout and quit:
        logging.debug('Clicking on Logout button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.LINK_TEXT, "Abmelden"))).click()
        logging.debug('Landing page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        browser.quit()

    def test_4c_punched_hellblau(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_4c_punched_hellblau.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Create list of available test documents
        print('Running checkout with freemium or freemium plus product.')
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have more than 25, but less than 170 pages for this test
        pdf_number = 12
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Go to login page and sign in:
        logging.debug('Clicking on login button.')
        browser.find_element_by_link_text('Login').click()
        logging.debug('Typing login.')
        browser.find_element_by_id('id_username').send_keys(login)
        logging.debug('Typing password.')
        browser.find_element_by_id('id_password').send_keys(password)
        logging.debug('Submitting login form.')
        browser.find_element_by_id('id_password').submit()

        # Profile page opens:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to products page:
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Open Standard volume:
        logging.debug('Clicking on "Print now" button for Standard.')
        browser.find_element_by_id('print_europe').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document:
        logging.debug('Uploading document ' + pdf_docs[pdf_number])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        try:
            logging.debug('Submitting document pages orientation.')
            browser.find_element_by_xpath("//button[@type='submit']").click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
        except WebDriverException:
            logging.debug('Document has no landscape pages.')

        # Set volume options:
        volume_options = browser.find_elements_by_xpath(
            "//div[@class='profil-select select-search-input div-as-input']")
        volume_options[1].click()
        browser.find_element_by_xpath("//div[@value='punched']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        volume_options[2].click()
        browser.find_element_by_xpath("//div[@value='light_blue']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))

        # Typing Standard volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[2]/div/div/div[2]/input').send_keys(
            'Stan/dard by-b0t! vol1 bright blue')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Select Credit Card payment method:
        browser.find_element_by_id('paypal3').click()
        logging.debug('Clicked on "Credit card" radiobutton')
        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-3']").click()
        # Initiate payment
        logging.debug('Clicking on "Print now" button.')
        browser.find_element_by_id('paypalPayment').click()

        # Switch to stripe frame
        logging.debug('Switching to stripe frame.')
        WebDriverWait(browser, 60).until(ec.frame_to_be_available_and_switch_to_it('stripe_checkout_app'))
        logging.debug('Typing card number (Stripe).')
        # Type card number
        browser.find_element_by_xpath("//input[@placeholder='Card number']").send_keys(selected_card_number)
        # Type card month/year
        logging.debug('Typing month/year (Stripe).')
        browser.find_element_by_xpath("//input[@placeholder='MM / YY']").send_keys('0123')
        # Type card CVC
        logging.debug('Typing CVC (Stripe)')
        browser.find_element_by_xpath("//input[@placeholder='CVC']").send_keys('456')
        # Type card zip code
        logging.debug('Typing zip code (Stripe).')
        try:
            browser.find_element_by_xpath("//input[@placeholder='ZIP Code']").send_keys('7890')
        except NoSuchElementException:
            # Not all card types require zip code
            logging.debug('Zip code field was not located.')
        # Submit Stripe form
        logging.debug('Submitting Stripe.')
        browser.find_element_by_xpath("//button[@type='submit']").click()
        # Switch back from frame
        logging.debug('Switching to default content.')
        browser.switch_to.default_content()

        # Successful upload page opens
        logging.debug('Successful upload page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to profile page
        logging.debug('Clicking on "Close" button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH, "//a[@class='closer']"))).click()

        # Logout:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on Logout button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.LINK_TEXT, "Abmelden"))).click()
        logging.debug('Landing page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        browser.quit()

    def test_1c_wireo_blau(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_1c_wireo_blau.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Create list of available test documents
        print('Running checkout with freemium or freemium plus product.')
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have more than 25, but less than 170 pages for this test
        pdf_number = 0
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Go to login page and sign in:
        logging.debug('Clicking on login button.')
        browser.find_element_by_link_text('Login').click()
        logging.debug('Typing login.')
        browser.find_element_by_id('id_username').send_keys(login)
        logging.debug('Typing password.')
        browser.find_element_by_id('id_password').send_keys(password)
        logging.debug('Submitting login form.')
        browser.find_element_by_id('id_password').submit()

        # Profile page opens:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to products page:
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Open Standard volume:
        logging.debug('Clicking on "Print now" button for Standard.')
        browser.find_element_by_id('print_europe').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document:
        logging.debug('Uploading document ' + pdf_docs[pdf_number])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        try:
            logging.debug('Submitting document pages orientation.')
            browser.find_element_by_xpath("//button[@type='submit']").click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
        except WebDriverException:
            logging.debug('Document has no landscape pages.')

        # Set volume options:
        volume_options = browser.find_elements_by_xpath(
            "//div[@class='profil-select select-search-input div-as-input']")
        volume_options[0].click()
        browser.find_element_by_xpath("//div[@value='1c']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))

        # Typing Standard volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[2]/div/div/div[2]/input').send_keys(
            'Stan/dard by-b0t! vol1 blue cover')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Select Credit Card payment method:
        browser.find_element_by_id('paypal3').click()
        logging.debug('Clicked on "Credit card" radiobutton')
        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-3']").click()
        # Initiate payment
        logging.debug('Clicking on "Print now" button.')
        browser.find_element_by_id('paypalPayment').click()

        # Switch to stripe frame
        logging.debug('Switching to stripe frame.')
        WebDriverWait(browser, 60).until(ec.frame_to_be_available_and_switch_to_it('stripe_checkout_app'))
        logging.debug('Typing card number (Stripe).')
        # Type card number
        browser.find_element_by_xpath("//input[@placeholder='Card number']").send_keys(selected_card_number)
        # Type card month/year
        logging.debug('Typing month/year (Stripe).')
        browser.find_element_by_xpath("//input[@placeholder='MM / YY']").send_keys('0123')
        # Type card CVC
        logging.debug('Typing CVC (Stripe)')
        browser.find_element_by_xpath("//input[@placeholder='CVC']").send_keys('456')
        # Type card zip code
        logging.debug('Typing zip code (Stripe).')
        try:
            browser.find_element_by_xpath("//input[@placeholder='ZIP Code']").send_keys('7890')
        except NoSuchElementException:
            # Not all card types require zip code
            logging.debug('Zip code field was not located.')
        # Submit Stripe form
        logging.debug('Submitting Stripe.')
        browser.find_element_by_xpath("//button[@type='submit']").click()
        # Switch back from frame
        logging.debug('Switching to default content.')
        browser.switch_to.default_content()

        # Successful upload page opens
        logging.debug('Successful upload page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to profile page
        logging.debug('Clicking on "Close" button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH, "//a[@class='closer']"))).click()

        # Logout:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on Logout button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.LINK_TEXT, "Abmelden"))).click()
        logging.debug('Landing page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        browser.quit()

    def test_1c_wireo_grun(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_1c_wireo_grun.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Set Paypal credentials:
        paypal_login = 'info-buyer@printpeter.de'
        paypal_password = 'fdjkru12'

        # Create list of available test documents
        print('Running checkout with freemium or freemium plus product.')
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have more than 25, but less than 170 pages for this test
        pdf_number = 4
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Go to login page and sign in:
        logging.debug('Clicking on login button.')
        browser.find_element_by_link_text('Login').click()
        logging.debug('Typing login.')
        browser.find_element_by_id('id_username').send_keys(login)
        logging.debug('Typing password.')
        browser.find_element_by_id('id_password').send_keys(password)
        logging.debug('Submitting login form.')
        browser.find_element_by_id('id_password').submit()

        # Profile page opens:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to products page:
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Open Standard volume:
        logging.debug('Clicking on "Print now" button for Standard.')
        browser.find_element_by_id('print_europe').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document:
        logging.debug('Uploading document ' + pdf_docs[pdf_number])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        try:
            logging.debug('Submitting document pages orientation.')
            browser.find_element_by_xpath("//button[@type='submit']").click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
        except WebDriverException:
            logging.debug('Document has no landscape pages.')

        # Set volume options:
        volume_options = browser.find_elements_by_xpath(
            "//div[@class='profil-select select-search-input div-as-input']")
        volume_options[0].click()
        browser.find_element_by_xpath("//div[@value='1c']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        volume_options[2].click()
        browser.find_element_by_xpath("//div[@value='green']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))

        # Typing Standard volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[2]/div/div/div[2]/input').send_keys(
            'Stan/dard by-b0t! vol1 green cover')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-3']").click()
        logging.debug('Clicking on "Print now" button.')
        browser.find_element_by_id('paypalPayment').click()
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Wizard page rendered.')
        # Make sure URL changed to Paypal
        logging.debug('Waiting for URL to be changed to "www.sandbox.paypal.com"')
        WebDriverWait(browser, 60).until(ec.url_contains('www.sandbox.paypal.com'))

        # PayPal checkout:
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        try:
            # Open log in page
            logging.debug('Clicking on login button (Paypal).')
            browser.find_element_by_xpath("//a[@class='btn full ng-binding']").click()
        except NoSuchElementException:
            logging.debug('Login button was not located.')
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Type Paypal login
        logging.debug('Typing Paypal login.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.NAME,
                                                                           'login_email'))).send_keys(paypal_login)
        # Send Paypal login
        logging.debug('Clicking on "Next" button.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.ID, 'btnNext'))).click()
        logging.debug('Paypal page rendring.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Type Paypal password
        logging.debug('Typing Paypal password.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.ID,
                                                                           'password'))).send_keys(paypal_password)
        # Send Paypal password
        logging.debug('Clicking on Login button.')
        browser.find_element_by_id('btnLogin').click()
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Confirm Paypal payment
        logging.debug('Clicking on "Continue" button.')
        browser.find_element_by_id('confirmButtonTop').click()
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))

        # Successful upload page opens:
        logging.debug('Successful upload page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to profile:
        logging.debug('Clicking on "Close" button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH, "//a[@class='closer']"))).click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Profile page rendered.')

        # Logout and quit:
        logging.debug('Clicking on Logout button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.LINK_TEXT, "Abmelden"))).click()
        logging.debug('Landing page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        browser.quit()

    def test_1c_wireo_violett(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_1c_wireo_violett.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Create list of available test documents
        print('Running checkout with freemium or freemium plus product.')
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have more than 25, but less than 170 pages for this test
        pdf_number = 4
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Go to login page and sign in:
        logging.debug('Clicking on login button.')
        browser.find_element_by_link_text('Login').click()
        logging.debug('Typing login.')
        browser.find_element_by_id('id_username').send_keys(login)
        logging.debug('Typing password.')
        browser.find_element_by_id('id_password').send_keys(password)
        logging.debug('Submitting login form.')
        browser.find_element_by_id('id_password').submit()

        # Profile page opens:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to products page:
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Open Standard volume:
        logging.debug('Clicking on "Print now" button for Standard.')
        browser.find_element_by_id('print_europe').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document:
        logging.debug('Uploading document ' + pdf_docs[pdf_number])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        try:
            logging.debug('Submitting document pages orientation.')
            browser.find_element_by_xpath("//button[@type='submit']").click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
        except WebDriverException:
            logging.debug('Document has no landscape pages.')

        # Set volume options:
        volume_options = browser.find_elements_by_xpath(
            "//div[@class='profil-select select-search-input div-as-input']")
        volume_options[0].click()
        browser.find_element_by_xpath("//div[@value='1c']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        volume_options[2].click()
        browser.find_element_by_xpath("//div[@value='purple']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))

        # Typing Standard volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[2]/div/div/div[2]/input').send_keys(
            'Stan/dard by-b0t! vol1 purple cover')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Select Credit Card payment method:
        browser.find_element_by_id('paypal3').click()
        logging.debug('Clicked on "Credit card" radiobutton')
        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-3']").click()
        # Initiate payment
        logging.debug('Clicking on "Print now" button.')
        browser.find_element_by_id('paypalPayment').click()

        # Switch to stripe frame
        logging.debug('Switching to stripe frame.')
        WebDriverWait(browser, 60).until(ec.frame_to_be_available_and_switch_to_it('stripe_checkout_app'))
        logging.debug('Typing card number (Stripe).')
        # Type card number
        browser.find_element_by_xpath("//input[@placeholder='Card number']").send_keys(selected_card_number)
        # Type card month/year
        logging.debug('Typing month/year (Stripe).')
        browser.find_element_by_xpath("//input[@placeholder='MM / YY']").send_keys('0123')
        # Type card CVC
        logging.debug('Typing CVC (Stripe)')
        browser.find_element_by_xpath("//input[@placeholder='CVC']").send_keys('456')
        # Type card zip code
        logging.debug('Typing zip code (Stripe).')
        try:
            browser.find_element_by_xpath("//input[@placeholder='ZIP Code']").send_keys('7890')
        except NoSuchElementException:
            # Not all card types require zip code
            logging.debug('Zip code field was not located.')
        # Submit Stripe form
        logging.debug('Submitting Stripe.')
        browser.find_element_by_xpath("//button[@type='submit']").click()
        # Switch back from frame
        logging.debug('Switching to default content.')
        browser.switch_to.default_content()

        # Successful upload page opens
        logging.debug('Successful upload page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to profile page
        logging.debug('Clicking on "Close" button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH, "//a[@class='closer']"))).click()

        # Logout:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on Logout button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.LINK_TEXT, "Abmelden"))).click()
        logging.debug('Landing page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        browser.quit()

    def test_1c_wireo_rot(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_1c_wireo_rot.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Set Paypal credentials:
        paypal_login = 'info-buyer@printpeter.de'
        paypal_password = 'fdjkru12'

        # Create list of available test documents
        print('Running checkout with freemium or freemium plus product.')
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have more than 25, but less than 170 pages for this test
        pdf_number = 11
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Go to login page and sign in:
        logging.debug('Clicking on login button.')
        browser.find_element_by_link_text('Login').click()
        logging.debug('Typing login.')
        browser.find_element_by_id('id_username').send_keys(login)
        logging.debug('Typing password.')
        browser.find_element_by_id('id_password').send_keys(password)
        logging.debug('Submitting login form.')
        browser.find_element_by_id('id_password').submit()

        # Profile page opens:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to products page:
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Open Standard volume:
        logging.debug('Clicking on "Print now" button for Standard.')
        browser.find_element_by_id('print_europe').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document:
        logging.debug('Uploading document ' + pdf_docs[pdf_number])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        try:
            logging.debug('Submitting document pages orientation.')
            browser.find_element_by_xpath("//button[@type='submit']").click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
        except WebDriverException:
            logging.debug('Document has no landscape pages.')

        # Set volume options:
        volume_options = browser.find_elements_by_xpath(
            "//div[@class='profil-select select-search-input div-as-input']")
        volume_options[0].click()
        browser.find_element_by_xpath("//div[@value='1c']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        volume_options[2].click()
        browser.find_element_by_xpath("//div[@value='red']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))

        # Typing Standard volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[2]/div/div/div[2]/input').send_keys(
            'Stan/dard by-b0t! vol1 red cover')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-3']").click()
        logging.debug('Clicking on "Print now" button.')
        browser.find_element_by_id('paypalPayment').click()
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Wizard page rendered.')
        # Make sure URL changed to Paypal
        logging.debug('Waiting for URL to be changed to "www.sandbox.paypal.com"')
        WebDriverWait(browser, 60).until(ec.url_contains('www.sandbox.paypal.com'))

        # PayPal checkout:
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        try:
            # Open log in page
            logging.debug('Clicking on login button (Paypal).')
            browser.find_element_by_xpath("//a[@class='btn full ng-binding']").click()
        except NoSuchElementException:
            logging.debug('Login button was not located.')
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Type Paypal login
        logging.debug('Typing Paypal login.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.NAME,
                                                                           'login_email'))).send_keys(paypal_login)
        # Send Paypal login
        logging.debug('Clicking on "Next" button.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.ID, 'btnNext'))).click()
        logging.debug('Paypal page rendring.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Type Paypal password
        logging.debug('Typing Paypal password.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.ID,
                                                                           'password'))).send_keys(paypal_password)
        # Send Paypal password
        logging.debug('Clicking on Login button.')
        browser.find_element_by_id('btnLogin').click()
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Confirm Paypal payment
        logging.debug('Clicking on "Continue" button.')
        browser.find_element_by_id('confirmButtonTop').click()
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))

        # Successful upload page opens:
        logging.debug('Successful upload page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to profile:
        logging.debug('Clicking on "Close" button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH, "//a[@class='closer']"))).click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Profile page rendered.')

        # Logout and quit:
        logging.debug('Clicking on Logout button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.LINK_TEXT, "Abmelden"))).click()
        logging.debug('Landing page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        browser.quit()

    def test_1c_wireo_gelb(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_1c_wireo_gelb.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Create list of available test documents
        print('Running checkout with freemium or freemium plus product.')
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have more than 25, but less than 170 pages for this test
        pdf_number = 11
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Go to login page and sign in:
        logging.debug('Clicking on login button.')
        browser.find_element_by_link_text('Login').click()
        logging.debug('Typing login.')
        browser.find_element_by_id('id_username').send_keys(login)
        logging.debug('Typing password.')
        browser.find_element_by_id('id_password').send_keys(password)
        logging.debug('Submitting login form.')
        browser.find_element_by_id('id_password').submit()

        # Profile page opens:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to products page:
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Open Standard volume:
        logging.debug('Clicking on "Print now" button for Standard.')
        browser.find_element_by_id('print_europe').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document:
        logging.debug('Uploading document ' + pdf_docs[pdf_number])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        try:
            logging.debug('Submitting document pages orientation.')
            browser.find_element_by_xpath("//button[@type='submit']").click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
        except WebDriverException:
            logging.debug('Document has no landscape pages.')

        # Set volume options:
        volume_options = browser.find_elements_by_xpath(
            "//div[@class='profil-select select-search-input div-as-input']")
        volume_options[0].click()
        browser.find_element_by_xpath("//div[@value='1c']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        volume_options[2].click()
        browser.find_element_by_xpath("//div[@value='yellow']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))

        # Typing Standard volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[2]/div/div/div[2]/input').send_keys(
            'Stan/dard by-b0t! vol1 yellow cover')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Select Credit Card payment method:
        browser.find_element_by_id('paypal3').click()
        logging.debug('Clicked on "Credit card" radiobutton')
        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-3']").click()
        # Initiate payment
        logging.debug('Clicking on "Print now" button.')
        browser.find_element_by_id('paypalPayment').click()

        # Switch to stripe frame
        logging.debug('Switching to stripe frame.')
        WebDriverWait(browser, 60).until(ec.frame_to_be_available_and_switch_to_it('stripe_checkout_app'))
        logging.debug('Typing card number (Stripe).')
        # Type card number
        browser.find_element_by_xpath("//input[@placeholder='Card number']").send_keys(selected_card_number)
        # Type card month/year
        logging.debug('Typing month/year (Stripe).')
        browser.find_element_by_xpath("//input[@placeholder='MM / YY']").send_keys('0123')
        # Type card CVC
        logging.debug('Typing CVC (Stripe)')
        browser.find_element_by_xpath("//input[@placeholder='CVC']").send_keys('456')
        # Type card zip code
        logging.debug('Typing zip code (Stripe).')
        try:
            browser.find_element_by_xpath("//input[@placeholder='ZIP Code']").send_keys('7890')
        except NoSuchElementException:
            # Not all card types require zip code
            logging.debug('Zip code field was not located.')
        # Submit Stripe form
        logging.debug('Submitting Stripe.')
        browser.find_element_by_xpath("//button[@type='submit']").click()
        # Switch back from frame
        logging.debug('Switching to default content.')
        browser.switch_to.default_content()

        # Successful upload page opens
        logging.debug('Successful upload page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to profile page
        logging.debug('Clicking on "Close" button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH, "//a[@class='closer']"))).click()

        # Logout:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on Logout button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.LINK_TEXT, "Abmelden"))).click()
        logging.debug('Landing page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        browser.quit()

    def test_1c_wireo_dunkelblau(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_1c_wireo_dunkelblau.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Set Paypal credentials:
        paypal_login = 'info-buyer@printpeter.de'
        paypal_password = 'fdjkru12'

        # Create list of available test documents
        print('Running checkout with freemium or freemium plus product.')
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have more than 25, but less than 170 pages for this test
        pdf_number = 11
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Go to login page and sign in:
        logging.debug('Clicking on login button.')
        browser.find_element_by_link_text('Login').click()
        logging.debug('Typing login.')
        browser.find_element_by_id('id_username').send_keys(login)
        logging.debug('Typing password.')
        browser.find_element_by_id('id_password').send_keys(password)
        logging.debug('Submitting login form.')
        browser.find_element_by_id('id_password').submit()

        # Profile page opens:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to products page:
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Open Standard volume:
        logging.debug('Clicking on "Print now" button for Standard.')
        browser.find_element_by_id('print_europe').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document:
        logging.debug('Uploading document ' + pdf_docs[pdf_number])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        try:
            logging.debug('Submitting document pages orientation.')
            browser.find_element_by_xpath("//button[@type='submit']").click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
        except WebDriverException:
            logging.debug('Document has no landscape pages.')

        # Set volume options:
        volume_options = browser.find_elements_by_xpath(
            "//div[@class='profil-select select-search-input div-as-input']")
        volume_options[0].click()
        browser.find_element_by_xpath("//div[@value='1c']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        volume_options[2].click()
        browser.find_element_by_xpath("//div[@value='dark_blue']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))

        # Typing Standard volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[2]/div/div/div[2]/input').send_keys(
            'Stan/dard by-b0t! vol1 dark blue cover')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-3']").click()
        logging.debug('Clicking on "Print now" button.')
        browser.find_element_by_id('paypalPayment').click()
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Wizard page rendered.')
        # Make sure URL changed to Paypal
        logging.debug('Waiting for URL to be changed to "www.sandbox.paypal.com"')
        WebDriverWait(browser, 60).until(ec.url_contains('www.sandbox.paypal.com'))

        # PayPal checkout:
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        try:
            # Open log in page
            logging.debug('Clicking on login button (Paypal).')
            browser.find_element_by_xpath("//a[@class='btn full ng-binding']").click()
        except NoSuchElementException:
            logging.debug('Login button was not located.')
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Type Paypal login
        logging.debug('Typing Paypal login.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.NAME,
                                                                           'login_email'))).send_keys(paypal_login)
        # Send Paypal login
        logging.debug('Clicking on "Next" button.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.ID, 'btnNext'))).click()
        logging.debug('Paypal page rendring.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Type Paypal password
        logging.debug('Typing Paypal password.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.ID,
                                                                           'password'))).send_keys(paypal_password)
        # Send Paypal password
        logging.debug('Clicking on Login button.')
        browser.find_element_by_id('btnLogin').click()
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Confirm Paypal payment
        logging.debug('Clicking on "Continue" button.')
        browser.find_element_by_id('confirmButtonTop').click()
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))

        # Successful upload page opens:
        logging.debug('Successful upload page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to profile:
        logging.debug('Clicking on "Close" button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH, "//a[@class='closer']"))).click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Profile page rendered.')

        # Logout and quit:
        logging.debug('Clicking on Logout button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.LINK_TEXT, "Abmelden"))).click()
        logging.debug('Landing page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        browser.quit()

    def test_1c_wireo_hellblau(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_4c_punched_hellblau.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Create list of available test documents
        print('Running checkout with freemium or freemium plus product.')
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have more than 25, but less than 170 pages for this test
        pdf_number = 12
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Go to login page and sign in:
        logging.debug('Clicking on login button.')
        browser.find_element_by_link_text('Login').click()
        logging.debug('Typing login.')
        browser.find_element_by_id('id_username').send_keys(login)
        logging.debug('Typing password.')
        browser.find_element_by_id('id_password').send_keys(password)
        logging.debug('Submitting login form.')
        browser.find_element_by_id('id_password').submit()

        # Profile page opens:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to products page:
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Open Standard volume:
        logging.debug('Clicking on "Print now" button for Standard.')
        browser.find_element_by_id('print_europe').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document:
        logging.debug('Uploading document ' + pdf_docs[pdf_number])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        try:
            logging.debug('Submitting document pages orientation.')
            browser.find_element_by_xpath("//button[@type='submit']").click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
        except WebDriverException:
            logging.debug('Document has no landscape pages.')

        # Set volume options:
        volume_options = browser.find_elements_by_xpath(
            "//div[@class='profil-select select-search-input div-as-input']")
        volume_options[0].click()
        browser.find_element_by_xpath("//div[@value='1c']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        volume_options[2].click()
        browser.find_element_by_xpath("//div[@value='light_blue']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))

        # Typing Standard volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[2]/div/div/div[2]/input').send_keys(
            'Stan/dard by-b0t! vol1 bright blue')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Select Credit Card payment method:
        browser.find_element_by_id('paypal3').click()
        logging.debug('Clicked on "Credit card" radiobutton')
        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-3']").click()
        # Initiate payment
        logging.debug('Clicking on "Print now" button.')
        browser.find_element_by_id('paypalPayment').click()

        # Switch to stripe frame
        logging.debug('Switching to stripe frame.')
        WebDriverWait(browser, 60).until(ec.frame_to_be_available_and_switch_to_it('stripe_checkout_app'))
        logging.debug('Typing card number (Stripe).')
        # Type card number
        browser.find_element_by_xpath("//input[@placeholder='Card number']").send_keys(selected_card_number)
        # Type card month/year
        logging.debug('Typing month/year (Stripe).')
        browser.find_element_by_xpath("//input[@placeholder='MM / YY']").send_keys('0123')
        # Type card CVC
        logging.debug('Typing CVC (Stripe)')
        browser.find_element_by_xpath("//input[@placeholder='CVC']").send_keys('456')
        # Type card zip code
        logging.debug('Typing zip code (Stripe).')
        try:
            browser.find_element_by_xpath("//input[@placeholder='ZIP Code']").send_keys('7890')
        except NoSuchElementException:
            # Not all card types require zip code
            logging.debug('Zip code field was not located.')
        # Submit Stripe form
        logging.debug('Submitting Stripe.')
        browser.find_element_by_xpath("//button[@type='submit']").click()
        # Switch back from frame
        logging.debug('Switching to default content.')
        browser.switch_to.default_content()

        # Successful upload page opens
        logging.debug('Successful upload page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to profile page
        logging.debug('Clicking on "Close" button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH, "//a[@class='closer']"))).click()

        # Logout:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on Logout button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.LINK_TEXT, "Abmelden"))).click()
        logging.debug('Landing page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        browser.quit()

    def test_1c_punched_blau(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_1c_punched_blau.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Create list of available test documents
        print('Running checkout with freemium or freemium plus product.')
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have more than 25, but less than 170 pages for this test
        pdf_number = 0
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Go to login page and sign in:
        logging.debug('Clicking on login button.')
        browser.find_element_by_link_text('Login').click()
        logging.debug('Typing login.')
        browser.find_element_by_id('id_username').send_keys(login)
        logging.debug('Typing password.')
        browser.find_element_by_id('id_password').send_keys(password)
        logging.debug('Submitting login form.')
        browser.find_element_by_id('id_password').submit()

        # Profile page opens:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to products page:
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Open Standard volume:
        logging.debug('Clicking on "Print now" button for Standard.')
        browser.find_element_by_id('print_europe').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document:
        logging.debug('Uploading document ' + pdf_docs[pdf_number])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        try:
            logging.debug('Submitting document pages orientation.')
            browser.find_element_by_xpath("//button[@type='submit']").click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
        except WebDriverException:
            logging.debug('Document has no landscape pages.')

        # Set volume options:
        volume_options = browser.find_elements_by_xpath(
            "//div[@class='profil-select select-search-input div-as-input']")
        volume_options[1].click()
        browser.find_element_by_xpath("//div[@value='punched']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))

        # Typing Standard volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[2]/div/div/div[2]/input').send_keys(
            'Stan/dard by-b0t! vol1 blue cover')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Select Credit Card payment method:
        browser.find_element_by_id('paypal3').click()
        logging.debug('Clicked on "Credit card" radiobutton')
        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-3']").click()
        # Initiate payment
        logging.debug('Clicking on "Print now" button.')
        browser.find_element_by_id('paypalPayment').click()

        # Switch to stripe frame
        logging.debug('Switching to stripe frame.')
        WebDriverWait(browser, 60).until(ec.frame_to_be_available_and_switch_to_it('stripe_checkout_app'))
        logging.debug('Typing card number (Stripe).')
        # Type card number
        browser.find_element_by_xpath("//input[@placeholder='Card number']").send_keys(selected_card_number)
        # Type card month/year
        logging.debug('Typing month/year (Stripe).')
        browser.find_element_by_xpath("//input[@placeholder='MM / YY']").send_keys('0123')
        # Type card CVC
        logging.debug('Typing CVC (Stripe)')
        browser.find_element_by_xpath("//input[@placeholder='CVC']").send_keys('456')
        # Type card zip code
        logging.debug('Typing zip code (Stripe).')
        try:
            browser.find_element_by_xpath("//input[@placeholder='ZIP Code']").send_keys('7890')
        except NoSuchElementException:
            # Not all card types require zip code
            logging.debug('Zip code field was not located.')
        # Submit Stripe form
        logging.debug('Submitting Stripe.')
        browser.find_element_by_xpath("//button[@type='submit']").click()
        # Switch back from frame
        logging.debug('Switching to default content.')
        browser.switch_to.default_content()

        # Successful upload page opens
        logging.debug('Successful upload page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to profile page
        logging.debug('Clicking on "Close" button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH, "//a[@class='closer']"))).click()

        # Logout:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on Logout button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.LINK_TEXT, "Abmelden"))).click()
        logging.debug('Landing page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        browser.quit()

    def test_1c_punched_grun(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_1c_punched_grun.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Set Paypal credentials:
        paypal_login = 'info-buyer@printpeter.de'
        paypal_password = 'fdjkru12'

        # Create list of available test documents
        print('Running checkout with freemium or freemium plus product.')
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have more than 25, but less than 170 pages for this test
        pdf_number = 4
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Go to login page and sign in:
        logging.debug('Clicking on login button.')
        browser.find_element_by_link_text('Login').click()
        logging.debug('Typing login.')
        browser.find_element_by_id('id_username').send_keys(login)
        logging.debug('Typing password.')
        browser.find_element_by_id('id_password').send_keys(password)
        logging.debug('Submitting login form.')
        browser.find_element_by_id('id_password').submit()

        # Profile page opens:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to products page:
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Open Standard volume:
        logging.debug('Clicking on "Print now" button for Standard.')
        browser.find_element_by_id('print_europe').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document:
        logging.debug('Uploading document ' + pdf_docs[pdf_number])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        try:
            logging.debug('Submitting document pages orientation.')
            browser.find_element_by_xpath("//button[@type='submit']").click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
        except WebDriverException:
            logging.debug('Document has no landscape pages.')

        # Set volume options:
        volume_options = browser.find_elements_by_xpath(
            "//div[@class='profil-select select-search-input div-as-input']")
        volume_options[1].click()
        browser.find_element_by_xpath("//div[@value='punched']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        volume_options[2].click()
        browser.find_element_by_xpath("//div[@value='green']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))

        # Typing Standard volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[2]/div/div/div[2]/input').send_keys(
            'Stan/dard by-b0t! vol1 green cover')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-3']").click()
        logging.debug('Clicking on "Print now" button.')
        browser.find_element_by_id('paypalPayment').click()
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Wizard page rendered.')
        # Make sure URL changed to Paypal
        logging.debug('Waiting for URL to be changed to "www.sandbox.paypal.com"')
        WebDriverWait(browser, 60).until(ec.url_contains('www.sandbox.paypal.com'))

        # PayPal checkout:
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        try:
            # Open log in page
            logging.debug('Clicking on login button (Paypal).')
            browser.find_element_by_xpath("//a[@class='btn full ng-binding']").click()
        except NoSuchElementException:
            logging.debug('Login button was not located.')
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Type Paypal login
        logging.debug('Typing Paypal login.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.NAME,
                                                                           'login_email'))).send_keys(paypal_login)
        # Send Paypal login
        logging.debug('Clicking on "Next" button.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.ID, 'btnNext'))).click()
        logging.debug('Paypal page rendring.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Type Paypal password
        logging.debug('Typing Paypal password.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.ID,
                                                                           'password'))).send_keys(paypal_password)
        # Send Paypal password
        logging.debug('Clicking on Login button.')
        browser.find_element_by_id('btnLogin').click()
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Confirm Paypal payment
        logging.debug('Clicking on "Continue" button.')
        browser.find_element_by_id('confirmButtonTop').click()
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))

        # Successful upload page opens:
        logging.debug('Successful upload page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to profile:
        logging.debug('Clicking on "Close" button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH, "//a[@class='closer']"))).click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Profile page rendered.')

        # Logout and quit:
        logging.debug('Clicking on Logout button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.LINK_TEXT, "Abmelden"))).click()
        logging.debug('Landing page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        browser.quit()

    def test_1c_punched_violett(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_1c_punched_violett.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Create list of available test documents
        print('Running checkout with freemium or freemium plus product.')
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have more than 25, but less than 170 pages for this test
        pdf_number = 4
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Go to login page and sign in:
        logging.debug('Clicking on login button.')
        browser.find_element_by_link_text('Login').click()
        logging.debug('Typing login.')
        browser.find_element_by_id('id_username').send_keys(login)
        logging.debug('Typing password.')
        browser.find_element_by_id('id_password').send_keys(password)
        logging.debug('Submitting login form.')
        browser.find_element_by_id('id_password').submit()

        # Profile page opens:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to products page:
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Open Standard volume:
        logging.debug('Clicking on "Print now" button for Standard.')
        browser.find_element_by_id('print_europe').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document:
        logging.debug('Uploading document ' + pdf_docs[pdf_number])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        try:
            logging.debug('Submitting document pages orientation.')
            browser.find_element_by_xpath("//button[@type='submit']").click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
        except WebDriverException:
            logging.debug('Document has no landscape pages.')

        # Set volume options:
        volume_options = browser.find_elements_by_xpath(
            "//div[@class='profil-select select-search-input div-as-input']")
        volume_options[1].click()
        browser.find_element_by_xpath("//div[@value='punched']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        volume_options[2].click()
        browser.find_element_by_xpath("//div[@value='purple']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))

        # Typing Standard volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[2]/div/div/div[2]/input').send_keys(
            'Stan/dard by-b0t! vol1 purple cover')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Select Credit Card payment method:
        browser.find_element_by_id('paypal3').click()
        logging.debug('Clicked on "Credit card" radiobutton')
        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-3']").click()
        # Initiate payment
        logging.debug('Clicking on "Print now" button.')
        browser.find_element_by_id('paypalPayment').click()

        # Switch to stripe frame
        logging.debug('Switching to stripe frame.')
        WebDriverWait(browser, 60).until(ec.frame_to_be_available_and_switch_to_it('stripe_checkout_app'))
        logging.debug('Typing card number (Stripe).')
        # Type card number
        browser.find_element_by_xpath("//input[@placeholder='Card number']").send_keys(selected_card_number)
        # Type card month/year
        logging.debug('Typing month/year (Stripe).')
        browser.find_element_by_xpath("//input[@placeholder='MM / YY']").send_keys('0123')
        # Type card CVC
        logging.debug('Typing CVC (Stripe)')
        browser.find_element_by_xpath("//input[@placeholder='CVC']").send_keys('456')
        # Type card zip code
        logging.debug('Typing zip code (Stripe).')
        try:
            browser.find_element_by_xpath("//input[@placeholder='ZIP Code']").send_keys('7890')
        except NoSuchElementException:
            # Not all card types require zip code
            logging.debug('Zip code field was not located.')
        # Submit Stripe form
        logging.debug('Submitting Stripe.')
        browser.find_element_by_xpath("//button[@type='submit']").click()
        # Switch back from frame
        logging.debug('Switching to default content.')
        browser.switch_to.default_content()

        # Successful upload page opens
        logging.debug('Successful upload page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to profile page
        logging.debug('Clicking on "Close" button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH, "//a[@class='closer']"))).click()

        # Logout:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on Logout button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.LINK_TEXT, "Abmelden"))).click()
        logging.debug('Landing page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        browser.quit()

    def test_1c_punched_rot(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_1c_punched_rot.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Set Paypal credentials:
        paypal_login = 'info-buyer@printpeter.de'
        paypal_password = 'fdjkru12'

        # Create list of available test documents
        print('Running checkout with freemium or freemium plus product.')
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have more than 25, but less than 170 pages for this test
        pdf_number = 11
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Go to login page and sign in:
        logging.debug('Clicking on login button.')
        browser.find_element_by_link_text('Login').click()
        logging.debug('Typing login.')
        browser.find_element_by_id('id_username').send_keys(login)
        logging.debug('Typing password.')
        browser.find_element_by_id('id_password').send_keys(password)
        logging.debug('Submitting login form.')
        browser.find_element_by_id('id_password').submit()

        # Profile page opens:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to products page:
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Open Standard volume:
        logging.debug('Clicking on "Print now" button for Standard.')
        browser.find_element_by_id('print_europe').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document:
        logging.debug('Uploading document ' + pdf_docs[pdf_number])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        try:
            logging.debug('Submitting document pages orientation.')
            browser.find_element_by_xpath("//button[@type='submit']").click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
        except WebDriverException:
            logging.debug('Document has no landscape pages.')

        # Set volume options:
        volume_options = browser.find_elements_by_xpath(
            "//div[@class='profil-select select-search-input div-as-input']")
        volume_options[1].click()
        browser.find_element_by_xpath("//div[@value='punched']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        volume_options[2].click()
        browser.find_element_by_xpath("//div[@value='red']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))

        # Typing Standard volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[2]/div/div/div[2]/input').send_keys(
            'Stan/dard by-b0t! vol1 red cover')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-3']").click()
        logging.debug('Clicking on "Print now" button.')
        browser.find_element_by_id('paypalPayment').click()
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Wizard page rendered.')
        # Make sure URL changed to Paypal
        logging.debug('Waiting for URL to be changed to "www.sandbox.paypal.com"')
        WebDriverWait(browser, 60).until(ec.url_contains('www.sandbox.paypal.com'))

        # PayPal checkout:
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        try:
            # Open log in page
            logging.debug('Clicking on login button (Paypal).')
            browser.find_element_by_xpath("//a[@class='btn full ng-binding']").click()
        except NoSuchElementException:
            logging.debug('Login button was not located.')
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Type Paypal login
        logging.debug('Typing Paypal login.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.NAME,
                                                                           'login_email'))).send_keys(paypal_login)
        # Send Paypal login
        logging.debug('Clicking on "Next" button.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.ID, 'btnNext'))).click()
        logging.debug('Paypal page rendring.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Type Paypal password
        logging.debug('Typing Paypal password.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.ID,
                                                                           'password'))).send_keys(paypal_password)
        # Send Paypal password
        logging.debug('Clicking on Login button.')
        browser.find_element_by_id('btnLogin').click()
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Confirm Paypal payment
        logging.debug('Clicking on "Continue" button.')
        browser.find_element_by_id('confirmButtonTop').click()
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))

        # Successful upload page opens:
        logging.debug('Successful upload page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to profile:
        logging.debug('Clicking on "Close" button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH, "//a[@class='closer']"))).click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Profile page rendered.')

        # Logout and quit:
        logging.debug('Clicking on Logout button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.LINK_TEXT, "Abmelden"))).click()
        logging.debug('Landing page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        browser.quit()

    def test_1c_punched_gelb(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_1c_punched_gelb.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Create list of available test documents
        print('Running checkout with freemium or freemium plus product.')
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have more than 25, but less than 170 pages for this test
        pdf_number = 11
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Go to login page and sign in:
        logging.debug('Clicking on login button.')
        browser.find_element_by_link_text('Login').click()
        logging.debug('Typing login.')
        browser.find_element_by_id('id_username').send_keys(login)
        logging.debug('Typing password.')
        browser.find_element_by_id('id_password').send_keys(password)
        logging.debug('Submitting login form.')
        browser.find_element_by_id('id_password').submit()

        # Profile page opens:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to products page:
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Open Standard volume:
        logging.debug('Clicking on "Print now" button for Standard.')
        browser.find_element_by_id('print_europe').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document:
        logging.debug('Uploading document ' + pdf_docs[pdf_number])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        try:
            logging.debug('Submitting document pages orientation.')
            browser.find_element_by_xpath("//button[@type='submit']").click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
        except WebDriverException:
            logging.debug('Document has no landscape pages.')

        # Set volume options:
        volume_options = browser.find_elements_by_xpath(
            "//div[@class='profil-select select-search-input div-as-input']")
        volume_options[1].click()
        browser.find_element_by_xpath("//div[@value='punched']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        volume_options[2].click()
        browser.find_element_by_xpath("//div[@value='yellow']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))

        # Typing Standard volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[2]/div/div/div[2]/input').send_keys(
            'Stan/dard by-b0t! vol1 yellow cover')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Select Credit Card payment method:
        browser.find_element_by_id('paypal3').click()
        logging.debug('Clicked on "Credit card" radiobutton')
        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-3']").click()
        # Initiate payment
        logging.debug('Clicking on "Print now" button.')
        browser.find_element_by_id('paypalPayment').click()

        # Switch to stripe frame
        logging.debug('Switching to stripe frame.')
        WebDriverWait(browser, 60).until(ec.frame_to_be_available_and_switch_to_it('stripe_checkout_app'))
        logging.debug('Typing card number (Stripe).')
        # Type card number
        browser.find_element_by_xpath("//input[@placeholder='Card number']").send_keys(selected_card_number)
        # Type card month/year
        logging.debug('Typing month/year (Stripe).')
        browser.find_element_by_xpath("//input[@placeholder='MM / YY']").send_keys('0123')
        # Type card CVC
        logging.debug('Typing CVC (Stripe)')
        browser.find_element_by_xpath("//input[@placeholder='CVC']").send_keys('456')
        # Type card zip code
        logging.debug('Typing zip code (Stripe).')
        try:
            browser.find_element_by_xpath("//input[@placeholder='ZIP Code']").send_keys('7890')
        except NoSuchElementException:
            # Not all card types require zip code
            logging.debug('Zip code field was not located.')
        # Submit Stripe form
        logging.debug('Submitting Stripe.')
        browser.find_element_by_xpath("//button[@type='submit']").click()
        # Switch back from frame
        logging.debug('Switching to default content.')
        browser.switch_to.default_content()

        # Successful upload page opens
        logging.debug('Successful upload page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to profile page
        logging.debug('Clicking on "Close" button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH, "//a[@class='closer']"))).click()

        # Logout:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on Logout button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.LINK_TEXT, "Abmelden"))).click()
        logging.debug('Landing page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        browser.quit()

    def test_1c_punched_dunkelblau(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_1c_punched_dunkelblau.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Set Paypal credentials:
        paypal_login = 'info-buyer@printpeter.de'
        paypal_password = 'fdjkru12'

        # Create list of available test documents
        print('Running checkout with freemium or freemium plus product.')
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have more than 25, but less than 170 pages for this test
        pdf_number = 11
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Go to login page and sign in:
        logging.debug('Clicking on login button.')
        browser.find_element_by_link_text('Login').click()
        logging.debug('Typing login.')
        browser.find_element_by_id('id_username').send_keys(login)
        logging.debug('Typing password.')
        browser.find_element_by_id('id_password').send_keys(password)
        logging.debug('Submitting login form.')
        browser.find_element_by_id('id_password').submit()

        # Profile page opens:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to products page:
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Open Standard volume:
        logging.debug('Clicking on "Print now" button for Standard.')
        browser.find_element_by_id('print_europe').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document:
        logging.debug('Uploading document ' + pdf_docs[pdf_number])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        try:
            logging.debug('Submitting document pages orientation.')
            browser.find_element_by_xpath("//button[@type='submit']").click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
        except WebDriverException:
            logging.debug('Document has no landscape pages.')

        # Set volume options:
        volume_options = browser.find_elements_by_xpath(
            "//div[@class='profil-select select-search-input div-as-input']")
        volume_options[1].click()
        browser.find_element_by_xpath("//div[@value='punched']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        volume_options[2].click()
        browser.find_element_by_xpath("//div[@value='dark_blue']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))

        # Typing Standard volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[2]/div/div/div[2]/input').send_keys(
            'Stan/dard by-b0t! vol1 dark blue cover')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-3']").click()
        logging.debug('Clicking on "Print now" button.')
        browser.find_element_by_id('paypalPayment').click()
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Wizard page rendered.')
        # Make sure URL changed to Paypal
        logging.debug('Waiting for URL to be changed to "www.sandbox.paypal.com"')
        WebDriverWait(browser, 60).until(ec.url_contains('www.sandbox.paypal.com'))

        # PayPal checkout:
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        try:
            # Open log in page
            logging.debug('Clicking on login button (Paypal).')
            browser.find_element_by_xpath("//a[@class='btn full ng-binding']").click()
        except NoSuchElementException:
            logging.debug('Login button was not located.')
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Type Paypal login
        logging.debug('Typing Paypal login.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.NAME,
                                                                           'login_email'))).send_keys(paypal_login)
        # Send Paypal login
        logging.debug('Clicking on "Next" button.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.ID, 'btnNext'))).click()
        logging.debug('Paypal page rendring.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Type Paypal password
        logging.debug('Typing Paypal password.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.ID,
                                                                           'password'))).send_keys(paypal_password)
        # Send Paypal password
        logging.debug('Clicking on Login button.')
        browser.find_element_by_id('btnLogin').click()
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))
        # Confirm Paypal payment
        logging.debug('Clicking on "Continue" button.')
        browser.find_element_by_id('confirmButtonTop').click()
        logging.debug('Paypal page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.ID, 'preloaderSpinner')))

        # Successful upload page opens:
        logging.debug('Successful upload page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to profile:
        logging.debug('Clicking on "Close" button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH, "//a[@class='closer']"))).click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Profile page rendered.')

        # Logout and quit:
        logging.debug('Clicking on Logout button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.LINK_TEXT, "Abmelden"))).click()
        logging.debug('Landing page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        browser.quit()

    def test_1c_punched_hellblau(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_1c_punched_hellblau.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Create list of available test documents
        print('Running checkout with freemium or freemium plus product.')
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have more than 25, but less than 170 pages for this test
        pdf_number = 12
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Go to login page and sign in:
        logging.debug('Clicking on login button.')
        browser.find_element_by_link_text('Login').click()
        logging.debug('Typing login.')
        browser.find_element_by_id('id_username').send_keys(login)
        logging.debug('Typing password.')
        browser.find_element_by_id('id_password').send_keys(password)
        logging.debug('Submitting login form.')
        browser.find_element_by_id('id_password').submit()

        # Profile page opens:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to products page:
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Open Standard volume:
        logging.debug('Clicking on "Print now" button for Standard.')
        browser.find_element_by_id('print_europe').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document:
        logging.debug('Uploading document ' + pdf_docs[pdf_number])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        try:
            logging.debug('Submitting document pages orientation.')
            browser.find_element_by_xpath("//button[@type='submit']").click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
        except WebDriverException:
            logging.debug('Document has no landscape pages.')

        # Set volume options:
        volume_options = browser.find_elements_by_xpath(
            "//div[@class='profil-select select-search-input div-as-input']")
        volume_options[1].click()
        browser.find_element_by_xpath("//div[@value='punched']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        volume_options[2].click()
        browser.find_element_by_xpath("//div[@value='light_blue']").click()
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))

        # Typing Standard volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[2]/div/div/div[2]/input').send_keys(
            'Stan/dard by-b0t! vol1 bright blue')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Select Credit Card payment method:
        browser.find_element_by_id('paypal3').click()
        logging.debug('Clicked on "Credit card" radiobutton')
        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-3']").click()
        # Initiate payment
        logging.debug('Clicking on "Print now" button.')
        browser.find_element_by_id('paypalPayment').click()

        # Switch to stripe frame
        logging.debug('Switching to stripe frame.')
        WebDriverWait(browser, 60).until(ec.frame_to_be_available_and_switch_to_it('stripe_checkout_app'))
        logging.debug('Typing card number (Stripe).')
        # Type card number
        browser.find_element_by_xpath("//input[@placeholder='Card number']").send_keys(selected_card_number)
        # Type card month/year
        logging.debug('Typing month/year (Stripe).')
        browser.find_element_by_xpath("//input[@placeholder='MM / YY']").send_keys('0123')
        # Type card CVC
        logging.debug('Typing CVC (Stripe)')
        browser.find_element_by_xpath("//input[@placeholder='CVC']").send_keys('456')
        # Type card zip code
        logging.debug('Typing zip code (Stripe).')
        try:
            browser.find_element_by_xpath("//input[@placeholder='ZIP Code']").send_keys('7890')
        except NoSuchElementException:
            # Not all card types require zip code
            logging.debug('Zip code field was not located.')
        # Submit Stripe form
        logging.debug('Submitting Stripe.')
        browser.find_element_by_xpath("//button[@type='submit']").click()
        # Switch back from frame
        logging.debug('Switching to default content.')
        browser.switch_to.default_content()

        # Successful upload page opens
        logging.debug('Successful upload page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Go to profile page
        logging.debug('Clicking on "Close" button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH, "//a[@class='closer']"))).click()

        # Logout:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on Logout button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.LINK_TEXT, "Abmelden"))).click()
        logging.debug('Landing page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        browser.quit()


if __name__ == '__main__':
    unittest.main()
