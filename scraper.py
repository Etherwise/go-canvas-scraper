import time
import random
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# ─── Helpers ──────────────────────────────────────────────────────────────

def random_delay(min_s=0.5, max_s=1.5):
    """Sleep for a random interval between actions to simulate human pauses."""
    delay = random.uniform(min_s, max_s)
    logging.info(f"Sleeping for {delay:.2f}s to simulate human delay.")
    time.sleep(delay)


def human_typing(element, text, min_delay=0.1, max_delay=0.3):
    """Type text one char at a time with a small random delay."""
    logging.info(f"Starting human typing of text: '{text}'")
    for ch in text:
        element.send_keys(ch)
        char_delay = random.uniform(min_delay, max_delay)
        logging.debug(f"Typed '{ch}', waiting {char_delay:.2f}s before next char.")
        time.sleep(char_delay)
    logging.info("Finished human typing.")


def click_with_delay(driver, css_selector, wait_time=10, pre_delay=(0.5,1.0), post_delay=(0.5,1.0)):
    """
    Wait for element located by CSS selector, scroll into view, click it,
    with random delays before and after.
    """
    logging.info(f"Preparing to click element: {css_selector}")
    random_delay(*pre_delay)
    el = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
    )
    logging.debug(f"Element found and clickable: {css_selector}")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
    logging.info(f"Scrolled into view: {css_selector}")
    random_delay(0.2, 0.5)
    el.click()
    logging.info(f"Clicked element: {css_selector}")
    random_delay(*post_delay)

# ─── Main Flow ─────────────────────────────────────────────────────────────

def run_scrape():
    logging.info("Starting browser setup.")
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # 1. Navigate to login page
        login_url = "https://www.gocanvas.com/login"
        logging.info(f"Navigating to {login_url}")
        driver.get(login_url)
        random_delay(1, 2)

        # 2. Enter email
        logging.info("Waiting for email input field.")
        email_el = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#login"))
        )
        human_typing(email_el, "development@the-resources-group.com")
        random_delay(0.5, 1.5)

        # 3. Enter password
        logging.info("Locating password field.")
        pwd_el = driver.find_element(By.CSS_SELECTOR, "#password")
        human_typing(pwd_el, "JKR791w!", min_delay=0.2, max_delay=0.4)
        random_delay(0.5, 1.5)

        # 4. Click login button
        login_btn_selector = "#btn_Log\\ In"
        logging.info("Clicking login button.")
        click_with_delay(driver, login_btn_selector, wait_time=10)
        logging.info("Login button clicked, waiting for post-login page.")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
        )
        random_delay(1, 2)

        # 5. Open dropdown menu
        dropdown_selector = "nav.nav--scrollable div.navigation-item > div.item--label"
        logging.info("Opening dropdown menu.")
        click_with_delay(driver, dropdown_selector)

        # 6. Click 3rd submenu item
        submenu_selector = "nav.nav--scrollable div.nav--sub-wrap > a:nth-child(3) > div"
        logging.info("Clicking 3rd submenu item.")
        click_with_delay(driver, submenu_selector)

        # 7. Click link in 3rd table row
        row_link_selector = "tr:nth-child(3) > td:nth-child(1) > div > a"
        logging.info("Clicking link in 3rd table row.")
        click_with_delay(driver, row_link_selector)

        # 8. Click final ibox-title link
        final_link_selector = "div.ibox-title.no-borders > a"
        logging.info("Clicking final ibox-title link.")
        click_with_delay(driver, final_link_selector)

        logging.info("Navigation complete.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise
    finally:
        logging.info("Closing browser.")
        random_delay(1, 2)
        driver.quit()
