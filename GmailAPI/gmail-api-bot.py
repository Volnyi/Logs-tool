from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
from bs4 import BeautifulSoup
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials


SCOPES = ['https://mail.google.com/']
file = 'inform.txt'
counter = 'counter.txt'


def log_file(text):
    """Запись данных в файл"""
    f = open(file, 'a+')
    f.write(text)
    f.close()


def delete_inform_from_file():
    """Очистить содержимое файла"""
    file1 = open("inform.txt", "w")
    file1.close


def getEmails():
    """Прочесть содержимое письма и записать это в файл"""
    creds = None
    if os.path.exists('token.pickle'):

        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    result = service.users().messages().list(userId='me').execute()
    messages = result.get('messages')

    for msg in messages:
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
        print('Вижу письмо')
        # print(txt['labelIds'])
        if txt['labelIds'][0] == 'UNREAD':
            try:
                print('Вижу непрочтенное письмо!')
                service.users().messages().modify(userId='me', id=msg['id'], body={"removeLabelIds": ['UNREAD']}).execute()
                items = txt['payload']
                local_items = items['headers']

                data = txt['payload']['parts'][0]['body']['data']
                data = data.replace("-", "+").replace("_", "/")
                decoded_data = base64.b64decode(data)
                soup = BeautifulSoup(decoded_data, "lxml")
                body = soup.body()

                for items in local_items:
                    if items['name'] == 'From':
                        if items['value'] == 'Readymag <>':
                            text_message = str(body[0])
                            print(text_message)
                            log_file(text_message)

            except Exception as e:
                print('Алям, мы сломались: + ' + str(e))

getEmails()


CREDENTIALS_FILE = '.json'  # Имя файла с закрытым ключом
# Читаем ключи из файла
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets',
                                                                                  'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API

spreadsheet = service.spreadsheets().create(body = {
    'properties': {'title': 'Первый тестовый документ', 'locale': 'ru_RU'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': 0,
                               'title': 'Лист номер один',
                               'gridProperties': {'rowCount': 100, 'columnCount': 15}}}]
}).execute()

spreadsheetId = ''

print('https://docs.google.com/spreadsheets/d/' + spreadsheetId)


file1 = open(file, "r")
lines = file1.readlines()

file_counter = open(counter, "r")
number_counter = int(file_counter.read())
file_counter.close()

for line in lines:
    if '*Имя Фамилия: *' in line:
        name = line.strip()[15:]
        print(line.strip()[15:])
    if '*Дата рождения: *' in line:
        born = line.strip()[18:]
        print(line.strip()[18:])
    if '*Номер телефона: *' in line:
        phone = line.strip()[19:]
        print(line.strip()[19:])
    if '*Email: *' in line:
        mail = line.strip()[9:]
        print(line.strip()[9:])
    if '*Город: *' in line:
        city = line.strip()[9:]
        print(line.strip()[9:])
    if '*Специализация: *' in line:
        specialist = line.strip()[17:]
        print(line.strip()[17:])
        print('-------------')
        print(file_counter)
        results = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": "Лист номер один!" + "A" + str(number_counter),
                 "majorDimension": "ROWS",
                 "values": [
                     [name, born, phone, mail, city, specialist]
                 ]}
            ]
        }).execute()

        number_counter += 1
        file_counter = open(counter, "w+")
        file_counter.write(str(number_counter))
        print(number_counter)
        file_counter.close()

file1.close

delete_inform_from_file()
