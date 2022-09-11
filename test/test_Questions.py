import pytest
from selenium import webdriver
from POM.Page_Object_Index import FaqQuestions, Cookies
import allure

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
items = []

base_url = 'https://qa-scooter.praktikum-services.ru/'


@allure.step('Инициализируем драйвер')
def init_driver():
    firefox_option = webdriver.FirefoxOptions()
    firefox_option.add_argument("-headless")
    wd = webdriver.Firefox(options=firefox_option)
    wd.implicitly_wait(1)
    return wd


@allure.step('Открываем страницу {url}')
def open_url(driver, url):
    driver.get(url)


@allure.step('Соглашаемся с настройками cookies')
def consent_cookies(driver):
    cookies = Cookies(driver)
    cookies.get_cookies()


@allure.step('Скроллим до списка FAQ')
def scroll_to_faq(driver):
    faq = FaqQuestions(driver)
    faq.scroll_to_header()
    return faq


@allure.step('Собираем данные по списку FAQ')
def get_faq(faq):
    return faq.get_faq()


@allure.step('Закрываем браузер')
def quit_driver(driver):
    driver.close()
    driver.quit()


@allure.step('Подготавливаем данные для тестирования')
@allure.title('Подготовка данных')
@pytest.fixture(scope='module')
def test_execution():
    global items

    driver = init_driver()
    open_url(driver, base_url)
    consent_cookies(driver)
    faq = scroll_to_faq(driver)
    items = get_faq(faq)
    quit_driver(driver)


def pytest_generate_tests(metafunc):

    if metafunc.definition.name == "test_questions":
        return metafunc.parametrize('expected', questions)
    else:
        return metafunc


@allure.suite('Тестирование FAQ')
@allure.testcase('TestCase-112')
@allure.title('Проверка вопроса FAQ')
@allure.description('Проверяем вопросы и ответы на соответствие эталонным')
@allure.step('Сравниваем эталонные и актуальные данные')
@pytest.mark.usefixtures('test_execution')
def test_questions(expected):

    actual = find_answer(expected['question'])
    assert actual is not None, "Ответ на этот вопрос не найден"
    assert expected['question'] == actual['question'], 'Вопрос отличается от ожидаемого'
    assert expected['answer'] == actual['answer'], 'Ответ отличается от ожидаемого'


def find_answer(question: str):
    for item in items:
        if item['question'] == question:
            return item
    return None
