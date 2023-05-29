
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from datetime import datetime
import re


# ID таблицы и название листа
SPREADSHEET_ID = 'SPREADSHEET_ID'
SHEET_NAME = 'SHEET_NAME'

# Авторизация и получение доступа к таблице
creds = ServiceAccountCredentials.from_json_keyfile_name('SERVICE_ACCOUNT.json', ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

# поиск последнего числа в столбце
regex_query = r'^\d+$'  # регулярное выражение, которое соответствует любому числу
cell_list = sheet.findall(re.compile(regex_query), in_column=5)
last_balance_value = int(cell_list[-1].value)


# Функция для добавления дохода
def add_income():
    amount = int(income_entry.get())
    category = income_category.get()

    # Получаем текущий остаток и добавляем доход
    new_balance = last_balance_value + amount

    # Добавляем запись в таблицу
    row = [str(data_field.get()), category, '', amount, new_balance]
    sheet.append_row(row)
    
    # Очищаем поле ввода и обновляем текстовую метку с остатком
    income_entry.delete(0, tk.END)
    balance_label.configure(text=f'Текущий остаток: {new_balance} рублей.')

# Функция для добавления расхода
def add_expense():
    amount = int(expense_entry.get())

    # Получаем текущий остаток и вычитаем расход
    
    new_balance = last_balance_value - amount
    
    # Добавляем запись в таблицу
    row = [datetime.now().strftime("%d.%m.%Y"), '', amount, '', new_balance]
    sheet.append_row(row)
    
    # Очищаем поле ввода и обновляем текстовую метку с остатком
    expense_entry.delete(0, tk.END)
    balance_label.configure(text=f'Текущий остаток: {new_balance} рублей.')

# Создаем графический интерфейс
root = tk.Tk()
root.title('Учет доходов и расходов')

income_category_array = ['Зарплата', 'Кешбэк', 'Проценты на остаток']


# Создаем элементы интерфейса
data_field = DateEntry(root, date_pattern='dd.mm.yyyy')
income_label = tk.Label(root, text='Добавить доход:')
income_entry = tk.Entry(root)
income_category = ttk.Combobox(values=income_category_array, state="readonly")
income_button = tk.Button(root, text='Добавить', command=add_income)

expense_label = tk.Label(root, text='Добавить расход:')
expense_entry = tk.Entry(root)
expense_button = tk.Button(root, text='Добавить', command=add_expense)

balance_label = tk.Label(root, text=f'Текущий остаток: {last_balance_value} рублей.')

# Размещаем элементы на форме
data_field.grid(row=0, column=0, padx=5, pady=5)
income_label.grid(row=0, column=1, padx=5, pady=5)
income_entry.grid(row=0, column=2, padx=5, pady=5)
income_category.grid(row=0, column=3, padx=5, pady=5)
income_button.grid(row=0, column=4, padx=5, pady=5)

expense_label.grid(row=1, column=0, padx=5, pady=5)
expense_entry.grid(row=1, column=1, padx=5, pady=5)
expense_button.grid(row=1, column=2, padx=5, pady=5)

balance_label.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

# Запускаем главный цикл обработки событий
root.mainloop()
