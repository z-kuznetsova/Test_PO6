import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope='module')
def driver():
    # Инициализация веб-драйвера
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://chicago-pizza.ru/")
    time.sleep(2)  # Ждем загрузки страницы
    yield driver
    driver.quit()

@pytest.fixture
def restart_driver():
    # Перезагрузка драйвера
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://chicago-pizza.ru/")
    time.sleep(2)  # Ждем загрузки страницы
    yield driver
    driver.quit()

def test_search_product(driver):
    search_box = driver.find_element(By.CSS_SELECTOR, 'input[type="search"]')
    search_box.send_keys("Римская пицца пепперони")
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # ожидание загрузки результатов
    results = driver.find_elements(By.XPATH, "//div[contains(text(), 'Римская пицца пепперони')]")
    assert len(results) > 0, "Товар не найден"


def test_add_to_cart(driver):
    # Добавление товара в корзину
    add_button = driver.find_element(By.XPATH, "//button[@aria-label='Добавить']")
    add_button.click()
    time.sleep(1)

    # Проверка, что товар добавлен
    cart_text = driver.find_element(By.CSS_SELECTOR, '.text-2xl.leading-none').text
    assert "Корзина" in cart_text, "Товар не добавлен в корзину"


def test_remove_from_cart(driver):
    minus_button = driver.find_element(By.XPATH, "//div[contains(@class, 'flex items-start gap-4')]//button[contains(@class, 'inline-flex')]")
    # Нажатие на кнопку удаления
    minus_button.click()

    # Ожидание, что корзина пуста
    empty_cart_text = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[@class='text-center text-gray-400' and text()='Здесь пока пусто']"))
    )
    assert "Здесь пока пусто" in empty_cart_text.text, "Корзина не пуста"

def test_login(driver):
    # Переход к форме авторизации
    login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/profile']"))
        )
    login_button.click()
    time.sleep(5)
    # Ввод номера телефона
    phone_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='text'][inputmode='numeric']"))
    )
    phone_input.send_keys("89293984818")

    # Ввод пароля
    password_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
    )
    password_input.send_keys("zlata2003")

    # Нажатие на кнопку "Войти"
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )
    submit_button.click()

    time.sleep(5)  # Ждем, чтобы увидеть результат входа

    # Ждем, пока элемент с именем пользователя станет видимым
    user_name_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "span.hidden.text-gray-900.lg\\:inline.dark\\:text-gray-400"))
    )

    # Проверяем, что текст элемента соответствует ожидаемому имени
    assert user_name_element.text == "Злата", f"Ожидалось имя 'Злата', но получено '{user_name_element.text}'"

def test_registration(restart_driver):
    driver = restart_driver
    # Переход к форме авторизации
    login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/profile']"))
        )
    login_button.click()
    time.sleep(2)

    # Ожидание появления кнопки "Регистрация" и нажатие на нее
    registration_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Регистрация')]"))
    )
    registration_button.click()
    time.sleep(2)

    # Ожидание появления формы регистрации
    phone_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder=' ']"))
    )

    # Ввод номера телефона
    phone_input.send_keys("89235610379")

    # Ввод пароля
    password_input = driver.find_elements(By.CSS_SELECTOR, "input[placeholder=' ']")[1]
    password_input.send_keys("zlata2003")

    # Ввод подтверждения пароля
    confirm_password_input = driver.find_elements(By.CSS_SELECTOR, "input[placeholder=' ']")[2]
    confirm_password_input.send_keys("zlata2003")

    # Ожидание появления чекбокса согласия и нажатие на него
    agreement_checkbox = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox' and contains(@class, 'text-primary')]"))
    )
    agreement_checkbox.click()

    time.sleep(2)

    # Нажатие на кнопку "Зарегистрироваться"
    register_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )
    register_button.click()
    time.sleep(2)

    # Ждем, пока элемент с именем пользователя станет видимым
    user_name_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "span.hidden.text-gray-900.lg\\:inline.dark\\:text-gray-400"))
    )

    # Проверяем, что текст элемента соответствует ожидаемому имени
    assert user_name_element.text == "Гость", f"Ожидалось имя 'Гость', но получено '{user_name_element.text}'"
