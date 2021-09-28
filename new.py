from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time


def options_value(element):
  """get options from dropdown"""
  options = [x.get_attribute("value")
             for x in element.find_elements_by_tag_name("option")]
  return options


def check_page(button):
  dropdown = WebDriverWait(driver, 2).until(
      EC.presence_of_element_located((By.XPATH, "//button[@data-id='"+button+"']")))
  if dropdown:
    pass
  else:
    driver.switch_to.default_content()
    driver.refresh()
    iframe = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
    driver.switch_to.frame(iframe)


def dropdown_selection(button, value):
  """change dropdown option"""
  check_page(button)
  driver.find_element_by_xpath("//button[@data-id='"+button+"']").click()
  time.sleep(1)
  driver.find_element_by_xpath(
      "//div[@class='bs-container btn-group bootstrap-select open']//ul/li[@data-original-index='"+value+"']/a").click()


PATH = "C:\Program Files (x86)\chromedriver.exe"
url = "https://www.amfiindia.com/research-information/other-data/mf-scheme-performance-details"
driver = webdriver.Chrome(PATH)
driver.get(url)

try:
  # Wait for 10 s at max for the page to load before throwing exception
  iframe = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
  print("Page is ready!")
  # get iframe tage and switch to the website within
  # iframe = driver.find_element_by_tag_name("iframe")
  driver.switch_to.frame(iframe)
  # Get the dropdown element and get the options value using the options_value function
  end_type = driver.find_element_by_id("end-type")
  end_type_options = options_value(end_type)
  primary_category = driver.find_element_by_id("primary-category")
  primary_category_options = options_value(primary_category)
  category = driver.find_element_by_id("category")
  category_options = options_value(category)
  # go_button = driver.find_element_by_xpath(
  #     "//button[@class='btn btn-primary amfi-btn']")
  # download = driver.find_element_by_id("download-report-excel")
  date = driver.find_element_by_id("nav-date")
  date.clear()
  date.send_keys("24/09/2021")
  time.sleep(1)

  driver.switch_to.default_content()
  driver.refresh()
  print("refreshed")
  time.sleep(10)
  print("loaded")
  iframe = WebDriverWait(driver, 50).until(
      EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
  driver.switch_to.frame(iframe)


except TimeoutException:
  print("Page Loading took too much time")


driver.quit()
