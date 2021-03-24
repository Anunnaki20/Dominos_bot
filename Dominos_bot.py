from selenium import webdriver
from selenium.webdriver.support.ui import Select
import json
import time


def coupon_gathering(driver):
    time.sleep(1)

    # Get the public local coupons
    public_coupons = dict()
    try:
        for i in range(1, 20):
            # Grab the public coupons and parse the data and put them in a dict
            code_text = driver.find_element_by_xpath(
                "//*[@id='js-pageSplit']/section/div[2]/div/div[3]/div[" + str(i) + "]/a/div[4]/p").text
            code = int(code_text[-5:-1])
            description = code_text[:-13]
            public_coupons[code] = description
    except:
        pass

    # TODO: Parse the list and put it into a JSON file with the code being the key and value being the description

    # TODO: Iterate over every code from 0000 to 9999. If a code is found put it in the
    #  JSON if it does not already exist

    for i in public_coupons:
        print(i)


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

    # click on teh nearest dominos
    time.sleep(1)
    nearest_doms = driver.find_element_by_xpath(
        "//*[@id='locationsResultsPage']/div[2]/div[2]/div[1]/div[3]/div/div[2]/div/a")
    driver.execute_script("arguments[0].click();", nearest_doms)

    # Select the coupon tab
    time.sleep(1)
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

    # click on the carryout button
    element = driver.find_element_by_xpath("//*[@id='Service_Type_Carryout']")
    driver.execute_script("arguments[0].click();", element)

    # # Select and send the location info
    # city_box = driver.find_element_by_name('City')
    # city_box.send_keys(city)
    # postalcode_box = driver.find_element_by_name('Postal_Code')
    # postalcode_box.send_keys(postal_code)
    # province_select = Select(driver.find_element_by_id('Region'))
    # province_select.select_by_value(province.upper())
    # location_button = driver.find_element_by_xpath("//*[@id='locationSearchForm']/div/div[4]/button")
    # driver.execute_script("arguments[0].click();", location_button)
    #
    # # click on teh nearest dominos
    # time.sleep(1)
    # nearest_doms = driver.find_element_by_xpath(
    #     "//*[@id='locationsResultsPage']/div[2]/div[2]/div[1]/div[3]/div/div[2]/div/a")
    # driver.execute_script("arguments[0].click();", nearest_doms)
    #
    # # Select the coupon tab
    # time.sleep(1)
    # nearest_doms = driver.find_element_by_xpath("//*[@id='_dpz']/header/nav[1]/div[1]/ul/li[6]/a")
    # driver.execute_script("arguments[0].click();", nearest_doms)

    #Select on your closest dominos
    dom_select(driver, city, postal_code, province)

    # Get the coupons
    coupon_gathering(driver)


if __name__ == "__main__":
    bot_start_up("Saskatoon", "S7N 0Y7", "Saskatchewan")
    while (True):
        pass
