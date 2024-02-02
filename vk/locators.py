from selenium.webdriver.common.by import By


class LoginPage:
    input_login = (By.CSS_SELECTOR, 'input[name="login"]')
    button_login = (By.CSS_SELECTOR, '.FlatButton--primary')
    input_password = (By.CSS_SELECTOR, '.vkc__Password__Wrapper .vkc__TextField__input')
    button_password = (By.CSS_SELECTOR, '.vkuiButton__in')


class HomePage:
    link_group = (By.CSS_SELECTOR, '#l_gr a')
    link_msg = (By.CSS_SELECTOR, '#l_msg a')


class Group:
    input_group_search = (By.CSS_SELECTOR, "#groups_list_search")
    link_founded_group = (By.CSS_SELECTOR, "a[class='group_row_title']")
    link_go_to_chat = (By.CSS_SELECTOR, "div[class='group_name']")


class Chat:
    search_game_chat = (By.CSS_SELECTOR, "[data-peer='2000000073']")
    link_members = (By.CSS_SELECTOR, "._im_chat_members")
    name_of_members_with_id = (By.CSS_SELECTOR, ".Entity__title a")
    name_of_members_with_status = (By.CSS_SELECTOR, ".Entity__main")
    close_layer = (By.CSS_SELECTOR, ".vkuiModalDismissButton ")
    input_group_chat = (By.CSS_SELECTOR, ".im_editable")
    send_msg = (By.CSS_SELECTOR, ".im-chat-input--send")


class ChatMembers:
    get_name_of_member_msg = (By.CSS_SELECTOR, ".im-mess-stack:last-child .im-mess-stack--lnk")
    get_msg = (By.CSS_SELECTOR, ".im-mess-stack:last-child .im-mess:last-child .im-mess--text")
    get_msg_a = (By.CSS_SELECTOR, ".im-mess-stack:last-child .im-mess:last-child .im-mess--text a")
