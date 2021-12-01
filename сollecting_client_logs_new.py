import PySimpleGUI as sg
import os
from datetime import datetime
import shutil
import json

sg.theme('DarkGreen')

"""Инфа для json`a и пути"""
key_copy = 'copy_dir'
key_past = 'past_dir'
file_name = 'You-are-gay-ha-ha.json'
file_path = str(os.chdir(os.environ['TEMP'])) + file_name
error_popap_text = 'Выбери нормальные пути или проваливай!'

"""Enter на клавиатуре"""
QT_ENTER_KEY1 = 'special 16777220'
QT_ENTER_KEY2 = 'special 16777221'


def get_dirs_from_temp():
    """Получить пути из файла в папке Temp"""
    f = open(file_path, 'r')
    copypast_dirs = json.load(f)
    f.close()
    return copypast_dirs


def save_dirs_in_temp(copy_value, past_value):
    """Сохранить пути в файл в папке Temp"""
    f = open(file_path, 'w')
    copypast_dirs = {key_copy: copy_value, key_past: past_value}
    f.write(json.dumps(copypast_dirs))
    f.close()


def update_temp_window():
    """Интерфейс для изменения путей в Temp"""
    try:
        copy_logs = get_dirs_from_temp()[key_copy]
        past_logs = get_dirs_from_temp()[key_past]
    except:
        copy_logs = 'Not found'
        past_logs = 'Not found'

    layout = [

        [sg.Text('Обязательно выбери пути откуда копировать и куда:')],
        [sg.Text('Где лежат логи:', size=(15, 1), auto_size_text=False),
            sg.InputText(copy_logs), sg.FolderBrowse(button_text='Выбрать', size=(12, 1), key=key_copy)],
        [sg.Text('Куда копировать:', size=(15, 1), auto_size_text=False),
            sg.InputText(past_logs), sg.FolderBrowse(button_text='Выбрать', size=(12, 1), key=key_past)],
        [sg.Button(button_text='Сохранить', size=(12, 1), key='Save_dirs'),
         sg.Button(button_text='Отмена', size=(12, 1), key='Cancel')]

    ]

    window = sg.Window('Выбор директорий', layout, return_keyboard_events=True)

    while True:
        """Обрабатываем события"""
        event, values = window.read()
        # print(event, values)

        if event == sg.WIN_CLOSED or event == 'Cancel':
            """Закрыть интерфейс"""
            window.close()
            break

        if event == 'Save_dirs':
            """Сохранение путей"""
            if values[key_copy] == '' or values[key_past] == 'Not found':
                # Вывод поп-апа с ошибкой
                sg.popup(error_popap_text)
            else:
                save_dirs_in_temp(values[key_copy], values[key_past])
                window.close()
                break


def main_window():
    """Интерфейс для сохранения файла"""
    try:
        get_dirs_from_temp()
    except:
        update_temp_window()

    layout = [

        [sg.Text('Нажми Enter на клавиатуре для копирования:')],
        [sg.InputText(size=(40, 1), key='_IN_')],
        [sg.Submit(button_text='Сохранить', size=(10, 1), key='Save_file'),
         sg.Button(button_text='Изменить', size=(10, 1), key='Change_dirs'),
         sg.Button(button_text='Отмена', size=(10, 1), key='Cancel')]

    ]

    window = sg.Window('Лого-копипаста', layout, return_keyboard_events=True)

    while True:
        """Обрабатываем события"""
        event, values = window.read()
        # print(event, values)

        if len(values['_IN_']) > 100:
            """Ограничение на ввод большого кол-ва символов"""
            window.Element('_IN_').Update(values['_IN_'][:-1])

        if event in ('\r', QT_ENTER_KEY1, QT_ENTER_KEY2):
            """Нажатие Enter на клавиатуре"""
            elem = window.FindElementWithFocus()
            if elem is not None and elem.Type == sg.ELEM_TYPE_BUTTON:
                elem.Click()

        if event == sg.WIN_CLOSED or event == 'Cancel':
            """Закрыть интерфейс"""
            window.close()
            break

        if event == 'Change_dirs':
            """Вызов интерфейса с изменением путей"""
            update_temp_window()

        if event == 'Save_file':
            """Сохранение файла с путями из Temp"""
            try:
                copy_logs = get_dirs_from_temp()[key_copy]
                past_logs = get_dirs_from_temp()[key_past]

                # Список файлов со временем изменения
                dir_list = [os.path.join(copy_logs, x) for x in os.listdir(copy_logs)]
                date_list = [[x, os.path.getmtime(x)] for x in dir_list]
                # Сортировка по возрастанию
                sort_date_list = sorted(date_list, key=lambda x: x[1], reverse=True)
                path_to_last_file = sort_date_list[0][0]

                # Генерация имени и копирование
                now = datetime.now()
                date_time = now.strftime("%H_h_%M_m_%S_s_-%d-%m-%Y")
                path_to_save_file = past_logs + '/' + values['_IN_'] + '_' + str(date_time) + '.log'
                shutil.copy(path_to_last_file, path_to_save_file)
                window.close()
                break
            except:
                update_temp_window()


if __name__ == "__main__":
    main_window()
