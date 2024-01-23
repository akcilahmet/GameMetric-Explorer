from Wait import WaitHelper as Wait_Helper
import UserFunctionAutomation as User_Function
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from datetime import datetime
from DatabaseManager import DatabaseManager as db_manager


class SensorTowerScraper:

    def login(driver, email, password):
        # 'Sign In'
        sign_in_button = Wait_Helper.wait_for_element(driver, By.XPATH, User_Function.SIGN_IN_BUTTON_PATH)
        sign_in_button.click()

        # 'Email'
        email_input = Wait_Helper.wait_for_element(driver, By.XPATH, User_Function.EMAIL_XPATH)
        email_input.send_keys(email)

        Wait_Helper.random_sleep(.3, 1)
        # 'Next-Step'
        next_step = Wait_Helper.wait_for_element(driver, By.XPATH, User_Function.NEXT_STEP_XPATH)
        next_step.click()

        # 'Password'
        password_input = Wait_Helper.wait_for_element(driver, By.XPATH, User_Function.PASSWORD_XPATH)
        password_input.send_keys(password)

        Wait_Helper.random_sleep(.3, 1)

        # 'Next-Step'
        next_step = Wait_Helper.wait_for_element(driver, By.XPATH, User_Function.NEXT_STEP_XPATH)
        next_step.click()

    # user_func model panel
    def user_model_panel(driver):
        try:
            user_func_panel = Wait_Helper.wait_for_element(driver, By.XPATH, User_Function.USER_FUNC_MODEL_PANEL_XPATH,
                                                           3)
            other = Wait_Helper.wait_for_element(driver, By.XPATH, User_Function.USER_FUNC_MODEL_OTHER_BTN_XPATH)
            other.click()
            confirm = Wait_Helper.wait_for_element(driver, By.XPATH, User_Function.USER_FUNC_MODEL_CONFIRM_BTN_XPATH)
            confirm.click()
        except TimeoutException:
            print('Panel not found ')

    def top_charts_games_selected(driver):
        # topcharts login
        topcharts_new = Wait_Helper.wait_for_element(driver, By.XPATH, User_Function.TOP_CHARTS_XPATH)
        topcharts_new.click()

        topcharts = Wait_Helper.wait_for_element(driver, By.XPATH, User_Function.TOP_CHARTS_SELECTER_XPATH)
        topcharts.click()

        Wait_Helper.random_sleep(5, 7)

        # Category
        category_dropdown = Wait_Helper.wait_for_element(driver, By.XPATH, User_Function.GAMES_CATEGORY_XPATH)
        category_dropdown.click()

        # games selected
        games = Wait_Helper.wait_for_element(driver, By.XPATH, User_Function.GAMES_CATEGORY_SELECTED_XPATH)
        games.click()

        # allgames selected
        allgames = Wait_Helper.wait_for_element(driver, By.XPATH, User_Function.ALLGAMES_CATEGORY_SELECTED_XPATH)
        allgames.click()

    def games_scraping(driver):
        global category_first_name
        html_content = driver.page_source

        soup = BeautifulSoup(html_content, 'html.parser')

        games_elements = soup.findAll('td',
                                      class_='MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium TopChartsInfiniteList-module__cellAppCard--pxnBK css-m2jc0v')

        for idx, game_element in enumerate(games_elements, start=1):
            game_link = game_element.find("a", {
                "class": "MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineHover BaseLink-module__link--ZB6lH TopChartsAppCard-module__appName--Dj2Ix css-1c1y066"})

            if game_link:
                game_name_element = game_link.find('span',
                                                   class_='MuiTypography-root MuiTypography-body1 MuiTypography-noWrap css-1wq0212')

                if game_name_element:
                    game_name = game_name_element.text.strip()
                    print(f'{idx}.{game_name}')

                    date_info_text = datetime.now()
                    print(date_info_text)
                    Wait_Helper.random_sleep(.1, .5)

                    game_href = game_link.get("href")
                    if game_href:
                        driver.execute_script("window.open('" + game_href + "', '_blank');")
                        Wait_Helper.random_sleep(1, 2)

                        # new tab
                        new_window_handle = driver.window_handles[-1]  # Son eklenen pencerenin tanımlayıcısını al
                        driver.switch_to.window(new_window_handle)
                        # new tab parse
                        Wait_Helper.random_sleep(1, 2)
                        new_window_html_content = driver.page_source
                        games_window = BeautifulSoup(new_window_html_content, 'html.parser')

                        Wait_Helper.random_sleep(1, 2)

                        # base_staticstic information
                        base_statistic = games_window.findAll('div',
                                                              class_='BaseStatistic-module__statistic--swhHO')
                        game_statistic = games_window.findAll('div',
                                                              class_='MuiGrid-root MuiGrid-item MuiGrid-grid-xs-6 MuiGrid-grid-md-4 css-uvp9to')
                        print("***Statistic Information***")
                        category_statistic = base_statistic[0]

                        download_statistic = game_statistic[0]
                        revenue_download_statistic = game_statistic[1]
                        category_ranking = game_statistic[2]

                        categories_info = category_statistic.findAll('span',
                                                                     class_='MuiTypography-root MuiTypography-body1 css-19d5dex')
                        download_info = download_statistic.find('span',
                                                                class_='MuiTypography-root MuiTypography-h1 BaseLink-module__link--ZB6lH AppOverviewKpiBase-module__value--cP3aS css-audbiy')
                        revenue_info = revenue_download_statistic.find('span',
                                                                       class_='MuiTypography-root MuiTypography-h1 BaseLink-module__link--ZB6lH AppOverviewKpiBase-module__value--cP3aS css-audbiy')
                        category_ranking_info = category_ranking.find('a',
                                                                      class_='MuiTypography-root MuiTypography-h1 MuiLink-root MuiLink-underlineHover BaseLink-module__link--ZB6lH AppOverviewKpiBase-module__value--cP3aS css-1blji8u')

                        my_db_manager = db_manager(
                            host="localhost",
                            user="root",
                            password="171017Aa",
                            database="gameanalyticschema"
                        )

                        for variable in categories_info:
                            category_name = variable.text
                            print(f'{category_name}' if category_name else 'Null')

                        download_text = download_info.text
                        revenue_text = revenue_info.text
                        category_ranking_text = category_ranking_info.text

                        print(f'{download_text}')
                        print(f'{revenue_text}')
                        print(f'{category_ranking_text}')

                        category_first_name=""
                        for i in categories_info:
                            my_db_manager.insert_category(i.text)
                            category_first_name = i.text
                            break
                        my_db_manager.insert_game_metric(
                            game_name,
                            category_first_name,
                            date_info_text,
                            download_text,
                            revenue_text,
                            category_ranking_text
                        )

                        Wait_Helper.random_sleep(1, .3)

                        driver.close()
                        Wait_Helper.random_sleep(1, 3)
                        driver.switch_to.window(driver.window_handles[0])
                        Wait_Helper.random_sleep(1, 3)

                Wait_Helper.random_sleep(.1, 1)
