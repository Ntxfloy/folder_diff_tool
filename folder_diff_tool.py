import tkinter as tk
from tkinter import filedialog, messagebox
import filecmp
import os
import shutil

# Функция для выбора папки
def choose_folder(label):
    folder_path = filedialog.askdirectory()
    if folder_path:
        label.config(text=folder_path)
    return folder_path

# Рекурсивная функция для сравнения содержимого папок
def compare_directories(dir1, dir2, result_text, unique_files):
    comparison = filecmp.dircmp(dir1, dir2)

    # Добавляем уникальные и совпадающие файлы в результат
    if comparison.left_only:
        result_text.append(f"Файлы, которые есть только в '{dir1}':\n" + "\n".join(f" - {file}" for file in comparison.left_only))
        for file in comparison.left_only:
            unique_files.append(os.path.join(dir1, file))

    if comparison.right_only:
        result_text.append(f"Файлы, которые есть только в '{dir2}':\n" + "\n".join(f" - {file}" for file in comparison.right_only))
        for file in comparison.right_only:
            unique_files.append(os.path.join(dir2, file))

    # Рекурсивно обрабатываем подкаталоги
    for subdir in comparison.common_dirs:
        compare_directories(os.path.join(dir1, subdir), os.path.join(dir2, subdir), result_text, unique_files)

# Функция для запуска сравнения папок
def compare_folders():
    folder1 = folder1_label.cget("text")
    folder2 = folder2_label.cget("text")

    if not os.path.isdir(folder1) or not os.path.isdir(folder2):
        messagebox.showerror("Ошибка", "Пожалуйста, выберите обе папки.")
        return

    # Список для накопления текста с результатами и уникальных файлов
    result_text = []
    unique_files.clear()
    compare_directories(folder1, folder2, result_text, unique_files)

    # Очистка предыдущего результата и отображение нового
    result_text_widget.config(state=tk.NORMAL)
    result_text_widget.delete(1.0, tk.END)
    result_text_widget.insert(tk.END, "\n\n".join(result_text) if result_text else "Все файлы и папки совпадают.")
    result_text_widget.config(state=tk.DISABLED)

# Функция для создания папки на рабочем столе с уникальными файлами
def create_folder_with_unique_files():
    if not unique_files:
        messagebox.showinfo("Информация", "Нет уникальных файлов для создания папки.")
        return

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    new_folder_path = os.path.join(desktop_path, "Уникальные файлы")
    os.makedirs(new_folder_path, exist_ok=True)

    for file_path in unique_files:
        if os.path.isfile(file_path):
            shutil.copy(file_path, new_folder_path)

    messagebox.showinfo("Успешно", f"Папка с уникальными файлами создана на рабочем столе: {new_folder_path}")

# Создаем интерфейс с помощью tkinter
root = tk.Tk()
root.title("Сравнение папок")
root.geometry("586x384")

# Интерфейс выбора папок
folder1_label = tk.Label(root, text="Не выбрана", width=50, anchor="center")
folder1_label.pack(pady=5)
folder1_button = tk.Button(root, text="Выберите первую папку", command=lambda: choose_folder(folder1_label))
folder1_button.pack()

folder2_label = tk.Label(root, text="Не выбрана", width=50, anchor="center")
folder2_label.pack(pady=5)
folder2_button = tk.Button(root, text="Выберите вторую папку", command=lambda: choose_folder(folder2_label))
folder2_button.pack()

# Кнопка запуска сравнения
compare_button = tk.Button(root, text="Сравнить папки", command=compare_folders)
compare_button.pack(pady=10)

# Кнопка создания папки на рабочем столе
create_folder_button = tk.Button(root, text="Создать папку с уникальными файлами", command=create_folder_with_unique_files)
create_folder_button.pack(pady=10)

# Создание Text с полосой прокрутки
result_frame = tk.Frame(root)
result_frame.pack(pady=10, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(result_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_text_widget = tk.Text(result_frame, wrap="word", yscrollcommand=scrollbar.set, state=tk.DISABLED)
result_text_widget.pack(fill=tk.BOTH, expand=True)
scrollbar.config(command=result_text_widget.yview)

# Список для хранения путей уникальных файлов
unique_files = []

root.mainloop()
