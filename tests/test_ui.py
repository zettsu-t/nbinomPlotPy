"""
Testing the UI
"""

import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from seleniumbase import BaseCase


class TestUI(BaseCase):
    """Testing the UI"""

    def test_basic(self):
        """Open a page and select an item"""
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)
        driver.get("http://localhost:8501")

        time.sleep(5)
        driver.save_screenshot("screen_shot_initial.png")
        item = WebDriverWait(driver, 20).until(expected_conditions.element_to_be_clickable(
            (By.XPATH, "/html/body/div/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[6]/div/div")))
        item.click()

        choises = driver.find_elements(By.XPATH, "/html/body/div/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[6]/div/div/div/div[1]/div[2]/input")[0]
        choises.send_keys(Keys.DOWN)
        choises.send_keys(Keys.DOWN)
        choises.send_keys(Keys.RETURN)

        time.sleep(5)
        driver.save_screenshot("screen_shot_second.png")
        driver.close()


# Describe headless browser testing
if __name__ == "__main__":
    unittest.main()
