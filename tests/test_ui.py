"""
Testing the UI
"""

import time
import unittest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


class TestUI(unittest.TestCase):
    """Testing the UI"""

    def test_basic(self):
        """Open a page and select an item"""
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.get("http://localhost:8501")

        time.sleep(1)
        driver.save_screenshot("screen_shot_initial.png")
        item = WebDriverWait(driver, 20).until(expected_conditions.element_to_be_clickable(
            (By.XPATH, "/html/body/div/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[6]/div/div")))
        item.click()

        choises = driver.find_elements(By.XPATH, "/html/body/div/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[6]/div/div/div/div[1]/div[2]/input")[0]
        choises.send_keys(Keys.DOWN)
        choises.send_keys(Keys.DOWN)
        choises.send_keys(Keys.RETURN)

        time.sleep(1)
        driver.save_screenshot("screen_shot_second.png")

        size_slider = driver.find_elements(By.XPATH, "/html/body/div/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[1]/div/div/div[1]/div/div")[0]
        move = ActionChains(driver)
        move.click_and_hold(size_slider).move_by_offset(24, 0).release().perform()
        time.sleep(1)

        size_element = driver.find_elements(By.XPATH, "/html/body/div/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[1]/div/div/div[1]/div/div")[0]
        actual_size = size_element.get_attribute("aria-valuenow")
        self.assertAlmostEqual(float(actual_size), 6.0)

        prob_slider = driver.find_elements(By.XPATH, "/html/body/div/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[2]/div/div/div[1]/div/div")[0]
        move = ActionChains(driver)
        move.click_and_hold(prob_slider).move_by_offset(144, 0).release().perform()
        time.sleep(1)

        prob_element = driver.find_elements(By.XPATH, "/html/body/div/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[2]/div/div/div[1]/div/div")[0]
        actual_prob = prob_element.get_attribute("aria-valuenow")
        self.assertAlmostEqual(float(actual_prob), 0.75)

        update_element = driver.find_elements(By.XPATH, "/html/body/div/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[5]/div/button")[0]
        update_element.click()
        time.sleep(1)

        mu_element = driver.find_elements(By.XPATH, "/html/body/div/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[3]/div/div[1]/div[1]/div/input")[0]
        actual_mu = mu_element.get_attribute("value")
        self.assertAlmostEqual(float(actual_mu), 2.0)

        mu_element_updated = driver.find_elements(By.XPATH, "/html/body/div/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[3]/div/div[1]/div[1]/div/input")[0]
        move_mu = ActionChains(driver)
        move_mu.click_and_hold(mu_element_updated).release().perform()
        time.sleep(1)

        driver.execute_script("arguments[0].value = '';", mu_element_updated)
        time.sleep(1)

        mu_element_updated.send_keys("7")
        mu_element_updated.send_keys(Keys.RETURN)
        time.sleep(1)

        up_button = driver.find_elements(By.XPATH, "/html/body/div/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[3]/div/div[1]/div[2]/button[2]")[0]
        down_button = driver.find_elements(By.XPATH, "/html/body/div/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[3]/div/div[1]/div[2]/button[1]")[0]
        up_button.click()
        down_button.click()
        up_button.click()
        time.sleep(1)

        mu_button_element = WebDriverWait(driver, 20).until(expected_conditions.element_to_be_clickable(
            (By.XPATH, "/html/body/div/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[4]/div/div/label[2]")))
        mu_button_element.click()
        time.sleep(1)

        update_element_updated = driver.find_elements(By.XPATH, "/html/body/div/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[5]/div/button")[0]
        update_element_updated.click()
        time.sleep(3)

        size_element_updated = driver.find_elements(By.XPATH, "/html/body/div/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[1]/div/div/div[1]/div/div")[0]
        actual_size_updated = size_element_updated.get_attribute("aria-valuenow")
        self.assertAlmostEqual(float(actual_size_updated), 24.0)

        driver.close()


# Describe headless browser testing
if __name__ == "__main__":
    unittest.main()
