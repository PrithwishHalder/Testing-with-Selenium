from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
import os
import glob


def options_value(element):
  """get options from dropdown"""
  options = [x.get_attribute("value")
             for x in element.find_elements_by_tag_name("option")]
  return options


def dropdown_selection(button, value):
  """change dropdown option"""
  driver.find_element_by_xpath("//button[@data-id='" + button + "']").click()
  time.sleep(1)
  category_type = driver.find_element_by_xpath(
      "//div[@class='bs-container btn-group bootstrap-select open']//ul/li[@data-original-index='" + value + "']/a").text
  driver.find_element_by_xpath(
      "//div[@class='bs-container btn-group bootstrap-select open']//ul/li[@data-original-index='" + value + "']/a").click()
  print(category_type)
  return category_type


def download_file():
  rows = driver.find_elements_by_xpath("//*[@id='fund-data']/tbody/tr")
  if len(rows) == 1:
    columns = driver.find_elements_by_xpath("//*[@id='fund-data']/tbody/tr/td")
    if len(columns) == 1:
      print("Data Unavailable")
      return None

  try:
    download = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "download-report-excel")))
    download.click()
    download = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.ID, "download-report-excel")))
  except:
    driver.switch_to.default_content()
    driver.refresh()
    print("reload", driver.current_url)
    time.sleep(5)
    download_file()


PATH = "C:\Program Files (x86)\chromedriver.exe"
url = "https://www.amfiindia.com/research-information/other-data/mf-scheme-performance-details"
DOWNLOAD_PATH = r'C:/Users/halde/Downloads'
SAVE_PATH = "C:/Users/halde/OneDrive/Desktop/CelebalTech/Task6 (Selenium)/Files/"
options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(PATH, options=options)
driver.get(url)

try:
  # Wait for 10 s at max for the page to load before throwing exception
  iframe = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
  print("Page is ready!")
  # get iframe tage and switch to the website within
  driver.switch_to.frame(iframe)
  # Get the dropdown element and get the options value using the options_value function
  end_type = driver.find_element_by_id("end-type")
  end_type_options = options_value(end_type)
  primary_category = driver.find_element_by_id("primary-category")
  primary_category_options = options_value(primary_category)
  category = driver.find_element_by_id("category")
  category_options = options_value(category)
  date = driver.find_element_by_id("nav-date")
  date.clear()
  date.send_keys("24/09/2021")
  time.sleep(2)

  for endType in end_type_options:
    if endType == "":
      pass
    else:
      filename1 = dropdown_selection("end-type", endType)
      filename1 = SAVE_PATH + filename1

      for primaryCategory in primary_category_options:
        if primaryCategory == "":
          pass
        else:
          index = str(primary_category_options.index(primaryCategory))
          filename2 = dropdown_selection("primary-category", index)
          filename2 = filename1 + "_" + filename2
          available_category_options = [
              category for category in category_options if primaryCategory in category]

          for category in available_category_options:
            if category == "":
              pass
            else:
              index = str(category_options.index(category))
              print(index)
              filename3 = dropdown_selection("category", index)
              filename = filename2 + "_" + filename3 + ".xls"
              go_button = WebDriverWait(driver, 10).until(
                  EC.element_to_be_clickable((By.CLASS_NAME, "amfi-btn")))
              go_button.click()
              time.sleep(5)
              download_file()
              files = glob.glob(DOWNLOAD_PATH + "\*.xls")
              print(files)
              file_path = max(files, key=os.path.getctime)
              print(file_path, filename)
              os.rename(file_path, filename)

except TimeoutException:
  print("Page Loading took too much time")

finally:
  driver.quit()
