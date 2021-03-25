from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
import time
import sys

# Globals
TIME_DELAY = 1
coupons_dict = dict()
LOWER = 0
UPPER = 9999

# test working code 8509

def scrap_public_codes(driver):
    """
    Gets the coupon data from the ones publicly available on the website
    :param driver: The web driver
    :return: NULL
    """

    # Get the public local coupons
    try:
        for i in range(1, 20):
            # Grab the public coupons and parse the data and put them in a dict
            code_text = driver.find_element_by_xpath(
                "//*[@id='js-pageSplit']/section/div[2]/div/div[3]/div[" + str(i) + "]/a/div[4]/p").text

            code_number = int(code_text[-5:-1])
            description = code_text[:-13]
            coupons_dict[code_number] = description
    except:
        pass


def test_code_range(driver, lower, upper):
    """
    Tests all the codes in a given range on the already open dominos page
    :param driver: The web driver
    :param lower: Your starting range for your coupon search
    :param upper: The end of your coupon search
    :post: Adds all the found codes to the coupon dictionary
    :return: NULL
    """
    wait = WebDriverWait(driver, 10)

    for i in range(lower, upper+1):
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="Coupon_Code"]')))
        code = driver.find_element_by_name('Coupon_Code')

        # if the code we are testing is already in the dictionary skip it
        if i in coupons_dict:
            continue

        # Send the code we are testing
        try:
            if i < 10:
                code.send_keys("000" + str(i))
                print("Testing code 000" + str(i))
            elif i < 100:
                code.send_keys("00" + str(i))
                print("Testing code 00" + str(i))
            elif i < 1000:
                code.send_keys("0" + str(i))
                print("Testing code 0" + str(i))
            else:
                code.send_keys(str(i))
                print("Testing code " + str(i))

            # Click on the button
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='js-pageSplit']/section/div[2]/div/div[1]/form/div/button")))
            driver.find_element_by_xpath("//*[@id='js-pageSplit']/section/div[2]/div/div[1]/form/div/button").click()

            # Get the text from the pop up
            wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='genericOverlay']/section/header/h1")))
            coupon_pop_up = driver.find_element_by_xpath("//*[@id='genericOverlay']/section/header/h1").text

            if coupon_pop_up == 'COUPON NOT AVAILABLE':
                # Close the COUPON NOT AVAILABLE pop up
                wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='genericOverlay']/section/header/button")))
                driver.find_element_by_xpath("//*[@id='genericOverlay']/section/header/button").click()
                # Remove the coupon code from the input box
                code.clear()

            else:
                # if the coupon is found put it in the dictionary
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='genericOverlay']/section/div/div[2]/div[1]/p")))
                coupon_desc = driver.find_element_by_xpath("//*[@id='genericOverlay']/section/div/div[2]/div[1]/p").text
                coupons_dict[i] = coupon_desc
                print("NEW CODE FOUND: " + str(i) + " " + coupons_dict[i])

                # Wait until we can close the coupon pop up then close the pop up
                wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='genericOverlay']/section/div/div[6]/div/a")))
                driver.find_element_by_xpath("//*[@id='genericOverlay']/section/div/div[6]/div/a").click()
                time.sleep(TIME_DELAY*3)
        except:
            print("ERROR")
            break


def file_loader(file):
    """
    Given a file load the file into the coupon_dict and start your search from there and end at the upper bound
    :param file: The name of the file in string form
    :postcond: Modifies the coupon_dict
    :return: NULL
    """
    with open(f'{file}.json', 'r') as openfile:
        # Reading from json file
        coupons_dict = json.load(openfile)

    global LOWER
    LOWER = int(list(coupons_dict)[-1])


def coupon_gathering(driver):
    time.sleep(TIME_DELAY)

    # Get the public local coupons
    scrap_public_codes(driver)

    # Test all codes based on the given range
    test_code_range(driver, LOWER, UPPER)

    # Testing only
    for key in coupons_dict:
        print("Code: " + str(key) + " " + coupons_dict[key])

    with open("coupon.json", "w") as outfile:
        json.dump(coupons_dict, outfile,indent=2)

    driver.close()


def dom_select(driver, city: 'str', postal_code: 'str', province: 'str'):
    """
    Inputs all the location information into the dominos website.
    Picks the closest dominos based on your location information
    :param driver: Driver from selenium
    :param city: Name of the city your a located in
    :param postal_code: Your postal_code
    :param province: Your province'
    :return: nothing
    """
    wait = WebDriverWait(driver, 10)

    # Select and send the location info
    city_box = driver.find_element_by_name('City')
    city_box.send_keys(city)
    postalcode_box = driver.find_element_by_name('Postal_Code')
    postalcode_box.send_keys(postal_code)
    province_select = Select(driver.find_element_by_id('Region'))
    province_select.select_by_value(province.upper())
    location_button = driver.find_element_by_xpath("//*[@id='locationSearchForm']/div/div[4]/button")
    driver.execute_script("arguments[0].click();", location_button)

    # click on the nearest dominos
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='locationsResultsPage']/div[2]/div[2]/div[1]/div[3]/div/div[2]/div/a")))
    nearest_doms = driver.find_element_by_xpath("//*[@id='locationsResultsPage']/div[2]/div[2]/div[1]/div[3]/div/div[2]/div/a")
    driver.execute_script("arguments[0].click();", nearest_doms)

    # Select the coupon tab
    time.sleep(TIME_DELAY)
    nearest_doms = driver.find_element_by_xpath("//*[@id='_dpz']/header/nav[1]/div[1]/ul/li[6]/a")
    driver.execute_script("arguments[0].click();", nearest_doms)


def bot_start_up(city: 'str', postal_code: 'str', province: 'str'):
    """
    Starts the bot up
    :param city: Name of the city your a located in
    :param postal_code: Your postal_code
    :param province: Your province'
    :return: nothing
    """
    # Check that the parameters of the correct data type
    assert type(city) is str, "City be a string"
    assert type(city) is str, "Postal code needs to be a string"
    assert type(city) is str, "Province code needs to be a string"

    # Using Chrome to access web
    driver = webdriver.Chrome()
    # Open the website
    driver.get('https://www.dominos.ca/en/pages/order/#!/locations/search/')
    time.sleep(TIME_DELAY)

    # click on the carryout button
    element = driver.find_element_by_xpath("//*[@id='Service_Type_Carryout']")
    driver.execute_script("arguments[0].click();", element)

    # Select on your closest dominos
    dom_select(driver, city, postal_code, province)

    # Get the coupons
    coupon_gathering(driver)


if __name__ == "__main__":

    # Set the coupon Range search
    LOWER = int(input("Enter the start of the coupon search: "))
    UPPER = int(input("Enter the end of the coupon search: "))

    # Ask if we want to load a file
    file_dump = input("Do you want to start your search from a file? (Y/N) ")
    if file_dump == 'y' or file_dump == 'Y':
        file_loader(input("What is the name of your file? "))

    bot_start_up("Saskatoon", "S7N 0Y7", "Saskatchewan")

