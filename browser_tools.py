import configparser
import logging
import re
import time
from typing import List, Dict

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from utils import load_config_file, setup_logging


def setup_browser() -> webdriver:
    options = Options()

    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-gpu')

    # path to local executable file
    #browser = webdriver.Chrome(executable_path="/Users/rikardfahlstrom/Documents/python_projects/selenium_drivers/chromedriver", options=options)
    browser = webdriver.Remote("http://chrome:4444/wd/hub", DesiredCapabilities.CHROME, options=options)

    logging.info('Browser object created')

    return browser


def download_data(browser: webdriver, configs: configparser.ConfigParser) -> BeautifulSoup:
    browser.get(configs['rekyl_portal']['url'])
    time.sleep(1)

    username = browser.find_element_by_id("username")
    password = browser.find_element_by_css_selector("input[type=password")

    username.send_keys(configs['rekyl_portal']['username'])
    password.send_keys(configs['rekyl_portal']['password'])

    browser.find_element_by_id("button_login_security_low").click()

    time.sleep(3)

    show_errands = Select(browser.find_element_by_name('maxhits'))

    show_errands.select_by_index(10)
    time.sleep(5)
    browser.find_element_by_name('maxhits').send_keys(Keys.RETURN)
    time.sleep(5)

    iframe = browser.find_element_by_id("iframe_workorder")
    browser.switch_to.frame(iframe)
    iframe_source = browser.page_source
    soup = BeautifulSoup(iframe_source, 'html.parser')

    browser.close()
    browser.quit()
    logging.info('Raw data downloaded')

    return soup


def get_table_rows_from_soup(page_soup):
    table = page_soup.find('table')
    table_body = table.find('tbody')

    table_rows = table_body.find_all('tr')  # <tr> define table rows

    return table_rows


def split_row_values_at_colon(row_values):
    updated_row_values = []

    for value in row_values:
        splitted_values = value.split(':')
        for split_value in splitted_values:
            updated_row_values.append(split_value.strip())

    return updated_row_values


def transform_table_rows(all_table_rows) -> List[Dict]:
    all_errands = []

    for table_row in all_table_rows:
        row_values = table_row.find_all('td')  # <td> is table cells
        if len(row_values) > 0:
            row_values = [row_value.text.strip() for row_value in row_values]
            row_values = split_row_values_at_colon(row_values)
            row_values[3] = re.sub(' +', ' ', row_values[3])  # Replace multiple spaces with single
            row_values = [y for x in row_values for y in x.split('\n\n', 1)]
            row_values = list(filter(None, row_values))  # Get rid of empty values

            single_errand_data = {
                'created_date': row_values[0],
                'rekyl_errand_id': row_values[1],
                'errand_status': row_values[2],
                'reporter': row_values[3].title(),
                'apartment': row_values[4].upper(),
                'errand_type': row_values[8],
                'errand_details': row_values[9].replace('\n', ' ').replace('\r', '').strip(),
            }
            all_errands.append(single_errand_data)

    logging.info(f'Raw data transformed, found {len(all_errands)} errands')
    all_errands.reverse()  # Reverse to insert oldest errand first in database

    return all_errands


if __name__ == '__main__':
    setup_logging()
    configs = load_config_file()
    browser = setup_browser()
    soup = download_data(browser, configs)
    all_table_rows = get_table_rows_from_soup(soup)
    all_errands = transform_table_rows(all_table_rows)
    print(all_errands)
