import allure
from selenium.webdriver.common.by import By


class OrderTrack:
    """Класс для описания окна отслеживания заказа"""

    order_input = (By.XPATH, '//input[@placeholder=""]')

    @allure.step('Инициализация драйвера в объекте OrderTrack')
    def __init__(self, driver):
        self.driver = driver

    @allure.step('Поиск номера заказа')
    def get_order_input(self):
        return self.driver.find_element(*self.order_input)
