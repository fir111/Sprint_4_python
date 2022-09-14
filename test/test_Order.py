import allure
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as ec
from pages.index import Cookies, OrderButton, IndexPage
from pages.order import PersonalData, RentalConditions, OrderConsentModal, SuccessfulOrderModal
from pages.track_order import OrderTrack


test_data = [{'name': 'Юлия', 'surname': 'Исаева', 'address': '123 Чистые пруды',
             'station': 'Динамо', 'phone': '89035555555', 'day': '15', 'period': 'семеро суток',
              'colour': 'чёрный жемчуг', 'comment': 'Нет комментариев'},
             {'name': 'Мария', 'surname': 'Исаева', 'address': '124 Чистые пруды',
              'station': 'Белорусская', 'phone': '89037777777', 'day': '10', 'period': 'сутки',
              'colour': 'серая безысходность', 'comment': 'Есть комментарии'}
             ]


@allure.title('Передаем параметры положительного сценария')
@pytest.fixture(params=test_data)
def order_params(request):
    return request.param


@allure.suite('Заказ самоката')
@allure.title('Заказ самоката')
class TestOrder:

    @allure.title('Инициализируем драйвер')
    @pytest.fixture(scope='function', autouse=True)
    def setup_and_teardown(self):
        firefox_option = webdriver.FirefoxOptions()
        # firefox_option.add_argument("-headless")
        self.driver = webdriver.Firefox(options=firefox_option)
        self.driver.implicitly_wait(1)
        self.wait = Wait(self.driver, timeout=5, poll_frequency=0.1)

        yield self.driver
        self.driver.quit()

    @allure.testcase('Заказ самоката')
    @allure.description('Проверяем процесс заказа самоката с положительным сценарием')
    @allure.title('Заказ самоката')
    def test_check_order_positive_scenario_order_number_received(self, order_params):

        index_page = IndexPage(self.driver)
        index_page.open_index_page()

        cookies = Cookies(self.driver)
        cookies.get_cookies()

        order_button = OrderButton(self.driver)
        order_button.click_order_button()

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
    def test_click_logo_goto_index_page(self):

        personal_data_page = PersonalData(self.driver, self.wait)
        personal_data_page.open_order_page()
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
    def test_click_yandex_logo_goto_yandex_index_page(self):

        index_page = IndexPage(self.driver)
        index_page.open_index_page()
        self.wait.until(ec.visibility_of_any_elements_located(index_page.image))

        handles_before = self.driver.window_handles
        index_page.click_yandex_link()
        self.wait.until(ec.number_of_windows_to_be(len(handles_before)+1))

        handles_current = self.driver.window_handles
        new_window = None
        for window in handles_current:
            if window not in handles_before:
                new_window = window
                break

        self.driver.switch_to.window(new_window)
        self.wait.until(ec.visibility_of_element_located((By.XPATH, '//h2[text()="Новый портал dzen.ru"]')))

        assert self.driver.title == 'Дзен', 'Переключение не на окно Yandex'
