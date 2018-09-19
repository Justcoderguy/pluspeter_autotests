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


class FreemiumFlow(unittest.TestCase):

    def setUp(self):

        self.browser = webdriver.Chrome('C:\ChromeDriver\chromedriver.exe')

    def test_freemium_flow(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_freemium_flow.log', filemode='w',
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
        # Document should have more than 25, but less than 160 pages for this test
        pdf_number = 3
        print('Selected document: ' + pdf_docs[pdf_number])

        # Reset Freemium print to make sure user can print:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com/admin/students/student/?q=karl%40printpeter')
        browser.find_element_by_id('id_username').send_keys(login)
        browser.find_element_by_id('id_password').send_keys(password)
        browser.find_element_by_xpath('//input[@type="submit"]').click()
        browser.get('https://staging.pluspeter.com/admin/students/11/reset-limit/?q=karl%40print')
        browser.find_element_by_xpath('//a[@class="user-options-handler grp-collapse-handler '
                                      'grp-switch-user-is-original"]').click()
        browser.find_element_by_xpath('//a[@class="grp-logout"]').click()

        # Open landing page:
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

        # Go to products page and open freemium volume:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on "Print now" button for Freemium.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.XPATH,
                                                                           "//div[@class='package freemium']")))
        browser.find_element_by_id('print_freemium').click()
        logging.debug('Wizard rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        try:
            # Check if Freemium volume opened
            browser.find_element_by_id('omnibox-file-input')
            freemium_available = True
        except NoSuchElementException:
            freemium_available = False
        assert freemium_available is True, 'Freemium print is not available.'

        # Adding a document
        logging.debug('Adding document ' + pdf_docs[pdf_number])
        browser.find_element_by_id('omnibox-file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Entering a volume title
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[1]/div/div[4]/input').send_keys(
            'Free/mium by-b0t!')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Mark checkbox-1
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-1']").click()
        # Mark checkbox-2
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
        # Initiate payment
        logging.debug('initiating payment.')
        browser.find_element_by_id('paypalPayment').click()

        # Successful upload page opens
        logging.debug('Successful upload page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        # Go to profile page
        logging.debug('Clicking on "Close" button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH,
                                                                         "//a[@class='closer']"))).click()

        # Logout:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        logging.debug('Clicking on Logout button.')
        WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.LINK_TEXT, "Abmelden"))).click()
        logging.debug('Landing page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))
        browser.quit()

    def test_freemium_freemium_plus_flow(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_freemium_freemium_plus_flow.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Create list of available test documents
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the numbers of the documents to be selected from list
        # Documents should have more than 25, but less than 160 pages for this test
        pdf_number_1 = 3
        pdf_number_2 = 3
        print('Selected document: ' + pdf_docs[pdf_number_1])
        print('Selected document: ' + pdf_docs[pdf_number_2])

        # Reset Freemium print to make sure user can print:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com/admin/students/student/?q=karl%40printpeter')
        browser.find_element_by_id('id_username').send_keys(login)
        browser.find_element_by_id('id_password').send_keys(password)
        browser.find_element_by_xpath('//input[@type="submit"]').click()
        browser.get('https://staging.pluspeter.com/admin/students/11/reset-limit/?q=karl%40print')
        browser.find_element_by_xpath('//a[@class="user-options-handler grp-collapse-handler '
                                      'grp-switch-user-is-original"]').click()
        browser.find_element_by_xpath('//a[@class="grp-logout"]').click()

        # Open landing page:
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

        # Go to products page and open freemium volume:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on "Print now" button for Freemium.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.XPATH,
                                                                           "//div[@class='package freemium']")))
        browser.find_element_by_id('print_freemium').click()
        logging.debug('Wizard rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        try:
            # Check if Freemium volume opened
            browser.find_element_by_id('omnibox-file-input')
            freemium_available = True
        except NoSuchElementException:
            freemium_available = False
        assert freemium_available is True, 'Freemium print is not available.'

        # Adding a document
        logging.debug('Adding document ' + pdf_docs[pdf_number_1])
        browser.find_element_by_id('omnibox-file-input').send_keys(test_docs_dir + pdf_docs[pdf_number_1])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Entering a volume title
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[1]/div/div[4]/input').send_keys(
            'Free/mium by-b0t! vol1')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding Freemium plus volume:
        browser.find_element_by_xpath('//a[@class="add-document"]').click()
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document to Freemium plus volume:
        logging.debug('Uploading document ' + pdf_docs[pdf_number_2])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number_2])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))

        # Typing Freemium plus volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[3]/div[2]/div/div/div[2]/input').send_keys(
            'Free/mium pl+s by-b0t! vol2')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        try:
            # Select Credit Card payment method:
            browser.find_element_by_id('paypal3').click()
            logging.debug('Clicked on "Credit card" radiobutton')
            # Mark first checkbox
            logging.debug('Marking first checkbox.')
            browser.find_element_by_xpath("//label[@for='checkbox-1']").click()
            # Mark second checkbox
            logging.debug('Marking second checkbox.')
            browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
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
        except WebDriverException:
            logging.debug('Order is free.')
            # Mark first checkbox
            logging.debug('Marking first checkbox.')
            browser.find_element_by_xpath("//label[@for='checkbox-1']").click()
            # Mark second checkbox
            logging.debug('Marking second checkbox.')
            browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
            # Initiate payment
            logging.debug('Clicking on "Print now" button.')
            browser.find_element_by_id('paypalPayment').click()

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

    def test_freemium_standard_flow(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_freemium_standard_flow.log', filemode='w',
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
        # Here sets the numbers of the documents to be selected from list
        # Documents should have more than 25, but less than 160 pages for this test
        pdf_number_1 = 3
        pdf_number_2 = 3
        print('Selected document: ' + pdf_docs[pdf_number_1])
        print('Selected document: ' + pdf_docs[pdf_number_2])

        # Reset Freemium print to make sure user can print:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com/admin/students/student/?q=karl%40printpeter')
        browser.find_element_by_id('id_username').send_keys(login)
        browser.find_element_by_id('id_password').send_keys(password)
        browser.find_element_by_xpath('//input[@type="submit"]').click()
        browser.get('https://staging.pluspeter.com/admin/students/11/reset-limit/?q=karl%40print')
        browser.find_element_by_xpath('//a[@class="user-options-handler grp-collapse-handler '
                                      'grp-switch-user-is-original"]').click()
        browser.find_element_by_xpath('//a[@class="grp-logout"]').click()

        # Open landing page:
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

        # Go to products page and open freemium volume:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on "Print now" button for Freemium.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.XPATH,
                                                                           "//div[@class='package freemium']")))
        browser.find_element_by_id('print_freemium').click()
        logging.debug('Wizard rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        try:
            # Check if Freemium volume opened
            browser.find_element_by_id('omnibox-file-input')
            freemium_available = True
        except NoSuchElementException:
            freemium_available = False
        assert freemium_available is True, 'Freemium print is not available.'

        # Adding a document
        logging.debug('Adding document ' + pdf_docs[pdf_number_1])
        browser.find_element_by_id('omnibox-file-input').send_keys(test_docs_dir + pdf_docs[pdf_number_1])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Entering a volume title
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[1]/div/div[4]/input').send_keys(
            'Free/mium by-b0t! vol1')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding Freemium plus volume:
        logging.debug('Clicking on "Add Freemium plus" button.')
        browser.find_element_by_xpath('//a[@class="add-document"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding Standard product:
        logging.debug('Clicking on "Add another document" button.')
        browser.find_element_by_xpath('//*[contains(text(), "Noch ein Dokument bestellen")]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        WebDriverWait(browser, 60).until(
            ec.visibility_of_element_located((By.ID, "product-select-wizard-modal")))
        logging.debug('Clicking on "print now" for Standard product.')
        browser.find_element_by_id('print_europe').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Removing Freemium plus volume:
        logging.debug('Collecting close button.')
        close_volume = browser.find_elements(By.XPATH, "//button[@class='closer closer--red closer--small']")
        logging.debug('Closing Freemium plus volume.')
        close_volume[1].click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding document to the Standard volume:
        logging.debug('Adding document to Standard volume.')
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number_2])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Typing Standard volume title:
        logging.debug('Typing Standard volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[3]/div[2]/div/div/div[2]/input').send_keys(
            'Stan/dard by-b0t! vol2')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-1']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
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

    def test_free_freeplus_standard(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_free_freeplus_standard.log', filemode='w',
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
        # Here sets the numbers of the documents to be selected from list
        # Documents should have more than 25, but less than 160 pages for this test
        pdf_number_1 = 3
        pdf_number_2 = 3
        pdf_number_3 = 3
        print('Selected document: ' + pdf_docs[pdf_number_1])
        print('Selected document: ' + pdf_docs[pdf_number_2])
        print('Selected document: ' + pdf_docs[pdf_number_3])

        # Reset Freemium print to make sure user can print:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com/admin/students/student/?q=karl%40printpeter')
        browser.find_element_by_id('id_username').send_keys(login)
        browser.find_element_by_id('id_password').send_keys(password)
        browser.find_element_by_xpath('//input[@type="submit"]').click()
        browser.get('https://staging.pluspeter.com/admin/students/11/reset-limit/?q=karl%40print')
        browser.find_element_by_xpath('//a[@class="user-options-handler grp-collapse-handler '
                                      'grp-switch-user-is-original"]').click()
        browser.find_element_by_xpath('//a[@class="grp-logout"]').click()

        # Open landing page:
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

        # Go to products page and open freemium volume:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on "Print now" button for Freemium.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.XPATH,
                                                                           "//div[@class='package freemium']")))
        browser.find_element_by_id('print_freemium').click()
        logging.debug('Wizard rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        try:
            # Check if Freemium volume opened
            browser.find_element_by_id('omnibox-file-input')
            freemium_available = True
        except NoSuchElementException:
            freemium_available = False
        assert freemium_available is True, 'Freemium print is not available.'

        # Adding a document
        logging.debug('Adding document ' + pdf_docs[pdf_number_1])
        browser.find_element_by_id('omnibox-file-input').send_keys(test_docs_dir + pdf_docs[pdf_number_1])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Entering a volume title
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[1]/div/div[4]/input').send_keys(
            'Free/mium by-b0t! vol1')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding Freemium plus volume:
        logging.debug('Clicking on "Add Freemium plus" button.')
        browser.find_element_by_xpath('//a[@class="add-document"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding Standard product:
        logging.debug('Clicking on "Add another document" button.')
        browser.find_element_by_xpath('//*[contains(text(), "Noch ein Dokument bestellen")]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        WebDriverWait(browser, 60).until(
            ec.visibility_of_element_located((By.ID, "product-select-wizard-modal")))
        logging.debug('Clicking on "print now" for Standard product.')
        browser.find_element_by_id('print_europe').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Removing Freemium plus volume:
        logging.debug('Collecting close button.')
        close_volume = browser.find_elements(By.XPATH, "//button[@class='closer closer--red closer--small']")
        logging.debug('Closing Freemium plus volume.')
        close_volume[1].click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding document to the Standard volume:
        logging.debug('Adding document to Standard volume.')
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number_2])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Typing Standard volume title:
        logging.debug('Typing Standard volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[3]/div[2]/div/div/div[2]/input').send_keys(
            'Stan/dard by-b0t! vol2')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding Freemium plus volume:
        logging.debug('Clicking on "Add another document" button.')
        browser.find_element_by_xpath('//*[contains(text(), "Noch ein Dokument bestellen")]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        WebDriverWait(browser, 60).until(
            ec.visibility_of_element_located((By.ID, "product-select-wizard-modal")))
        logging.debug('Clicking on "print now" for Standard product.')
        browser.find_element_by_id('print_freemium_plus').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding document to Freemium plus volume:
        logging.debug('Scrolling to the second volume.')
        browser.execute_script('window.scrollTo(0, 500)')
        file_input = browser.find_elements_by_name('file-input')
        logging.debug('Adding document to Freemium plus volume.')
        file_input[0].send_keys(test_docs_dir + pdf_docs[pdf_number_3])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Typing Freemium plus volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[3]/div[2]/div/div/div[2]/input').send_keys(
            'Free/mium pl+s by-b0t! vol2')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-1']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
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

    def test_freemium_plus_standard_flow(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_freemium_plus_flow_free.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Create list of available test documents
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have more than 25, but less than 160 pages for this test
        pdf_number_1 = 11
        pdf_number_2 = 12
        print('Selected document: ' + pdf_docs[pdf_number_1])
        print('Selected document: ' + pdf_docs[pdf_number_2])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        logging.debug('Landing page rendering.')
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

        # Go to products page and open freemium volume:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on "Print now" button for Freemium.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.XPATH,
                                                                           "//div[@class='package freemium']")))
        browser.find_element_by_id('print_freemium').click()
        logging.debug('Wizard rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        try:
            # If Freemium is available, order this product:
            logging.debug('Trying to add document to Freemium volume.')
            browser.find_element_by_id('omnibox-file-input').send_keys(test_docs_dir + pdf_docs[pdf_number_1])
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(
                ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
            # Entering a volume title
            logging.debug('Typing volume title.')
            browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[1]/div/div[4]/input').send_keys(
                'Free/mium by-b0t!')
            logging.debug('Clicking on wizard.')
            browser.find_element_by_xpath('//*[@id="wizard"]').click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(
                ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

            # Mark checkbox-1
            logging.debug('Marking first checkbox.')
            browser.find_element_by_xpath("//label[@for='checkbox-1']").click()
            # Mark checkbox-2
            logging.debug('Marking second checkbox.')
            browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
            # Initiate payment
            logging.debug('initiating payment.')
            browser.find_element_by_id('paypalPayment').click()

            # Successful upload page opens
            logging.debug('Successful upload page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
            # Go to profile page
            logging.debug('Clicking on "Close" button.')
            WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH,
                                                                             "//a[@class='closer']"))).click()
            logging.debug('Profile page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
            # Go to products page
            logging.debug('Clicking on "Print now" button.')
            WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
            logging.debug('Product selection page rendering.')
            WebDriverWait(browser, 60).until(
                ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
            # Open Freemium popup
            logging.debug('Clicking on "Print now" button for Freemium.')
            WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.XPATH,
                                                                               "//div[@class='package freemium']")))
            browser.find_element_by_id('print_freemium').click()
        except WebDriverException:
            logging.debug('Freemium is not available.')

        # Opening Freemium plus volume:
        logging.debug('Wizard rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on "Print now" button for freemium plus.')
        browser.find_element_by_id('print_freemium_plus').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document:
        logging.debug('Uploading document ' + pdf_docs[pdf_number_1])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number_1])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))

        # Typing Freemium plus volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[2]/div/div/div[2]/input').send_keys(
            'Free/mium by-b0t! vol1')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding Standard product:
        logging.debug('Clicking on "Add another document" button.')
        browser.find_element_by_xpath('//*[contains(text(), "Noch ein Dokument bestellen")]').click()
        logging.debug('Products page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on "print now" for Standard product.')
        browser.find_element_by_id('print_europe').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding document to the Standard volume:
        logging.debug('Collecting file inputs.')
        file_input = browser.find_elements(By.NAME, 'file-input')
        try:
            # If first volume has free space:
            logging.debug('Adding document to the second file input.')
            file_input[1].send_keys(test_docs_dir + pdf_docs[pdf_number_2])
        except IndexError:
            # If first volume has no free space:
            logging.debug('Adding document to the first file input.')
            file_input[0].send_keys(test_docs_dir + pdf_docs[pdf_number_2])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Typing Standard volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[3]/div[2]/div/div/div[2]/input').send_keys(
            'Stan/dard by-b0t! vol2')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        try:
            # Select Credit Card payment method:
            browser.find_element_by_id('paypal3').click()
            logging.debug('Clicked on "Credit card" radiobutton')
            product_free = False
        except WebDriverException:
            product_free = True
        assert product_free is False, 'Unable to select payment method.'

        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-1']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
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

    def test_freemium_plus_flow_free(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_freemium_plus_flow_free.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Create list of available test documents
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have more than 25, but less than 160 pages for this test
        pdf_number = 3
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        logging.debug('Landing page rendering.')
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

        # Go to products page and open freemium volume:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on "Print now" button for Freemium.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.XPATH,
                                                                           "//div[@class='package freemium']")))
        browser.find_element_by_id('print_freemium').click()
        logging.debug('Wizard rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        try:
            # If Freemium is available, order this product:
            logging.debug('Trying to add document to Freemium volume.')
            browser.find_element_by_id('omnibox-file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(
                ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
            # Entering a volume title
            logging.debug('Typing volume title.')
            browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[1]/div/div[4]/input').send_keys(
                'Free/mium by-b0t!')
            logging.debug('Clicking on wizard.')
            browser.find_element_by_xpath('//*[@id="wizard"]').click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(
                ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

            # Mark checkbox-1
            logging.debug('Marking first checkbox.')
            browser.find_element_by_xpath("//label[@for='checkbox-1']").click()
            # Mark checkbox-2
            logging.debug('Marking second checkbox.')
            browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
            # Initiate payment
            logging.debug('initiating payment.')
            browser.find_element_by_id('paypalPayment').click()

            # Successful upload page opens
            logging.debug('Successful upload page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
            # Go to profile page
            logging.debug('Clicking on "Close" button.')
            WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH,
                                                                             "//a[@class='closer']"))).click()
            logging.debug('Profile page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
            # Go to products page
            logging.debug('Clicking on "Print now" button.')
            WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
            logging.debug('Product selection page rendering.')
            WebDriverWait(browser, 60).until(
                ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
            # Open Freemium popup
            logging.debug('Clicking on "Print now" button for Freemium.')
            WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.XPATH,
                                                                               "//div[@class='package freemium']")))
            browser.find_element_by_id('print_freemium').click()
        except WebDriverException:
            logging.debug('Freemium is not available.')

        # Opening Freemium plus volume:
        logging.debug('Wizard rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on "Print now" button for freemium plus.')
        browser.find_element_by_id('print_freemium_plus').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document:
        logging.debug('Uploading document ' + pdf_docs[pdf_number])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))

        # Typing Freemium plus volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[2]/div/div/div[2]/input').send_keys(
            'Free/mium by-b0t!')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        try:
            # Select Credit Card payment method:
            browser.find_element_by_id('paypal3').click()
            logging.debug('Clicked on "Credit card" radiobutton')
            product_free = False
        except WebDriverException:
            product_free = True
        assert product_free is True, 'Order is not free.'

        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-1']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
        # Initiate payment
        logging.debug('Clicking on "Print now" button.')
        browser.find_element_by_id('paypalPayment').click()

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

    def test_freemium_plus_flow_CC(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_freemium_plus_flow_CC.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Create list of available test documents
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have more than 25, but less than 160 pages for this test
        pdf_number = 11
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        logging.debug('Landing page rendering.')
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

        # Go to products page and open freemium volume:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on "Print now" button for Freemium.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.XPATH,
                                                                           "//div[@class='package freemium']")))
        browser.find_element_by_id('print_freemium').click()
        logging.debug('Wizard rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        try:
            # If Freemium is available, order this product:
            logging.debug('Trying to add document to Freemium volume.')
            browser.find_element_by_id('omnibox-file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(
                ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
            # Entering a volume title
            logging.debug('Typing volume title.')
            browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[1]/div/div[4]/input').send_keys(
                'Free/mium by-b0t!')
            logging.debug('Clicking on wizard.')
            browser.find_element_by_xpath('//*[@id="wizard"]').click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(
                ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

            # Mark checkbox-1
            logging.debug('Marking first checkbox.')
            browser.find_element_by_xpath("//label[@for='checkbox-1']").click()
            # Mark checkbox-2
            logging.debug('Marking second checkbox.')
            browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
            # Initiate payment
            logging.debug('initiating payment.')
            browser.find_element_by_id('paypalPayment').click()

            # Successful upload page opens
            logging.debug('Successful upload page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
            # Go to profile page
            logging.debug('Clicking on "Close" button.')
            WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH,
                                                                             "//a[@class='closer']"))).click()
            logging.debug('Profile page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
            # Go to products page
            logging.debug('Clicking on "Print now" button.')
            WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
            logging.debug('Product selection page rendering.')
            WebDriverWait(browser, 60).until(
                ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
            # Open Freemium popup
            logging.debug('Clicking on "Print now" button for Freemium.')
            WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.XPATH,
                                                                               "//div[@class='package freemium']")))
            browser.find_element_by_id('print_freemium').click()
        except WebDriverException:
            logging.debug('Freemium is not available.')

        # Opening Freemium plus volume:
        logging.debug('Wizard rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on "Print now" button for freemium plus.')
        browser.find_element_by_id('print_freemium_plus').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document:
        logging.debug('Uploading document ' + pdf_docs[pdf_number])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))

        # Typing Freemium plus volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[2]/div/div/div[2]/input').send_keys(
            'Free/mium by-b0t!')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        try:
            # Select Credit Card payment method:
            browser.find_element_by_id('paypal3').click()
            logging.debug('Clicked on "Credit card" radiobutton')
            product_free = False
        except WebDriverException:
            product_free = True
        assert product_free is False, 'Unable to select payment method.'

        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-1']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
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

    def test_freemium_plus_flow_PP(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_freemium_plus_flow_PP.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Set Paypal credentials:
        paypal_login = 'info-buyer@printpeter.de'
        paypal_password = 'fdjkru12'

        # Create list of available documents:
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have more than 25, but less than 160 pages for this test
        pdf_number = 12
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        logging.debug('Landing page rendering.')
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
        # Click on print Freemium:
        logging.debug('Clicking on "Print now" button for Freemium.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.XPATH,
                                                                           "//div[@class='package freemium']")))
        browser.find_element_by_id('print_freemium').click()

        try:
            # If Freemium is available, order this product:
            logging.debug('Trying to add document to Freemium volume.')
            browser.find_element_by_id('omnibox-file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(
                ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
            # Entering a volume title
            logging.debug('Typing volume title.')
            browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[1]/div/div[4]/input').send_keys(
                'Free/mium by-b0t!')
            logging.debug('Clicking on wizard.')
            browser.find_element_by_xpath('//*[@id="wizard"]').click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(
                ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

            # Mark checkbox-1
            logging.debug('Marking first checkbox.')
            browser.find_element_by_xpath("//label[@for='checkbox-1']").click()
            # Mark checkbox-2
            logging.debug('Marking second checkbox.')
            browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
            # Initiate payment
            logging.debug('initiating payment.')
            browser.find_element_by_id('paypalPayment').click()

            # Successful upload page opens
            logging.debug('Successful upload page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
            # Go to profile page
            logging.debug('Clicking on "Close" button.')
            WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH,
                                                                             "//a[@class='closer']"))).click()
            logging.debug('Profile page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
            # Go to products page
            logging.debug('Clicking on "Print now" button.')
            WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
            logging.debug('Product selection page rendering.')
            WebDriverWait(browser, 60).until(
                ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
            # Open Freemium popup
            logging.debug('Clicking on "Print now" button for Freemium.')
            WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.XPATH,
                                                                               "//div[@class='package freemium']")))
            browser.find_element_by_id('print_freemium').click()
        except WebDriverException:
            logging.debug('Freemium is not available.')

        # Open Freemium plus volume:
        logging.debug('Wizard rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on "Print now" button for freemium plus.')
        browser.find_element_by_id('print_freemium_plus').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document:
        logging.debug('Uploading document ' + pdf_docs[pdf_number])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))

        # Typing Freemium plus volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[2]/div/div/div[2]/input').send_keys(
            'Free/mium by-b0t!')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        try:
            # Find Credit Card payment method to make sure product is not free:
            browser.find_element_by_id('paypal3')
            logging.debug('Located "Credit card" radiobutton')
            product_free = False
        except NoSuchElementException:
            product_free = True
        assert product_free is False, 'Unable to find payment method.'

        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-1']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
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

    def test_freemium_plus_two_vols(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_freemium_plus_two_vols.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Create list of available documents:
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the numbers of the documents to be selected from list
        # Document should have more than 25, but less than 160 pages for this test
        pdf_number_1 = 11
        pdf_number_2 = 12
        print('Selected document: ' + pdf_docs[pdf_number_1])
        print('Selected document: ' + pdf_docs[pdf_number_2])

        # Open landing page:
        browser = self.browser
        browser.get('https://staging.pluspeter.com')
        browser.maximize_window()
        logging.debug('Landing page rendering.')
        WebDriverWait(browser, 10).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

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
        # Go to Products page:
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Opening Freemium limit popup:
        logging.debug('Clicking on "Print now" button for Freemium.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.XPATH,
                                                                           "//div[@class='package freemium']")))
        browser.find_element_by_id('print_freemium').click()

        try:
            # If Freemium is available, order this product:
            WebDriverWait(browser, 60).until(
                ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
            logging.debug('Trying to add document to Freemium volume.')
            browser.find_element_by_id('omnibox-file-input').send_keys(test_docs_dir + pdf_docs[pdf_number_1])
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(
                ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
            # Entering a volume title
            logging.debug('Typing volume title.')
            browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[1]/div/div[4]/input').send_keys(
                'Free/mium by-b0t!')
            logging.debug('Clicking on wizard.')
            browser.find_element_by_xpath('//*[@id="wizard"]').click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(
                ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

            # Mark checkbox-1
            logging.debug('Marking first checkbox.')
            browser.find_element_by_xpath("//label[@for='checkbox-1']").click()
            # Mark checkbox-2
            logging.debug('Marking second checkbox.')
            browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
            # Initiate payment
            logging.debug('initiating payment.')
            browser.find_element_by_id('paypalPayment').click()

            # Successful upload page opens
            logging.debug('Successful upload page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
            # Go to profile page
            logging.debug('Clicking on "Close" button.')
            WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH,
                                                                             "//a[@class='closer']"))).click()
            logging.debug('Profile page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
            # Go to products page
            logging.debug('Clicking on "Print now" button.')
            WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
            logging.debug('Product selection page rendering.')
            WebDriverWait(browser, 60).until(
                ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
            # Open Freemium popup
            logging.debug('Clicking on "Print now" button for Freemium.')
            WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.XPATH,
                                                                               "//div[@class='package freemium']")))
            browser.find_element_by_id('print_freemium').click()
        except WebDriverException:
            logging.debug('Freemium is not available.')

        # Opening Freemium plus volume:
        logging.debug('Clicking on "Print now" button for Freemium plus.')
        browser.find_element_by_id('print_freemium_plus').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document:
        logging.debug('Uploading document ' + pdf_docs[pdf_number_1])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number_1])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Typing Freemium plus volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[2]/div/div/div[2]/input').send_keys(
            'Free/mium by-b0t! vol1')
        logging.debug('Clicking on wizard.')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding second volume:
        logging.debug('Clicking on "Add another document" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.XPATH, "//a[@href='#']"))).click()
        logging.debug('Products page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        # Opening Freemium limit popup:
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.XPATH,
                                                                           "//div[@class='package freemium']")))
        browser.find_element_by_id('print_freemium').click()
        # Opening Freemium plus volume:
        logging.debug('Clicking on "Print now" button for Freemium plus.')
        browser.find_element_by_id('print_freemium_plus').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Scrolling to the second volume.')
        browser.execute_script('window.scrollTo(0, 900)')
        # Adding document to the second volume:
        logging.debug('Collecting file inputs.')
        file_input = browser.find_elements(By.NAME, 'file-input')
        try:
            # If first volume has free space:
            logging.debug('Adding document to the second file input.')
            file_input[1].send_keys(test_docs_dir + pdf_docs[pdf_number_2])
        except IndexError:
            # If first volume has no free space:
            logging.debug('Adding document to the first file input.')
            file_input[0].send_keys(test_docs_dir + pdf_docs[pdf_number_2])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Typing second Freemium plus volume title:
        logging.debug('Typing volume title.')
        browser.find_element_by_xpath('//*[@id="wizard"]/div[3]/div[2]/div/div/div[2]/input').send_keys(
            'Free/mium by-b0t! vol2')
        browser.find_element_by_xpath('//*[@id="wizard"]').click()
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        try:
            # Select Credit Card payment method:
            browser.find_element_by_id('paypal3').click()
            logging.debug('Clicked on "Credit card" radiobutton')
            product_free = False
        except WebDriverException:
            product_free = True
        assert product_free is False, 'Unable to select payment method.'

        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-1']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
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

    def test_freemium_big_doc(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_freemium_big_doc.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Create list of available pdf documents
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the numbers of the documents to be selected from list
        # Document should have more than 160 pages for this test
        pdf_number = 4
        print('Selected document: ' + pdf_docs[pdf_number])

        # Reset Freemium print
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com/admin/students/student/?q=karl%40printpeter')
        browser.find_element_by_id('id_username').send_keys(login)
        browser.find_element_by_id('id_password').send_keys(password)
        browser.find_element_by_xpath('//input[@type="submit"]').click()
        browser.get('https://staging.pluspeter.com/admin/students/11/reset-limit/?q=karl%40print')
        browser.find_element_by_xpath('//a[@class="user-options-handler grp-collapse-handler '
                                      'grp-switch-user-is-original"]').click()
        browser.find_element_by_xpath('//a[@class="grp-logout"]').click()

        # Open landing page:
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

        # Go to products page and open Freemium volume:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on "Print now" button for Freemium.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.XPATH,
                                                                           "//div[@class='package freemium']")))
        browser.find_element_by_id('print_freemium').click()
        logging.debug('Wizard rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        try:
            # Check if Freemium is available:
            browser.find_element_by_id('omnibox-file-input')
            freemium_available = True
        except NoSuchElementException:
            freemium_available = False
        assert freemium_available is True, 'Freemium is not available.'

        # Adding a document
        logging.debug('Adding document ' + pdf_docs[pdf_number])
        browser.find_element_by_id('omnibox-file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        try:
            # Check if popup is displayed
            browser.find_element_by_xpath('//*[contains(text(), "Dein Dokument hatte mehr als 160 Seiten")]')
            doc_was_split = True
        except NoSuchElementException:
            doc_was_split = False
        assert doc_was_split is True, 'Split document popup is missing.'
        browser.quit()

    def test_freemium_not_enough_pages(self):
        logging.basicConfig(level=logging.DEBUG, filename='test_freemium_not_enough_pages.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Create list of available pdf documents
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the numbers of the documents to be selected from list
        # Document should have less than 25 pages for this test
        pdf_number = 10
        print('Selected document: ' + pdf_docs[pdf_number])

        # Reset Freemium print
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com/admin/students/student/?q=karl%40printpeter')
        browser.find_element_by_id('id_username').send_keys(login)
        browser.find_element_by_id('id_password').send_keys(password)
        browser.find_element_by_xpath('//input[@type="submit"]').click()
        browser.get('https://staging.pluspeter.com/admin/students/11/reset-limit/?q=karl%40print')
        browser.find_element_by_xpath('//a[@class="user-options-handler grp-collapse-handler '
                                      'grp-switch-user-is-original"]').click()
        browser.find_element_by_xpath('//a[@class="grp-logout"]').click()

        # Open landing page:
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

        # Go to products page and open Freemium volume:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on "Print now" button for Freemium.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.XPATH,
                                                                           "//div[@class='package freemium']")))
        browser.find_element_by_id('print_freemium').click()
        logging.debug('Wizard rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        try:
            # Check if Freemium is available
            browser.find_element_by_id('omnibox-file-input')
            freemium_available = True
        except NoSuchElementException:
            freemium_available = False
        assert freemium_available is True, 'Freemium is not available.'

        logging.debug('Adding document ' + pdf_docs[pdf_number])
        browser.find_element_by_id('omnibox-file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        try:
            # Check if not enough pages popup is displayed.
            WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.ID, "error-popup")))
            browser.find_element_by_xpath('//*[contains(text(),"Das PDF muss mindestens 25 Seiten haben.")]')
            not_enough_pages = True
        except NoSuchElementException:
            not_enough_pages = False
        assert not_enough_pages is True, 'Not enough pages popup is missing.'
        browser.quit()

    def test_freemium_invalid_format(self):
        logging.basicConfig(level=logging.DEBUG, filename='test_freemium_not_pdf.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Create list of available pdf documents
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if not item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        pdf_number = 0
        print('Selected document: ' + pdf_docs[pdf_number])

        # Reset Freemium print
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com/admin/students/student/?q=karl%40printpeter')
        browser.find_element_by_id('id_username').send_keys(login)
        browser.find_element_by_id('id_password').send_keys(password)
        browser.find_element_by_xpath('//input[@type="submit"]').click()
        browser.get('https://staging.pluspeter.com/admin/students/11/reset-limit/?q=karl%40print')
        browser.find_element_by_xpath('//a[@class="user-options-handler grp-collapse-handler '
                                      'grp-switch-user-is-original"]').click()
        browser.find_element_by_xpath('//a[@class="grp-logout"]').click()

        # Open landing page:
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

        # Go to products page and open Freemium volume:
        logging.debug('Profile page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on "Print now" button.')
        WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
        logging.debug('Product selection page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on "Print now" button for Freemium.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.XPATH,
                                                                           "//div[@class='package freemium']")))
        browser.find_element_by_id('print_freemium').click()
        logging.debug('Wizard rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        try:
            # Check if Freemium is available
            browser.find_element_by_id('omnibox-file-input')
            freemium_available = True
        except NoSuchElementException:
            freemium_available = False
        assert freemium_available is True, 'Freemium is not available.'

        logging.debug('Adding document ' + pdf_docs[pdf_number])
        browser.find_element_by_id('omnibox-file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        try:
            # Check if invalid format popup is displayed.
            WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.ID, "error-popup")))
            browser.find_element_by_xpath('//*[contains(text(),"Dieses Format wird nicht unterstützt.")]')
            invalid_format = True
        except NoSuchElementException:
            invalid_format = False
        assert invalid_format is True, 'Invalid format popup is missing.'
        browser.quit()

    def test_freemium_plus_big_doc(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_freemium_plus_big_doc.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Create list of available documents:
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have more than 160 pages for this test
        pdf_number = 4
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        logging.debug('Landing page rendering.')
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
        # Click on print Freemium:
        logging.debug('Clicking on "Print now" button for Freemium.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.XPATH,
                                                                           "//div[@class='package freemium']")))
        browser.find_element_by_id('print_freemium').click()

        try:
            # If Freemium is available, order this product:
            WebDriverWait(browser, 60).until(
                ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
            logging.debug('Wizard page rendered.')
            logging.debug('Trying to add document to Freemium volume.')
            browser.find_element_by_id('omnibox-file-input')
            pdf_number = 3
            browser.find_element_by_id('omnibox-file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(
                ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
            # Entering a volume title
            logging.debug('Typing volume title.')
            browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[1]/div/div[4]/input').send_keys(
                'Free/mium by-b0t!')
            logging.debug('Clicking on wizard.')
            browser.find_element_by_xpath('//*[@id="wizard"]').click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(
                ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

            # Mark checkbox-1
            logging.debug('Marking first checkbox.')
            browser.find_element_by_xpath("//label[@for='checkbox-1']").click()
            # Mark checkbox-2
            logging.debug('Marking second checkbox.')
            browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
            # Initiate payment
            logging.debug('initiating payment.')
            browser.find_element_by_id('paypalPayment').click()

            # Successful upload page opens
            logging.debug('Successful upload page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
            # Go to profile page
            logging.debug('Clicking on "Close" button.')
            WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH,
                                                                             "//a[@class='closer']"))).click()
            logging.debug('Profile page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
            # Go to products page
            logging.debug('Clicking on "Print now" button.')
            WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
            logging.debug('Product selection page rendering.')
            WebDriverWait(browser, 60).until(
                ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
            # Open Freemium popup
            logging.debug('Clicking on "Print now" button for Freemium.')
            WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.XPATH,
                                                                               "//div[@class='package freemium']")))
            browser.find_element_by_id('print_freemium').click()
        except NoSuchElementException:
            logging.debug('Freemium is not available.')

        # Open Freemium plus volume:
        logging.debug('Wizard rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on "Print now" button for freemium plus.')
        browser.find_element_by_id('print_freemium_plus').click()
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document:
        pdf_number = 4
        logging.debug('Uploading document ' + pdf_docs[pdf_number])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))

        try:
            # Check if popup is displayed
            browser.find_element_by_xpath('//*[contains(text(), "Dein Dokument hatte mehr als 160 Seiten")]')
            doc_was_split = True
        except NoSuchElementException:
            doc_was_split = False
        assert doc_was_split is True, 'Split document popup is missing.'
        browser.quit()

    def test_freemium_plus_not_enough_pages(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_freemium_plus_not_enough_pages.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Create list of available documents:
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have more than 160 pages for this test
        pdf_number = 10
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        logging.debug('Landing page rendering.')
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
        # Click on print Freemium:
        logging.debug('Clicking on "Print now" button for Freemium.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.XPATH,
                                                                           "//div[@class='package freemium']")))
        browser.find_element_by_id('print_freemium').click()

        try:
            # If Freemium is available, order this product:
            WebDriverWait(browser, 60).until(
                ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
            logging.debug('Trying to add document to Freemium volume.')
            browser.find_element_by_id('omnibox-file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(
                ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
            # Entering a volume title
            logging.debug('Typing volume title.')
            browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[1]/div/div[4]/input').send_keys(
                'Free/mium by-b0t!')
            logging.debug('Clicking on wizard.')
            browser.find_element_by_xpath('//*[@id="wizard"]').click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(
                ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

            # Mark checkbox-1
            logging.debug('Marking first checkbox.')
            browser.find_element_by_xpath("//label[@for='checkbox-1']").click()
            # Mark checkbox-2
            logging.debug('Marking second checkbox.')
            browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
            # Initiate payment
            logging.debug('initiating payment.')
            browser.find_element_by_id('paypalPayment').click()

            # Successful upload page opens
            logging.debug('Successful upload page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
            # Go to profile page
            logging.debug('Clicking on "Close" button.')
            WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH,
                                                                             "//a[@class='closer']"))).click()
            logging.debug('Profile page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
            # Go to products page
            logging.debug('Clicking on "Print now" button.')
            WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
            logging.debug('Product selection page rendering.')
            WebDriverWait(browser, 60).until(
                ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
            # Open Freemium popup
            logging.debug('Clicking on "Print now" button for Freemium.')
            WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.XPATH,
                                                                               "//div[@class='package freemium']")))
            browser.find_element_by_id('print_freemium').click()
        except WebDriverException:
            logging.debug('Freemium is not available.')

        # Open Freemium plus volume:
        logging.debug('Wizard rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on "Print now" button for freemium plus.')
        browser.find_element_by_id('print_freemium_plus').click()
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
            # Select Credit Card payment method:
            browser.find_element_by_id('paypal3').click()
            logging.debug('Clicked on "Credit card" radiobutton')
            freemium_available = False
        except WebDriverException:
            freemium_available = True
        assert freemium_available is False, 'Unable to select payment method.'

        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-1']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
        # Initiate payment
        logging.debug('Clicking on "Print now" button.')
        browser.find_element_by_id('paypalPayment').click()
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        try:
            # Check if popup is displayed
            WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.ID, "error-popup")))
            browser.find_element_by_xpath('//*[contains(text(), "Eine Bestellung muss aus mindestens 25")]')
            not_enough_pages = True
        except NoSuchElementException:
            not_enough_pages = False
        assert not_enough_pages is True, 'Not enough pages popup is missing.'
        browser.quit()

    def test_freemium_plus_invalid_format(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_freemium_plus_invalid_format.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Create list of available documents:
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if not item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have invalid format for this test
        pdf_number = 0
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        logging.debug('Landing page rendering.')
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
        # Click on print Freemium:
        logging.debug('Clicking on "Print now" button for Freemium.')
        WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.XPATH,
                                                                           "//div[@class='package freemium']")))
        browser.find_element_by_id('print_freemium').click()

        try:
            # If Freemium is available, order this product:
            WebDriverWait(browser, 60).until(
                ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
            logging.debug('Trying to add document to Freemium volume.')
            browser.find_element_by_id('omnibox-file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(
                ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
            # Entering a volume title
            logging.debug('Typing volume title.')
            browser.find_element_by_xpath('//*[@id="wizard"]/div[2]/div[1]/div/div[4]/input').send_keys(
                'Free/mium by-b0t!')
            logging.debug('Clicking on wizard.')
            browser.find_element_by_xpath('//*[@id="wizard"]').click()
            logging.debug('Wizard page rendering.')
            WebDriverWait(browser, 60).until(
                ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

            # Mark checkbox-1
            logging.debug('Marking first checkbox.')
            browser.find_element_by_xpath("//label[@for='checkbox-1']").click()
            # Mark checkbox-2
            logging.debug('Marking second checkbox.')
            browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
            # Initiate payment
            logging.debug('initiating payment.')
            browser.find_element_by_id('paypalPayment').click()

            # Successful upload page opens
            logging.debug('Successful upload page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
            # Go to profile page
            logging.debug('Clicking on "Close" button.')
            WebDriverWait(browser, 60).until(ec.presence_of_element_located((By.XPATH,
                                                                             "//a[@class='closer']"))).click()
            logging.debug('Profile page rendering.')
            WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                 "//div[@class='loading_box']")))
            # Go to products page
            logging.debug('Clicking on "Print now" button.')
            WebDriverWait(browser, 60).until(ec.element_to_be_clickable((By.LINK_TEXT, 'Jetzt Drucken'))).click()
            logging.debug('Product selection page rendering.')
            WebDriverWait(browser, 60).until(
                ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
            # Open Freemium popup
            logging.debug('Clicking on "Print now" button for Freemium.')
            WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.XPATH,
                                                                               "//div[@class='package freemium']")))
            browser.find_element_by_id('print_freemium').click()
        except WebDriverException:
            logging.debug('Freemium is not available.')

        # Open Freemium plus volume:
        logging.debug('Wizard rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Clicking on "Print now" button for freemium plus.')
        browser.find_element_by_id('print_freemium_plus').click()
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
            # Check if popup is displayed
            WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.ID, "error-popup")))
            browser.find_element_by_xpath('//*[contains(text(), "Dieses Format wird nicht unterstützt.")]')
            not_enough_pages = True
        except NoSuchElementException:
            not_enough_pages = False
        assert not_enough_pages is True, 'Not enough pages popup is missing.'
        browser.quit()

    def test_standard_big_doc(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_standard_big_doc.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Create list of available documents:
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have more than 170 pages for this test
        pdf_number = 9
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        logging.debug('Landing page rendering.')
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

        try:
            # Check if popup is displayed
            browser.find_element_by_xpath('//*[contains(text(), "Dein Dokument hatte mehr als 170 Seiten")]')
            doc_was_split = True
        except NoSuchElementException:
            doc_was_split = False
        assert doc_was_split is True, 'Split document popup is missing.'
        browser.quit()

    def test_standard_not_enough_pages(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_standard_not_enough_pages.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Create list of available documents:
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have less than 25 pages for this test
        pdf_number = 10
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        logging.debug('Landing page rendering.')
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
        logging.debug('Wizard rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        # Adding a document:
        logging.debug('Uploading document ' + pdf_docs[pdf_number])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))

        # Mark first checkbox
        logging.debug('Marking first checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-2']").click()
        # Mark second checkbox
        logging.debug('Marking second checkbox.')
        browser.find_element_by_xpath("//label[@for='checkbox-3']").click()
        # Initiate payment
        logging.debug('Clicking on "Print now" button.')
        browser.find_element_by_id('paypalPayment').click()
        WebDriverWait(browser, 60).until(
            ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))

        try:
            # Check if popup is displayed
            WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.ID, "error-popup")))
            browser.find_element_by_xpath('//*[contains(text(), "Eine Bestellung muss aus mindestens 25")]')
            not_enough_pages = True
        except NoSuchElementException:
            not_enough_pages = False
        assert not_enough_pages is True, 'Not enough pages popup is missing.'
        browser.quit()

    def test_standard_invalid_format(self):

        logging.basicConfig(level=logging.DEBUG, filename='test_standard_invalid_format.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')

        # logging.disable(logging.DEBUG)

        # Set authorization credentials:
        login = 'karl@printpeter.de'
        password = 'pleasechange'

        # Create list of available documents:
        pdf_docs = []
        for item in os.listdir(test_docs_dir):
            if not item.endswith('.pdf'):
                logging.debug('Adding ' + item)
                pdf_docs.append(item)
            else:
                logging.debug('Skipping ' + item)
                pass
        # Here sets the number of the document to be selected from list
        # Document should have invalid format for this test
        pdf_number = 0
        print('Selected document: ' + pdf_docs[pdf_number])

        # Open landing page:
        browser = self.browser
        browser.maximize_window()
        browser.get('https://staging.pluspeter.com')
        logging.debug('Landing page rendering.')
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

        # Adding a document:
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH, "//div[@class='loading_box']")))
        logging.debug('Uploading document ' + pdf_docs[pdf_number])
        browser.find_element_by_name('file-input').send_keys(test_docs_dir + pdf_docs[pdf_number])
        logging.debug('Wizard page rendering.')
        WebDriverWait(browser, 60).until(ec.invisibility_of_element_located((By.XPATH,
                                                                             "//div[@class='loading_box']")))

        try:
            # Check if popup is displayed
            WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.ID, "error-popup")))
            browser.find_element_by_xpath('//*[contains(text(), "Dieses Format wird nicht unterstützt.")]')
            not_enough_pages = True
        except NoSuchElementException:
            not_enough_pages = False
        assert not_enough_pages is True, 'Not enough pages popup is missing.'
        browser.quit()


def suite_positive():
    pos_suite = unittest.TestSuite()
    pos_suite.addTest(FreemiumFlow('test_freemium_flow'))
    pos_suite.addTest(FreemiumFlow('test_freemium_freemium_plus_flow'))
    pos_suite.addTest(FreemiumFlow('test_freemium_standard_flow'))
    pos_suite.addTest(FreemiumFlow('test_free_freeplus_standard'))
    pos_suite.addTest(FreemiumFlow('test_freemium_plus_standard_flow'))
    pos_suite.addTest(FreemiumFlow('test_freemium_plus_flow_free'))
    pos_suite.addTest(FreemiumFlow('test_freemium_plus_flow_CC'))
    pos_suite.addTest(FreemiumFlow('test_freemium_plus_flow_PP'))
    pos_suite.addTest(FreemiumFlow('test_freemium_plus_two_vols'))
    pos_suite.addTest(FreemiumFlow('test_freemium_plus_two_vols'))
    return pos_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite_positive())
