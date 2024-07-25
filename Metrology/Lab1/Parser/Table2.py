import math
import tkinter as tk
from tkinter import ttk
import parser5
def calculate_metrics(operators, operands):
    n1 = len(operators)
    N1 = sum(operators.values())
    n2 = len(operands)
    N2 = sum(operands.values())
    n = n1 + n2
    N = N1 + N2
    y = N * (n2**2)
    return n1, N1, n2, N2, n, N, y

def update_table(operators_dict, operands_dict, metrics_label):

    for row in table_data:
        for col in table_data[row]:
            table_data[row][col].config(text="")

    row_num = 1
    for key in operators_dict:
        table_data[row_num][0].config(text=row_num)
        table_data[row_num][1].config(text=key)
        table_data[row_num][2].config(text=operators_dict[key])
        row_num += 1

    row_num = 1
    for key in operands_dict:
        table_data[row_num][0].config(text=row_num)
        table_data[row_num][3].config(text=key)
        table_data[row_num][4].config(text=operands_dict[key])
        row_num += 1

    n1, N1, n2, N2, n, N, y = calculate_metrics(operators_dict, operands_dict)
    metrics_label.config(text=f"Словарь программы: n = {n1} + {n2} = {n1+n2}\nДлина программы: N = {N1} + {N2} = {N1+N2}\nОбъём программы: y = {N} * log2({n}) = {N*math.log2(n)}")

    table_data[row_num + 1][1].config(text=f"n1 = {n1}")
    table_data[row_num + 1][2].config(text=f"N1 = {N1}")
    table_data[row_num + 1][3].config(text=f"n2 = {n2}")
    table_data[row_num + 1][4].config(text=f"N2 = {N2}")

table_data = {}
def main(operators_dict, operands_dict):

    def on_canvas_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    root = tk.Tk()
    root.title("Таблица операторов и операндов")
    root.configure(bg="#1e1e1e")

    frame = tk.Frame(root, bg="#1e1e1e")
    frame.grid(row=0, column=0, sticky="nsew")

    headers = ["#", "Операторы", "Количество", "Операнды", "Количество"]

    for col, header in enumerate(headers):
        label = tk.Label(frame, text=header, padx=10, pady=5, relief=tk.RIDGE, font=('Helvetica', 8, 'bold'), bg="#2a2a2a", fg="white",width=9)
        label.grid(row=0, column=col)

    scrollbar = tk.Scrollbar(frame, orient="vertical")
    scrollbar.grid(row=1, column=len(headers), sticky="ns")

    canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set, bg="#1e1e1e", height=500)
    canvas.grid(row=1, column=0, columnspan=len(headers), sticky="nsew")

    canvas.bind("<Configure>", on_canvas_configure)

    table_frame = tk.Frame(canvas, bg="#1e1e1e")
    canvas.create_window((0, 0), window=table_frame, anchor="nw")

    for row in range(1, max(len(operators_dict), len(operands_dict)) + 6):
        table_data[row] = {}
        for col in range(5):
            label = tk.Label(table_frame, padx=10, pady=5, relief=tk.RIDGE, bg="#2a2a2a", fg="white",width=9)
            label.grid(row=row, column=col, sticky="nsew")
            table_data[row][col] = label

    metrics_label = tk.Label(frame, text="", padx=10, pady=5, font=('Helvetica', 10), bg="#1e1e1e", fg="white")
    metrics_label.grid(row=max(len(operators_dict), len(operands_dict)) + 7, column=0, columnspan=5, pady=10, sticky="nsew")

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_columnconfigure(len(headers), weight=1)

    scrollbar.config(command=canvas.yview)

    update_table(operators_dict, operands_dict, metrics_label)

    root.mainloop()

if __name__ == '__main__':
    parser5.calculate_metrics()
    main(parser5.operators, parser5.operands)
