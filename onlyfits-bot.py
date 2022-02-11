import telebot
from telebot import types
import time
import numpy as np
import pandas as pd
from datetime import datetime
import os
import textwrap
import pickle

from test_parser_for_bot import *




with open('current_clients.pkl', 'rb') as f:
    current_users = pickle.load(f)

print(current_users)


def get_time():
    now = datetime.now()
    now_h = now.strftime("%d/%m/%Y %H:%M:%S")
    return now_h

TOKEN = "5118074175:AAGdSNqLzaRCEWw5wR1XNH_5v5wF1e8eq1M"
testTOKEN = "288367920:AAEuc2Lqw94_jG3Qi0j_7Uqh4FSuGKHl-zw"
tb = telebot.TeleBot(TOKEN)

files_folder = '/Users/artemii/OneDrive/Documents/ONLYFITS/program-design-jan-2022/Материалы/resources/'
clients_folder = '/Users/artemii/OneDrive/Documents/ONLYFITS/.2930/'

tests = ['eat26', 'main', 'bdi']

eat26_convert = pd.read_csv(
    '/Users/artemii/OneDrive/Documents/ONLYFITS/program-design-jan-2022/Предзапись/eat26-convert-for-bot.csv',
    sep = ';', dtype = str)
eat26_keys = pd.read_csv(
    '/Users/artemii/OneDrive/Documents/ONLYFITS/program-design-jan-2022/Предзапись/eat26-keys.csv',
    sep = ';', dtype = str)

main_convert = pd.read_csv(
    '/Users/artemii/OneDrive/Documents/ONLYFITS/program-design-jan-2022/Предзапись/main-test-convert-for-bot.csv',
    sep = ';', dtype = str)
main_keys = pd.read_csv(
    '/Users/artemii/OneDrive/Documents/ONLYFITS/program-design-jan-2022/Предзапись/main-test-keys.csv',
    sep = ';', dtype = str)

bdi_convert = pd.read_csv(
    '/Users/artemii/OneDrive/Documents/ONLYFITS/program-design-jan-2022/Предзапись/bdi-convert-for-bot.csv',
    sep = ';', dtype = str)
bdi_keys = pd.read_csv(
    '/Users/artemii/OneDrive/Documents/ONLYFITS/program-design-jan-2022/Предзапись/bdi-keys.csv',
    sep = ';', dtype = str)

tests_dict = {'eat26':{'convert': eat26_convert, 'keys': eat26_keys},
              'main':{'convert': main_convert, 'keys': main_keys},
              'bdi':{'convert': bdi_convert, 'keys': bdi_keys}}

# User id info
coaches = {520834290:"Ксения Календарева", 594759110:"Елена", 1472202629:"trener.idel",
           541765907:"Дарья", 141659022:"Янина", 287460510:"Ирина",
           409750031:"Анастасия", 310119054:"Наталья Лаврененко",
           3755631:"Artemii", 2019105955:"Artemii Nikitin",
           970257969: "Наталья Минажетдинова", 388199486: "Артем"}

coaches_test = {3755631:"Artemii", 2019105955:"Artemii Nikitin"}

ids = [3755631, 2019105955]

# User State dictionary
trenerskaya = {x: dict(name=coaches[x], menu_cur='main',
                       menu_prev=str(), step=str(), message_to_delete=0, log=str()) for x in (coaches.keys())}
print(trenerskaya)


@tb.message_handler(commands=['start', 'help'])
def handle_start(message):
    if message.chat.id not in coaches:
        tb.reply_to(message,
                    "Здравствуйте. Пожалуйста, зарегистрируйтесь, нажав на кнопку ниже, либо введите пароль: ",
                    reply_markup=markup0)
    else:
        where(message.chat.id)


def database_dump(usr, call):
    current_users = {'init':'init'}
    with open('current_clients.pkl', 'wb') as f:
        pickle.dump(current_users, f)
    dump_reply = 'dump complete'
    tb.send_message(usr, text=str(current_users) + dump_reply)

# def erase_results_menu(usr, call):
#     eraser_keyboard = {}
#     for user in current_users.keys():
#         eraser_keyboard[str('erase_' + user)] = user
#     tb.send_message(usr, text = 'Удалить результаты пользователя из базф данных',
#                     reply_markup=makeQuestionKeyboard(question_options),
#                     parse_mode='HTML')
#
# def erase_results(usr, call):
#     user_to_erase = call.split('_')[1]
#     user_to_erase = int(user_to_erase)
#     current_users[user_to_erase][main]['responses'][]
#     for test in tests:
#         current_users[user_to_erase][test]['responses'] = pd.DataFrame()
#         current_users[user_to_erase][test]['responses']['client_telegram_id'] = user_to_erase
#     current_users[user_to_erase][test]['responses']['client_telegram_id']

# Message listener
def handle_messages(messages):
    for message in messages:
        #Sign Up
        if message.text == 'database_dump_2929':
            dump_reply = db_dump()
            tb.send_message(message.chat.id, text=str(current_users + dump_reply))
        elif message.text == 'betatester':
            test_mainscreen(message)
        elif message.text == 'Регистрация':
            line = str('\n'+ str(message.from_user) + ' - ' + str(message.chat.id))
            with open('users.txt', 'a', encoding='utf-8') as f:
                f.write(line)
            f.close()
            getnamemsg = tb.send_message(message.chat.id, "Здравствуйте! Введите, пожалуйста, Ваше имя",
                                         reply_markup=types.ReplyKeyboardRemove())
            tb.register_next_step_handler(getnamemsg, get_name)
            tb.register_next_step_handler(getnamemsg, get_name)
        elif message.chat.id in ids:
            move(message.chat.id, 'to_admin')
        elif message.text != '/start':
            where(message.chat.id)

def get_name(message):
    cid = message.chat.id
    name= message.text
    print(cid, '-', name)
    line = str('\n'+ str(cid) + ' - ' + str(name))
    with open('coachid.txt', 'a', encoding='utf-8') as f:
        f.write(line)
    tb.send_message(message.chat.id, "Спасибо, Вы зарегистрировались в боте Onlyfits Куратор.")



# Keyboard constructor
def makeKeyboard(menu):
    mrkp = types.InlineKeyboardMarkup(row_width=2)
    print(keyboards[menu])
    print(type(keyboards[menu]))
    for key, value in keyboards[menu].items():
        mrkp.add(types.InlineKeyboardButton(text=value, callback_data=key))
    return mrkp

def makeQuestionKeyboard(options_dict):
    mrkp = types.InlineKeyboardMarkup(row_width=2)
    for key, value in options_dict.items():
        mrkp.add(types.InlineKeyboardButton(text=value, callback_data=key))
    return mrkp


# Menu buttons

itembtn0 = types.KeyboardButton('Регистрация')
markup0 = types.ReplyKeyboardMarkup(row_width=2)
markup0.add(itembtn0)

keyboards = {'admin': {'send_message': 'Отправить сообщение',
                       'send_resources': 'Отправить материалы',
                       'databasedump': 'Дамп',
                       'eraseresults': 'Удалить результаты тестов',
                       'to_main': 'Главное меню'},

             'main': {'to_resources':' Материалы Программы',
                      'to_clients': 'Мои клиенты'
                      },

             'clients': {},

             'tests': {'totest_eat26': 'Отношение к Питанию',
                       'totest_main': 'Общий Тест',
                       'totest_bdi': 'Настроение'
                       },

             'resources': {
                            'get_intro': 'Вступление',
                            'get_reporting': 'Руководство по Отчётности',
                            'get_balanceddiet': 'Сбалансированный Рацион',
                            'get_portions': 'Система Порций',
                            'get_hplowgi': 'HP low-GI Рацион',
                            'get_energybalance':'Энергетический Баланс',
                            'get_physact': 'Физическая Активность',
                            'get_ro3': 'План Питания "Правило Трёх" ',
                            'get_generaltech': 'Общие техники и принципы проведения консультаций',
                            'to_main': 'Главное меню'
                           }
             }


def test_mainscreen(message):
    line = str('\n'+ get_time() + ' ' + str(message.from_user) + ' - ' + str(message.chat.id))
    with open('users.txt', 'a', encoding='utf-8') as f:
        f.write(line)
    f.close()

    line = str(get_time() + str(message.from_user.id) + ' ' + str(message.from_user.username) +
               ' ' + ' entered test mainscreen' + '\n')
    print(line)
    with open('log.txt', 'a', encoding='utf-8') as f:
        f.write(line)
        f.close()
    tb.send_message(3755631, line)
    if message.from_user.id not in current_users:
        current_users[message.from_user.id] = {x: dict(responses = pd.DataFrame(), current_question_index = 0) for x in tests}
        current_users[message.from_user.id]['log'] = str()
        current_users[message.from_user.id]['tests_to_do'] = tests
        current_users[message.from_user.id]['current_test'] = str()
        current_users[message.from_user.id]['current_question_code'] = str()
        current_users[message.from_user.id]['main']['responses']['client_telegram_id'] = [str(message.from_user.id)]
        current_users[message.from_user.id]['eat26']['responses']['client_telegram_id'] = [str(message.from_user.id)]
        current_users[message.from_user.id]['bdi']['responses']['client_telegram_id'] = [str(message.from_user.id)]
        current_users[message.from_user.id]['main']['responses']['client_telegram_first_name'] = [str(message.from_user.first_name)]
        current_users[message.from_user.id]['main']['responses']['client_telegram_last_name'] = [str(message.from_user.last_name)]
        current_users[message.from_user.id]['main']['responses']['client_telegram_username'] = [str(message.from_user.username)]
        print(current_users)
        print(message.from_user.id)
        now = datetime.now()
        now_h = now.strftime("%d-%m-%Y")
        user_main_test_file_name = 'user_test_responses/' + str(message.from_user.id) + '_' + 'main' + '_' + now_h
        current_users[message.from_user.id]['main']['responses'].to_csv(user_main_test_file_name)
        user_eat26_test_file_name = 'user_test_responses/' + str(message.from_user.id) + '_' + 'eat26' + '_' + now_h
        current_users[message.from_user.id]['main']['responses'].to_csv(user_eat26_test_file_name)
        user_bdi_test_file_name = 'user_test_responses/' + str(message.from_user.id) + '_' + 'bdi' + '_' + now_h
        current_users[message.from_user.id]['main']['responses'].to_csv(user_bdi_test_file_name)
    tb.send_message(message.chat.id, "Пройдите, пожалуйста, все три теста: ", reply_markup=makeKeyboard('tests'),
                            parse_mode='HTML')

def question_generator(usr, test):

    question_options = {}
    user_test_dict = current_users[usr]
    print(user_test_dict)
    requested_test = test.split('_')[1]
    test_data_dict = tests_dict[requested_test]
    test_convert = test_data_dict['convert']
    test_keys = test_data_dict['keys']
    current_question_row = test_convert.iloc[user_test_dict[requested_test]['current_question_index'],:]
    current_question_code = current_question_row['Number']
    current_question = current_question_row['Question']
    current_question_type = current_question_row['subscale']
    line = str(get_time() + ' ' + str(usr) + ' '
               + ' in test ' + requested_test + ' on question '
               + current_question_code + '\n')
    print(line)
    with open('log.txt', 'a', encoding='utf-8') as f:
        f.write(line)
        f.close()
    tb.send_message(3755631, line)

    if current_question_type == 'text':
        current_users[usr]['current_test'] = requested_test
        current_users[usr]['current_question_code'] = current_question_code
        gettextanswer = tb.send_message(usr, text = current_question)
        tb.register_next_step_handler(gettextanswer, save_text_answer)

    elif current_question_type == 'multiple':
        tb.send_message(usr, text = current_question)
        user_test_dict[requested_test]['current_question_index'] += 1
        current_users[usr] = user_test_dict
        question_generator(usr, test)

    elif current_question_type == 'date':
        current_users[usr]['current_test'] = requested_test
        current_users[usr]['current_question_code'] = current_question_code
        gettextanswer = tb.send_message(usr, text = current_question)
        tb.register_next_step_handler(gettextanswer, check_answer)

    else:
        option_string = 'abcdefg'
        for option in option_string:
            if not pd.isnull(current_question_row[option]):
                question_option_key = 'questionanswered' + '_' + str(requested_test)+ '_' + \
                                      str(current_question_code) + '_' + str(option)
                question_option_value = current_question_row[option]
                question_options[question_option_key] = question_option_value
                print(question_options)
        tb.send_message(usr, text = current_question, reply_markup=makeQuestionKeyboard(question_options),
                                parse_mode='HTML')

def check_answer(message):
    if '/' in message.text:
        save_text_answer(message)
    else:
        tb.send_message(message.from_user.id, text = 'Не удалось прочесть дату рождения.'
                                    '\n\nВведите, пожалуйста дату в формате ДД/ММ/ГГГГ,'
                                    'где ДД - день (например 02 - это второе число) и так далее'
                                    'Должно получиться что-то вроде 02/01/2000 - это второе января 2000 года'
                                    '\n\nСпасибо!')
        current_test = current_users[message.from_user.id]['current_test']
        current_test_for_question_generator = 'totest_' + current_test
        question_generator(message.from_user.id, current_test_for_question_generator)


def save_text_answer(message):
    print('save_text_answer function active')
    current_test = current_users[message.from_user.id]['current_test']
    current_question_code = current_users[message.from_user.id]['current_question_code']
    answer_text = message.text
    answer = 'questionanswered' + '_' + str(current_test) + '_' + \
             str(current_question_code) + '_' + str(answer_text)
    print(answer)
    save_answer(message.from_user.id, answer)

def save_answer(usr, answer):
    print('save_answer function active')
    tests_left_dict = {}
    answer_data = answer.split('_')
    answered_test_name = answer_data[1]
    answered_question_code = answer_data[2]
    option_selected = answer_data[3]
    user_test_dict = current_users[usr]
    test_data_dict = tests_dict[answered_test_name]
    test_convert = test_data_dict['convert']
    current_question_row = test_convert.iloc[user_test_dict[answered_test_name]['current_question_index'],:]
    current_question_code = current_question_row['Number']

    line = str(get_time() + ' ' + str(usr) + ' '
               + ' answered test ' + answered_test_name + ' question '
               + answered_question_code + '\n')
    print(line)
    with open('log.txt', 'a', encoding='utf-8') as f:
        f.write(line)
        f.close()
    tb.send_message(3755631, line)

    if answered_question_code == current_question_code:
        answers_df = user_test_dict[answered_test_name]['responses']
        answers_df[answered_question_code] = option_selected
        user_test_dict[answered_test_name]['current_question_index'] += 1
        if user_test_dict[answered_test_name]['current_question_index'] == len(test_convert):
            user_test_dict[answered_test_name]['current_question_index'] = 0
            print(user_test_dict['tests_to_do'])
            print(answered_test_name)
            user_test_dict['tests_to_do'].remove(answered_test_name)
            tests_left = user_test_dict['tests_to_do']
            for test in tests_left:
                test_key = str('totest_' + test)
                tests_left_dict[test_key] = keyboards['tests'][test_key]
            current_users[usr] = user_test_dict
            with open('current_clients.pkl', 'wb') as f:
                pickle.dump(current_users, f)
            if tests_left == []:
                get_results = {'gettestresults': 'Ваша Индивидуальная Программа ONLYFITS.you'}
                tb.send_message(usr, text = "Спасибо, вы прошли все тесты",
                            reply_markup=makeQuestionKeyboard(get_results),
                            parse_mode='HTML')
                current_users[usr]['tests_to_do'] = tests
                line = str(get_time() + ' ' + str(usr) + ' '
                    + ' completed all tests ' + '\n')
                print(line)
                with open('log.txt', 'a', encoding='utf-8') as f:
                    f.write(line)
                    f.close()
                tb.send_message(3755631, line)
            else:
                tb.send_message(usr, text = "Спасибо, вы прошли тест " +
                                        keyboards['tests'][str('totest_' + answered_test_name)],
                            reply_markup=makeQuestionKeyboard(tests_left_dict),
                            parse_mode='HTML')
                line = str(get_time() + ' ' + str(usr) + ' '
                    + ' completed test '
                    + answered_test_name + '\n')
                print(line)
                with open('log.txt', 'a', encoding='utf-8') as f:
                    f.write(line)
                    f.close()
                tb.send_message(3755631, line)
            now = datetime.now()
            now_h = now.strftime("%d-%m-%Y")
            user_test_result_file_name = 'user_test_responses/' + str(usr) + '_' + answered_test_name + '_' + now_h
            user_test_dict[answered_test_name]['responses'].to_csv(user_test_result_file_name)
        else:
            test = 'totest_' + answered_test_name
            current_users[usr] = user_test_dict
            with open('current_clients.pkl', 'wb') as f:
                pickle.dump(current_users, f)
            question_generator(usr, test)


def gettestresults(usr, call):
    eat26_results = current_users[usr]['eat26']['responses']
    main_results = current_users[usr]['main']['responses']
    bdi_results = current_users[usr]['bdi']['responses']
    welcome = welcome_client(eat26_results, main_results, bdi_results)
    welcome_message = welcome['welcome_message']
    tb.send_message(usr, text=welcome_message)
    line = str(get_time() + ' ' + str(usr) + ' '
        + ' requested results and received welcome' + '\n')
    print(line)
    with open('log.txt', 'a', encoding='utf-8') as f:
        f.write(line)
        f.close()
    tb.send_message(3755631, line)

#Menus
def where(usr):
    move_to_menu = trenerskaya[usr]['menu_cur']
    message_to_delete = trenerskaya[usr]['message_to_delete']
    if message_to_delete != 0:
        tb.delete_message(usr, message_to_delete)
    if move_to_menu == 'clients':
        path = str(clients_folder + '/')
        client_profiles = os.listdir(path)
        if '.DS_Store' in client_profiles:
            client_profiles.remove('.DS_Store')
            print('ds store removed')
        client_dict = {}
        for client_file in client_profiles:
            if client_file.endswith('.rs'):
                client_button = client_file[:-3]
                client_profile_call = 'getprofile_' + client_file
                client_dict[client_profile_call] = client_button
        client_dict['to_main'] = 'Главное меню'
        print(client_dict)
        keyboards['clients'] = client_dict

    message_sent = tb.send_message(chat_id=usr,
                              text = 'Меню',
                              reply_markup= makeKeyboard(move_to_menu),
                              parse_mode='HTML')
    trenerskaya[usr]['message_to_delete'] = message_sent.message_id
    print(message_to_delete)
    print(message_sent.message_id)



# Обрабатывает перемещения по меню
def move(usr, menu):
    if not (trenerskaya[usr]['menu_cur'] == menu.split('_')[1]):
        trenerskaya[usr]['menu_prev'] = trenerskaya[usr]['menu_cur']
        trenerskaya[usr]['menu_cur'] = menu.split('_')[1]
    trenerskaya[usr]['log'] = str(get_time() + ' ' + trenerskaya[usr]['name'] +
                                  ' moved ' + trenerskaya[usr]['menu_prev'] +
                                  ' > ' + trenerskaya[usr]['menu_cur'])

    tb.send_message(3755631, trenerskaya[usr]['log'])
    line = str(trenerskaya[usr]['log'] + '\n')
    print(line)
    with open('log.txt', 'a', encoding='utf-8') as f:
        f.write(line)
    f.close()
    where(usr)




#CallBack Handler

@tb.callback_query_handler(func=lambda call: call.from_user.id not in coaches.keys())
def call_from_user(call):
    if call.data.startswith('totest_'):
        question_generator(call.from_user.id, call.data)
        tb.answer_callback_query(call.id, '\U0000231B')
    elif call.data.startswith('questionanswered_'):
        save_answer(call.from_user.id, call.data)
        tb.answer_callback_query(call.id, '\U0000231B')
    elif call.data.startswith('gettestresults'):
        gettestresults(call.from_user.id, call.data)
        tb.answer_callback_query(call.id, '\U0000231B')

# Обрабатывает нажатия кнопок кураторами
@tb.callback_query_handler(func=lambda call: call.from_user.id in coaches.keys())
def call_from_coach(call):
    if call.data.startswith('to_'):
        move(call.from_user.id, call.data)
        tb.answer_callback_query(call.id, '\U0001F4D6')
    elif call.data.startswith('get_'):
        send_file(call.from_user.id, call.data)
        tb.answer_callback_query(call.id, '\U0000231B')
    elif call.data.startswith('getprofile_'):
        get_profile(call.from_user.id, call.data)
        tb.answer_callback_query(call.id, '\U0000231B')
    elif call.data.startswith('totest_'):
        question_generator(call.from_user.id, call.data)
        tb.answer_callback_query(call.id, '\U0000231B')
    elif call.data.startswith('questionanswered_'):
        save_answer(call.from_user.id, call.data)
        tb.answer_callback_query(call.id, '\U0000231B')
    elif call.data.startswith('gettestresults'):
        gettestresults(call.from_user.id, call.data)
        tb.answer_callback_query(call.id, '\U0000231B')
    elif call.data.startswith('databasedump'):
        database_dump(call.from_user.id, call.data)
        tb.answer_callback_query(call.id, '\U0000231B')
    elif call.data.startswith('erase_'):
        erase_results(call.from_user, call.data)
        tb.answer_callback_query(call.id, '\U0000231B')
    elif call.data.startswith('eraseresults'):
        erase_results_menu(call.from_user.id, call.data)
        tb.answer_callback_query(call.id, '\U0000231B')
    elif call.data == 'send_resources':
        print('send resources command')
        for i in coaches.keys():
            print('sending to ' + coaches[i])
            tb.send_message(chat_id=i,
                            text = 'Меню', reply_markup=makeKeyboard('main'),
                            parse_mode='HTML')
    elif call.data == 'send_message':
        print('send message command')
        tb.answer_callback_query(call.id, '\U00002709')
        greet = tb.send_message(chat_id=call.from_user.id,
                            text = 'Сообщение:')
        tb.register_next_step_handler(greet, send_text_msg)

def send_text_msg(msg):
    for i in coaches.keys():
            print('sending to ' + coaches[i])
            tb.send_message(chat_id=i,
                            text = msg.text)
    trenerskaya[msg.chat.id]['log'] = str(get_time() + ' ' +
                                          trenerskaya[msg.chat.id]['name'] +
                                          ' sent ' + msg.text + ' to coaches')

    line = str(trenerskaya[msg.chat.id]['log'] + '\n')
    print(line)
    tb.send_message(3755631, trenerskaya[msg.chat.id]['log'])
    with open('log.txt', 'a', encoding='utf-8') as f:
        f.write(line)
        f.close()

#Send files
def send_file(usr, file):
    print(file)
    path = str(files_folder + file.split('_')[1] + '/')
    get_doc = os.listdir(path)
    print(get_doc)
    if '.DS_Store' in get_doc:
        get_doc.remove('.DS_Store')
        print('ds store removed')
    get_doc = str(path + get_doc[0])
    print(get_doc)
    doc = open(get_doc, 'rb')
    tb.send_document(usr, doc)
    doc.close()
    trenerskaya[usr]['log'] = str(get_time() + ' ' +
                                  trenerskaya[usr]['name'] + ' requested file ' + get_doc)

    tb.send_message(3755631, trenerskaya[usr]['log'])
    line = str(trenerskaya[usr]['log'] + '\n')
    print(line)
    with open('log.txt', 'a', encoding='utf-8') as f:
        f.write(line)
        f.close()


# Get user profiles

def get_profile(usr, profile):
    path = str(clients_folder + profile.split('_')[1])
    with open(path, 'r') as file:
        profile_text = file.read().replace('\n', '\n\n')
    tb.send_message(usr, profile_text)
    trenerskaya[usr]['log'] = str(get_time() + ' ' +
                                  trenerskaya[usr]['name'] +
                                  ' requested profile ' + profile.split('_')[1])
    tb.send_message(3755631, trenerskaya[usr]['log'])
    line = str(trenerskaya[usr]['log'] + '\n')
    print(line)
    with open('log.txt', 'a', encoding='utf-8') as f:
        f.write(line)
        f.close()
#Next Step Handler
tb.enable_save_next_step_handlers(delay=2)
tb.load_next_step_handlers()


# Get Updates
tb.set_update_listener(handle_messages)
tb.infinity_polling()
