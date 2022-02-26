
# Функция, которая будет обрабатывать отчёты о консультациях
def getconsultclient(usr):
    global coaches
    coach_name = coaches[usr]
    coach_clients = trenerskaya[coach_name]['clients']
    for client in coach_clients:
        coach_clients_dict['consultwithclient_' + client] = client
    tb.send_message(usr, 'Выберите, пожалуйста, клиента',
            reply_markup=makeQuestionKeyboard(coach_clients_dict),
            pasre_mode='HTML'
            )



def getconsulttype(usr, client_call):
    global trenerskaya
    current_client = client_call.split('_')[1]
    trenerskaya[coach_name]['current_client'] = current_client
    tb.send_message(usr, 'Выберите, пожалуйста, тип консультации',
            reply_markup=makeQuestionKeyboard(consult_type_dict),
            parse_mode='HTML'
            )
    trenerskaya[coach_name]['consult_mode'] = True
