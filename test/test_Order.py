import allure
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as ec
from POM.Page_Object_Index import Cookies, OrderButton, IndexPage
from POM.Page_Object_Order import PersonalData, RentalConditions, OrderConsentModal, SuccessfulOrderModal
from POM.Page_Object_TrackOrder import OrderTrack


test_data = [{'name': 'Юлия', 'surname': 'Исаева', 'address': '123 Чистые пруды',
             'station': 'Динамо', 'phone': '89035555555', 'day': '15', 'period': 'семеро суток',
              'colour': 'чёрный жемчуг', 'comment': 'Нет комментариев'},
             {'name': 'Мария', 'surname': 'Исаева', 'address': '124 Чистые пруды',
              'station': 'Белорусская', 'phone': '89037777777', 'day': '10', 'period': 'сутки',
              'colour': 'серая безысходность', 'comment': 'Есть комментарии'}
             ]


@allure.step('Параметризация тестов')
@allure.title('Передаем параметры')
@pytest.fixture(params=test_data)
def order_params(request):
    return request.param


@allure.step('Инициализация драйвера')
@allure.title('Инициализация драйвера для класса TestOrder')
@pytest.fixture(scope='class', autouse=True)
def init_driver(request):
    base_url = 'https://qa-scooter.praktikum-services.ru/'
    firefox_option = webdriver.FirefoxOptions()
    firefox_option.add_argument("-headless")
    driver = webdriver.Firefox(options=firefox_option)
    driver.implicitly_wait(2)
    request.cls.driver = driver
    request.cls.wait = Wait(request.cls.driver, timeout=3, poll_frequency=0.1)
    request.cls.driver.get(base_url)
    cookies = Cookies(request.cls.driver)
    cookies.click_consent_button()
    yield request.cls.driver
    request.cls.driver.quit()


@allure.suite('Заказ самоката')
@allure.description('Проверяем процесс заказа самоката с положительным сценарием')
@pytest.mark.usefixtures('init_driver')
class TestOrder:

    base_url = 'https://qa-scooter.praktikum-services.ru/'
    url = 'https://qa-scooter.praktikum-services.ru/order'
    driver = None

    @allure.step('Заказываем самокат')
    @allure.title('Открываем главную страницу и принимаем cookies')
    @pytest.fixture(scope='function', autouse=True)
    def setup_class(self):
        self.driver.get(self.base_url)

    @allure.step('Нажимаем кнопку заказа самоката')
    def click_order_button(self):
        order_button = OrderButton(self.driver)
        order_button.click_order_button()

    @allure.testcase('Заказ самоката')
    @allure.description('Проверяем процесс заказа самоката')
    @allure.title('Заказ самоката')
    def test_fill_order(self, order_params):
        self.click_order_button()

        personal_data_form = PersonalData(self.driver, self.wait)
        personal_data_form.find_header()

        personal_data_form.fill_name(order_params['name'])
        personal_data_form.fill_surname(order_params['surname'])
        personal_data_form.fill_address(order_params['address'])
        personal_data_form.fill_station(order_params['station'])
        personal_data_form.fill_phone(order_params['phone'])
        personal_data_form.click_next_button()

        rental_conditions = RentalConditions(self.driver, self.wait)
        rental_conditions.find_header()

        rental_conditions.fill_data(order_params['day'])
        rental_conditions.fill_rental_period(order_params['period'])
        rental_conditions.fill_colour(order_params['colour'])
        rental_conditions.fill_comment(order_params['comment'])
        rental_conditions.click_order_button()

        consent_modal = OrderConsentModal(self.driver, self.wait)
        consent_modal.find_header()
        consent_modal.click_consent_button()

        order_modal = SuccessfulOrderModal(self.driver, self.wait)
        order_modal.find_header()
        order_number = order_modal.get_order_number()
        order_modal.click_check_status_button()

        order_track = OrderTrack(self.driver).get_order_input()

        assert order_track.get_attribute('value') == order_number, 'Номер заказа полученный ' \
                                                                   'в модальном окне не совпадает ' \
                                                                   'с номером заказа на странице' \
                                                                   ' отслеживания заказа'

    @allure.testcase('Клик на лого Самокат')
    @allure.description('Проверяем переход на главную страницу сервера по клику на лого Самокат')
    @allure.title('Клик на лого Самокат')
    def test_click_logo(self):
        self.driver.get(self.url)
        personal_data_page = PersonalData(self.driver, self.wait)
        personal_data_page.find_header()

        index_page_objects = IndexPage(self.driver)
        index_page_objects.click_logo_link()
        self.wait.until(ec.visibility_of_any_elements_located(index_page_objects.image))

        images = [x.get_attribute('src') for x in index_page_objects.get_scooter_images()]

        assert 'https://qa-scooter.praktikum-services.ru/assets/scooter.png' in images,\
            'Некорректно изображение самоката на главной странице'

    @allure.testcase('Клик на лого Yandex')
    @allure.description('Проверяем переход на главную страницу сайта Yandex по клику на лого Yandex')
    @allure.title('Клик на лого Yandex')
    def test_click_yandex(self):
        self.driver.get(self.base_url)
        index_page_objects = IndexPage(self.driver)
        self.wait.until(ec.visibility_of_any_elements_located(index_page_objects.image))

        handles_before = self.driver.window_handles
        index_page_objects.click_yandex_link()
        self.wait.until(ec.number_of_windows_to_be(len(handles_before)+1))

        handles_current = self.driver.window_handles
        new_window = None
        for window in handles_current:
            if window not in handles_before:
                new_window = window
                break

        self.driver.switch_to.window(new_window)
        self.wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'home-logo__default')))

        assert self.driver.title == 'Яндекс', 'Переключение не на окно Yandex'
