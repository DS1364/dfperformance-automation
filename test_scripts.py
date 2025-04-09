import time
import pytest
import allure
from allure_commons.types import AttachmentType, Severity
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

# Fixture to set up and tear down the WebDriver
@pytest.fixture(scope="module")
def setup():
    opt = Options()
    opt.add_experimental_option("debuggerAddress", "localhost:9014")  # Connect to existing Chrome instance
    # Add CI-friendly options
    opt.add_argument("--no-sandbox")  # Required for CI environments
    opt.add_argument("--disable-dev-shm-usage")  # Avoid shared memory issues in CI
    opt.add_argument("--disable-gpu")  # Helps with headless stability
    opt.add_argument("--window-size=1920,1080")  # Ensure proper rendering
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opt)
    wait = WebDriverWait(driver, 30)
    yield driver, wait
    driver.quit()

# Helper Functions (Steps)
@allure.step("Open the website")
def open_website(driver, wait):
    driver.get("https://dfperformance.azurewebsites.net")
    # Wait for the page to load
    wait.until(EC.title_contains("Datafortune"))  # Adjust based on your page's title
    allure.attach(driver.get_screenshot_as_png(), name="website_opened", attachment_type=AttachmentType.PNG)
    return "Page loaded successfully"

@allure.step("Sign in with Microsoft")
def sign_in_to_dashboard(driver, wait):
    sign_in_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn loginButton')]"))
    )
    sign_in_button.click()
    # Wait for dashboard URL and a dashboard-specific element
    wait.until(EC.url_contains("dashboard"))
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Dashboard')]")))  # Adjust XPath
    allure.attach(driver.get_screenshot_as_png(), name="dashboard_loaded", attachment_type=AttachmentType.PNG)
    return "Dashboard page loaded"

@allure.step("Click Dashboard button")
def click_dashboard_button(driver, wait):
    button_xpath = "/html/body/ngx-app/ngx-pages/ngx-one-column-layout/nb-layout/div/div/div/nb-sidebar/div/div/nb-menu/ul/li[3]/a"
    button = wait.until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
    button.click()
    wait.until(EC.url_contains("dashboard"))
    allure.attach(driver.get_screenshot_as_png(), name="dashboard_button_clicked", attachment_type=AttachmentType.PNG)
    return "Dashboard button clicked"

@allure.step("Click user profile")
def click_user_profile(driver, wait):
    user_name_element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "user-name")))
    user_name_element.click()
    allure.attach(driver.get_screenshot_as_png(), name="user_profile_clicked", attachment_type=AttachmentType.PNG)
    return "User profile clicked"

@allure.step("Select profile from dropdown")
def select_profile(driver, wait):
    profile_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='cdk-overlay-0']/nb-context-menu/nb-menu/ul/li[1]/a")))
    profile_option.click()
    allure.attach(driver.get_screenshot_as_png(), name="profile_selected", attachment_type=AttachmentType.PNG)
    return "Profile selected"

@allure.step("Verify profile detail")
def verify_profile_detail(driver, wait, field, xpath, expected):
    element = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
    assert expected in element.text, f"{field} mismatch: Expected '{expected}', got '{element.text}'"
    return f"{field} verified: {element.text}"

@allure.step("Click Assign Skills button")
def click_assign_skills_button(driver, wait):
    click_user_profile(driver, wait)
    assign_skills_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='cdk-overlay-0']/nb-context-menu/nb-menu/ul/li[2]/a")))
    assign_skills_button.click()
    allure.attach(driver.get_screenshot_as_png(), name="assign_skills_clicked", attachment_type=AttachmentType.PNG)
    return "Assign Skills button clicked"

@allure.step("Click Add Skills button")
def click_add_skills_button(driver, wait):
    add_skills_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/ngx-app/ngx-pages/ngx-one-column-layout/nb-layout/div[1]/div/div/div/div/nb-layout-column/assign-skills/div/div/div[2]/nb-card/nb-card-header/button")))
    add_skills_button.click()
    allure.attach(driver.get_screenshot_as_png(), name="add_skills_clicked", attachment_type=AttachmentType.PNG)
    return "Add Skills button clicked"

@allure.step("Select category")
def select_category(driver, wait):
    category_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#cdk-overlay-1 > nb-dialog-container > nb-card > nb-card-body > form > div:nth-child(1) > div:nth-child(1) > nb-select > button")))
    category_button.click()
    category_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#nb-option-1")))
    category_option.click()
    allure.attach(driver.get_screenshot_as_png(), name="category_selected", attachment_type=AttachmentType.PNG)
    return "Category selected"

@allure.step("Select skill")
def select_skill(driver, wait):
    skill_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='cdk-overlay-1']/nb-dialog-container/nb-card/nb-card-body/form/div[1]/div[2]/nb-select/button")))
    skill_button.click()
    skill_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#nb-option-9")))
    skill_option.click()
    allure.attach(driver.get_screenshot_as_png(), name="skill_selected", attachment_type=AttachmentType.PNG)
    return "Skill selected"

@allure.step("Fill experience")
def fill_experience(driver, wait):
    experience_label = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='cdk-overlay-1']/nb-dialog-container/nb-card/nb-card-body/form/div[2]/div[1]/input")))
    experience_label.clear()
    experience_label.send_keys("1")
    allure.attach(driver.get_screenshot_as_png(), name="experience_filled", attachment_type=AttachmentType.PNG)
    return "Experience filled"

@allure.step("Fill Version")
def fill_version(driver, wait):
    version_label = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#cdk-overlay-1 > nb-dialog-container > nb-card > nb-card-body > form > div:nth-child(2) > div:nth-child(2) > input")))
    version_label.clear()
    version_label.send_keys("1")
    allure.attach(driver.get_screenshot_as_png(), name="version_filled", attachment_type=AttachmentType.PNG)
    return "Version filled"

@allure.step("Fill description")
def fill_description(driver, wait):
    description_label = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#cdk-overlay-1 > nb-dialog-container > nb-card > nb-card-body > form > div:nth-child(3) > div > textarea")))
    description_label.clear()
    description_label.send_keys("Manual input description.")
    allure.attach(driver.get_screenshot_as_png(), name="description_filled", attachment_type=AttachmentType.PNG)
    return "Description filled"

@allure.step("Submit form")
def submit_form(driver, wait):
    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='cdk-overlay-1']/nb-dialog-container/nb-card/nb-card-footer/button[2]")))
    submit_button.click()
    allure.attach(driver.get_screenshot_as_png(), name="form_submitted", attachment_type=AttachmentType.PNG)
    return "Form submitted"

@allure.step("Click Self Evaluation button")
def click_self_evaluation_button(driver, wait):
    self_evaluation_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/ngx-app/ngx-pages/ngx-one-column-layout/nb-layout/div[1]/div/div/nb-sidebar/div/div/nb-menu/ul/li[4]/a")))
    self_evaluation_button.click()
    allure.attach(driver.get_screenshot_as_png(), name="self_evaluation_clicked", attachment_type=AttachmentType.PNG)
    return "Self Evaluation button clicked"

@allure.step("Open calendar dropdown")
def open_calendar_dropdown(driver, wait):
    calendar_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/ngx-app/ngx-pages/ngx-one-column-layout/nb-layout/div[1]/div/div/div/div/nb-layout-column/user-kra/div/div/div[1]/nb-select/button")))
    calendar_button.click()
    allure.attach(driver.get_screenshot_as_png(), name="calendar_opened", attachment_type=AttachmentType.PNG)
    return "Calendar dropdown opened"

@allure.step("Select calendar option")
def select_calendar_option(driver, wait):
    calendar_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='nb-option-2']")))
    calendar_option.click()
    allure.attach(driver.get_screenshot_as_png(), name="calendar_option_selected", attachment_type=AttachmentType.PNG)
    return "Calendar option selected"

@allure.step("Click calendar date")
def click_calendar_date(driver, wait):
    date_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/ngx-app/ngx-pages/ngx-one-column-layout/nb-layout/div[1]/div/div/div/div/nb-layout-column/user-kra/div/div/div[1]/div/span[1]")))
    date_button.click()
    allure.attach(driver.get_screenshot_as_png(), name="calendar_date_clicked", attachment_type=AttachmentType.PNG)
    return "Calendar date clicked"

@allure.step("Scroll to Achievements")
def scroll_to_achievements(driver, wait):
    achievements_element = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/ngx-app/ngx-pages/ngx-one-column-layout/nb-layout/div[1]/div/div/div/div/nb-layout-column/user-kra/div/div/div[2]/div[1]/td/div")))
    ActionChains(driver).move_to_element(achievements_element).perform()
    allure.attach(driver.get_screenshot_as_png(), name="achievements_scrolled", attachment_type=AttachmentType.PNG)
    return "Scrolled to Achievements"

@allure.step("Locate Manager Summary")
def locate_manager_summary(driver, wait):
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/ngx-app/ngx-pages/ngx-one-column-layout/nb-layout/div[1]/div/div/div/div/nb-layout-column/user-kra/div/div/div[2]/div[2]/td/div/label")))
    allure.attach(driver.get_screenshot_as_png(), name="manager_summary_located", attachment_type=AttachmentType.PNG)
    return "Manager Summary located"

@allure.step("Edit skill")
def edit_skill(driver, wait):
    click_assign_skills_button(driver, wait)
    edit_skill_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/ngx-app/ngx-pages/ngx-one-column-layout/nb-layout/div[1]/div/div/div/div/nb-layout-column/assign-skills/div/div/div[2]/nb-card/nb-card-body/div/nb-list/nb-list-item[1]/div/span[2]/span")))
    # edit_skill_button.click()  # Uncomment if edit involves interaction
    allure.attach(driver.get_screenshot_as_png(), name="skill_edited", attachment_type=AttachmentType.PNG)
    return "Skill edited"

@allure.step("Remove skill")
def remove_skill(driver, wait):
    remove_skill_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/ngx-app/ngx-pages/ngx-one-column-layout/nb-layout/div[1]/div/div/div/div/nb-layout-column/assign-skills/div/div/div[2]/nb-card/nb-card-body/div[1]/nb-list/nb-list-item[1]/div/span[3]/span")))
    remove_skill_button.click()
    allure.attach(driver.get_screenshot_as_png(), name="skill_removed", attachment_type=AttachmentType.PNG)
    return "Skill removed"

@allure.step("Accept skill")
def accept_skill(driver, wait):
    accept_skill_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/ngx-app/ngx-pages/ngx-one-column-layout/nb-layout/div[Requires: sign_in_to_dashboard]1]/div/div/div/div/nb-layout-column/assign-skills/div/div/div[2]/nb-card/nb-card-body/div[1]/nb-list/nb-list-item[1]/div/span[4]/span/span")))
    accept_skill_button.click()
    allure.attach(driver.get_screenshot_as_png(), name="skill_accepted", attachment_type=AttachmentType.PNG)
    return "Skill accepted"

# Test Cases
@allure.title("Test 1: Open website")
@allure.description("Verifies the website opens successfully.")
@allure.severity(Severity.BLOCKER)
def test_open_website(setup):
    driver, wait = setup
    result = open_website(driver, wait)
    print(result)

@allure.title("Test 2: Sign in to dashboard")
@allure.description("Tests signing in with Microsoft and navigating to dashboard.")
@allure.severity(Severity.BLOCKER)
def test_sign_in_to_dashboard(setup):
    driver, wait = setup
    open_website(driver, wait)
    result = sign_in_to_dashboard(driver, wait)
    print(result)

@allure.title("Test 3: Click Dashboard button")
@allure.description("Verifies clicking the Dashboard button.")
@allure.severity(Severity.CRITICAL)
def test_click_dashboard_button(setup):
    driver, wait = setup
    open_website(driver, wait)
    sign_in_to_dashboard(driver, wait)
    result = click_dashboard_button(driver, wait)
    print(result)

@allure.title("Test 4: Click user profile")
@allure.description("Tests clicking the user profile dropdown.")
@allure.severity(Severity.CRITICAL)
def test_click_user_profile(setup):
    driver, wait = setup
    open_website(driver, wait)
    sign_in_to_dashboard(driver, wait)
    result = click_user_profile(driver, wait)
    print(result)

@allure.title("Test 5: Select profile")
@allure.description("Verifies selecting the profile from the dropdown.")
@allure.severity(Severity.CRITICAL)
def test_select_profile(setup):
    driver, wait = setup
    open_website(driver, wait)
    sign_in_to_dashboard(driver, wait)
    click_user_profile(driver, wait)
    result = select_profile(driver, wait)
    print(result)

@allure.title("Test 6: Verify profile name")
@allure.description("Checks if the profile name matches the expected value.")
@allure.severity(Severity.NORMAL)
def test_verify_profile_name(setup):
    driver, wait = setup
    open_website(driver, wait)
    sign_in_to_dashboard(driver, wait)
    click_user_profile(driver, wait)
    select_profile(driver, wait)
    result = verify_profile_detail(driver, wait, "Name", "//p[span[contains(text(),'Name:')]]", "Pratik Wavhal")
    print(result)

@allure.title("Test 7: Verify profile email")
@allure.description("Checks if the profile email matches the expected value.")
@allure.severity(Severity.NORMAL)
def test_verify_profile_email(setup):
    driver, wait = setup
    open_website(driver, wait)
    sign_in_to_dashboard(driver, wait)
    click_user_profile(driver, wait)
    select