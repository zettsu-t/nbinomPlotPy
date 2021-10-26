"""
Testing the UI
"""

import unittest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

XPATH_TOP = "/html/body/div/div[1]/div/div/div/div/"
XPATH_SIDEBAR = XPATH_TOP + "section[1]/div[1]/div[2]/div[1]/"
XPATH_SIZE = XPATH_SIDEBAR + "div[1]/div/div/div[1]/div/div"
XPATH_SIZE_VALUE = XPATH_SIZE + "/div"
XPATH_PROB = XPATH_SIDEBAR + "div[2]/div/div/div[1]/div/div"
XPATH_PROB_VALUE = XPATH_PROB + "/div"
XPATH_MU = XPATH_SIDEBAR + "div[3]/div/div[1]/div[1]/div/input"
XPATH_MU_DOWN = XPATH_SIDEBAR + "div[3]/div/div[1]/div[2]/button[1]"
XPATH_MU_UP = XPATH_SIDEBAR + "div[3]/div/div[1]/div[2]/button[2]"
XPATH_FIX_MU = XPATH_SIDEBAR + "div[4]/div/div/label[2]"
XPATH_UPDATE = XPATH_SIDEBAR + "div[5]/div/button"
XPATH_QUANTILES = XPATH_SIDEBAR + "div[6]/div/div"
XPATH_QUANTILE_INPUT = XPATH_QUANTILES + "/div/div[1]/div[2]/input"
XPATH_CHART = XPATH_TOP + "section[2]/div/div[1]/div[2]/div/div/div/img"
XPATH_RESET = XPATH_SIDEBAR + "div[7]/div/button"


class TestUI(unittest.TestCase):
    """Testing the UI"""

    def open_connection(self, url, timeout):
        """Open a page and select an item"""

        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.get(url)

        wait = WebDriverWait(driver, timeout)
        wait.until(EC.visibility_of_element_located((By.XPATH, XPATH_CHART)))
        driver.find_elements(By.XPATH, XPATH_QUANTILES)[0].click()
        driver.save_screenshot("screen_shot_initial.png")
        return driver

    def change_quantile(self, driver, timeout):
        """Select the quantile parameter"""
        wait = WebDriverWait(driver, timeout)

        choises = driver.find_elements(By.XPATH, XPATH_QUANTILE_INPUT)[0]
        choises.send_keys(Keys.DOWN)
        choises.send_keys(Keys.DOWN)
        choises.send_keys(Keys.RETURN)
        wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_QUANTILES)))
        driver.save_screenshot("screen_shot_second.png")

    def change_size(self, driver, timeout):
        """Change the size parameter"""
        wait = WebDriverWait(driver, timeout)

        updated_size = "6.0"
        size_slider = driver.find_elements(By.XPATH, XPATH_SIZE)[0]
        move = ActionChains(driver)
        move.click_and_hold(size_slider).move_by_offset(24, 0)
        move.release().perform()
        wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_SIZE)))
        wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_UPDATE)))
        wait.until(EC.text_to_be_present_in_element(
            (By.XPATH, XPATH_SIZE_VALUE), updated_size))

        size_element = driver.find_elements(By.XPATH, XPATH_SIZE)[0]
        actual_size = size_element.get_attribute("aria-valuenow")
        self.assertAlmostEqual(float(actual_size), float(updated_size))
        size_slider.click()

    def change_prob(self, driver, timeout):
        """Change the prob parameter"""
        wait = WebDriverWait(driver, timeout)

        updated_prob = "0.75"
        prob_slider = driver.find_elements(By.XPATH, XPATH_PROB)[0]
        move = ActionChains(driver)
        move.click_and_hold(prob_slider).move_by_offset(144, 0)
        move.release().perform()
        wait.until(EC.text_to_be_present_in_element(
            (By.XPATH, XPATH_PROB_VALUE), updated_prob))
        wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_PROB)))
        wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_UPDATE)))

        prob_element = driver.find_elements(By.XPATH, XPATH_PROB)[0]
        actual_prob = prob_element.get_attribute("aria-valuenow")
        self.assertAlmostEqual(float(actual_prob), float(updated_prob))
        prob_slider.click()

    def update_by_size(self, driver, timeout):
        """Update by the size parameter"""
        wait = WebDriverWait(driver, timeout)

        old_element = driver.find_elements(By.XPATH, XPATH_MU)[0]
        update_element = driver.find_elements(By.XPATH, XPATH_UPDATE)[0]
        update_element.click()
        wait.until(EC.staleness_of(old_element))

        mu_element = driver.find_elements(By.XPATH, XPATH_MU)[0]
        actual_mu = mu_element.get_attribute("value")
        self.assertAlmostEqual(float(actual_mu), 2.0)

        mu_element_updated = driver.find_elements(By.XPATH, XPATH_MU)[0]
        move = ActionChains(driver)
        move.click_and_hold(mu_element_updated).release().perform()
        wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_MU)))

    def change_mu(self, driver, timeout):
        """Change the mu parameter"""
        wait = WebDriverWait(driver, timeout)

        updated_mu = "7.00"
        mu_element = driver.find_elements(By.XPATH, XPATH_MU)[0]
        driver.execute_script("arguments[0].value = '';", mu_element)

        mu_element.send_keys(updated_mu)
        mu_element.send_keys(Keys.RETURN)
        wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_MU)))
        wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_UPDATE)))
        wait.until(EC.text_to_be_present_in_element_value(
            (By.XPATH, XPATH_MU), updated_mu))

        up_button = driver.find_elements(By.XPATH, XPATH_MU_UP)[0]
        down_button = driver.find_elements(By.XPATH, XPATH_MU_DOWN)[0]
        up_button.click()
        wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_MU_UP)))
        wait.until(EC.text_to_be_present_in_element_value(
            (By.XPATH, XPATH_MU), "8.00"))

        down_button.click()
        wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_MU_DOWN)))
        wait.until(EC.text_to_be_present_in_element_value(
            (By.XPATH, XPATH_MU), "7.00"))

        up_button.click()
        wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_MU_UP)))
        wait.until(EC.text_to_be_present_in_element_value(
            (By.XPATH, XPATH_MU), "8.00"))

        mu_button_element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, XPATH_FIX_MU)))
        mu_button_element.click()
        wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_UPDATE)))

    def update_by_mu(self, driver, timeout):
        """Update by the mu parameter"""
        wait = WebDriverWait(driver, timeout)

        updated_size = "24.0"
        old_element = driver.find_elements(By.XPATH, XPATH_SIZE)[0]
        update_element = driver.find_elements(By.XPATH, XPATH_UPDATE)[0]
        update_element.click()
        wait.until(EC.staleness_of(old_element))
        wait.until(EC.text_to_be_present_in_element(
            (By.XPATH, XPATH_SIZE_VALUE), updated_size))

        size_element_updated = driver.find_elements(By.XPATH, XPATH_SIZE)[0]
        name = "aria-valuenow"
        actual_size_updated = size_element_updated.get_attribute(name)
        self.assertAlmostEqual(float(actual_size_updated), float(updated_size))

    def click_reset(self, driver, timeout):
        """Reset all parameters"""
        wait = WebDriverWait(driver, timeout)

        old_size_element = driver.find_elements(By.XPATH, XPATH_SIZE)[0]
        old_prob_element = driver.find_elements(By.XPATH, XPATH_PROB)[0]
        old_mu_element = driver.find_elements(By.XPATH, XPATH_MU)[0]
        reset_element = driver.find_elements(By.XPATH, XPATH_RESET)[0]
        reset_element.click()
        wait.until(EC.staleness_of(old_size_element))
        wait.until(EC.staleness_of(old_prob_element))
        wait.until(EC.staleness_of(old_mu_element))

        size_element = driver.find_elements(By.XPATH, XPATH_SIZE)[0]
        actual_size = size_element.get_attribute("aria-valuenow")
        self.assertAlmostEqual(float(actual_size), 4.0)

        prob_element = driver.find_elements(By.XPATH, XPATH_PROB)[0]
        actual_prob = prob_element.get_attribute("aria-valuenow")
        self.assertAlmostEqual(float(actual_prob), 0.25)

        mu_element = driver.find_elements(By.XPATH, XPATH_MU)[0]
        actual_mu = mu_element.get_attribute("value")
        self.assertAlmostEqual(float(actual_mu), 12.0)

    def test_basic(self):
        """Walk through all inputs"""
        timeout = 3
        url = "http://localhost:8501"
        driver = self.open_connection(url=url, timeout=timeout)
        self.change_quantile(driver=driver, timeout=timeout)
        self.change_size(driver=driver, timeout=timeout)
        self.change_prob(driver=driver, timeout=timeout)
        self.update_by_size(driver=driver, timeout=timeout)
        self.change_mu(driver=driver, timeout=timeout)
        self.update_by_mu(driver=driver, timeout=timeout)
        self.click_reset(driver=driver, timeout=timeout)
        driver.close()


# Describe headless browser testing
if __name__ == "__main__":
    unittest.main()
