from selenium.webdriver.common.by import By
import allure
import re
from selenium.webdriver.support import expected_conditions as ec


class PersonalData:
    """ Класс для описания страницы с персональными данными"""

    header = (By.XPATH, '//div[@id="root"]//div[text()="Для кого самокат"]')
    name = (By.XPATH, '//div[@id="root"]//input[@placeholder="* Имя"]')
    surname = (By.XPATH, '//div[@id="root"]//input[@placeholder="* Фамилия"]')
    address = (By.XPATH, '//div[@id="root"]//input[@placeholder="* Адрес: куда привезти заказ"]')
    phone = (By.XPATH, '//div[@id="root"]//input[@placeholder="* Телефон: на него позвонит курьер"]')
    station = (By.XPATH, '//div[@id="root"]//input[@placeholder="* Станция метро"]')
    station_names_list = (By.CLASS_NAME, 'select-search__row')
    next_button = (By.XPATH, '//div[@id="root"]//button[text()="Далее"]')

    @allure.step('Инициализация драйвера в объекте Personal Data')
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    @allure.step('Ждем заголовок страницы ввода песональных данных')
    def find_header(self):
        self.wait.until(ec.visibility_of_element_located(self.header))

    @allure.step('Заполняем поле Имя')
    def fill_name(self, name):
        self.driver.find_element(*self.name).send_keys(name)

    @allure.step('Заполняем поле Фамилия')
    def fill_surname(self, surname):
        self.driver.find_element(*self.surname).send_keys(surname)

    @allure.step('Заполняем поле Адрес')
    def fill_address(self, address):
        self.driver.find_element(*self.address).send_keys(address)

    @allure.step('Заполняем поле Телефон')
    def fill_phone(self, phone):
        self.driver.find_element(*self.phone).send_keys(phone)

    @allure.step('Кликаем на поле ввода станций метро')
    def click_station_input(self):
        self.driver.find_element(*self.station).click()

    @allure.step('Получаем список станций')
    def get_stations(self):
        self.click_station_input()
        return self.driver.find_elements(*self.station_names_list)

    @allure.step('Просматриваем станцию')
    def get_station(self, station):
        station_button = station.find_element(By.XPATH, '//button')
        station_name = station.find_element(By.XPATH, '//div[2]').text
        return station_button, station_name

    @allure.step('Заполняем поле Станция метро')
    def fill_station(self, user_station_name):
        stations = self.get_stations()
        for station in stations:
            self.driver.execute_script('arguments[0].scrollIntoView();', station)
            if station.text == user_station_name:
                station.click()
                break

    @allure.step('Нажимаем кнопку Далее')
    def click_next_button(self):
        self.driver.find_element(*self.next_button).click()


class RentalConditions:
    """ Класс для описания страницы с условиями аренды"""

    header = (By.XPATH, '//div[@id="root"]//div[text()="Про аренду"]')
    data_input = (By.XPATH, '//div[@id="root"]//input[@placeholder="* Когда привезти самокат"]')
    day = (By.CLASS_NAME, 'react-datepicker__day')
    period_dropdown = (By.CLASS_NAME, 'Dropdown-arrow')
    period_dropdown_item = (By.CLASS_NAME, 'Dropdown-option')
    colour_box = (By.XPATH, '//div[text()="Цвет самоката"]/parent::div')
    colour_label = (By.TAG_NAME, 'label')
    colour_check_box = (By.XPATH, '//input[@type="checkbox"]')
    comment = (By.XPATH, '//div[@id="root"]//input[@placeholder="Комментарий для курьера"]')
    order_button = (By.XPATH, '//div/div/div[2]/div[3]//button[text()="Заказать"]')

    @allure.step('Инициализация драйвера в объекте RentalConditions')
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    @allure.step('Ждем заголовок формы ввода параметров аренды')
    def find_header(self):
        self.wait.until(ec.visibility_of_element_located(self.header))

    @allure.step('Ищем поле ввода данных')
    def find_data_input(self):
        return self.driver.find_element(*self.data_input)

    @allure.step('Получаем календарь')
    def get_calendar(self):
        return self.driver.find_elements(*self.day)

    @allure.step('Заполняем дату')
    def fill_data(self, data):
        input_field = self.find_data_input()
        input_field.click()
        calendar = self.get_calendar()
        for day in calendar:
            if day.text == data:
                day.click()
                break

    @allure.step('Выбираем период аренды')
    def find_rental_period_dropdown(self):
        return self.driver.find_element(*self.period_dropdown)

    @allure.step('Получаем список сроков аренды')
    def get_dropdown_items(self):
        return self.driver.find_elements(*self.period_dropdown_item)

    @allure.step('Заполняем период аренды')
    def fill_rental_period(self, period):
        self.find_rental_period_dropdown().click()
        items = self.get_dropdown_items()
        for item in items:
            if item.text == period:
                item.click()
                break

    @allure.step('Получаем окно выбора цвета самоката')
    def get_colour_box(self):
        return self.driver.find_element(*self.colour_box)

    @allure.step('Получаем цвета самоката')
    def get_colour_labels(self, colour_box):
        return colour_box.find_elements(*self.colour_label)

    @allure.step('Получаем чекбокс для выбранного цвета самоката')
    def get_check_box(self, label):
        box_id = label.get_attribute('for')
        return self.driver.find_element(By.ID, box_id)

    @allure.step('Заполняем цвет самоката')
    def fill_colour(self, colour):
        colour_box = self.get_colour_box()
        checkbox_labels = self.get_colour_labels(colour_box)
        for label in checkbox_labels:
            if label.text == colour:
                self.get_check_box(label).click()
                break

    @allure.step('Заполняем комментарий для курьера')
    def fill_comment(self, comment):
        self.driver.find_element(*self.comment).send_keys(comment)

    @allure.step('Нажимаем кнопку Заказать')
    def click_order_button(self):
        self.driver.find_element(*self.order_button).click()


class OrderConsentModal:
    """ Класс для описания модального окна подтверждения заказа"""
    header = (By.XPATH, '//div[text()="Хотите оформить заказ?"]')
    consent_button = (By.XPATH, '//button[text()="Да"]')

    @allure.step('Инициализация драйвера в объекте OrderConsentModal')
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    @allure.step('Ждем заголовок окна подтверждения заказа')
    def find_header(self):
        self.wait.until(ec.visibility_of_element_located(self.header))

    @allure.step('Подтверждение заказа')
    def click_consent_button(self):
        self.driver.find_element(*self.consent_button).click()


class SuccessfulOrderModal:
    """ Класс для описания модального окна Заказ оформлен"""

    header = (By.XPATH,'//div[text()="Заказ оформлен"]')
    order_information = (By.XPATH, '//div[contains(text(), "Номер заказа")]')
    check_status_button = (By.XPATH, '//button[text()="Посмотреть статус"]')

    @allure.step('Инициализация драйвера для объекта SuccessfulOrderModal')
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    @allure.step('Ждем заголовок модального окна номера заказа')
    def find_header(self):
        self.wait.until(ec.visibility_of_element_located(self.header))

    @allure.step('Получаем номер заказа')
    def get_order_number(self):
        message = self.driver.find_element(*self.order_information).text
        try:
            order_number = re.search(r'\d{1,}', message).group(0)
        except ValueError:
            order_number = 'No order number'
        return order_number

    @allure.step('Кликаем кнопку Посмотреть статус')
    def click_check_status_button(self):
        self.driver.find_element(*self.check_status_button).click()

