from Wait import WaitHelper as Wait_Helper
from selenium import webdriver
from Scraper import SensorTowerScraper as STScraper


def start_webdriver():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome()
    driver.set_window_size(1920, 1080)
    return driver

if __name__ == "__main__":

    driver = start_webdriver()
    url = 'https://app.sensortower.com/'
    driver.get(url)

    STScraper.login(driver, 'kerimoglumuzikhol@gmail.com', '171017Aa')
    STScraper.user_model_panel(driver)
    STScraper.top_charts_games_selected(driver)

    Wait_Helper.random_sleep(3,5)

    STScraper.games_scraping(driver)

input("Tarayıcıyı kapatmak için bir tuşa basın.")

# Tarayıcıyı kapat
driver.quit()
