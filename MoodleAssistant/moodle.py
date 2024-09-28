import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Import for handling exceptions
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementClickInterceptedException,
    ElementNotInteractableException
)

# Import webdriver_manager for automatic driver management
from webdriver_manager.chrome import ChromeDriverManager

# Define URLs
LOGIN_LINK = 'https://edu.mmcs.sfedu.ru/login/index.php'
ASSIGN_OPTIONS = 'https://edu.mmcs.sfedu.ru/course/modedit.php?update={0}&return=1'
DOWNLOAD_ANSWERS = 'https://edu.mmcs.sfedu.ru/mod/assign/view.php?id={0}&group={1}&action=downloadall'
DOWNLOAD_GRADES = 'https://edu.mmcs.sfedu.ru/mod/assign/view.php?id={0}&group={1}&plugin=offline&pluginsubtype=assignfeedback&action=viewpluginpage&pluginaction=downloadgrades'
UPLOAD_GRADES = 'https://edu.mmcs.sfedu.ru/mod/assign/view.php?id={0}&plugin=offline&pluginsubtype=assignfeedback&action=viewpluginpage&pluginaction=uploadgrades'


def setup_driver():
    """
  Sets up the Selenium WebDriver for Chrome using webdriver_manager to handle driver downloads.

  :return: Configured Selenium WebDriver instance
  """
    # Initialize Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')  # Start browser maximized
    options.add_argument('--disable-infobars')  # Disable infobars
    options.add_argument('--disable-extensions')  # Disable extensions
    options.add_argument('--disable-gpu')  # Applicable to Windows OS only
    options.add_argument('--no-sandbox')  # Bypass OS security model
    # Uncomment the following line to run Chrome in headless mode
    # options.add_argument('--headless')

    # Setup ChromeDriver using webdriver_manager
    service = ChromeDriverManager().install()

    # Initialize the WebDriver
    driver = webdriver.Chrome(executable_path=service, options=options)

    return driver


def open_login(username=None, password=None, credfile='credentials.json'):
    """
  Logs into the Moodle platform using provided credentials or from a JSON file.

  :param username: Username for login (optional if credfile is provided)
  :param password: Password for login (optional if credfile is provided)
  :param credfile: Path to the JSON file containing credentials
  :return: Selenium WebDriver instance after login
  """
    driver = setup_driver()
    driver.get(LOGIN_LINK)

    # Load credentials from file if not provided
    if username is None or password is None:
        if os.path.isfile(credfile):
            with open(credfile, 'r', encoding='utf-8-sig') as f:
                cred = json.load(f)
                username = cred.get('username')
                password = cred.get('password')
        else:
            driver.quit()
            raise FileNotFoundError("Credentials file not found and username/password not provided.")

    try:
        # Wait until the username field is present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'username'))
        )

        # Find username and password fields and input credentials
        username_field = driver.find_element(By.NAME, 'username')
        password_field = driver.find_element(By.NAME, 'password')

        username_field.clear()
        username_field.send_keys(username)

        password_field.clear()
        password_field.send_keys(password)

        # Click the 'Log in' button
        # The login button might have different selectors; adjust if necessary
        try:
            login_button = driver.find_element(By.ID, 'loginbtn')  # Common ID for Moodle login button
        except NoSuchElementException:
            # Alternative selector if 'loginbtn' ID is not present
            login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Log in')]")

        login_button.click()

        # Optionally, wait until login is successful by checking for a specific element
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'region-main'))  # Adjust as needed
        )

    except TimeoutException:
        driver.quit()
        raise Exception("Login failed or elements not found within the given time.")

    return driver


def find_elements_by_text(element, text):
    """
  Finds all child elements of a given element that contain the specified text.

  :param element: Selenium WebElement to search within
  :param text: Text to search for
  :return: List of WebElements containing the text
  """
    xpath = f".//*[contains(text(), '{text}')]"
    return element.find_elements(By.XPATH, xpath)


def get_open_assigns(driver_instance):
    """
  Retrieves a list of open assignments (without badges) from the main region.

  :param driver_instance: Selenium WebDriver instance
  :return: List of WebElements representing open assignments
  """
    try:
        # Wait until the main region is present
        main_region = WebDriverWait(driver_instance, 10).until(
            EC.presence_of_element_located((By.ID, 'region-main'))
        )

        # Find all elements with class 'assign'
        assigns = main_region.find_elements(By.CLASS_NAME, 'assign')

        # Filter assignments that do not contain elements with class 'badge'
        assigns_open = [assign for assign in assigns if not assign.find_elements(By.CLASS_NAME, 'badge')]

        return assigns_open

    except TimeoutException:
        raise Exception("Main region not found within the given time.")


def get_assignm_id(driver_instance, lesson):
    """
  Retrieves the assignment ID for a given lesson name.

  :param driver_instance: Selenium WebDriver instance
  :param lesson: Name of the lesson to find
  :return: Assignment ID as a string
  """
    assigns_open = get_open_assigns(driver_instance)

    # Filter assignments that contain the specified lesson text
    matching_assigns = [assign for assign in assigns_open if find_elements_by_text(assign, lesson)]

    if not matching_assigns:
        raise ValueError(f"No open assignment found with the lesson name '{lesson}'.")

    # Assuming the first match is the desired one
    assign_id = matching_assigns[0].get_attribute('data-id')

    if not assign_id:
        raise ValueError("Assignment ID not found.")

    return assign_id

def go_to(driver: WebDriver, url: str, timeout: int = 1):
    """
    Navigates the browser to the specified URL.

    :param driver: Selenium WebDriver instance.
    :param url: URL to navigate to.
    :param timeout: Maximum time to wait for the page to load.
    """
    driver.get(url)
    # Optionally, wait until the page is fully loaded by checking the ready state
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        print(f"Navigated to {url}")
    except TimeoutException:
        print(f"Warning: Page at {url} did not load within {timeout} seconds.")


def click_text(driver: WebDriver, text: str):
    """
    Finds and clicks a web element based on its exact visible text or value attribute.

    :param driver: Selenium WebDriver instance.
    :param text: The exact visible text or value of the element to click.
    """
    # Construct the XPath to match either text() or @value
    xpath_exact = f"//*[text()='{text}' or @value='{text}']"

    try:
        # Find the element
        element = driver.find_element(By.XPATH, xpath_exact)

        # Scroll to the element using ActionChains
        ActionChains(driver).move_to_element(element).perform()

        # Click the element
        element.click()

        print(f"Clicked on element with text or value: '{text}'")
    except Exception as e:
        print(f"Failed to click on element with text or value '{text}': {e}")


# Example usage:
if __name__ == "__main__":
    try:
        # Replace with actual username and password or ensure 'credentials.json' is present
        driver = open_login(username="your_username", password="your_password")

        # Example: Get open assignments
        open_assignments = get_open_assigns(driver)
        print(f"Found {len(open_assignments)} open assignments.")

        # Example: Get assignment ID for a specific lesson
        lesson_name = "Introduction to Algorithms"  # Replace with your lesson name
        assign_id = get_assignm_id(driver, lesson_name)
        print(f"Assignment ID for '{lesson_name}': {assign_id}")

        # You can now use assign_id with other URLs as needed
        # For example:
        # download_url = DOWNLOAD_ANSWERS.format(assign_id, group_id)
        # driver.get(download_url)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Always close the driver after operations
        if 'driver' in locals():
            driver.quit()
