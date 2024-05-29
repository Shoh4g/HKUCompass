import time, json, os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def is_element_present_id(driver, element_id):
    try:
        driver.find_element(By.ID, element_id)
        return True
    except NoSuchElementException:
        return False

def is_element_present_class(driver, class_name):
    try:
        driver.find_element(By.CLASS_NAME, class_name)
        return True
    except NoSuchElementException:
        return False

# Fetches auth bearer token to all the API
def get_bearer_token(driver, logger):
  logger.info('Fetching Bearer Token')
  url = "https://class-planner.hku.hk/"
  driver.get(url)
  token = None
  try:
    WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.TAG_NAME, "input"))
    )
    email_input = driver.find_element(By.TAG_NAME, 'input')
    email_input.send_keys(os.getenv("HKU_USERNAME"))
    email_input.send_keys(Keys.RETURN)
    WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.ID, "passwordInput"))
    )
    pass_input = driver.find_element(By.ID, 'passwordInput')
    pass_input.send_keys(os.getenv("HKU_PASSWORD"))
    pass_input.send_keys(Keys.RETURN)
    flag = is_element_present_class(driver, "MuiDataGrid-columnHeaderTitleContainer")
    while not flag:
      time.sleep(2)
      if (is_element_present_id(driver, 'idSIButton9')):
        driver.find_element(By.ID, 'idSIButton9').click()
        time.sleep(2)
      elif (is_element_present_id(driver, 'idBtn_Back')):
        driver.find_element(By.ID, 'idBtn_Back').click()
        time.sleep(2)
      flag = is_element_present_class(driver, "MuiDataGrid-columnHeaderTitleContainer")
    local = driver.execute_script("return {...localStorage}")
    for key in local:
      local = local[key]
      break
    local = json.loads(local)
    secret = local['secret']
    token = 'Bearer ' + secret
  except Exception as ex:
    logger.error('Error in fetching bearer token: ' + str(ex))
  return token