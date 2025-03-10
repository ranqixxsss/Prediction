import zipfile  # 处理 ZIP 文件
import pandas as pd  # 处理 Excel 和 CSV 文件
import os  # 处理文件和路径操作
import re  # 处理字符串替换
import tkinter as tk  # 创建 GUI 界面
from tkinter import filedialog, messagebox, scrolledtext  # GUI 组件用于文件对话框、消息框和滚动文本框


def extract_zip(extract_button, convert_button, log_text):
    """
    解压 ZIP 文件的函数。选择 ZIP 文件并解压到用户指定的目录。

    :param extract_button: 解压按钮（用于在执行过程中禁用）
    :param convert_button: 转换按钮（用于在执行过程中禁用）
    :param log_text: 日志框（用于显示操作日志）
    """

    # 禁用按钮，防止用户在操作过程中多次点击
    extract_button.config(state="disabled")
    convert_button.config(state="disabled")
    log_text.delete(1.0, tk.END)  # 清空日志框

    # 让用户选择 ZIP 文件
    zip_path = filedialog.askopenfilename(title="选择 ZIP 文件", filetypes=[("ZIP Files", "*.zip")])
    if not zip_path:
        # 如果用户未选择文件，恢复按钮状态并返回
        extract_button.config(state="normal")
        convert_button.config(state="normal")
        return

    # 让用户选择解压目标文件夹
    extract_path = filedialog.askdirectory(title="选择解压目标文件夹")
    if not extract_path:
        extract_button.config(state="normal")
        convert_button.config(state="normal")
        return

    try:
        # 打开 ZIP 文件
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            log_text.insert(tk.END, "正在解压文件...\n")

            # 遍历 ZIP 内的所有文件
            for file in zip_ref.infolist():
                try:
                    # 解决 ZIP 文件名编码问题（Windows 下 ZIP 默认编码是 cp437）
                    filename = file.filename.encode('cp437').decode('gbk')
                except UnicodeDecodeError:
                    filename = file.filename  # 如果解码失败，使用原始文件名

                file_path = os.path.join(extract_path, filename)

                # 如果是目录，则创建目录并跳过后续解压操作
                if file.is_dir():
                    os.makedirs(file_path, exist_ok=True)
                    continue

                # 确保目标文件的父目录存在
                os.makedirs(os.path.dirname(file_path), exist_ok=True)

                # 解压文件
                with zip_ref.open(file.filename) as source, open(file_path, "wb") as target:
                    target.write(source.read())

                # 记录日志
                log_text.insert(tk.END, f"解压: {filename}\n")
                log_text.yview(tk.END)  # 滚动到最新日志

        messagebox.showinfo("成功", "解压完成！")  # 弹出成功提示框
    except Exception as e:
        messagebox.showerror("错误", f"解压过程中发生错误: {e}")  # 弹出错误提示框

    # 恢复按钮状态
    extract_button.config(state="normal")
    convert_button.config(state="normal")


def convert_to_csv(extract_button, convert_button, log_text):
    """
    将 Excel 文件转换为 CSV 格式，并保存到用户指定的目录。

    :param extract_button: 解压按钮（用于在执行过程中禁用）
    :param convert_button: 转换按钮（用于在执行过程中禁用）
    :param log_text: 日志框（用于显示操作日志）
    """

    # 禁用按钮，防止重复操作
    extract_button.config(state="disabled")
    convert_button.config(state="disabled")
    log_text.delete(1.0, tk.END)  # 清空日志框

    # 选择 Excel 文件
    xlsx_path = filedialog.askopenfilename(title="选择 Excel 文件", filetypes=[("Excel Files", "*.xlsx")])
    if not xlsx_path:
        convert_button.config(state="normal")
        extract_button.config(state="normal")
        return

    # 选择 CSV 文件的保存目录
    output_folder = filedialog.askdirectory(title="选择保存路径")
    if not output_folder:
        convert_button.config(state="normal")
        extract_button.config(state="normal")
        return

    # 手动定义 Excel 表名到 CSV 文件名的映射
    sheet_name_map = {
        "糖尿病（无冠心病）": "diabetes_no_CHD",
        "高血压（无冠心病）": "hypertension_no_CHD",
        "糖尿病（有冠心病）": "diabetes_with_CHD",
        "高血压（有冠心病）": "hypertension_with_CHD"
    }

    try:
        # 读取 Excel 文件的所有 Sheet
        sheets = pd.read_excel(xlsx_path, sheet_name=None, engine="openpyxl")
        log_text.insert(tk.END, "正在转换为 CSV 格式...\n")

        for sheet_name, df in sheets.items():
            # 获取对应的英文名称，如果没有匹配项，默认使用“Sheet_原名”
            english_name = sheet_name_map.get(sheet_name, f"Sheet_{sheet_name}")

            # 清理文件名，去掉不合法字符
            english_name = re.sub(r'[/*?"<>|]', '_', english_name)
            csv_path = os.path.join(output_folder, f"{english_name}.csv")

            # 将数据写入 CSV 文件
            df.to_csv(csv_path, index=False, encoding="utf-8")

            # 记录日志
            log_text.insert(tk.END, f"转换: {sheet_name} -> {csv_path}\n")
            log_text.yview(tk.END)  # 滚动到最新日志

        messagebox.showinfo("成功", "所有 Sheet 已转换完成！")  # 弹出成功提示框
    except Exception as e:
        messagebox.showerror("错误", f"读取 Excel 或转换过程中发生错误: {e}")  # 弹出错误提示框

    # 恢复按钮状态
    extract_button.config(state="normal")
    convert_button.config(state="normal")


def create_gui():
    """
    创建主 GUI 界面，包括解压 ZIP 和 Excel 转 CSV 按钮，以及日志显示窗口。
    """

    root = tk.Tk()
    root.title("数据处理工具")  # 设置窗口标题
    root.geometry("500x400")  # 设置窗口大小

    # 创建标题标签
    title_label = tk.Label(root, text="选择操作", font=("Arial", 14))
    title_label.pack(pady=10)

    # 创建“解压 ZIP”按钮
    extract_button = tk.Button(root, text="解压 ZIP 文件",
                               command=lambda: extract_zip(extract_button, convert_button, log_text), width=20)
    extract_button.pack(pady=10)

    # 创建“转换 Excel 到 CSV”按钮
    convert_button = tk.Button(root, text="转换 Excel 到 CSV",
                               command=lambda: convert_to_csv(extract_button, convert_button, log_text), width=20)
    convert_button.pack(pady=10)

    # 创建滚动文本框，用于显示日志信息
    log_text = scrolledtext.ScrolledText(root, width=50, height=12, wrap=tk.WORD, state=tk.NORMAL)
    log_text.pack(pady=10)

    # 启动 GUI 事件循环
    root.mainloop()


# 运行 GUI 程序
create_gui()
