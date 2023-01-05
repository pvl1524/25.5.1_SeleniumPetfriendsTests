# 25.5.1_SeleniumPetfriendsTests


Практическое задание к 25 модулю курса SkillFactory "Тестировщик-автоматизатор на Python".

Тестируемый проект расположен по адресу https://petfriends.skillfactory.ru.

В директории /tests располагается файл test_petfriends.py с тестами.

Тесты написаны в классе, что соответствует принципам ООП и позволяет удобно пользоваться его методами.

При выполнении задания используется Selenium четвертой версии. Также используется плагин pytest-check, установка pip install pytest-check.
Crhomedriver можно найти по адресу https://chromedriver.chromium.org/downloads

Тест test_all_pets проверяет, что на странице со списком всех питомцев:

	- У всех питомцев есть фотография.
	- У всех питомцев есть имя, возраст и порода.

На странице со списком питомцев пользователя:

	- test_mypets_page_show_all_pets. Присутствуют все питомцы.
	- test_half_or_greater_of_pets_has_photos. Хотя бы у половины питомцев есть фото.
	- test_all_my_pets_has_non_empty_name_type_age. У всех питомцев есть имя, возраст и порода.
	- test_my_pets_has_different_names.  У всех питомцев разные имена.
	- test_my_pets_are_unique. В списке нет повторяющихся питомцев с одинаковым именем, породой и возрастом одновременно.