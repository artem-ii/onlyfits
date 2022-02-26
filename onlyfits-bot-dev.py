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
from clients import *


current_clients_db = 'current_clients_dev.pkl'
coaches_db = 'coaches_db_dev.pkl'

current_users = {'init':'init'}
with open(current_clients_db, 'wb') as f:
    pickle.dump(current_users, f)
dump_reply = 'dump complete'
#tb.send_message(usr, text=str(current_users) + dump_reply)

with open(current_clients_db, 'rb') as f:
    current_users = pickle.load(f)

print(current_users)


def get_time():
    now = datetime.now()
    now_h = now.strftime("%d/%m/%Y %H:%M:%S")
    return now_h

TOKEN = "5118074175:AAGdSNqLzaRCEWw5wR1XNH_5v5wF1e8eq1M"
testTOKEN = "288367920:AAEuc2Lqw94_jG3Qi0j_7Uqh4FSuGKHl-zw"
tb = telebot.TeleBot(testTOKEN)

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

nutri_convert = pd.read_csv(
    '/Users/artemii/OneDrive/Documents/ONLYFITS/program-design-jan-2022/bot/report_tests/nutri_report.csv',
    sep = ';', dtype = str)
psy_convert = pd.read_csv(
    '/Users/artemii/OneDrive/Documents/ONLYFITS/program-design-jan-2022/bot/report_tests/nutri_report.csv',
    sep = ';', dtype = str)
first_convert = pd.read_csv(
    '/Users/artemii/OneDrive/Documents/ONLYFITS/program-design-jan-2022/bot/report_tests/nutri_report.csv',
    sep = ';', dtype = str)
second_convert = pd.read_csv(
    '/Users/artemii/OneDrive/Documents/ONLYFITS/program-design-jan-2022/bot/report_tests/nutri_report.csv',
    sep = ';', dtype = str)
last_convert = pd.read_csv(
    '/Users/artemii/OneDrive/Documents/ONLYFITS/program-design-jan-2022/bot/report_tests/nutri_report.csv',
    sep = ';', dtype = str)


# User id info
coaches_real = {520834290:"Ксения Календарева", 594759110:"Елена", 1472202629:"trener.idel",
           541765907:"Дарья", 141659022:"Янина", 287460510:"Ирина",
           409750031:"Анастасия", 310119054:"Наталья Лаврененко",
           3755631:"Artemii", 2019105955:"Artemii Nikitin",
           970257969: "Наталья Минажетдинова", 388199486: "Артем"}

coaches = {3755631:"Artemii"}
#, 2019105955:"Artemii Nikitin"}

ids = [3755631]
#, 2019105955]


# User State dictionary
trenerskaya = {x: dict(name=coaches[x], menu_cur='main',
                       menu_prev=str(), clients=clients_dict[coaches[x]], consult_mode=False,
                       message_to_delete=0, consult_test_index=0,
                       log=str()) for x in (coaches.keys())}
print(trenerskaya)


tests_dict = {'eat26':{'convert': eat26_convert, 'keys': eat26_keys},
              'main':{'convert': main_convert, 'keys': main_keys},
              'bdi':{'convert': bdi_convert, 'keys': bdi_keys}}

report_tests_dict = {'nutri':{'name': 'Питание и активность', 'convert': nutri_convert, 'keys': eat26_keys},
                     'first':{'name': 'Первая консультация', 'convert': first_convert, 'keys': main_keys},
                     'second':{'name': 'Вторая консультация', 'convert': second_convert, 'keys': main_keys},
                     'psy':{'name': 'Навыки', 'convert': psy_convert, 'keys': main_keys},
                     'last':{'name': 'Заключительная консультация', 'convert': last_convert, 'keys': bdi_keys}}

consult_type_dict = {
        'initconsult_first': 'Первая консультация',
        'initconsult_second': 'Вторая консультация',
        'initconsult_last': 'Заключительная консультация',
        'initconsult_nutri': 'Питание и активность',
        'initconsult_psy': 'Навыки',
        'consult': 'Назад',
        'to_main': 'Главное меню'
        }



#@tb.message_handler(func=lambda message: trenerskaya[message.from_user.id]['consult_mode'] == True)




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
        if trenerskaya[message.from_user.id]['consult_mode']:
            handle_report_notes(message)
        elif message.text == 'database_dump_2929':
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
                      'to_clients': 'Мои клиенты',
                      'consult': 'Начать консультацию'
                      },

             'clients': {},

             'reports': {},

             'tests': {'totest_eat26': 'Отношение к Питанию',
                       'totest_main': 'Общий Тест',
                       'totest_bdi': 'Настроение'
                       },

             'resources': {'to_coachres': 'Материалы для кураторов',
                           'to_clientres': 'Материалы для клиентов'
                           },

             'coachres': {'to_generalres': 'Общие материалы',
                            'to_nutrires': 'Материалы по питанию и активности',
                            'to_main': 'Главное меню'
                            },
             'generalres': {'get_intro': 'Вступление',
                            'get_reporting': 'Руководство по Отчётности',
                            'get_generaltech': 'Общие техники и принципы проведения консультаций',
                            'get_firstconsult': 'Первая консультация',
                            'get_secondconsult': 'Вторая консультация',
                            'to_coachres': 'Назад',
                            'to_main': 'Главное меню'
                            },
             'nutrires': {'get_balanceddiet': 'Сбалансированный Рацион',
                            'get_portions': 'Система Порций',
                            'get_hplowgi': 'HP low-GI Рацион',
                            'get_energybalance':'Энергетический Баланс',
                            'get_physact': 'Физическая Активность',
                            'get_ro3': 'План Питания "Правило Трёх" ',
                            'to_coachres': 'Назад',
                            'to_main': 'Главное меню'
                          },
             'clientres': {'get_client1': 'Д/з Первая консультация',
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
        current_users[message.from_user.id]['message_to_delete'] = 0
        current_users[message.from_user.id]['current_question_code'] = str()
        current_users[message.from_user.id]['main']['responses']['client_telegram_id'] = [str(message.from_user.id)]
        current_users[message.from_user.id]['eat26']['responses']['client_telegram_id'] = [str(message.from_user.id)]
        current_users[message.from_user.id]['bdi']['responses']['client_telegram_id'] = [str(message.from_user.id)]
        current_users[message.from_user.id]['main']['responses']['client_telegram_first_name'] = [str(message.from_user.first_name)]
        current_users[message.from_user.id]['main']['responses']['client_telegram_last_name'] = [str(message.from_user.last_name)]
        current_users[message.from_user.id]['main']['responses']['client_telegram_username'] = [str(message.from_user.username)]
        current_users[message.from_user.id]['message_to_delete'] = 0
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
    current_users[message.from_user.id]['message_to_delete'] = 0
    sent_message = tb.send_message(message.chat.id, "Пройдите, пожалуйста, все три теста: ",
                                   reply_markup=makeKeyboard('tests'),
                                   parse_mode='HTML')
    current_users[message.from_user.id]['message_to_delete'] = sent_message.message_id


def question_generator(usr, test):

    if 'message_to_delete' in current_users[usr].keys():
        message_to_delete = current_users[usr]['message_to_delete']
    else:
        current_users[usr]['message_to_delete'] = 0
        message_to_delete = current_users[usr]['message_to_delete']

    question_options = {}
    user_test_dict = current_users[usr]
    print(user_test_dict)
    requested_test = test.split('_')[1]
    test_data_dict = tests_dict[requested_test]
    test_convert = test_data_dict['convert']
    test_keys = test_data_dict['keys']
    current_question_row = test_convert.iloc[user_test_dict[requested_test]['current_question_index'],:]
    current_users[usr]['current_test'] = requested_test
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
        if message_to_delete not in [-1, 0]:
            tb.delete_message(usr, message_to_delete)
        current_users[usr]['current_test'] = requested_test
        current_users[usr]['current_question_code'] = current_question_code
        gettextanswer = tb.send_message(usr, text = current_question)
        current_users[usr]['message_to_delete'] = gettextanswer.message_id
        tb.register_next_step_handler(gettextanswer, save_text_answer)

    elif current_question_type == 'multiple':
        tb.send_message(usr, text = current_question)
        user_test_dict[requested_test]['current_question_index'] += 1
        current_users[usr] = user_test_dict
        question_generator(usr, test)

    elif current_question_type == 'date':
        if message_to_delete not in [-1, 0]:
            tb.delete_message(usr, message_to_delete)
        current_users[usr]['current_test'] = requested_test
        current_users[usr]['current_question_code'] = current_question_code
        gettextanswer = tb.send_message(usr, text = current_question)
        current_users[usr]['message_to_delete'] = gettextanswer.message_id
        tb.register_next_step_handler(gettextanswer, check_answer)

    else:
        if message_to_delete not in [-1, 0]:
            tb.delete_message(usr, message_to_delete)
        option_string = 'abcdefg'
        for option in option_string:
            if not pd.isnull(current_question_row[option]):
                question_option_key = 'questionanswered' + '_' + str(requested_test)+ '_' + \
                                      str(current_question_code) + '_' + str(option)
                question_option_value = current_question_row[option]
                question_options[question_option_key] = question_option_value
        question_options['questionanswered_' + str(requested_test) + '_' +
                         'qback' + '_' +
                         str(user_test_dict[requested_test]['current_question_index'])] = 'К предыдущему вопросу'
        #question_options['testmenu'] = 'К меню с тестами'
        print(question_options)
        message_sent = tb.send_message(usr, text = current_question,
                                       reply_markup=makeQuestionKeyboard(question_options),
                                       parse_mode='HTML')
        current_users[usr]['message_to_delete'] = message_sent.message_id


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
    usr = message.from_user.id
    if current_users[usr]['message_to_delete'] != 0:
        message_to_delete = current_users[usr]['message_to_delete']
        tb.delete_message(usr, message_to_delete)
        tb.delete_message(usr, message_to_delete + 1)
        current_users[usr]['message_to_delete'] = -1


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
    user_test_dict = current_users[usr]
    tests_left_dict = {}
    answer_data = answer.split('_')
    if answer_data[2] == 'qback':
        current_test = answer_data[1]
        user_test_dict[current_test]['current_question_index'] -= 1
        test = 'totest_' + current_test
        question_generator(usr, test)
    else:
        answered_test_name = answer_data[1]
        answered_question_code = answer_data[2]
        option_selected = answer_data[3]

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
                with open(current_clients_db, 'wb') as f:
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
                with open(current_clients_db, 'wb') as f:
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
    message_text = 'Меню'
    move_to_menu = trenerskaya[usr]['menu_cur']
    message_to_delete = trenerskaya[usr]['message_to_delete']
    if message_to_delete != 0:
        tb.delete_message(usr, message_to_delete)
    if move_to_menu == 'main':
        trenerskaya[usr]['consult_mode'] = False
    if move_to_menu == 'clients':
        message_text = 'Список клиентов'
        path = str(clients_folder + '/')
        client_profiles = os.listdir(path)
        coach_clients = trenerskaya[usr]['clients']
        if '.DS_Store' in client_profiles:
            client_profiles.remove('.DS_Store')
            print('ds store removed')
        coach_client_profiles = []
        for profile in client_profiles:
            if profile[:-3] in coach_clients:
                coach_client_profiles.append(profile)
        client_dict = {}
        for client_file in coach_client_profiles:
            if client_file.endswith('.rs'):
                client_button = client_file[:-3]
                client_profile_call = 'getprofile_' + client_button
                client_dict[client_profile_call] = client_button
        client_dict['to_main'] = 'Главное меню'
        print(client_dict)
        keyboards['clients'] = client_dict
    elif move_to_menu == 'reports':
        message_text = 'Отчёты консультаций клиента ' + trenerskaya[usr]['current_client']
        requested_client_code = trenerskaya[usr]['current_client']
        client_reports_folder = os.path.join(clients_folder,
                               'consult_reports',
                               requested_client_code)
        client_reports = os.listdir(client_reports_folder)
        if '.DS_Store' in client_reports:
            client_reports.remove('.DS_Store')
            print('ds store removed')
        report_type_keyboard = {}
        nutri_reports = []
        psy_reports = []
        first_report = []
        second_report = []
        last_report = []
        for file in client_reports:
            if file.endswith('.rp'):
                if 'nutri' in file:
                    nutri_reports.append(file)
                elif 'psy' in file:
                    psy_reports.append(file)
                elif 'first' in file:
                    first_report.append(file)
                elif 'second' in file:
                    second_report.append(file)
                elif 'last' in file:
                    last_report.append(file)
        trenerskaya[usr]['current_client_reports'] = {}
        trenerskaya[usr]['current_client_reports']['nutri'] = nutri_reports
        trenerskaya[usr]['current_client_reports']['psy'] = psy_reports
        trenerskaya[usr]['current_client_reports']['first'] = first_report
        trenerskaya[usr]['current_client_reports']['second'] = second_report
        trenerskaya[usr]['current_client_reports']['last'] = last_report

        for report_type in trenerskaya[usr]['current_client_reports'].keys():
            if len(trenerskaya[usr]['current_client_reports'][report_type]) > 0:
                report_type_keyboard['getreportslist_' + report_type] =\
                    report_tests_dict[report_type]['name']
        last_selected_client = trenerskaya[usr]['current_client']
        report_type_keyboard['getprofile_' + last_selected_client] = 'Назад'
        keyboards['reports'] = report_type_keyboard

    message_sent = tb.send_message(chat_id=usr,
                                   text=message_text,
                                   reply_markup=makeKeyboard(move_to_menu),
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

    if len(menu.split('_')) > 2:
        trenerskaya[usr]['current_client'] = menu.split('_')[2]
    tb.send_message(3755631, trenerskaya[usr]['log'])
    line = str(trenerskaya[usr]['log'] + '\n')
    print(line)
    with open('log.txt', 'a', encoding='utf-8') as f:
        f.write(line)
    f.close()
    where(usr)





def send_text_msg(msg):
    for i in coaches.keys():
            print('sending to ' + coaches[i])
#            m = \
            tb.send_message(chat_id=i,
                                text = msg.text)
#                            ,
# Добавляю это для одного раза, чтобы убрать кнопку регистрация у кураторов
#                                reply_markup=types.ReplyKeyboardRemove())
#            tb.delete_message(i, m.message_id)
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

    for file in get_doc:
        get_doc = str(path + file)
        print(file)
        doc = open(get_doc, 'rb')
        tb.send_document(usr, doc)
        doc.close()
        trenerskaya[usr]['log'] = str(get_time() + ' ' +
                                      trenerskaya[usr]['name'] + ' requested file ' + file)
        tb.send_message(3755631, trenerskaya[usr]['log'])
        line = str(trenerskaya[usr]['log'] + '\n')
        print(line)
        with open('log.txt', 'a', encoding='utf-8') as f:
            f.write(line)
            f.close()


# Get user profiles and consultation reports

def get_client_page(usr, client):
    print(trenerskaya)
    message_to_delete = trenerskaya[usr]['message_to_delete']
    if message_to_delete != 0:
        tb.delete_message(usr, message_to_delete)
    requested_client_code = client.split('_')[1]
    path = os.path.join(clients_folder, 'consult_reports', requested_client_code)
    os.makedirs(path, exist_ok=True)
    reports_folder = os.path.join(clients_folder,
                                  'consult_reports')
    client_reports_list = os.listdir(reports_folder)
    if requested_client_code in client_reports_list:
        client_page_keyboard = {'getprofiletext_' + requested_client_code: 'Профиль',
                                'to_reports_' + requested_client_code: 'Отчёты о консультациях'}
    else:
        client_page_keyboard = {'getprofiletext_' + requested_client_code: 'Профиль'}
    if trenerskaya[usr]['consult_mode']:
        consult_type = trenerskaya[usr]['consult_type']
        client_page_keyboard['initconsult_' + consult_type] = 'Назад'
    else:
        client_page_keyboard['to_clients'] = 'Назад'
    message_sent = tb.send_message(chat_id=usr,
                                   text='Меню клиента ' + requested_client_code,
                                   reply_markup=makeQuestionKeyboard(client_page_keyboard),
                                   parse_mode='HTML')
    trenerskaya[usr]['message_to_delete'] = message_sent.message_id

def get_reports_list(usr, type):
    message_to_delete = trenerskaya[usr]['message_to_delete']
    if message_to_delete != 0:
        tb.delete_message(usr, message_to_delete)
    report_type = type.split('_')[1]
    trenerskaya[usr]['last_report_type_selected'] = report_type
    report_files = trenerskaya[usr]['current_client_reports'][report_type]
    client_reports_oftype_keyboard = {}
    for report_file in report_files:
        client_reports_oftype_keyboard['getreporttext_' + report_file] = report_file[:-3]
    client_reports_oftype_keyboard['to_reports'] = 'Назад'
    report_type_name = report_tests_dict[report_type]['name']
    message_sent = tb.send_message(chat_id=usr,
                                   text='Отчёты ' + report_type_name,
                                   reply_markup=makeQuestionKeyboard(client_reports_oftype_keyboard),
                                   parse_mode='HTML')
    trenerskaya[usr]['message_to_delete'] = message_sent.message_id

def get_report(usr, report_name):
    current_client = trenerskaya[usr]['current_client']
    report_file_name = report_name.split('_')[1]
    print(report_file_name)
    message_to_delete = trenerskaya[usr]['message_to_delete']
    if message_to_delete != 0:
        tb.delete_message(usr, message_to_delete)
    report_file_path = os.path.join(clients_folder,
                               'consult_reports',
                               current_client,
                               report_file_name)
    with open(report_file_path, 'r') as file:
        report_text = file.read().replace('\n', '\n\n')
    last_report_type_selected = trenerskaya[usr]['last_report_type_selected']
    back_button = {'getreportslist_' + last_report_type_selected: 'К списку отчётов'}
    message_sent = tb.send_message(usr, report_text,
                                   reply_markup=makeQuestionKeyboard(back_button))
    trenerskaya[usr]['message_to_delete'] = message_sent.message_id

def get_profile(usr, profile):
    message_to_delete = trenerskaya[usr]['message_to_delete']
    if message_to_delete != 0:
        tb.delete_message(usr, message_to_delete)
    current_client_code = profile.split('_')[1]
    path = str(clients_folder + profile.split('_')[1] + '.rs')
    with open(path, 'r') as file:
        profile_text = file.read().replace('\n', '\n\n')
    back_button = {'getprofile_' + current_client_code: 'Назад'}
    if trenerskaya[usr]['consult_mode']:
        consult_type = trenerskaya[usr]['consult_type']
        options_consult = {'taskforclient': 'Отправить материалы клиенту',
                           'initconsult_' + consult_type: 'Скрыть профиль клиента',
                           'report': 'Завершить и заполнить отчёт'}
        message_sent = tb.send_message(usr, profile_text,
                                       reply_markup=makeQuestionKeyboard(options_consult))
    else:
        message_sent = tb.send_message(usr, profile_text,
                                       reply_markup=makeQuestionKeyboard(back_button))

    trenerskaya[usr]['log'] = str(get_time() + ' ' +
                                  trenerskaya[usr]['name'] +
                                  ' requested profile ' + profile.split('_')[1])
    trenerskaya[usr]['message_to_delete'] = message_sent.message_id
    tb.send_message(3755631, trenerskaya[usr]['log'])
    line = str(trenerskaya[usr]['log'] + '\n')
    print(line)
    with open('log.txt', 'a', encoding='utf-8') as f:
        f.write(line)
        f.close()

# __________________________________________________________
# Функции, которые будут обрабатывать отчёты о консультациях
def getconsultclient(usr):
    message_to_delete = trenerskaya[usr]['message_to_delete']
    if message_to_delete != 0:
        tb.delete_message(usr, message_to_delete)

    coach_name = coaches[usr]
    coach_clients = trenerskaya[usr]['clients']
    coach_clients_dict = {}
    for client in coach_clients:
        coach_clients_dict['consultwithclient_' + client] = client
    coach_clients_dict['to_main'] = 'Назад'
    sent_message = tb.send_message(usr, 'Выберите, пожалуйста, клиента',
                                   reply_markup=makeQuestionKeyboard(coach_clients_dict),
                                   parse_mode='HTML')
    trenerskaya[usr]['message_to_delete'] = sent_message.message_id


def getconsulttype(usr, client_call):
    message_to_delete = trenerskaya[usr]['message_to_delete']
    if message_to_delete != 0:
        tb.delete_message(usr, message_to_delete)
    current_client = client_call.split('_')[1]
    trenerskaya[usr]['current_client'] = current_client
    sent_message = tb.send_message(usr, 'Выберите, пожалуйста, тип консультации',
                                   reply_markup=makeQuestionKeyboard(consult_type_dict),
                                   parse_mode='HTML')
    trenerskaya[usr]['message_to_delete'] = sent_message.message_id


def consult_init(usr, init_call):
    message_to_delete = trenerskaya[usr]['message_to_delete']
    if message_to_delete != 0:
        tb.delete_message(usr, message_to_delete)
    consult_type = init_call.split('_')[1]
    trenerskaya[usr]['consult_type'] = consult_type
    current_client = trenerskaya[usr]['current_client']
    date = datetime.now()
    date = date.strftime("%d-%m-%Y")
    consult_type_humanreadable = consult_type_dict[init_call]
    report_filename = date + '-' + consult_type + '-'\
                      + current_client + '.rp'
    path = os.path.join(clients_folder, 'consult_reports', current_client)
    report_path = os.path.join(clients_folder,
                               'consult_reports',
                               current_client,
                               report_filename)
    if not trenerskaya[usr]['consult_mode']:
        os.makedirs(path, exist_ok=True)
        first_line = 'Консультация начата ' + get_time() + '\n' +\
                     'Куратор: ' + trenerskaya[usr]['name'] + '\n' +\
                     'Клиент: ' + trenerskaya[usr]['current_client'] + '\n' +\
                     'Тип консультации: ' + consult_type_humanreadable
        with open(report_path,  'a', encoding='utf-8') as report:
            report.write(first_line)
            report.close()
        trenerskaya[usr]['consult_mode'] = True

    options_consult = {'taskforclient': 'Отправить материалы клиенту',
                       'getprofile_' + current_client: 'Вывести страницу клиента',
                       'report': 'Завершить и заполнить отчёт'}
    sent_message = tb.send_message(usr, "Консультация начата. Вы можете отправлять заметки, либо выбрать опцию:",
                                   reply_markup=makeQuestionKeyboard(options_consult),
                                   parse_mode="HTML")
    trenerskaya[usr]['message_to_delete'] = sent_message.message_id


def handle_report_notes(message):
    usr = message.from_user.id
    consult_type = trenerskaya[usr]['consult_type']
    current_client = trenerskaya[usr]['current_client']
    now = datetime.now()
    date = now.strftime("%d-%m-%Y")
    time = now.strftime("%H:%M:%S")
    report_filename = date + '-' + consult_type + '-'\
                      + current_client + '.rp'
    report_path = os.path.join(clients_folder,
                               'consult_reports',
                               current_client,
                               report_filename)
    note = time + ' ' + message.text
    with open(report_path,  'a', encoding='utf-8') as report:
        report.write('\n' + note + '\n')
        report.close()


def consult_test_generator(usr, call):
    message_to_delete = trenerskaya[usr]['message_to_delete']
    consult_type = trenerskaya[usr]['consult_type']
    current_client = trenerskaya[usr]['current_client']
    date = datetime.now()
    date = date.strftime("%d-%m-%Y")
    report_filename = date + '-' + consult_type + '-'\
                      + current_client + '.rp'
    report_path = os.path.join(clients_folder,
                               'consult_reports',
                               current_client,
                               report_filename)
    if trenerskaya[usr]['consult_mode']:
        last_line = 'Консультация закончена ' + get_time()
        with open(report_path,  'a', encoding='utf-8') as report:
            report.write('\n\n' + last_line)
            report.close()
        trenerskaya[usr]['consult_mode'] = False
        trenerskaya[usr]['consult_test'] = pd.DataFrame()
        trenerskaya[usr]['consult_test_index'] = 0
    test_convert = report_tests_dict[consult_type]['convert']
    current_question_row = test_convert.iloc[trenerskaya[usr]['consult_test_index'],:]
    current_question_code = current_question_row['Number']
    trenerskaya[usr]['current_question_code'] = current_question_code
    current_question = current_question_row['Question']
    current_question_type = current_question_row['type']
    line = str(get_time() + ' ' + str(usr) + ' '
               + ' in test ' + consult_type + ' on question '
               + current_question_code + '\n')
    print(line)
    with open('log.txt', 'a', encoding='utf-8') as f:
        f.write(line)
        f.close()
    tb.send_message(3755631, line)
    if message_to_delete not in [-1, 0]:
        tb.delete_message(usr, message_to_delete)
    if current_question_type == 'text':
        # if message_to_delete not in [-1, 0]:
        #     tb.delete_message(usr, message_to_delete)
        gettextanswer = tb.send_message(usr, text=current_question)
        trenerskaya[usr]['message_to_delete'] = gettextanswer.message_id
        tb.register_next_step_handler(gettextanswer, save_report_text_answer)
    else:

        options = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
        question_options = {}
        for option in options:
            if not pd.isnull(current_question_row[option]):
                question_option_key = 'reportquestionanswered' + '_' + str(consult_type)+ '_' + \
                                      str(current_question_code) + '_' + str(option)
                question_option_value = current_question_row[option]
                question_options[question_option_key] = question_option_value
#        question_options['reportquestionanswered_' + str(consult_type) + '_' +
#                         'qback' + '_' +
#                         str(trenerskaya[requested_test]['current_question_index'])] = 'К предыдущему вопросу'
        #question_options['testmenu'] = 'К меню с тестами'
        print(question_options)
        message_sent = tb.send_message(usr, text=current_question,
                                       reply_markup=makeQuestionKeyboard(question_options),
                                       parse_mode='HTML')
        trenerskaya[usr]['message_to_delete'] = message_sent.message_id


def save_report_text_answer(message):
    usr = message.from_user.id
    if trenerskaya[usr]['message_to_delete'] != 0:
        message_to_delete = trenerskaya[usr]['message_to_delete']
        tb.delete_message(usr, message_to_delete)
        tb.delete_message(usr, message_to_delete + 1)
        trenerskaya[usr]['message_to_delete'] = -1


    print('save_report_text_answer function active')
    consult_type = trenerskaya[message.from_user.id]['consult_type']
    current_question_code = trenerskaya[message.from_user.id]['current_question_code']
    answer_text = message.text
    answer = 'reportquestionanswered' + '_' + str(consult_type) + '_' + \
             str(current_question_code) + '_' + str(answer_text)
    print(answer)
    save_report_answer(message.from_user.id, answer)

def save_report_answer(usr, answer):
    print('save_report_answer function active')
    coach_test_dict = trenerskaya[usr]['consult_test']
    answer_data = answer.split('_')
    consult_type = trenerskaya[usr]['consult_type']
    client_code = trenerskaya[usr]['current_client']
    if answer_data[2] == 'qback':
        consult_type = answer_data[1]
        trenerskaya[usr]['consult_test_index'] -= 1
        question_generator(usr, 'report')
    else:
        answered_consult_type = answer_data[1]
        answered_question_code = answer_data[2]
        option_selected = answer_data[3]
        print(answered_question_code)
        print(option_selected)

        test_convert = report_tests_dict[answered_consult_type]['convert']
        current_question_row = test_convert.iloc[trenerskaya[usr]['consult_test_index'],:]
        current_question = current_question_row['Question']
        print(current_question)
        current_question_code = current_question_row['Number']
        print(current_question_code)

        line = str(get_time() + ' ' + str(usr) + ' '
                   + ' answered test in ' + answered_consult_type + ' consult. Question '
                   + answered_question_code + '\n')
        print(line)
        with open('log.txt', 'a', encoding='utf-8') as f:
            f.write(line)
            f.close()
        tb.send_message(3755631, line)

        if answered_question_code == current_question_code:
            client_code = trenerskaya[usr]['current_client']
            if 'client_code' not in coach_test_dict.columns:
                print('adding client code')
                print(client_code)
                now = datetime.now()
                date = now.strftime("%d-%m-%Y")
                coach_test_dict['date'] = [date]
                coach_test_dict['consult_type'] = [consult_type]
                coach_test_dict['client_code'] = [client_code]
            coach_test_dict[current_question] = [option_selected]
            print(coach_test_dict)
            trenerskaya[usr]['consult_test_index'] += 1
            if trenerskaya[usr]['consult_test_index'] == len(test_convert):
                trenerskaya[usr]['consult_test_index'] = 0
                trenerskaya[usr]['consult_test'] = coach_test_dict
                with open(coaches_db, 'wb') as f:
                    pickle.dump(trenerskaya, f)
                tb.send_message(usr, text = "Спасибо, отчёт сохранён.")
                line = str(get_time() + ' ' + trenerskaya[usr]['name']
                           + ' submitted report '
                           + answered_consult_type + '\n')
                print(line)
                with open('log.txt', 'a', encoding='utf-8') as f:
                    f.write(line)
                    f.close()
                tb.send_message(3755631, line)
                now = datetime.now()
                date = now.strftime("%d-%m-%Y")
                report_table_filename = date + '-' + consult_type + '-'\
                                  + client_code + '.tb'
                report_table_path = os.path.join(clients_folder,
                                                 'consult_reports',
                                                 client_code,
                                                 report_table_filename)

                report_filename = date + '-' + consult_type + '-'\
                                  + client_code + '.rp'
                report_path = os.path.join(clients_folder,
                                           'consult_reports',
                                           client_code,
                                           report_filename)
                coach_test_dict.to_csv(report_table_path)
                report_line = str()
                for question in coach_test_dict.iloc[:, 3:]:
                    report_line += question + ': ' + coach_test_dict[question].item() + '\n'
                with open(report_path,  'a', encoding='utf-8') as report:
                    report.write('\n\n' + report_line)
                    report.close()
                trenerskaya[usr]['message_to_delete'] = 0
                where(usr)
            else:
                with open(coaches_db, 'wb') as f:
                    pickle.dump(trenerskaya, f)
                consult_test_generator(usr, 'report')


# Функции для просмотра отчётов по консультациям




#
#CallBack Handler

@tb.callback_query_handler(func=lambda call: call.from_user.id not in coaches.keys())
def call_from_user(call):
    if call.data.startswith('totest_'):
        question_generator(call.from_user.id, call.data)
        tb.answer_callback_query(call.id, '\U0000231B')
    elif call.data.startswith('questionanswered_'):
        save_answer(call.from_user.id, call.data)
        if call.data.split('_')[3].isalpha():
            pop_text = 'Вы выбрали вариант ' + call.data.split('_')[3]
        else:
            toquestionnum = int(call.data.split('_')[3]) - 1
            pop_text = 'Назад к вопросу ' + str(toquestionnum)
        tb.answer_callback_query(call.id, pop_text)
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
        get_client_page(call.from_user.id, call.data)
        tb.answer_callback_query(call.id, '\U0000231B')
    elif call.data.startswith('getprofiletext_'):
        get_profile(call.from_user.id, call.data)
        tb.answer_callback_query(call.id, '\U0000231B')
    elif call.data.startswith('totest_'):
        question_generator(call.from_user.id, call.data)
        tb.answer_callback_query(call.id, '\U0000231B')
    elif call.data.startswith('questionanswered_'):
        save_answer(call.from_user.id, call.data)
        if call.data.split('_')[3].isalpha():
            pop_text = 'Вы выбрали вариант ' + call.data.split('_')[3]
        else:
            toquestionnum = int(call.data.split('_')[3]) - 1
            pop_text = 'Назад к вопросу ' + str(toquestionnum)
        tb.answer_callback_query(call.id, pop_text)
    elif call.data.startswith('gettestresults'):
        gettestresults(call.from_user.id, call.data)
        tb.answer_callback_query(call.id, '\U0000231B')
    elif call.data == 'consult':
        getconsultclient(call.from_user.id)
        tb.answer_callback_query(call.id, '\U0000231B')
    elif call.data.startswith('consultwithclient'):
        getconsulttype(call.from_user.id, call.data)
        tb.answer_callback_query(call.id, '\U0000231B')
    elif call.data.startswith('initconsult'):
        consult_init(call.from_user.id, call.data)
        tb.answer_callback_query(call.id, 'Консультация начата')
    elif call.data == 'report':
        consult_test_generator(call.from_user.id, call.data)
        tb.answer_callback_query(call.id, 'Консультация закончена')
    elif call.data.startswith('reportquestionanswered'):
        save_report_answer(call.from_user.id, call.data)
        tb.answer_callback_query(call.id, 'Ответ принят')
    elif call.data.startswith('getreportslist_'):
        get_reports_list(call.from_user.id, call.data)
        tb.answer_callback_query(call.id, 'Отчёты')
    elif call.data.startswith('getreporttext_'):
        get_report(call.from_user.id, call.data)
        tb.answer_callback_query(call.id, 'Отчёты')
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


#Next Step Handler
tb.enable_save_next_step_handlers(delay=2)
tb.load_next_step_handlers()


# Get Updates
tb.set_update_listener(handle_messages)
tb.infinity_polling()

