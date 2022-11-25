import pytest
import allure
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait as Wait
from pages.index import FaqQuestions, Cookies, IndexPage

questions = [
    {'question': 'Сколько это стоит? И как оплатить?',
     'answer': 'Сутки — 400 рублей. Оплата курьеру — наличными или картой.'},
    {'question': 'Хочу сразу несколько самокатов! Так можно?',
     'answer': 'Пока что у нас так: один заказ — один самокат. Если хотите покататься с друзьями,'
               ' можете просто сделать несколько заказов — один за другим.'},
    {'question': 'Как рассчитывается время аренды?',
     'answer': 'Допустим, вы оформляете заказ на 8 мая. Мы привозим самокат 8 мая в течение дня.'
               ' Отсчёт времени аренды начинается с момента, когда вы оплатите заказ курьеру. '
               'Если мы привезли самокат 8 мая в 20:30, суточная аренда закончится 9 мая в 20:30.'
     },
    {'question': 'Можно ли заказать самокат прямо на сегодня?',
     'answer': 'Только начиная с завтрашнего дня. Но скоро станем расторопнее.'
     },
    {'question': 'Можно ли продлить заказ или вернуть самокат раньше?',
     'answer': 'Пока что нет! Но если что-то срочное — всегда можно позвонить в поддержку по красивому номеру 1010.'},
    {'question': 'Вы привозите зарядку вместе с самокатом?',
     'answer': 'Самокат приезжает к вам с полной зарядкой. '
               'Этого хватает на восемь суток — даже если будете кататься без передышек и во сне.'
               ' Зарядка не понадобится.'},
    {'question': 'Можно ли отменить заказ?',
     'answer': 'Да, пока самокат не привезли. Штрафа не будет, объяснительной записки тоже не попросим. Все же свои.'},
    {'question': 'Я жизу за МКАДом, привезёте?',
     'answer': 'Да, обязательно. Всем самокатов! И Москве, и Московской области.'}
]


@allure.title('Параметризуем тест ожидаемыми значениями')
@pytest.fixture(params=questions)
def expected(request):
    return request.param


@allure.suite('Тестирование FAQ')
@allure.title('Проверка списка FAQ')
class TestQuestions:

    @allure.title('Инициализируем драйвер')
    @pytest.fixture(scope='class', autouse=True)
    def setup_and_teardown(self, request):

        firefox_option = webdriver.FirefoxOptions()
        #firefox_option.add_argument("-headless")
        driver = webdriver.Firefox(options=firefox_option)
        driver.implicitly_wait(1)

        IndexPage(driver).open_index_page()
        Cookies(driver).get_cookies()
        FaqQuestions(driver).scroll_to_header()
        request.cls.driver = driver

        yield driver
        driver.quit()

    @allure.title('Проверка вопроса FAQ')
    @allure.description('Проверяем вопросы и ответы на соответствие ожидаемым')
    @allure.step('Сравниваем ожидаемые и актуальные данные')
    def test_faq_items_are_equal_expected(self, request, expected):

        driver = request.cls.driver
        question = expected['question']

        faq = FaqQuestions(driver)
        question_container = faq.get_faq_by_question(question)
        faq.click_question_button(question_container)
        answer = faq.get_answer(question_container)

        assert question_container is not None, f"Вопрос {question} не найден"
        assert answer == expected['answer']

