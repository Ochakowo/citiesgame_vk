import json
import time
from datetime import datetime
from func import *
from locators import *
import random


class AuthenticationVK:
    def __init__(self):
        self.preconditions = Preconditions()
        self.base_func = BaseFunc(self.preconditions.browser)

    def login_vk(self):
        """Запуск браузера, логин"""
        self.preconditions.start_browser()


class GroupChat:
    def __init__(self, base_func):
        self.base_func = base_func

    def join_group_chat(self):
        """Переход с главной страницы в сообщения"""
        self.base_func.click_element(HomePage.link_msg)
        self.base_func.click_element(Chat.search_game_chat)

        def get_dict_with_members():
            """Открываем список мемберов, отдаём словарь тех кто в онлайне"""
            self.base_func.click_element(Chat.link_members)
            time.sleep(2)

            dict_with_members_status, count = {}, 0
            online_members = self.base_func.get_elements(*Chat.name_of_members_with_status)
            for i in range(len(online_members)):
                count += 1
                if 2 < count < len(online_members):
                    member_name_and_status = online_members[i].text.split('\n')
                    member_name = member_name_and_status[0]
                    member_status = member_name_and_status[1]
                    dict_with_members_status[member_name] = member_status

            dict_with_members_id, count = {}, 0
            elements = self.base_func.get_elements(*Chat.name_of_members_with_id)
            for n, i in zip(elements, elements[0:]):
                count += 1
                if 2 < count <= len(elements):
                    dict_with_members_id[n.text] = i.get_attribute('href').rsplit('/', 1)[-1]

            self.base_func.click_element(Chat.close_layer)
            master_dict = dict_with_members_id
            dict_with_online_members = {key: dict_with_members_id[key] for key, value
                                        in dict_with_members_status.items() if value == 'online'}

            if dict_with_online_members == {}:
                print(f"Игроков онлайн нет.\n")
            else:
                print(f"Игроки онлайн: {(list(dict_with_online_members.keys()))}\n")
            return dict_with_online_members, master_dict

        def get_list_with_cities(json_file):
            """Читаю json файл с именами городов, получаю лист с именами городов"""
            with open(json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
            list_with_cities = [item["name"] for item in data]
            return list_with_cities

        def get_random_member(members: dict):
            """Получение рандомного мембера из словаря игроков"""
            full_name = (random.choice(list(members.keys())))
            name_id = members[full_name]
            return full_name, name_id

        def get_last_letter(city: str):
            """Получение последней или предпоследней буквы выбранного города"""
            last_letter = city[-1].upper()
            if last_letter in ("Ь", "Ъ", "Ы"):
                last_letter = city[-2].upper()
            return last_letter

        def choose_random_city_and_random_member(members: dict, cities: list):
            full_name, name_id = get_random_member(members)
            city_name = random.choice(list(cities))
            list_with_used_cities.append(city_name)
            last_letter = get_last_letter(city_name)
            result_msg = f"Город {city_name}. @{name_id}, тебе на {last_letter}."
            self.base_func.input_text(Chat.input_group_chat, result_msg)
            self.base_func.click_element(Chat.send_msg)
            print_msg()
            return full_name, name_id

        def choose_specific_city_and_random_member(members: dict, cities: list, first_letter: str):
            full_name, name_id = get_random_member(members)
            cities_with_first_letter = [city for city in cities if city.startswith(first_letter)]
            city_name = random.choice(list(cities_with_first_letter))
            list_with_used_cities.append(city_name)
            last_letter = get_last_letter(city_name)
            result_msg = f"Город {city_name}. @{name_id}, тебе на {last_letter}."
            self.base_func.input_text(Chat.input_group_chat, result_msg)
            self.base_func.click_element(Chat.send_msg)
            print_msg()
            return full_name, name_id

        def choose_last_city_and_random_member(members: dict, last_city: str):
            full_name, name_id = get_random_member(members)
            last_letter = get_last_letter(last_city)
            result_msg = f"Город {last_city}. @{name_id}, тебе на {last_letter}."
            self.base_func.input_text(Chat.input_group_chat, result_msg)
            self.base_func.click_element(Chat.send_msg)
            print_msg()
            return full_name, name_id

        def check_next_member(full_name: str):
            start_time, timeout_seconds = time.time(), 5
            while time.time() - start_time < timeout_seconds:
                next_member = self.base_func.get_element(*ChatMembers.get_name_of_member_msg).text
                if next_member == full_name:
                    return True
            else:
                return False

        def delete_member(members: dict, full_name: str, id: str):
            del members[full_name]
            msg_del = f"Игрок @{id} выбывает."
            self.base_func.input_text(Chat.input_group_chat, msg_del)
            self.base_func.click_element(Chat.send_msg)
            print_msg()
            time.sleep(1)
            if members == {}:
                print("")
                win_msg = "Я победил!"
                self.base_func.input_text(Chat.input_group_chat, win_msg)
                self.base_func.click_element(Chat.send_msg)
                print_msg()
            else:
                print(f"Оставшиеся игроки: {list(dict_with_online_members.keys())}\n")
            return members

        def get_current_msg():
            time.sleep(1)
            current_msg_as_text = (self.base_func.get_element(*ChatMembers.get_msg)).text
            current_member = (self.base_func.get_element(*ChatMembers.get_name_of_member_msg)).text
            return current_msg_as_text, current_member

        def print_msg():
            current_msg_as_text, current_member = get_current_msg()
            now_time = datetime.now().strftime("%H:%M:%S")
            return print(f"{now_time} - {current_member}: {current_msg_as_text}")

        list_with_all_cities = get_list_with_cities('cities.json')
        dict_with_online_members, master_dict = get_dict_with_members()
        list_with_used_cities = []
        list_with_cities_for_game = [city for city in list_with_all_cities if city not in list_with_used_cities]

        while True:
            current_msg_as_text, current_member = get_current_msg()

            if current_member not in (list(master_dict.keys())):
                if "Старт" in current_msg_as_text:
                    print_msg()
                    dict_with_online_members, _ = get_dict_with_members()
                    if dict_with_online_members == {}:
                        print("Нет игроков онлайн.")
                        continue
                    full_name, id = choose_random_city_and_random_member(dict_with_online_members, list_with_all_cities)
                    next_member = check_next_member(full_name)
                    if not next_member:
                        dict_with_online_members = delete_member(dict_with_online_members, full_name, id)
                    continue

                if "выбывает" in current_msg_as_text:
                    specific_city = list_with_used_cities[-1]
                    full_name, id = choose_last_city_and_random_member(dict_with_online_members, specific_city)
                    next_member = check_next_member(full_name)
                    if not next_member:
                        dict_with_online_members = delete_member(dict_with_online_members, full_name, id)
                    continue
                continue

            if current_member in (list(master_dict.keys())):
                if "Старт" in current_msg_as_text:
                    print_msg()
                    print(f"{current_member} начал игру.")
                    dict_with_online_members, _ = get_dict_with_members()
                    list_with_used_cities.clear()
                    continue

                if "победил" in current_msg_as_text:
                    print_msg()
                    print(f"{current_member} победил.")
                    continue

                if "выбывает" in current_msg_as_text:
                    print_msg()
                    nickname = current_msg_as_text.split("@")[1].split(" ")[0]
                    for key in [key for key, value in dict_with_online_members.items() if value == nickname]:
                        del dict_with_online_members[key]
                    print(f"Оставшиеся игроки: {list(dict_with_online_members.keys())}\n")
                    continue

                if "Город" in current_msg_as_text:
                    print_msg()
                    nickname = current_msg_as_text.split("@")[1].split(",")[0].split(" ")[0]
                    incoming_city = current_msg_as_text.split(".")[0].split(" ", 1)[1]
                    last_letter_in_incoming_city = get_last_letter(incoming_city)
                    penultimate_letter = current_msg_as_text[-2]
                    if incoming_city in list_with_used_cities or last_letter_in_incoming_city != penultimate_letter:
                        id = dict_with_online_members[current_member]
                        dict_with_online_members = delete_member(dict_with_online_members, current_member, id)
                        continue
                    elif incoming_city not in list_with_used_cities:
                        list_with_used_cities.append(incoming_city)
                    if nickname not in (list(master_dict.values())):
                        full_name, id = (choose_specific_city_and_random_member(dict_with_online_members,
                                                                                list_with_cities_for_game,
                                                                                penultimate_letter))
                        next_member = check_next_member(full_name)
                        if not next_member:
                            dict_with_online_members = delete_member(dict_with_online_members, full_name, id)
                        continue
                    continue
                continue


if __name__ == "__main__":
    try:
        vk_automation = AuthenticationVK()
        vk_automation.login_vk()
        join_group_chat = GroupChat(vk_automation.base_func)
        join_group_chat.join_group_chat()
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
