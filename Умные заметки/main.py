from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, \
    QHBoxLayout, QVBoxLayout, QMessageBox

import json

app = QApplication([])

"""Заметки в json"""
notes = {
    "Добро пожаловать!": {
        "текст": "Это самое лучшее приложение для заметок в мире!",
        "теги": ["добро", "инструкция"]
    }
}
# with open("notes_data.json", "w", encoding='utf-8') as file:
#     json.dump(notes, file, ensure_ascii=False)

"""Интерфейс приложения"""
# параметры окна приложения
notes_win = QWidget()
notes_win.setWindowTitle('Умные заметки')
notes_win.resize(900, 600)

# виджеты окна приложения
list_notes = QListWidget()
list_notes_label = QLabel('Список заметок')

button_note_create = QPushButton('Создать заметку')  # появляется окно с полем "Введите имя заметки"
button_note_del = QPushButton('Удалить заметку')
button_note_save = QPushButton('Сохранить заметку')

field_tag = QLineEdit('')
field_tag.setPlaceholderText('Введите тег...')
field_text = QTextEdit()
button_tag_add = QPushButton('Добавить к заметке')
button_tag_del = QPushButton('Открепить от заметки')
button_tag_search = QPushButton('Искать заметки по тегу')
list_tags = QListWidget()
list_tags_label = QLabel('Список тегов')

# расположение виджетов по лэйаутам
layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)

col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)
row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)
col_2.addWidget(button_note_save)

col_2.addLayout(row_1)

col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)
row_3 = QHBoxLayout()
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)
col_2.addWidget(button_tag_search)

col_2.addLayout(row_3)

layout_notes.addLayout(col_1, stretch=2)
layout_notes.addLayout(col_2, stretch=1)
notes_win.setLayout(layout_notes)

"""Функционал приложения"""


def save_info_to_file():
    with open("notes_data.json", "w") as outfile:
        json.dump(notes, outfile, sort_keys=True, ensure_ascii=False)


def show_error(text):
    msgBox = QMessageBox()
    msgBox.setWindowTitle("Ошибка!")
    msgBox.setText(text)
    msgBox.exec_()


def show_note():
    # получаем текст из заметки с выделенным названием и отображаем его в поле редактирования
    key = list_notes.selectedItems()[0].text()
    field_text.setText(notes[key]["текст"])
    list_tags.clear()
    list_tags.addItems(notes[key]["теги"])


def add_note():
    note_name, ok = QInputDialog.getText(notes_win, "Добавить заметку", "Название заметки: ")
    print(note_name, ok)
    if ok and note_name:
        notes[note_name] = {"текст": "", "теги": []}
        list_notes.addItem(note_name)


def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]["текст"] = field_text.toPlainText()
        save_info_to_file()
    else:
        show_error("Заметка для сохранения не выбрана!")


def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        save_info_to_file()
    else:
        show_error("Заметка для удаления не выбрана!")


"""Работа с тегами заметки"""


def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if tag not in notes[key]["теги"] and tag:
            notes[key]["теги"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
            save_info_to_file()
    else:
        show_error("Заметка для добавления тега не выбрана!")


def del_tag():
    if list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]["теги"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["теги"])
        save_info_to_file()
    else:
        show_error("Тег для удаления не выбран!")


def search_tag():
    tag = field_tag.text()
    if button_tag_search.text() == "Искать заметки по тегу" and tag:
        notes_filtered = {}  # тут будут заметки с выделенным тегом
        for note in notes:
            if tag in notes[note]["теги"]:
                notes_filtered[note] = notes[note]
        button_tag_search.setText("Сбросить поиск")
        list_notes.clear()
        field_text.clear()
        list_tags.clear()
        field_tag.clear()
        list_notes.addItems(notes_filtered)
    elif button_tag_search.text() == "Сбросить поиск":
        list_notes.clear()
        field_text.clear()
        list_tags.clear()
        field_tag.clear()
        list_notes.addItems(notes)
        button_tag_search.setText("Искать заметки по тегу")


"""Запуск приложения"""
# подключение обработки событий
button_note_create.clicked.connect(add_note)
list_notes.itemClicked.connect(show_note)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(del_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)

# запуск приложения
notes_win.show()

with open("notes_data.json", "r") as file:
    notes = json.load(file)
list_notes.addItems(notes)

app.exec_()
