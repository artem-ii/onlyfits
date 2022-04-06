import telebot
from telebot import types
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
import os
import textwrap
import pickle

from test_parser_for_bot import *
from clients import *


current_clients_db = 'current_clients.pkl'
coaches_db = 'coaches_db.pkl'

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
clients_folder = '/Users/artemii/OneDrive/Documents/ONLYFITS/.03/'
bot_folder = '/Users/artemii/OneDrive/Documents/ONLYFITS/program-design-jan-2022/bot/'
tests = ['eat26', 'main', 'bdi']
passwords = ['betatester', 'Th6ydI8', 'JKz82e7']
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
    '/Users/artemii/OneDrive/Documents/ONLYFITS/program-design-jan-2022/bot/report_tests/psy_report.csv',
    sep = ';', dtype = str)
first_convert = pd.read_csv(
    '/Users/artemii/OneDrive/Documents/ONLYFITS/program-design-jan-2022/bot/report_tests/first_report.csv',
    sep = ';', dtype = str)
second_convert = pd.read_csv(
    '/Users/artemii/OneDrive/Documents/ONLYFITS/program-design-jan-2022/bot/report_tests/second_report.csv',
    sep = ';', dtype = str)
last_convert = pd.read_csv(
    '/Users/artemii/OneDrive/Documents/ONLYFITS/program-design-jan-2022/bot/report_tests/last_report.csv',
    sep = ';', dtype = str)


# User id info
coaches = {520834290:"Ксения Календарева", 594759110:"Елена", 1472202629:"trener.idel",
           541765907:"Дарья", 141659022:"Янина", 287460510:"Ирина",
           409750031:"Анастасия", 310119054:"Наталья Лаврененко",
           3755631:"Artemii",
           970257969: "Наталья Минажетдинова",
           388199486: "Артем",
           234047265: "Оксана Круглова"}
    #,
    #      2019105955:"Artemii Nikitin"}

coaches_test = {3755631:"Artemii"}
    #, 2019105955:"Artemii Nikitin"}


ids = [3755631]
       #2019105955]

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
        tb.reply_to(message, "Здравствуйте. Пожалуйста, введите пароль: ")
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
        if message.chat.id in ids:
            move(message.chat.id, 'to_admin')
        elif message.chat.id in coaches.keys():
            if trenerskaya[message.from_user.id]['consult_mode']:
                handle_report_notes(message)
            elif message.text != '/start':
                where(message.chat.id)
        elif message.text == 'database_dump_2929':
            dump_reply = db_dump()
            tb.send_message(message.chat.id, text=str(current_users + dump_reply))
        elif message.text in passwords:
            test_mainscreen(message)
        elif message.text == 'Регистрация':
            line = str('\n'+ str(message.from_user) + ' - ' + str(message.chat.id))
            with open('users.txt', 'a', encoding='utf-8') as f:
                f.write(line)
            f.close()
            getnamemsg = tb.send_message(message.chat.id, "Здравствуйте! Введите, пожалуйста, Ваше имя",
                                         reply_markup=types.ReplyKeyboardRemove())
            tb.register_next_step_handler(getnamemsg, get_name)
        elif message.chat.id not in coaches.keys():
            handle_client(message)


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

             'homework': {},

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

    elif current_question_type == 'date'\
            or current_question_type == 'weight':
        if message_to_delete not in [-1, 0]:
            tb.delete_message(usr, message_to_delete)
        current_users[usr]['current_test'] = requested_test
        current_users[usr]['current_question_code'] = current_question_code
        current_users[usr]['current_question_type'] = current_question_type
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
    #current_question_type = current_users[usr]['current_question_type']
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
        try:
            tb.delete_message(usr, message_to_delete)
            tb.delete_message(usr, message_to_delete + 1)
            current_users[usr]['message_to_delete'] = -1
        except:
            pass


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
        try:
            tb.delete_message(usr, message_to_delete)
        except:
            pass
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
    elif move_to_menu == 'homework':
        message_text = 'Домашние задания'

        homework_folder = os.path.join(bot_folder, 'homework')
        homeworks = os.listdir(homework_folder)
        if '.DS_Store' in homeworks:
            homeworks.remove('.DS_Store')
            print('ds store removed')
        homeworkkeys = [('givehomework_' + x) for x in homeworks]
        homeworks_dict = dict(zip(homeworkkeys, homeworks))
        keyboards['homework'] = homeworks_dict
    message_sent = tb.send_message(chat_id=usr,
                                   text=message_text,
                                   reply_markup=makeKeyboard(move_to_menu),
                                   parse_mode='HTML')
    trenerskaya[usr]['message_to_delete'] = message_sent.message_id
    print(message_to_delete)
    print(message_sent.message_id)

def givehomework(usr, call):
    homework = call.split('_')[1]
    requested_client_code = trenerskaya[usr]['current_client']
    print(requested_client_code)
    print(current_users.keys())
    for client in current_users.keys():
        print(client)
        if client != 'init':
            print(current_users[client])
            client_telegram_id = client
            client_file_list = os.listdir('temp_client_dataframes')
            #print(client_file_list)
            current_client_files_list = list()
            file_datetime_list = list()
            current_client_file_recent = str()

            for filename in client_file_list:
                if str(client_telegram_id) in filename:
                    if filename.startswith('all_tests_program_generated-'):
                        current_client_files_list.append(filename)
            print(current_client_files_list)
            if len(current_client_files_list) > 0:
                if 'client_code' not in current_users[client]:
                    for current_client_file in current_client_files_list:
                        filename_elements = current_client_file.split('-')
                        file_datetime_str = filename_elements[2]
                        file_datetime_str = file_datetime_str[:-4]
                        file_datetime = datetime.strptime(file_datetime_str, '%d_%m_%Y %H_%M_%S')
                        file_datetime_list.append(file_datetime)
                    file_datetime_list.sort()
                    last_datetime_index = len(file_datetime_list) - 1
                    print(file_datetime_list)
                    print(last_datetime_index)
                    recent_file_datetime = file_datetime_list[last_datetime_index]
                    recent_file_datetime_str = recent_file_datetime.strftime('%d_%m_%Y %H_%M_%S')
                    for current_client_file in current_client_files_list:
                        if recent_file_datetime_str in current_client_file:
                            current_client_file_recent = current_client_file
                    print(current_client_file_recent)
                    file_path = os.path.join(bot_folder,
                                             'temp_client_dataframes',
                                             current_client_file_recent)
                    client_dataframe = pd.read_csv(file_path)
                    client_code = client_dataframe['client_code'].item()
                    current_users[client_telegram_id]['client_code'] = client_code
                    print(current_users[client_telegram_id]['client_code'])
            if current_users[client]['client_code'] == requested_client_code:
                current_users[client]['homework'] = homework
                print(current_users)
                pass

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
                                'to_reports_' + requested_client_code: 'Отчёты о консультациях',
                                'to_homework_' + requested_client_code: 'Задать домашнее задание'}
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


# Функции для клиентов

def handle_client(message):
    usr = message.from_user.id
    if 'message_to_delete' in current_users[usr].keys():
        message_to_delete = current_users[usr]['message_to_delete']
    else:
        current_users[usr]['message_to_delete'] = 0
        message_to_delete = current_users[usr]['message_to_delete']

    if message_to_delete not in [-1, 0]:
        try:
            print('trying to delete...')
            tb.delete_message(usr, message_to_delete)
        except:
            pass

    client_telegram_id = message.from_user.id
    client_file_list = os.listdir('temp_client_dataframes')
    #print(client_file_list)
    current_client_files_list = list()
    file_datetime_list = list()
    current_client_file_recent = str()

    for filename in client_file_list:
        if str(client_telegram_id) in filename:
            if filename.startswith('all_tests_program_generated-'):
                current_client_files_list.append(filename)
    print(current_client_files_list)
    if len(current_client_files_list) > 0:
        if 'client_code' not in current_users[usr]:
            for current_client_file in current_client_files_list:
                filename_elements = current_client_file.split('-')
                file_datetime_str = filename_elements[2]
                file_datetime_str = file_datetime_str[:-4]
                file_datetime = datetime.strptime(file_datetime_str, '%d_%m_%Y %H_%M_%S')
                file_datetime_list.append(file_datetime)
            file_datetime_list.sort()
            last_datetime_index = len(file_datetime_list) - 1
            print(file_datetime_list)
            print(last_datetime_index)
            recent_file_datetime = file_datetime_list[last_datetime_index]
            recent_file_datetime_str = recent_file_datetime.strftime('%d_%m_%Y %H_%M_%S')
            for current_client_file in current_client_files_list:
                if recent_file_datetime_str in current_client_file:
                    current_client_file_recent = current_client_file
            print(current_client_file_recent)
            file_path = os.path.join(bot_folder,
                                     'temp_client_dataframes',
                                     current_client_file_recent)
            client_dataframe = pd.read_csv(file_path)
            client_code = client_dataframe['client_code'].item()
            current_users[client_telegram_id]['client_code'] = client_code
            print(current_users[client_telegram_id]['client_code'])
        client_main_keyboard = {"clientrequest_diary": "Сделать запись",}
        # client_main_keyboard = {"clientrequest_plan": "Запланировать",
        #                         "clientrequest_diary": "Сделать запись",
        #                         "clientrequest_homework": "Домашнее задание",
        #                         "clientrequest_file": "Отправить файл",
        #                         "clientrequest_report": "Посмотреть мои записи"}
        message_sent = tb.send_message(client_telegram_id, "Выберите, пожалуйста, действие",
                               reply_markup=makeQuestionKeyboard(client_main_keyboard),
                               parse_mode="HTML")
    else:
        message_sent = tb.send_message(client_telegram_id,
                                       "Введите, пожалуйста, существующий пароль, чтобы пройти диагностический тест.")
    current_users[usr]['message_to_delete'] = message_sent.message_id
    print(current_users[usr]['message_to_delete'])


record_type_human_readable_dict = {'food': 'Еда',
                                   'place': 'Место',
                                   'foodcomment': 'Комментарии',
                                   'activcomment': 'Комментарии',
                                   'mainmeal': 'Основной приём пищи',
                                   'snack': 'Перекус',
                                   'activity': 'Физическая активность',
                                   'activtype': 'Тип активности',
                                   'activtime': 'Длительность активности',
                                   'comment': 'Комментарии',
                                   'calories': 'Калории'
                                   }

def handle_client_request(usr, request_call):
    overeat = False
    save = False
    print(current_users[usr])
    print(current_users[usr]['message_to_delete'])
    print(request_call)
    if 'message_to_delete' in current_users[usr].keys():
        message_to_delete = current_users[usr]['message_to_delete']
    else:
        current_users[usr]['message_to_delete'] = 0
        message_to_delete = current_users[usr]['message_to_delete']

    if message_to_delete not in [-1, 0]:
        print('not zero')
        try:
            print('Trying to delete...')
            tb.delete_message(usr, message_to_delete)
        except:
            pass

    client_telegram_id = usr
    action = request_call.split('_')[1]
    if action == 'diary':
        client_action_keyboard = {"clientrequest_meal": "Приём пищи",
                                  "clientrequest_activity": "Физическая активность",
                                  "clientrequest_rec.comment": "Комментарий"}
        client_diary_record = pd.DataFrame()
        client_diary_record['Дата'] = [get_time().split(' ')[0]]
        client_diary_record['Время'] = [get_time().split(' ')[1]]
        current_users[client_telegram_id]['diary_record'] = client_diary_record

    elif action == 'meal':
        client_diary_record = pd.DataFrame()
        client_action_keyboard = {"clientrequest_mainmeal": "Основной приём пищи",
                                  "clientrequest_snack": "Перекус"}

    elif action == 'mainmeal' or action == 'snack':
        print('mainmeal')
        client_diary_record = current_users[client_telegram_id]['diary_record']
        client_diary_record['Тип записи'] = record_type_human_readable_dict[action]
        current_users[client_telegram_id]['diary_record'] = client_diary_record
        client_action_keyboard = {"clientrequest_rec.food": "Что вы съели?",
                                  "clientrequest_rec.place": "Где вы это съели?",
                                  "clientrequest_rec.foodcomment": "Комментарии",
                                  "clientrequest_rec.calories": "Калории",
                                  "clientrequest_overeat": "Нажмите, если переели",
                                  "clientrequest_save": "Сохранить"
                                  }

    elif action == 'activity':
        client_diary_record = current_users[client_telegram_id]['diary_record']
        client_diary_record['Тип записи'] = record_type_human_readable_dict[action]
        current_users[client_telegram_id]['diary_record'] = client_diary_record
        client_action_keyboard = {"clientrequest_rec.activtype": "Что вы делали?",
                                  "clientrequest_rec.activtime": "Длительность активности (мин)",
                                  "clientrequest_rec.activcomment": "Комментарии",
                                  "clientrequest_save": "Сохранить"
                                  }
    elif action == 'overeat':
        client_diary_record = current_users[client_telegram_id]['diary_record']
        client_diary_record['*'] = ['Да']
        current_users[client_telegram_id]['diary_record'] = client_diary_record
        record_type_hr = client_diary_record['Тип записи'].item()
        record_type = \
        list(record_type_human_readable_dict.keys())[list(
            record_type_human_readable_dict.values()).index(record_type_hr)]
        client_action_keyboard = 0
        current_users[usr]['message_to_delete'] = 0
        handle_client_request(usr, 'clientrequest_' + record_type)
        overeat = True

    #elif action == 'homework':


    elif action == 'save':
        save = True
        client_diary_record = current_users[client_telegram_id]['diary_record']
        diary_files_path = os.path.join(clients_folder,
                                        'diary_files')
        os.makedirs(diary_files_path, exist_ok=True)
        diary_files = os.listdir(diary_files_path)
        client_diary_filename = current_users[client_telegram_id]['client_code'] + '.dr'
        client_diary_files = list()
        for file in diary_files:
            if file == client_diary_filename:
                client_diary_files.append(file)
        print(client_diary_files)
        client_diary_file_path = os.path.join(diary_files_path,
                                              client_diary_filename)
        if client_diary_files == []:
            client_diary_record.to_csv(client_diary_file_path, encoding='utf8', index=False)
        else:
            client_diary_dataframe = pd.read_csv(client_diary_file_path)
            diary_df_list = [client_diary_dataframe, client_diary_record]
            updated_diary_df = pd.concat(diary_df_list, ignore_index=True)
            updated_diary_df.to_csv(client_diary_file_path, encoding='utf8', index=False)
        tb.send_message(client_telegram_id, "Запись сохранена, отправьте любое сообщение, "
                                            "чтобы сделать новую запись или посмотреть существующие.")
        client_action_keyboard = 0
        #client_action_keyboard = {"clientrequest_plan": "Запланировать",
        #                        "clientrequest_diary": "Сделать запись",
        #                        "clientrequest_homework": "Домашнее задание",
        #                        "clientrequest_file": "Отправить файл"}

    elif action == 'report':
        current_users[usr]['diary_pdf_files'] = {}
        diary_files_path = os.path.join(clients_folder,
                                        'diary_files')
        os.makedirs(diary_files_path, exist_ok=True)
        diary_files = os.listdir(diary_files_path)
        client_diary_filename = current_users[client_telegram_id]['client_code'] + '.dr'
        client_diary_files = list()
        for file in diary_files:
            if file == client_diary_filename:
                client_diary_files.append(file)
        print(client_diary_files)
        client_diary_file_path = os.path.join(diary_files_path, client_diary_filename)
        client_diary_dataframe = pd.read_csv(client_diary_file_path)

        diary_page = pd.DataFrame()
        for ind, diary_record in client_diary_dataframe.iterrows():
            print(diary_record)
            print(type(diary_record))
            record_date = diary_record['Дата']
            record_date = datetime.strptime(record_date, '%d/%m/%Y')
            diary_pages_list = [diary_page, diary_record.to_frame().T]
            if len(diary_page) == 0:
                diary_page = diary_record.to_frame().T
            else:
                diary_page = pd.concat(diary_pages_list, ignore_index=True)
            print(diary_page)
            if ind == 0:
                start_date = record_date
            elif (record_date - start_date).days == 7:
                start_date_str = start_date.strftime('%d-%m-%Y')
                record_date_str = record_date.strftime('%d-%m-%Y')
                report_filename = start_date_str + ' - ' + record_date_str + '.pdf'
                current_users[usr]['diary_pdf_files'][report_filename] = diary_page
                diary_page = pd.DataFrame()
                try:
                    start_date = client_diary_dataframe.loc[:, "Дата"]
                    start_date = start_date.iloc[ind + 1, :]
                    start_date = start_date.item()
                    start_date = datetime.strptime(start_date, '%d/%m/%Y')
                except:
                    print(start_date)
            elif ind == len(client_diary_dataframe)-1:
                start_date_str = start_date.strftime('%d-%m-%Y')
                record_date_str = record_date.strftime('%d-%m-%Y')
                report_filename = start_date_str + ' - ' + record_date_str + '.pdf'
                current_users[usr]['diary_pdf_files'][report_filename] = diary_page
                diary_page = pd.DataFrame()
                current_users[usr]['diary_pdf_files'][report_filename].head()
                print(current_users[usr]['diary_pdf_files'])

            for report in current_users[usr]['diary_pdf_files'].values():
                #report = report.dropna()
                print(type(report))
                # https://stackoverflow.com/questions/32137396/how-do-i-plot-only-a-table-in-matplotlib
                fig, ax = plt.subplots(figsize=(12, 4))
                print(fig)
                print(ax)
                ax.axis('tight')
                ax.axis('off')
                the_table = ax.table(cellText=report.values, colLabels=report.columns, loc='center')

                # https://stackoverflow.com/questions/4042192/reduce-left-and-right-margins-in-matplotlib-plot
                pp = PdfPages("foo.pdf")
                pp.savefig(fig, bbox_inches='tight')
                pp.close()
                report_path = os.path.join(bot_folder, 'foo.pdf')
                doc = open(report_path, 'rb')
                tb.send_document(usr, doc)
    elif action == 'homework':
        starthomework(client_telegram_id)
    elif action.startswith('rec'):
        record_type = action.split('.')[1]
        current_users[usr]['record_type'] = record_type
        if record_type == 'comment':
            client_diary_record = current_users[client_telegram_id]['diary_record']
            client_diary_record['Тип записи'] = record_type_human_readable_dict[record_type]
            current_users[client_telegram_id]['diary_record'] = client_diary_record
        client_action_keyboard = {}
        print(record_type)

    if client_action_keyboard == {}:
        print('Waiting input from user...')
        message_sent = tb.send_message(client_telegram_id, "Введите, пожалуйста, запись")
        tb.register_next_step_handler(message_sent, make_diary_record)
    elif overeat:
        print('Overeat record made')
    elif save:
        print('Diary record saved')
    else:
        print('Menu generated')
        message_sent = tb.send_message(client_telegram_id, "Выберите, пожалуйста, вид записи",
                                       reply_markup=makeQuestionKeyboard(client_action_keyboard),
                                       parse_mode="HTML")
    if not overeat:
        try:
            current_users[usr]['message_to_delete'] = message_sent.message_id
            print(current_users[usr]['message_to_delete'])
        except:
            pass


def make_diary_record(message):
    client_telegram_id = message.from_user.id
    record_type = current_users[client_telegram_id]['record_type']
    record_type_human_readable = record_type_human_readable_dict[record_type]
    client_diary_record = current_users[client_telegram_id]['diary_record']
    client_diary_record[record_type_human_readable] = [message.text]
    current_users[client_telegram_id]['diary_record'] = client_diary_record
    print(client_diary_record)
    parent_record_type_hr = current_users[client_telegram_id]['diary_record']['Тип записи'].item()
    parent_record_type = \
        list(record_type_human_readable_dict.keys())[list(
            record_type_human_readable_dict.values()).index(parent_record_type_hr)]
    call_argument = 'clientrequest_' + parent_record_type
    if record_type == 'comment':
        handle_client_request(client_telegram_id, 'clientrequest_save')
    else:
        handle_client_request(client_telegram_id, call_argument)


# def starthomework(usr):
#     if 'message_to_delete' in current_users[usr].keys():
#         message_to_delete = current_users[usr]['message_to_delete']
#     else:
#         current_users[usr]['message_to_delete'] = 0
#         message_to_delete = current_users[usr]['message_to_delete']
#
#     question_options = {}
#     user_homework_dict = current_users[usr]
#     print(user_test_dict)
#     requested_homework = current_users[usr]['homework']
#     homework_data_dict = homework_dict[requested_homework]
#     homework_convert = homework_data_dict['convert']
#     homework_keys = homework_data_dict['keys']
#     current_question_row = homework_convert.iloc[user_homework_dict[requested_homework]['current_question_index'],:]
#     current_users[usr]['current_homework'] = requested_homework
#     current_question_code = current_question_row['Number']
#     current_question = current_question_row['Question']
#     current_question_type = current_question_row['subscale']
#     line = str(get_time() + ' ' + str(usr) + ' '
#                + ' in homework ' + requested_homework + ' on question '
#                + current_question_code + '\n')
#     print(line)
#     with open('log.txt', 'a', encoding='utf-8') as f:
#         f.write(line)
#         f.close()
#     tb.send_message(3755631, line)
#
#     if current_question_type == 'text':
#         if message_to_delete not in [-1, 0]:
#             tb.delete_message(usr, message_to_delete)
#         current_users[usr]['current_test'] = requested_test
#         current_users[usr]['current_question_code'] = current_question_code
#         gettextanswer = tb.send_message(usr, text = current_question)
#         current_users[usr]['message_to_delete'] = gettextanswer.message_id
#         tb.register_next_step_handler(gettextanswer, save_text_answer)
#
#     elif current_question_type == 'multiple':
#         tb.send_message(usr, text = current_question)
#         user_test_dict[requested_test]['current_question_index'] += 1
#         current_users[usr] = user_test_dict
#         question_generator(usr, test)
#
#     elif current_question_type == 'date':
#         if message_to_delete not in [-1, 0]:
#             tb.delete_message(usr, message_to_delete)
#         current_users[usr]['current_test'] = requested_test
#         current_users[usr]['current_question_code'] = current_question_code
#         gettextanswer = tb.send_message(usr, text = current_question)
#         current_users[usr]['message_to_delete'] = gettextanswer.message_id
#         tb.register_next_step_handler(gettextanswer, check_answer)
#
#     else:
#         if message_to_delete not in [-1, 0]:
#             tb.delete_message(usr, message_to_delete)
#         option_string = 'abcdefg'
#         for option in option_string:
#             if not pd.isnull(current_question_row[option]):
#                 question_option_key = 'homeworkquestionanswered' + '_' + str(requested_homework)+ '_' + \
#                                       str(current_question_code) + '_' + str(option)
#                 question_option_value = current_question_row[option]
#                 question_options[question_option_key] = question_option_value
#         question_options['homeworkquestionanswered_' + str(requested_test) + '_' +
#                          'qback' + '_' +
#                          str(user_test_dict[requested_homework]['current_question_index'])] = 'К предыдущему вопросу'
#         #question_options['testmenu'] = 'К меню с тестами'
#         print(question_options)
#         message_sent = tb.send_message(usr, text = current_question,
#                                        reply_markup=makeQuestionKeyboard(question_options),
#                                        parse_mode='HTML')
#         current_users[usr]['message_to_delete'] = message_sent.message_id
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
    elif call.data.startswith('clientrequest_'):
        handle_client_request(call.from_user.id, call.data)
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
    elif call.data.startswith('givehomework_'):
        givehomework(call.from_user.id, call.data)
        tb.answer_callback_query(call.id, 'Домашнее задание задано')
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
