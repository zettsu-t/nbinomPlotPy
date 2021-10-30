"""
Testing the UI
"""

import glob
import os
import subprocess
import tempfile
import time
import unittest
import cv2

# export USE_HEADLESS_BROWSER=1
# and this uses a headless mode (for local)
# instead of Xvfb (for GitHub Actions)
USE_HEADLESS_BROWSER = os.environ.get("USE_HEADLESS_BROWSER") is not None
if not USE_HEADLESS_BROWSER:
    import matplotlib
    # Write this here before importing Selenium and have Pylint ignore this
    matplotlib.use('TKAgg')

import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import nb_plot_streamlit.ui


XPATH_TOP = '/html/body/div/div[1]/div/div/div/div/'
XPATH_SIDEBAR = XPATH_TOP + 'section[1]/div[1]/div[2]/div[1]/'
XPATH_SIZE = XPATH_SIDEBAR + 'div[1]/div/div/div[1]/div/div'
XPATH_SIZE_VALUE = XPATH_SIZE + '/div'
XPATH_PROB = XPATH_SIDEBAR + 'div[2]/div/div/div[1]/div/div'
XPATH_PROB_VALUE = XPATH_PROB + '/div'
XPATH_MU = XPATH_SIDEBAR + 'div[3]/div/div[1]/div[1]/div/input'
XPATH_MU_DOWN = XPATH_SIDEBAR + 'div[3]/div/div[1]/div[2]/button[1]'
XPATH_MU_UP = XPATH_SIDEBAR + 'div[3]/div/div[1]/div[2]/button[2]'
XPATH_FIX_MU = XPATH_SIDEBAR + 'div[4]/div/div/label[2]'
XPATH_UPDATE = XPATH_SIDEBAR + 'div[5]/div/button'
XPATH_QUANTILES = XPATH_SIDEBAR + 'div[6]/div/div'
XPATH_QUANTILE_INPUT = XPATH_QUANTILES + '/div/div[1]/div[2]/input'
XPATH_CHART = XPATH_TOP + 'section[2]/div/div[1]/div[2]/div/div/div/img'
XPATH_RESET = XPATH_SIDEBAR + 'div[7]/div/button'
XPATH_DOWNLOAD = XPATH_TOP + 'section[2]/div/div[1]/div[3]/div/button'
XPATH_CHART_SRC = XPATH_TOP + 'section[2]/div/div[1]/div[1]'

EXPECTED_SNAPSHOTS = "tests/data/*.png"
SNAPSHOT_DIR = "tests/snapshots"
SNAPSHOT_FILENAME_INITIAL = "screen_shot_initial.png"
SNAPSHOT_FILENAME_QUANTILE2 = "screen_shot_quantile2.png"
SNAPSHOT_FILENAME_QUANTILE3 = "screen_shot_quantile3.png"


def is_process_alive(proc_name):
    """Check if a process is alive"""

    command = f"ps aux | egrep -v grep | egrep -e \\\\b{proc_name}\\\\b"
    result = subprocess.run(command, shell=True, check=False).returncode
    return result == 0


def open_driver(mode, download_dir):
    """Open a headless browser"""

    options = Options()
    options.add_argument(mode)

    # https://sqa.stackexchange.com/questions/2197/
    # how-to-download-a-file-using-seleniums-webdriver
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting",
                           False)
    options.set_preference("browser.download.dir", download_dir)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk",
                           nb_plot_streamlit.ui.DEFAULT_CSV_MIME)
    return webdriver.Firefox(options=options)


def open_connection(url, timeout, download_dir, snapshot_dir):
    """Open a page and select an item"""

    driver = None
    if not is_process_alive("Xvfb"):
        raise ProcessLookupError("No Xvfb process found")

    if USE_HEADLESS_BROWSER:
        driver = open_driver(mode="--headless", download_dir=download_dir)
    else:
        driver = open_driver(mode="--xvfb", download_dir=download_dir)
    driver.get(url)

    wait = WebDriverWait(driver, timeout)
    wait.until(EC.visibility_of_element_located((By.XPATH, XPATH_CHART)))
    driver.find_elements(By.XPATH, XPATH_CHART)[0].click()

    time.sleep(1)
    snapshot_filename = os.path.join(snapshot_dir, SNAPSHOT_FILENAME_INITIAL)
    driver.save_screenshot(snapshot_filename)

    driver.find_elements(By.XPATH, XPATH_QUANTILES)[0].click()

    return driver


def wait_until_changes(element, key, old_value, timesec):
    """Wait until an attribute of an HTML tag is updated"""

    for _ in range(timesec):
        new_value = element.get_attribute(key)
        if not new_value == old_value:
            break
        time.sleep(1)


def change_quantile(driver, timeout):
    """Select the quantile parameter"""

    key = "src"
    element = driver.find_elements(By.XPATH, XPATH_CHART_SRC)[0]
    old_value = element.get_attribute(key)
    choises = driver.find_elements(By.XPATH, XPATH_QUANTILE_INPUT)[0]
    choises.click()
    choises.send_keys(Keys.DOWN)
    choises.send_keys(Keys.RETURN)
    element.click()
    wait_until_changes(element=element, key=key, old_value=old_value,
                       timesec=timeout)


class TestUI(unittest.TestCase):
    """Testing the UI"""

    def compare_snapshots(self, snapshot_dir):
        """Compare shapshots"""

        filenames = glob.glob(EXPECTED_SNAPSHOTS)
        self.assertTrue(len(filenames) > 0)
        for filename in filenames:
            expected = cv2.imread(filename)
            out_filename = os.path.join(
                snapshot_dir, os.path.basename(filename))
            actual = cv2.imread(out_filename)
            self.assertTrue(np.array_equal(actual, expected))

    def change_quantile_set(self, driver, timeout, download_dir, snapshot_dir):
        """Change the quantile parameter"""

        self.click_download(driver=driver, timeout=timeout, n_rows=34,
                            download_dir=download_dir)

        change_quantile(driver=driver, timeout=timeout)

        snapshot_filename = os.path.join(
            snapshot_dir, SNAPSHOT_FILENAME_QUANTILE2)
        driver.save_screenshot(snapshot_filename)
        self.click_download(driver=driver, timeout=timeout, n_rows=44,
                            download_dir=download_dir)

        change_quantile(driver=driver, timeout=timeout)
        snapshot_filename = os.path.join(
            snapshot_dir, SNAPSHOT_FILENAME_QUANTILE3)
        driver.save_screenshot(snapshot_filename)
        self.click_download(driver=driver, timeout=timeout, n_rows=54,
                            download_dir=download_dir)

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

    def update_by_size(self, driver, timeout, expected_mu):
        """Update by the size parameter"""

        wait = WebDriverWait(driver, timeout)

        old_element = driver.find_elements(By.XPATH, XPATH_MU)[0]
        update_element = driver.find_elements(By.XPATH, XPATH_UPDATE)[0]
        update_element.click()
        wait.until(EC.staleness_of(old_element))

        mu_element = driver.find_elements(By.XPATH, XPATH_MU)[0]
        actual_mu = mu_element.get_attribute("value")
        self.assertAlmostEqual(float(actual_mu), expected_mu)

        mu_element_updated = driver.find_elements(By.XPATH, XPATH_MU)[0]
        move = ActionChains(driver)
        move.click_and_hold(mu_element_updated).release().perform()
        wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_MU)))

    def change_mu(self, driver, timeout, expected_mu):
        """Change the mu parameter"""

        wait = WebDriverWait(driver, timeout)

        mu_element = driver.find_elements(By.XPATH, XPATH_MU)[0]
        actual_mu = mu_element.get_attribute("value")
        self.assertAlmostEqual(float(actual_mu), expected_mu)

        updated_mu = "7.00"
        self.assertTrue(np.abs(expected_mu - float(updated_mu)) > 0.5)
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

    def click_download(self, driver, timeout, n_rows, download_dir):
        """Reset all parameters"""

        wait = WebDriverWait(driver, timeout)
        wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_DOWNLOAD)))
        driver.find_elements(By.XPATH, XPATH_DOWNLOAD)[0].click()
        df_filename = os.path.join(download_dir,
                                   nb_plot_streamlit.ui.DEFAULT_CSV_FILENAME)
        df = pd.read_csv(df_filename)
        os.remove(df_filename)

        # Pylint reports false positive
        self.assertAlmostEqual(df.shape[0], n_rows)
        self.assertAlmostEqual(df.shape[1], 2)

    def test_basic(self):
        """Walk through all inputs"""

        if not is_process_alive("streamlit"):
            raise ProcessLookupError("No Streamlit server found")

        timeout = 30
        url = "http://localhost:8501"
        with tempfile.TemporaryDirectory() as temp_dir:
            snapshot_dir = SNAPSHOT_DIR
            os.makedirs(snapshot_dir, exist_ok=True)
            driver = open_connection(url=url, timeout=timeout,
                                     download_dir=temp_dir,
                                     snapshot_dir=snapshot_dir)
            self.change_quantile_set(driver=driver, timeout=timeout,
                                     download_dir=temp_dir,
                                     snapshot_dir=snapshot_dir)

            # export GITHUB_ACTIONS=1
            # and it skip the check below
            if os.environ.get("GITHUB_ACTIONS") is None:
                self.compare_snapshots(snapshot_dir)

        self.change_size(driver=driver, timeout=timeout)
        self.change_prob(driver=driver, timeout=timeout)

        expected_mu = 2.0
        self.update_by_size(driver=driver, timeout=timeout,
                            expected_mu=expected_mu)
        self.change_mu(driver=driver, timeout=timeout,
                       expected_mu=expected_mu)

        self.update_by_mu(driver=driver, timeout=timeout)
        self.click_reset(driver=driver, timeout=timeout)
        driver.close()


if __name__ == "__main__":
    unittest.main()
