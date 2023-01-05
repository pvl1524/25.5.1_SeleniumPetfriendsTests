from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pytest_check import check
import math

# Запуск тестов:
# pytest -v --driver Chrome --driver-path chromedriver.exe test_petfriends.py
# pytest -v --driver Firefox --driver-path geckodriver.exe test_petfriends.py

class TestPetFrieds:

    def setup(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def open(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.base_url)
        self.driver.maximize_window()

    def login(self):
        # Открыть основную страницу PetFriends
        self.open()

        # Кликнуть по кнопке Зарегистрироваться
        WebDriverWait(self.driver, 10).until \
            (EC.element_to_be_clickable((By.XPATH, "//button[@onclick=\"document.location='/new_user';\"]"))).click()

        # Кликнуть по ссылке У меня уже есть аккаунт
        WebDriverWait(self.driver, 10).until \
            (EC.element_to_be_clickable((By.LINK_TEXT, u"У меня уже есть аккаунт"))).click()

        # Вводим email
        field_email = self.driver.find_element(By.ID, "email")
        field_email.clear()
        field_email.send_keys("pvl1524@yandex.ru")

        # Вводим пароль
        field_pass = self.driver.find_element(By.ID, "pass")
        field_pass.clear()
        field_pass.send_keys("c7ja82-UUHW@")

        # Кликнуть по кнопке Войти
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

        assert self.driver.current_url == 'https://petfriends.skillfactory.ru/all_pets'
        assert self.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    def mypets_elements(self):
        self.login()

        # Кликнуть по ссылке Мои питомцы
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/my_pets']"))).click()

        check.equal(self.driver.current_url,
                    'https://petfriends.skillfactory.ru/my_pets'), "Некорректный адрес страницы Мои питомцы"

        names = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr/td[1]")))
        types = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr/td[2]")))
        ages = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr/td[3]")))
        photos = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr/th/img")))
        return names, types, ages, photos

    def number_pets(self):
        # Находим элемент div со статистикой, расположенный слева от таблицы
        div_stat = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='.col-sm-4 left']")))

        div_elems = [i.text for i in div_stat][0]  # Сохрание текста div в строку
        index_start_pets = div_elems.find('Питомцев')  # Индекс начала слова Питомцев
        num_pets = int(div_elems[index_start_pets + 10])  # Число питомцев
        return num_pets

        # print("num_pets ", num_pets)


    def test_all_pets(self):

        self.login()

        self.driver.implicitly_wait(10)

        images = self.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
        names_main = self.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
        descriptions = self.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

        for i in range(len(names_main)):
            check.not_equal(names_main[i].text, ''), "Должно быть указано имя питомца"
            check.not_equal(images[i].get_attribute('src'), ''), "Не все питомцы с фотографией"
            check.not_equal(descriptions[i].text, ''), "Описание питомца (порода, возраст) не должно быть пустым"
            check.is_in(', ', descriptions[i].text)
            parts = descriptions[i].text.split(", ")
            check.greater(len(parts[0]), 0), "Должна быть указана порода питомца"
            check.greater(len(parts[1]), 0), "Должен быть указан возраст питомца"


    def test_mypets_page_show_all_pets(self):
        names, _, _, _ = self.mypets_elements()
        num_pets = self.number_pets()

        # Сравниваем число питомцев из статистики и число строк таблицы с данными
        check.equal(num_pets, len(names)), "Количество питомцев в таблице и статистике должно быть равным"


    def test_half_or_greater_of_pets_has_photos(self):

        _, _, _, photos = self.mypets_elements()

        counter_ph = 0

        for i in range(len(photos)):
            if photos[i].get_attribute('src') != '':
                counter_ph += 1
        num_pets = self.number_pets()
        # print("num_pets ", num_pets)
        # print("Число фотографий", counter_ph, "Round", math.ceil(num_pets/2))

        check.greater_equal(counter_ph, math.ceil(num_pets / 2)), "Фото есть меньше, чем у половины питомцев"

    def test_all_my_pets_has_non_empty_name_type_age(self):

        # Сохраняем имена, породы, возраст в переменные (кроме фото)
        names, types, ages, _ = self.mypets_elements()

        for i in range(len(names)):
            # Проверяем, что у всех питомцев есть имя, порода и возраст
            check.not_equal(names[i].text, ''), "Должно быть указано имя питомца"

            check.not_equal(types[i].text, ''), "Должна быть указана порода питомца"

            check.not_equal(ages[i].text, ''), "Должен быть указан возраст питомца"

    def test_my_pets_has_different_names(self):
        names, _, _, _ = self.mypets_elements()
        names_list= []

        for i in range(len(names)):
            # Создаем список имен питомцев
            names_list.append(names[i].text)
        # print(f"Список name_list {names_list}")

        # Отсутствуют дублирующиеся имена питомцев
        check.equal(len(names_list), len(set(names_list))), "Присутсвуют питомцы с одинаковыми именами"

    def test_my_pets_are_unique(self):
        # Сохраняем имена, породы, возраст в переменные (кроме фото)
        names, types, ages, _ = self.mypets_elements()
        pets = []

        for i in range(len(names)):
            # Создаем список с данными питомцев
            pets.append(names[i].text + types[i].text + str(ages[i].text))
        # print("Список pets", pets)

        # Отсутствуют дублирующиеся питомцы - сочетание имени, породы и возраста
        check.equal(len(pets), len(set(pets))), "Присутсвуют дублирующиеся питомцы с одинаковыми именами, породой и возрастом"

    def teardown(self):
        self.driver.quit()