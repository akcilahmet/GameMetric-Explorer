import time
import logging
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

SIGN_IN_BUTTON_PATH = '//*[@id=":rb:"]/span'
EMAIL_XPATH = '//*[@id="email"]'
PASSWORD_XPATH = '//*[@id="password"]'
NEXT_STEP_XPATH = '//*[@id="new_user"]/input[2]'
USER_FUNC_MODEL_PANEL_XPATH = '/html/body/div[6]/div[2]'
USER_FUNC_MODEL_OTHER_BTN_XPATH = '/html/body/div[6]/div[2]/div[2]/div[2]/button[8]'
USER_FUNC_MODEL_CONFIRM_BTN_XPATH = '/html/body/div[6]/div[2]/div[3]/button'
TOP_CHARTS_XPATH = '/html/body/div[3]/div/div[2]/ul[3]/li[1]/span'
TOP_CHARTS_SELECTER_XPATH = '/html/body/div[3]/div/div[2]/ul[3]/li[3]/div/ul[1]/li[1]'
GAMES_CATEGORY_XPATH = '//*[@id="mainContent"]/div[1]/div/div[2]/div/div[4]/div'
GAMES_CATEGORY_SELECTED_XPATH = '//*[@id="menu-"]/div[3]/ul/li[9]'
ALLGAMES_CATEGORY_SELECTED_XPATH = '//*[@id="menu-"]/div[3]/ul/li[10]'

logging.basicConfig(level=logging.INFO)


def wait_for_element(driver, by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by, value)))
def wait_for_elements(driver, by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.visibility_of_all_elements_located((by, value)))


def login(driver, email, password):
    # 'Sign In'
    sign_in_button = wait_for_element(driver, By.XPATH, SIGN_IN_BUTTON_PATH)
    sign_in_button.click()

    # 'Email'
    email_input = wait_for_element(driver, By.XPATH, EMAIL_XPATH)
    email_input.send_keys(email)

    # 'Password'
    password_input = wait_for_element(driver, By.XPATH, PASSWORD_XPATH)
    password_input.send_keys(password)

    # 'Next-Step'
    next_step = wait_for_element(driver, By.XPATH, NEXT_STEP_XPATH)
    next_step.click()


# user_func model panel olma durumuna göre islem secimi
def user_model_panel(driver):
    try:
        ## eger panel yok ise except bloguna gecis yapar
        user_func_panel = wait_for_element(driver, By.XPATH, USER_FUNC_MODEL_PANEL_XPATH, 3)
        other = wait_for_element(driver, By.XPATH, USER_FUNC_MODEL_OTHER_BTN_XPATH)
        other.click()
        confirm = wait_for_element(driver, By.XPATH, USER_FUNC_MODEL_CONFIRM_BTN_XPATH)
        confirm.click()
    except TimeoutException:
        print('Panel not found ')


def top_charts_games_selected(driver):
    # topcharts_new buton icerisinde topcharts kismina giris yapildi

    topcharts_new = wait_for_element(driver, By.XPATH, TOP_CHARTS_XPATH)
    topcharts_new.click()

    topcharts = wait_for_element(driver, By.XPATH, TOP_CHARTS_SELECTER_XPATH)
    topcharts.click()

    # kategorileri games icerisindeki kategorileri bulma islemi
    random_sleep(5, 7)

    # Category dropdown'ını bulana kadar bekle
    category_dropdown = wait_for_element(driver, By.XPATH, GAMES_CATEGORY_XPATH)
    category_dropdown.click()

    # games selected
    games = wait_for_element(driver, By.XPATH, GAMES_CATEGORY_SELECTED_XPATH)
    games.click()

    # allgames selected
    allgames = wait_for_element(driver, By.XPATH, ALLGAMES_CATEGORY_SELECTED_XPATH)
    allgames.click()


#todo Objenin kendısını al sonra butona iniş yap. ID wlerine göre de alınabilir . Açılan yeni sayfadaki html veriyi al geç
def games_scraping(driver):
    html_content = driver.page_source

    soup = BeautifulSoup(html_content, 'html.parser')

    games_elements= soup.findAll('td',
                                    class_='MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium TopChartsInfiniteList-module__cellAppCard--pxnBK css-m2jc0v')


    # buttons = wait_for_elements(driver, By.CSS_SELECTOR,
    #                             '.MuiTypography-root.MuiTypography-body1.MuiTypography-noWrap.css-1wq0212')


    for idx, game_element in enumerate(games_elements, start=1):
        # Her bir öğenin içindeki 'a' etiketini seç
        game_link = game_element.find("a", {
            "class": "MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineHover BaseLink-module__link--ZB6lH TopChartsAppCard-module__appName--Dj2Ix css-1c1y066"})

        if game_link:
            # 'a' etiketinin içindeki 'span' etiketini seç
            game_name_element = game_link.find('span', class_='MuiTypography-root MuiTypography-body1 MuiTypography-noWrap css-1wq0212')

            if game_name_element:
                # Oyun adını al
                game_name = game_name_element.text.strip()
                print(f'{idx}.{game_name}')
                random_sleep(.1, .5)

                game_href = game_link.get("href")
                if game_href:
                    driver.execute_script("window.open('" + game_href + "', '_blank');")
                    random_sleep(1, 2)

            random_sleep(.1, 1)


    # for btn in buttons:
    #     btn.click()
    #     random_sleep(2,4)
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")






def random_sleep(min, max):
    random_sleep_duration = random.uniform(min, max)
    time.sleep(random_sleep_duration)


if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome()
    driver.set_window_size(1920, 1080)
    url = 'https://app.sensortower.com/'
    driver.get(url)

    login(driver, 'kerimoglumuzikhol@gmail.com', '171017Aa')
    user_model_panel(driver)
    top_charts_games_selected(driver)

    random_sleep_duration = random.uniform(3, 5)
    time.sleep(random_sleep_duration)

    games_scraping(driver)

input("Tarayıcıyı kapatmak için bir tuşa basın.")

# Tarayıcıyı kapat
driver.quit()
