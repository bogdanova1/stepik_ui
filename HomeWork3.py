from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import string
import sys
import traceback
import locators as _locators


def test_registration(email, password):
    try:
        # Arrange
        browser = webdriver.Chrome()
        browser.implicitly_wait(5)
        browser.get(_locators.main_page_link)

        # Act
        browser.find_element_by_id(_locators.login).click()
        browser.find_element_by_id("id_registration-email").send_keys(email)
        browser.find_element_by_id("id_registration-password1").send_keys(password)
        browser.find_element_by_id("id_registration-password2").send_keys(password)
        browser.find_element_by_css_selector("button[name = 'registration_submit']").click()

        # Assert
        message = browser.find_element_by_class_name("alertinner")
        assert "Спасибо за регистрацию!" in message.text, "No message about registration"

        browser.find_element_by_id(_locators.logout).click()
        assert browser.current_url == _locators.main_page_link, "No return to main page"
    except AssertionError:
        print("\033[93mTest failed")
        print("Traceback:")
        for tbItem in traceback.format_tb(sys.exc_info()[2]):
            print(tbItem)
        print("AssertionError:" + str(sys.exc_info()[1]))
        print("\033[0m")
    except Exception:
        print("\033[91mTest failed")
        print("Traceback:")
        for tbItem in traceback.format_tb(sys.exc_info()[2]):
            print(tbItem)
        print("'%s: '%s" % (sys.exc_info()[0].__name__,str(sys.exc_info()[1])))
        print("\033[0m")
    else:
        print("\033[92m Test successfully passed! \033[0m")
    finally:
        browser.quit()


def test_authorization(email, password):
    try:
        # Arrange
        browser = webdriver.Chrome()
        browser.implicitly_wait(5)
        browser.get(_locators.main_page_link)

        # Act
        browser.find_element_by_id(_locators.login).click()
        browser.find_element_by_id("id_login-username").send_keys(email)
        browser.find_element_by_id("id_login-password").send_keys(password)
        browser.find_element_by_css_selector("button[name = 'login_submit']").click()

        # Assert
        message = browser.find_element_by_class_name("alertinner")
        assert "Рады видеть вас снова" in message.text, "No message about authorization"
        browser.find_element_by_id(_locators.logout).click()
        assert browser.current_url == _locators.main_page_link, "No return to main page"

    finally:
        browser.quit()


def test_view_all_articles():
    try:
        # Arrange
        browser = webdriver.Chrome()
        browser.implicitly_wait(5)
        browser.get(_locators.main_page_link)

        # Act
        browser.find_element_by_link_text(_locators.all_items).click()

        # Assert
        header = browser.find_elements_by_css_selector('.page-header h1')
        assert len(header) > 0 and header[0].text == 'Все товары', "Нет заголовка"
        assert len(browser.find_elements_by_class_name('side_categories')) > 0, "Нет области фильтров"
        assert len(browser.find_elements_by_class_name('form-horizontal')) > 0, \
            "Нет количества найденных результатов"
        assert len(browser.find_elements_by_css_selector('ol.row')) > 0, "Нет таблицы с товарами"
        assert len(browser.find_elements_by_css_selector('article img')) > 0, "Нет изображения товара"
        assert len(browser.find_elements_by_css_selector('article h3')) > 0, "Нет название товара"
        assert len(browser.find_elements_by_css_selector('article .price_color')) > 0, "Нет цены товара"
        assert len(browser.find_elements_by_css_selector('article .availability')) > 0, \
            "Нет доступности товара на складе"
        assert len(browser.find_elements_by_css_selector('article button.btn')) > 0 or \
               len(browser.find_elements_by_css_selector('article span.btn')) > 0, 'Нет кнопки "Добавить в корзину"'
        if len(browser.find_elements_by_class_name('pager')) > 0:  # есть пагинация
            browser.find_elements_by_css_selector('.next a')[0].click()
            assert browser.current_url.endswith("catalogue/?page=2"), "Нет перехода на 2 страницу"

    finally:
        browser.quit()


def test_view_article():
    try:
        # Arrange
        browser = webdriver.Chrome()
        browser.implicitly_wait(5)
        browser.get(_locators.main_page_link)

        # Act
        browser.find_element_by_link_text(_locators.all_items).click()
        article_link = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "article a"))
        )
        article_link.click()

        # Assert
        assert len(browser.find_elements_by_css_selector('.product_page img')) > 0, "Нет изображения товара"
        assert len(browser.find_elements_by_css_selector('.product_page h1')) > 0, "Нет название товара"
        assert len(browser.find_elements_by_css_selector('.product_page .price_color')) > 0, "Нет цены товара"
        assert len(browser.find_elements_by_css_selector('.product_page .availability')) > 0, \
            "Нет доступности товара на складе"
        assert len(
            browser.find_elements_by_css_selector('.product_page #write_review')) > 0, 'Нет кнопки "Написать отзыв"'
        assert len(browser.find_elements_by_css_selector(
            '.product_page button.btn')) > 0, 'Нет кнопки "Добавить в корзину" или кнопки "Сообщить мне"'
        assert len(browser.find_elements_by_css_selector(
            '.product_page #product_description')) > 0, 'Нет заголовка "Описание товара"'
        assert len(browser.find_elements_by_css_selector('.product_page .sub-header')) > 1 and \
               browser.find_elements_by_css_selector('.product_page .sub-header')[
                   1].text == 'Информация о товаре', 'Нет заголовка "Информация о товаре"'
        assert len(
            browser.find_elements_by_css_selector('.product_page #reviews')) > 0, 'Нет заголовка "Отзывы Клиентов"'

        browser.find_element_by_css_selector('.breadcrumb a[href="/ru/"]').click()
        assert browser.current_url == _locators.main_page_link, "No return to main page"

    finally:
        browser.quit()


def test_search_article_by_part_name(part_name):
    try:
        # Arrange
        browser = webdriver.Chrome()
        browser.implicitly_wait(5)
        browser.get(_locators.main_page_link)

        # Act
        browser.find_element_by_css_selector("input[type = 'search']").send_keys(part_name)
        browser.find_element_by_css_selector('.navbar-form.navbar-right input[type = "submit"]').click()

        # Assert
        title_text = browser.find_element_by_class_name('page-header').text
        assert part_name in title_text, \
            "Page title '%s' should contain search text '%s'" % (title_text, part_name)
        articles = browser.find_elements_by_css_selector(".product_pod")
        for article in articles:
            assert part_name.upper() in article.find_element_by_css_selector("h3 a").text.upper(), \
                "Article name '%s' should contain search text '%s'" % (part_name, article.text)
            assert part_name.upper() in article.find_element_by_css_selector("img").get_attribute("alt").upper(), \
                "Article image '%s' should contain search text '%s'" % (part_name, article.text)

    finally:
        browser.quit()


def test_add_article_to_cart():
    try:
        # Arrange
        browser = webdriver.Chrome()
        browser.implicitly_wait(5)
        browser.get(_locators.main_page_link + "catalogue/")

        # Act
        articles = browser.find_elements_by_tag_name('article')
        article_title = ''
        for article in articles:
            if len(article.find_elements_by_tag_name('button')) > 0:
                article_title = article.find_element_by_css_selector('article h3').text
                article.find_element_by_tag_name('button').click()
                break

        # Assert
        if article_title != '':
            browser.find_element_by_css_selector(".btn-group>a[href='/ru/basket/']").click()
            bucket_items = browser.find_elements_by_class_name('basket-items')
            add_basket = False
            for bucket_item in bucket_items:
                if bucket_item.find_element_by_css_selector("h3").text == article_title:
                    add_basket = True
                    break
            assert add_basket, "Товар '%s' не добавлен в корзину" % (article_title)
        else:
            print("Нет товаров для добавления в корзину")
    finally:
        browser.quit()


def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits
    return prefix + "".join([random.choice(symbols) for i in range(maxlen)])


# 1. Регистрация
password = random_string("", 9)
email = password + "@test.com"
test_registration(email, password)

# 2. Авторизация
test_authorization('1@test.com', 'QqWwEe!1@2')

# 3. Просмотр товаров
test_view_all_articles()

# 4. Просмотр карточки товара
test_view_article()

# 5. Поиск товара по части наименовани
test_search_article_by_part_name("coder")

# 6. Добавление товара в корзину
test_add_article_to_cart()
