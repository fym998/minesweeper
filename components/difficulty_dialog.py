import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys


rows, cols, mines = 0,0,0

def show_difficulty_dialog(default_rows=9, default_cols=9, default_mines=5):
    # 创建主窗口
    root = tk.Tk()
    root.title("选择扫雷难度")

    # 设置默认值

    global rows, cols, mines
    rows, cols, mines = default_rows, default_cols, default_mines
    # 定义行数、列数和雷数输入框的提示文本
    def validate_input():
        global rows, cols, mines
        try:
            # 获取输入值
            rows = int(entry_rows.get())
            cols = int(entry_cols.get())
            mines = int(entry_mines.get())

            # 验证行数和列数是否符合要求
            if rows < 9:
                rows = 9
            if cols < 9:
                cols = 9

            # 验证雷数是否符合要求
            if mines < 1:
                mines = 1
            if mines >= rows * cols:
                mines = rows * cols - 1

            # 返回调整后的值
            return rows, cols, mines

        except ValueError:
            messagebox.showerror("扫雷", "请输入有效的数字！")
            return None

    # 定义提交按钮
    def submit():
        global rows, cols, mines
        result = validate_input()
        if result:
            rows, cols, mines = result
            # messagebox.showinfo("难度设置", f"行数: {rows}, 列数: {cols}, 雷数: {mines}")
            root.quit()
            root.destroy()  # 关闭窗口

    # 行数输入框
    label_rows = ttk.Label(root, text="行数:")
    label_rows.grid(row=0, column=0)
    entry_rows = ttk.Entry(root)
    entry_rows.insert(0, default_rows)
    entry_rows.grid(row=0, column=1)

    # 列数输入框
    label_cols = ttk.Label(root, text="列数:")
    label_cols.grid(row=1, column=0)
    entry_cols = ttk.Entry(root)
    entry_cols.insert(0, default_cols)
    entry_cols.grid(row=1, column=1)

    # 雷数输入框
    label_mines = ttk.Label(root, text="雷数:")
    label_mines.grid(row=2, column=0)
    entry_mines = ttk.Entry(root)
    entry_mines.insert(0, default_mines)
    entry_mines.grid(row=2, column=1)

    # 提交按钮
    button_submit = ttk.Button(root, text="确认", command=submit)
    button_submit.grid(row=3, column=0, columnspan=2)

    # 运行主循环
    root.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))
    root.mainloop()

    return rows, cols, mines
