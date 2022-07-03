from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time, logging

# Update the two fields below with the username and password + uncomment
#USERNAME = 
#PASSWORD = 

# This table stores the prefix used for the delete button of each type of contents
TYPE_OF_CONTENTS = ['comments','posts']

# Some global variables that store data on elements displayed on the Reddit website
LOGIN_BUTTON = '/html/body/div[1]/div/div[2]/div[1]/header/div/div[2]/div/div[1]/a[1]'
CONFIRM_DELETE_BUTTON = '/html/body/div[1]/div/div[2]/div[4]/div/div/section/footer/button[2]'
ICON_DELETE = "icon-delete"
MORE_OPTIONS = "[aria-label='more options']"

def main():
    logging.basicConfig(filename='file.log',level = logging.INFO,format = '%(asctime)s:%(levelname)s:%(name)s:%(message)s')
    # Adding some options: headless mode, only capture errors in the log
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--log-level=2")
    
    # We won't load images for performance, we disable notifications
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.default_content_setting_values.notifications": 2
    }
    options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(options=options)

    # Log onto the profile
    driver.get("https://www.reddit.com/")
    login_button = driver.find_element(by=By.XPATH,value=LOGIN_BUTTON)
    login_button.click()
    driver.implicitly_wait(30)
    iframe = driver.find_element(by=By.TAG_NAME,value="iframe")
    driver.switch_to.frame(iframe)
    driver.implicitly_wait(30)
    username_field = driver.find_element(by=By.CSS_SELECTOR,value='#loginUsername')
    username_field.send_keys(USERNAME)
    driver.implicitly_wait(30)
    password_field = driver.find_element(by=By.CSS_SELECTOR,value='#loginPassword')
    password_field.send_keys(PASSWORD)
    driver.implicitly_wait(30)
    password_field.send_keys(Keys.ENTER)
    time.sleep(12)
    
    # Navigate to the profile to get the content type
    for contents in TYPE_OF_CONTENTS:
        logging.info("Navigating to the page to remove this content: "+contents)
        driver.get("https://www.reddit.com/user/"+USERNAME+"/"+contents)
        
        # Scroll all the way to the bottom of the page, in order to load all the contents    
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")
            # If the new height equals the last height, it means we've reached the bottom of the page
            if new_height == last_height:            
                logging.info("Reached the end of the "+contents+" page. Let's now remove the "+contents+"...")
                break
            last_height = new_height
            
        # We scroll back to the top of the page
        back_to_the_top = driver.find_element(by=By.XPATH,value="/html/body")
        driver.execute_script("return arguments[0].scrollIntoView(true);", back_to_the_top)
        
        # We now extract all the <button> tags
        driver.implicitly_wait(30)
        buttons = driver.find_elements(by=By.CSS_SELECTOR,value=MORE_OPTIONS)

        # Loop through the list of buttons...
        if len(buttons) > 0:
            for button in buttons:
                try:
                    button.click()
                    driver.implicitly_wait(5)
                    # Select the trash can button and click it
                    trash_can = driver.find_element(by=By.CLASS_NAME,value=ICON_DELETE)
                    trash_can.click()
                    driver.implicitly_wait(5)
                    # Confirm deletion of the content
                    confirm_delete_button = driver.find_element(by=By.XPATH,value=CONFIRM_DELETE_BUTTON)
                    confirm_delete_button.click()
                    logging.info("Removed " + contents + " " + str(buttons.index(button)))
                    time.sleep(3)
                except Exception as e:
                    logging.info(contents + " not removed: " + str(type(e)))
                    pass    
        else:
            logging.info("No " + contents  + " found.")
    
    logging.info("End of the script.")
    time.sleep(3)
    driver.quit()
if __name__ == "__main__":
    main()
