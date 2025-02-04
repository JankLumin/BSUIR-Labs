import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

EN_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
EN_LOWER = EN_UPPER.lower()

RU_UPPER = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
RU_LOWER = RU_UPPER.lower()

def get_alphabets(language):
    if language == "English":
        return EN_UPPER, EN_LOWER
    else:
        return RU_UPPER, RU_LOWER

def caesar_encrypt(text, shift, language):
    alph_upper, alph_lower = get_alphabets(language)
    len_alpha = len(alph_upper)
    result = ""
    for char in text:
        if char in alph_upper:
            index = alph_upper.find(char)
            new_index = (index + shift) % len_alpha
            result += alph_upper[new_index]
        elif char in alph_lower:
            index = alph_lower.find(char)
            new_index = (index + shift) % len_alpha
            result += alph_lower[new_index]
        else:
            result += char
    return result

def caesar_decrypt(text, shift, language):
    return caesar_encrypt(text, -shift, language)

def generate_key(text, key, language):
    alph_upper, alph_lower = get_alphabets(language)
    key_filtered = "".join([ch for ch in key if ch in alph_upper or ch in alph_lower])
    if not key_filtered:
        return ""
    expanded_key = ""
    key_index = 0
    for char in text:
        if char in alph_upper or char in alph_lower:
            expanded_key += key_filtered[key_index % len(key_filtered)]
            key_index += 1
        else:
            expanded_key += char
    return expanded_key

def vigenere_encrypt(text, key, language):
    alph_upper, alph_lower = get_alphabets(language)
    len_alpha = len(alph_upper)
    expanded_key = generate_key(text, key, language)
    if not expanded_key:
        return text
    cipher_text = ""
    for t_char, k_char in zip(text, expanded_key):
        if t_char in alph_upper:
            shift = alph_upper.find(k_char.upper())
            new_index = (alph_upper.find(t_char) + shift) % len_alpha
            cipher_text += alph_upper[new_index]
        elif t_char in alph_lower:
            shift = alph_upper.find(k_char.upper())
            new_index = (alph_lower.find(t_char) + shift) % len_alpha
            cipher_text += alph_lower[new_index]
        else:
            cipher_text += t_char
    return cipher_text

def vigenere_decrypt(text, key, language):
    alph_upper, alph_lower = get_alphabets(language)
    len_alpha = len(alph_upper)
    expanded_key = generate_key(text, key, language)
    if not expanded_key:
        return text
    original_text = ""
    for t_char, k_char in zip(text, expanded_key):
        if t_char in alph_upper:
            shift = alph_upper.find(k_char.upper())
            new_index = (alph_upper.find(t_char) - shift + len_alpha) % len_alpha
            original_text += alph_upper[new_index]
        elif t_char in alph_lower:
            shift = alph_upper.find(k_char.upper())
            new_index = (alph_lower.find(t_char) - shift + len_alpha) % len_alpha
            original_text += alph_lower[new_index]
        else:
            original_text += t_char
    return original_text

def read_file(filename):
    try:
        with open(filename, 'r', encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        messagebox.showerror("Ошибка чтения файла", str(e))
        return None

def write_file(filename, text):
    try:
        with open(filename, 'w', encoding="utf-8") as f:
            f.write(text)
    except Exception as e:
        messagebox.showerror("Ошибка записи файла", str(e))

class CipherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Шифры")
        self.geometry("300x500")
        self.minsize(300, 500)
        self.cipher_type = tk.StringVar(value="Цезаря")
        self.action = tk.StringVar(value="Зашифровать")
        self.language = tk.StringVar(value="English")
        self.shift_value = tk.StringVar()
        self.vigenere_key = tk.StringVar()
        self.input_filename = tk.StringVar(value="Файл не выбран")
        self.output_filename = tk.StringVar(value="Файл не выбран")
        self.create_widgets()

    def create_widgets(self):
        frame_cipher = ttk.LabelFrame(self, text="Выбор шифра")
        frame_cipher.pack(padx=10, pady=10, fill="x")
        rb_caesar = ttk.Radiobutton(frame_cipher, text="Шифр Цезаря", variable=self.cipher_type, value="Цезаря", command=self.toggle_params)
        rb_vigenere = ttk.Radiobutton(frame_cipher, text="Шифр Виженера", variable=self.cipher_type, value="Виженера", command=self.toggle_params)
        rb_caesar.pack(side="left", padx=10, pady=5)
        rb_vigenere.pack(side="left", padx=10, pady=5)
        frame_action = ttk.LabelFrame(self, text="Действие")
        frame_action.pack(padx=10, pady=10, fill="x")
        rb_encrypt = ttk.Radiobutton(frame_action, text="Зашифровать", variable=self.action, value="Зашифровать")
        rb_decrypt = ttk.Radiobutton(frame_action, text="Дешифровать", variable=self.action, value="Дешифровать")
        rb_encrypt.pack(side="left", padx=10, pady=5)
        rb_decrypt.pack(side="left", padx=10, pady=5)
        frame_language = ttk.LabelFrame(self, text="Язык")
        frame_language.pack(padx=10, pady=10, fill="x")
        rb_en = ttk.Radiobutton(frame_language, text="English", variable=self.language, value="English")
        rb_ru = ttk.Radiobutton(frame_language, text="Русский", variable=self.language, value="Русский")
        rb_en.pack(side="left", padx=10, pady=5)
        rb_ru.pack(side="left", padx=10, pady=5)
        self.frame_params = ttk.LabelFrame(self, text="Параметры")
        self.frame_params.pack(padx=10, pady=10, fill="x")
        self.label_shift = ttk.Label(self.frame_params, text="Сдвиг:")
        self.entry_shift = ttk.Entry(self.frame_params, textvariable=self.shift_value, width=10)
        self.label_key = ttk.Label(self.frame_params, text="Ключ:")
        self.entry_key = ttk.Entry(self.frame_params, textvariable=self.vigenere_key, width=15)
        self.toggle_params()
        frame_files = ttk.LabelFrame(self, text="Файлы")
        frame_files.pack(padx=10, pady=10, fill="x")
        btn_input = ttk.Button(frame_files, text="Выбрать входной файл", command=self.select_input_file)
        btn_input.pack(padx=10, pady=5, anchor="w")
        self.label_input = ttk.Label(frame_files, textvariable=self.input_filename)
        self.label_input.pack(padx=10, pady=5, anchor="w")
        btn_output = ttk.Button(frame_files, text="Выбрать файл для сохранения", command=self.select_output_file)
        btn_output.pack(padx=10, pady=5, anchor="w")
        self.label_output = ttk.Label(frame_files, textvariable=self.output_filename)
        self.label_output.pack(padx=10, pady=5, anchor="w")
        btn_process = ttk.Button(self, text="Выполнить", command=self.process_file)
        btn_process.pack(padx=10, pady=15)

    def toggle_params(self, *args):
        for widget in self.frame_params.winfo_children():
            widget.pack_forget()
        cipher = self.cipher_type.get()
        if cipher == "Цезаря":
            self.label_shift.pack(side="left", padx=10, pady=5)
            self.entry_shift.pack(side="left", padx=10, pady=5)
        else:
            self.label_key.pack(side="left", padx=10, pady=5)
            self.entry_key.pack(side="left", padx=10, pady=5)

    def select_input_file(self):
        filename = filedialog.askopenfilename(title="Выберите входной файл", filetypes=[("Все файлы", "*.*")])
        if filename:
            self.input_filename.set(filename)

    def select_output_file(self):
        filename = filedialog.asksaveasfilename(title="Выберите файл для сохранения", defaultextension=".txt", filetypes=[("Все файлы", "*.*")])
        if filename:
            self.output_filename.set(filename)

    def process_file(self):
        in_file = self.input_filename.get()
        out_file = self.output_filename.get()
        if in_file == "Файл не выбран" or out_file == "Файл не выбран":
            messagebox.showwarning("Внимание", "Пожалуйста, выберите входной и выходной файлы.")
            return
        text = read_file(in_file)
        if text is None:
            return
        cipher = self.cipher_type.get()
        action = self.action.get()
        lang = self.language.get()
        result = ""
        if cipher == "Цезаря":
            try:
                shift = int(self.shift_value.get())
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректное числовое значение для сдвига.")
                return
            if action == "Зашифровать":
                result = caesar_encrypt(text, shift, lang)
            else:
                result = caesar_decrypt(text, shift, lang)
        else:
            key = self.vigenere_key.get().strip()
            if not key:
                messagebox.showerror("Ошибка", "Введите ключ для шифра Виженера.")
                return
            alph_upper, alph_lower = get_alphabets(lang)
            if any(ch not in alph_upper and ch not in alph_lower for ch in key):
                messagebox.showerror("Ошибка", "Ключ должен состоять только из букв выбранного языка.")
                return
            if action == "Зашифровать":
                result = vigenere_encrypt(text, key, lang)
            else:
                result = vigenere_decrypt(text, key, lang)
        write_file(out_file, result)
        messagebox.showinfo("Готово", f"Результат сохранён в:\n{out_file}")

if __name__ == "__main__":
    app = CipherApp()
    app.mainloop()
