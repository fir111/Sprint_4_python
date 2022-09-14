import pytest
import allure
from selenium import webdriver
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
    def setup_and_teardown(self):

        firefox_option = webdriver.FirefoxOptions()
        firefox_option.add_argument("-headless")
        self.driver = webdriver.Firefox(options=firefox_option)
        self.driver.implicitly_wait(1)

        yield self.driver
        self.driver.quit()

    @allure.step('Подготавливаем данные для тестирования')
    @allure.title('Подготовка данных')
    @pytest.mark.dependency()
    @pytest.fixture(scope='class')
    def get_faq(self):

        index = IndexPage(self.driver)
        index.open_index_page()

        cookies = Cookies(self.driver)
        cookies.get_cookies()

        faq = FaqQuestions(self.driver)
        faq.scroll_to_header()
        pytest.shared = faq.get_faq()

    @allure.testcase('TestCase-112')
    @allure.title('Проверка вопроса FAQ')
    @allure.description('Проверяем вопросы и ответы на соответствие ожидаемым')
    @allure.step('Сравниваем ожидаемые и актуальные данные')
    @pytest.mark.usefixtures('get_faq')
    @pytest.mark.dependency(depends=["TestQuestions::get_faq"])
    def test_questions(self, expected):

        actual = self.find_answer(expected['question'])
        assert actual is not None, "Ответ на этот вопрос не найден"
        assert expected['question'] == actual['question'], 'Вопрос отличается от ожидаемого'
        assert expected['answer'] == actual['answer'], 'Ответ отличается от ожидаемого'

    def find_answer(self, expected):
        for item in pytest.shared:
            if item['question'] == expected:
                return item
        return None
