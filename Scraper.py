from Wait import WaitHelper as Wait_Helper

import UserFunctionAutomation as User_Function
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

class SensorTowerScraper:

    def login(driver, email, password):
        # 'Sign In'
        sign_in_button = Wait_Helper.wait_for_element(driver, By.XPATH, User_Function.SIGN_IN_BUTTON_PATH)
        sign_in_button.click()

        # 'Email'
        email_input = Wait_Helper.wait_for_element(driver, By.XPATH, User_Function.EMAIL_XPATH)
        email_input.send_keys(email)

        # 'Password'
        password_input = Wait_Helper.wait_for_element(driver, By.XPATH, User_Function.PASSWORD_XPATH)
        password_input.send_keys(password)

        # 'Next-Step'
        next_step = Wait_Helper.wait_for_element(driver, By.XPATH, User_Function.NEXT_STEP_XPATH)
        next_step.click()

    # user_func model panel olma durumuna göre islem secimi
    def user_model_panel(driver):
        try:
            ## eger panel yok ise except bloguna gecis yapar
            user_func_panel = Wait_Helper.wait_for_element(driver, By.XPATH, User_Function.USER_FUNC_MODEL_PANEL_XPATH,
                                                          3)
            other = Wait_Helper.wait_for_element(driver, By.XPATH, User_Function.USER_FUNC_MODEL_OTHER_BTN_XPATH)
            other.click()
            confirm = Wait_Helper.wait_for_element(driver, By.XPATH, User_Function.USER_FUNC_MODEL_CONFIRM_BTN_XPATH)
            confirm.click()
        except TimeoutException:
            print('Panel not found ')

    def top_charts_games_selected(driver):
        # topcharts_new buton icerisinde topcharts kismina giris yapildi

        topcharts_new = Wait_Helper.wait_for_element(driver, By.XPATH, User_Function.TOP_CHARTS_XPATH)
        topcharts_new.click()

        topcharts = Wait_Helper.wait_for_element(driver, By.XPATH, User_Function.TOP_CHARTS_SELECTER_XPATH)
        topcharts.click()

        # kategorileri games icerisindeki kategorileri bulma islemi
        Wait_Helper.random_sleep(5, 7)

        # Category dropdown'ını bulana kadar bekle
        category_dropdown = Wait_Helper.wait_for_element(driver, By.XPATH, User_Function.GAMES_CATEGORY_XPATH)
        category_dropdown.click()

        # games selected
        games = Wait_Helper.wait_for_element(driver, By.XPATH, User_Function.GAMES_CATEGORY_SELECTED_XPATH)
        games.click()

        # allgames selected
        allgames = Wait_Helper.wait_for_element(driver, By.XPATH, User_Function.ALLGAMES_CATEGORY_SELECTED_XPATH)
        allgames.click()

    # todo Objenin kendısını al sonra butona iniş yap. ID wlerine göre de alınabilir . Açılan yeni sayfadaki html veriyi al geç
    def games_scraping(driver):
        html_content = driver.page_source

        soup = BeautifulSoup(html_content, 'html.parser')

        games_elements = soup.findAll('td',
                                      class_='MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium TopChartsInfiniteList-module__cellAppCard--pxnBK css-m2jc0v')

        # buttons = wait_for_elements(driver, By.CSS_SELECTOR,
        #                             '.MuiTypography-root.MuiTypography-body1.MuiTypography-noWrap.css-1wq0212')

        for idx, game_element in enumerate(games_elements, start=1):
            # Her bir öğenin içindeki 'a' etiketini seç
            game_link = game_element.find("a", {
                "class": "MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineHover BaseLink-module__link--ZB6lH TopChartsAppCard-module__appName--Dj2Ix css-1c1y066"})

            if game_link:
                # 'a' etiketinin içindeki 'span' etiketini seç
                game_name_element = game_link.find('span',
                                                   class_='MuiTypography-root MuiTypography-body1 MuiTypography-noWrap css-1wq0212')

                if game_name_element:
                    # Oyun adını al
                    game_name = game_name_element.text.strip()
                    print(f'{idx}.{game_name}')
                    Wait_Helper.random_sleep(.1, .5)

                    game_href = game_link.get("href")
                    if game_href:
                        driver.execute_script("window.open('" + game_href + "', '_blank');")
                        Wait_Helper.random_sleep(1, 2)

                Wait_Helper.random_sleep(.1, 1)