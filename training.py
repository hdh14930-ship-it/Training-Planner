import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime

DATA_FILE = 'trainings.json'

class TrainingPlanner(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Training Planner")
        self.geometry("600x450")
        self.trainings = []

        # --- Вводимые параметры
        self.label_date = tk.Label(self, text="Дата (YYYY-MM-DD):")
        self.label_date.pack()
        self.entry_date = tk.Entry(self)
        self.entry_date.pack()

        self.label_type = tk.Label(self, text="Тип тренировки:")
        self.label_type.pack()
        self.entry_type = tk.Entry(self)
        self.entry_type.pack()

        self.label_duration = tk.Label(self, text="Длительность (мин):")
        self.label_duration.pack()
        self.entry_duration = tk.Entry(self)
        self.entry_duration.pack()

        # --- Кнопка добавления
        self.button_add = tk.Button(self, text="Добавить тренировку", command=self.add_training)
        self.button_add.pack(pady=4)

        # --- Фильтрация
        self.filter_frame = tk.Frame(self)
        self.filter_frame.pack(pady=6)
        
        tk.Label(self.filter_frame, text="Фильтр — Тип:").pack(side=tk.LEFT)
        self.filter_type = tk.Entry(self.filter_frame, width=12)
        self.filter_type.pack(side=tk.LEFT, padx=5)
        tk.Label(self.filter_frame, text="Дата:").pack(side=tk.LEFT)
        self.filter_date = tk.Entry(self.filter_frame, width=12)
        self.filter_date.pack(side=tk.LEFT, padx=5)

        self.button_filter = tk.Button(self.filter_frame, text="Применить фильтр", command=self.apply_filter)
        self.button_filter.pack(side=tk.LEFT, padx=5)
        self.button_reset = tk.Button(self.filter_frame, text="Сброс фильтра", command=self.reset_filter)
        self.button_reset.pack(side=tk.LEFT, padx=5)

        # --- Таблица
        columns = ("date", "type", "duration")
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=12)
        for col, colname in zip(columns, ["Дата", "Тип", "Длительность"]):
            self.tree.heading(col, text=colname)
            self.tree.column(col, anchor=tk.CENTER, width=120)
        self.tree.pack(padx=8, pady=8, fill=tk.BOTH, expand=True)

        # --- Сохраняем данные при выходе
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # --- Загрузка данных
        self.load_data()

    def add_training(self):
        date = self.entry_date.get().strip()
        tr_type = self.entry_type.get().strip()
        duration = self.entry_duration.get().strip()

        # --- Проверка корректности
        if not self.validate_date(date):
            messagebox.showerror("Ошибка", "Дата должна быть в формате YYYY-MM-DD")
            return

        if not tr_type:
            messagebox.showerror("Ошибка", "Укажите тип тренировки")
            return

        if not self.validate_duration(duration):
            messagebox.showerror("Ошибка", "Длительность должна быть положительным целым числом")
            return

        item = {
            "date": date,
            "type": tr_type,
            "duration": int(duration)
        }
        self.trainings.append(item)
        self.update_table()
        self.save_data()
        self.entry_date.delete(0, tk.END)
        self.entry_type.delete(0, tk.END)
        self.entry_duration.delete(0, tk.END)

    def validate_date(self, date_text):
        try:
            datetime.strptime(date_text, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def validate_duration(self, duration):
        try:
            d = int(duration)
            return d > 0
        except Exception:
            return False

    def update_table(self, filtered_trainings=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        data = filtered_trainings if filtered_trainings is not None else self.trainings
        for item in data:
            self.tree.insert('', tk.END, values=(item["date"], item["type"], item["duration"]))

    def apply_filter(self):
        ftype = self.filter_type.get().strip().lower()
        fdate = self.filter_date.get().strip()
        result = []
        for item in self.trainings:
            cond = True
            if ftype and ftype not in item["type"].lower():
                cond = False
            if fdate and fdate != item["date"]:
                cond = False
            if cond:
                result.append(item)
        self.update_table(result)

    def reset_filter(self):
        self.filter_type.delete(0, tk.END)
        self.filter_date.delete(0, tk.END)
        self.update_table()

    def save_data(self):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.trainings, f, ensure_ascii=False, indent=2)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    self.trainings = json.load(f)
                    for tr in self.trainings:
                        tr["duration"] = int(tr["duration"])
            except Exception:
                self.trainings = []
        self.update_table()

    def on_closing(self):
        self.save_data()
        self.destroy()

if __name__ == '__main__':
    app = TrainingPlanner()
    app.mainloop()
