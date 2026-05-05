import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

# Инициализация данных
try:
    with open('expenses.json', 'r', encoding='utf-8') as f:
        expenses = json.load(f)
except FileNotFoundError:
    expenses = []

def validate_input(amount_str, date_str):
    """Валидация ввода: сумма — положительное число, дата — корректный формат"""
    try:
        amount = float(amount_str)
        if amount <= 0:
            messagebox.showerror("Ошибка", "Сумма должна быть положительным числом!")
            return False
    except ValueError:
        messagebox.showerror("Ошибка", "Сумма должна быть числом!")
        return False

    try:
        datetime.strptime(date_str, '%d.%m.%Y')
    except ValueError:
        messagebox.showerror("Ошибка", "Дата должна быть в формате ДД.ММ.ГГГГ!")
        return False
    return True

def add_expense():
    """Добавление расхода в таблицу и JSON"""
    amount = entry_amount.get()
    category = combo_category.get()
    date = entry_date.get()

    if not validate_input(amount, date):
        return

    # Добавляем в список
    expenses.append({
        'amount': float(amount),
        'category': category,
        'date': date
    })

    # Сохраняем в JSON
    with open('expenses.json', 'w', encoding='utf-8') as f:
        json.dump(expenses, f, ensure_ascii=False, indent=4)

    # Обновляем таблицу
    update_table()
    # Очищаем поля ввода
    entry_amount.delete(0, tk.END)
    entry_date.delete(0, tk.END)

def update_table():
    """Обновление таблицы с расходами"""
    # Очищаем таблицу
    for item in tree.get_children():
        tree.delete(item)

    # Заполняем таблицу данными
    for expense in expenses:
        tree.insert('', 'end', values=(
            expense['amount'],
            expense['category'],
            expense['date']
        ))

def calculate_total():
    """Подсчёт суммы за период"""
    start_date_str = entry_start_date.get()
    end_date_str = entry_end_date.get()

    try:
        start_date = datetime.strptime(start_date_str, '%d.%m.%Y')
        end_date = datetime.strptime(end_date_str, '%d.%m.%Y')
    except ValueError:
        messagebox.showerror("Ошибка", "Даты периода должны быть в формате ДД.ММ.ГГГГ!")
        return

    total = sum(
        expense['amount'] for expense in expenses
        if start_date <= datetime.strptime(expense['date'], '%d.%m.%Y') <= end_date
    )
    label_total.config(text=f"Итого за период: {total:.2f} руб.")

def filter_by_category():
    """Фильтрация по категории"""
    category = filter_combo.get()
    filtered = [e for e in expenses if e['category'] == category]
    update_filtered_table(filtered)

def filter_by_date():
    """Фильтрация по дате"""
    date_filter = entry_filter_date.get()
    try:
        datetime.strptime(date_filter, '%d.%m.%Y')
    except ValueError:
        messagebox.showerror("Ошибка", "Дата фильтрации должна быть в формате ДД.ММ.ГГГГ!")
        return
    filtered = [e for e in expenses if e['date'] == date_filter]
    update_filtered_table(filtered)

def update_filtered_table(data):
    """Обновление таблицы с отфильтрованными данными"""
    for item in tree.get_children():
        tree.delete(item)
    for expense in data:
        tree.insert('', 'end', values=(
            expense['amount'],
            expense['category'],
            expense['date']
        ))

# Создание окна
root = tk.Tk()
root.title("Expense Tracker — Трекер расходов")
root.geometry("600x500")

# Поля ввода
tk.Label(root, text="Сумма:").grid(row=0, column=0, padx=5, pady=5)
entry_amount = tk.Entry(root)
entry_amount.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Категория:").grid(row=1, column=0, padx=5, pady=5)
combo_category = ttk.Combobox(root, values=["Еда", "Транспорт", "Развлечения", "Другое"])
combo_category.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Дата (ДД.ММ.ГГГГ):").grid(row=2, column=0, padx=5, pady=5)
entry_date = tk.Entry(root)
entry_date.grid(row=2, column=1, padx=5, pady=5)

# Кнопка добавления
btn_add = tk.Button(root, text="Добавить расход", command=add_expense)
btn_add.grid(row=3, column=0, columnspan=2, pady=10)

# Таблица расходов
tree = ttk.Treeview(root, columns=("Сумма", "Категория", "Дата"), show="headings")
tree.heading("Сумма", text="Сумма")
tree.heading("Категория", text="Категория")
tree.heading("Дата", text="Дата")
tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

# Подсчёт суммы за период
tk.Label(root, text="Начало периода (ДД.ММ.ГГГГ):").grid(row=5, column=0, padx=5, pady=5)
entry_start_date = tk.Entry(root)
entry_start_date.grid(row=5, column=1, padx=5, pady=5)

tk.Label(root, text="Конец периода (ДД.ММ.ГГГГ):").grid(row=6, column=0, padx=5, pady=5)
entry_end_date = tk.Entry(root)
entry_end_date.grid(row=6, column=1, padx=5, pady=5)

btn_calculate = tk.Button(root, text="Посчитать сумму за период", command=calculate_total)
btn_calculate.grid(row=7, column=0, columnspan=2, pady=5)

label_total = tk.Label(root, text="Итого за период: 0.00 руб.")
label_total.grid(row=8, column=0, columnspan=2, pady=5)

# Фильтрация
tk.Label(root, text="Фильтр по категории:").grid(row=9, column=0, padx=5, pady=5)
filter_combo = ttk.Combobox(root, values=["Еда", "Транспорт", "Развлечения", "Другое"])
filter_combo.grid(row=9, column=1, padx=5, pady=5)

btn_filter_category = tk.Button(root, text="Применить фильтр по категории", command=filter_by_category)
btn_filter_category.grid(row=10, column=0, columnspan=2, pady=5)

tk.Label(root, text="Фильтр по дате (ДД.ММ.ГГГГ):").grid(row=11, column=0, padx=5, pady=5)
entry_filter_date = tk.Entry(root)
entry_filter_date.grid(row=11, column=1, padx=5, pady=5)

btn_filter_date = tk.Button(root, text="Применить фильтр по дате", command=filter_by_date)
btn_filter_date.grid(row=12, column=0, columnspan=2, pady=5)

# Обновляем таблицу при запуске
update_table()

root.mainloop()
