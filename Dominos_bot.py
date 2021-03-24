from selenium import webdriver
from selenium.webdriver.support.ui import Select
import json
import time
import sys

TIME_DELAY = 1


def coupon_gathering(driver):
    time.sleep(TIME_DELAY)

    # Get the public local coupons
    coupons_dict = dict()
    found_codes = list()
    try:
        for i in range(1, 20):
            # Grab the public coupons and parse the data and put them in a dict
            code_text = driver.find_element_by_xpath(
                "//*[@id='js-pageSplit']/section/div[2]/div/div[3]/div[" + str(i) + "]/a/div[4]/p").text

            code_number = int(code_text[-5:-1])
            description = code_text[:-13]
            coupons_dict[code_number] = description
            found_codes.append(code_text)
            found_codes.sort()
    except:
        pass

    # Test every possible code
    code = driver.find_element_by_name('Coupon_Code')
    for i in range(1500, 10000):

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
            driver.find_element_by_xpath("//*[@id='js-pageSplit']/section/div[2]/div/div[1]/form/div/button").click()
            time.sleep(TIME_DELAY)
            # Get the text from the pop up
            coupon_pop_up = driver.find_element_by_xpath("//*[@id='genericOverlay']/section/header/h1").text
            time.sleep(TIME_DELAY)

            if coupon_pop_up == 'COUPON NOT AVAILABLE':
                driver.find_element_by_xpath("//*[@id='genericOverlay']/section/header/button").click()
            else:
                # if the coupon is found put it in the dictionary
                coupon_desc = driver.find_element_by_xpath("//*[@id='genericOverlay']/section/div/div[2]/div[1]/p").text
                coupons_dict[code] = coupon_desc
                driver.find_element_by_xpath("//*[@id='genericOverlay']/section/div/div[6]/div/a").click()
            # Remove the coupon code from the input box
            code.clear()
        except:
            print("ERROR")
            break

    # Testing only
    for key in coupons_dict:
        print("Code: " + str(key) + " " + coupons_dict[key])
    print(found_codes)

    # with open("sample.json", "w") as outfile:
    #     json.dump(coupons_dict, outfile)


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
    time.sleep(TIME_DELAY)
    nearest_doms = driver.find_element_by_xpath(
        "//*[@id='locationsResultsPage']/div[2]/div[2]/div[1]/div[3]/div/div[2]/div/a")
    driver.execute_script("arguments[0].click();", nearest_doms)

    # Select the coupon tab
    time.sleep(TIME_DELAY)
    nearest_doms = driver.find_element_by_xpath("//*[@id='_dpz']/header/nav[1]/div[1]/ul/li[6]/a")
    driver.execute_script("arguments[0].click();", nearest_doms)


def bot_start_up(city: 'str', postal_code: 'str', province: 'str'):
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
    bot_start_up("Saskatoon", "S7N 0Y7", "Saskatchewan")
    while (True):
        pass
