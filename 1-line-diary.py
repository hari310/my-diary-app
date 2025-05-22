import tkinter as tk
from datetime import datetime

# 🎨 カラーテーマの設定
THEMES = {
    "🌸 パステル": {"bg": "#FFFAF0", "button": "#FFDAB9", "table": "#FFFFFF"},
    "🌙 ダークモード": {"bg": "#2E2E2E", "button": "#505050", "table": "#3C3C3C"},
    "🍃 グリーン": {"bg": "#E6F4EA", "button": "#A8D5BA", "table": "#FFFFFF"},
    "🌞 ビタミンカラー": {"bg": "#FFF5CC", "button": "#FFA07A", "table": "#FFFFFF"},
}

current_theme = "🌸 パステル"  # デフォルトテーマ

# Tkinterウィンドウの作成
root = tk.Tk()
root.title("🌸 一行日記アプリ 🌸")

# テーマを適用する関数
def apply_theme():
    theme = THEMES[current_theme]
    root.configure(bg=theme["bg"])
    result_label.configure(bg=theme["bg"])
    save_button.configure(bg=theme["button"])
    recall_button.configure(bg=theme["button"])
    export_button.configure(bg=theme["button"])

def change_theme(selection):
    global current_theme
    current_theme = selection
    apply_theme()

# テーマ選択メニュー
theme_var = tk.StringVar(root)
theme_var.set(current_theme)
theme_menu = tk.OptionMenu(root, theme_var, *THEMES.keys(), command=change_theme)
theme_menu.pack(pady=5)

# ✏️ 📌 日記を書く部分（入力欄）をここに追加！
tk.Label(root, text="今日のひとこと ✏️（最大50文字）:", font=("Comic Sans MS", 12), bg=THEMES[current_theme]["bg"]).pack()
text_entry = tk.Entry(root, width=40, font=("Comic Sans MS", 12))  # 入力欄の定義
text_entry.pack(pady=10)  # 入力欄を画面に配置

# 📌 保存機能
def save_diary():
    entry = text_entry.get()
    if len(entry) > 50:
        result_label.config(text="⚠️ 50文字以内にしてください！", fg="red")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    with open("diary.txt", "a") as file:
        file.write(f"{timestamp} - {entry}\n")

    result_label.config(text="✅ 日記を保存しました！", fg="green")
    text_entry.delete(0, tk.END)

# 📖 回想機能（過去の日記を表形式で表示）
def show_diary():
    try:
        with open("diary.txt", "r") as file:
            diary_entries = file.readlines()

        diary_window = tk.Toplevel(root)
        diary_window.title("📖 過去の日記")
        diary_window.configure(bg=THEMES[current_theme]["bg"])

        tk.Label(diary_window, text="📖 過去の記録", font=("Comic Sans MS", 12), bg=THEMES[current_theme]["bg"]).pack()

        frame = tk.Frame(diary_window, bg=THEMES[current_theme]["table"])
        frame.pack(padx=10, pady=5, fill="both")

        tk.Label(frame, text="✔️", font=("Comic Sans MS", 12), bg=THEMES[current_theme]["table"]).grid(row=0, column=0, padx=5)
        tk.Label(frame, text="日付", font=("Comic Sans MS", 12), bg=THEMES[current_theme]["table"]).grid(row=0, column=1, padx=5)
        tk.Label(frame, text="内容", font=("Comic Sans MS", 12), bg=THEMES[current_theme]["table"]).grid(row=0, column=2, padx=5)

        entry_vars = []

        for i, entry in enumerate(diary_entries, start=1):
            date, content = entry.strip().split(" - ")
            var = tk.BooleanVar()
            tk.Checkbutton(frame, variable=var, bg=THEMES[current_theme]["table"]).grid(row=i, column=0, padx=5)
            tk.Label(frame, text=date, font=("Comic Sans MS", 12), bg=THEMES[current_theme]["table"]).grid(row=i, column=1, padx=5)
            tk.Label(frame, text=content, font=("Comic Sans MS", 12), bg=THEMES[current_theme]["table"]).grid(row=i, column=2, padx=5)
            entry_vars.append((var, entry))

        # 🗑️ 削除機能（チェックをつけた行のみ削除）
        def delete_selected():
            new_entries = [entry for var, entry in entry_vars if not var.get()]
            with open("diary.txt", "w") as file:
                file.writelines(new_entries)

            entry_vars.clear()

            for widget in frame.winfo_children():
                widget.destroy()

            tk.Label(frame, text="✔️", font=("Comic Sans MS", 12), bg=THEMES[current_theme]["table"]).grid(row=0, column=0, padx=5)
            tk.Label(frame, text="日付", font=("Comic Sans MS", 12), bg=THEMES[current_theme]["table"]).grid(row=0, column=1, padx=5)
            tk.Label(frame, text="内容", font=("Comic Sans MS", 12), bg=THEMES[current_theme]["table"]).grid(row=0, column=2, padx=5)

            with open("diary.txt", "r") as file:
                diary_entries = file.readlines()

            for i, entry in enumerate(diary_entries, start=1):
                date, content = entry.strip().split(" - ")
                var = tk.BooleanVar()
                tk.Checkbutton(frame, variable=var, bg=THEMES[current_theme]["table"]).grid(row=i, column=0, padx=5)
                tk.Label(frame, text=date, font=("Comic Sans MS", 12), bg=THEMES[current_theme]["table"]).grid(row=i, column=1, padx=5)
                tk.Label(frame, text=content, font=("Comic Sans MS", 12), bg=THEMES[current_theme]["table"]).grid(row=i, column=2, padx=5)
                entry_vars.append((var, entry))

            result_label.config(text="🗑 選択した日記を削除しました！", fg="red")

        delete_button = tk.Button(diary_window, text="🗑 削除", command=delete_selected, bg=THEMES[current_theme]["button"], font=("Comic Sans MS", 12))
        delete_button.pack(pady=5)

        tk.Button(diary_window, text="閉じる", command=diary_window.destroy, bg=THEMES[current_theme]["button"], font=("Comic Sans MS", 12)).pack(pady=5)

    except FileNotFoundError:
        result_label.config(text="⚠️ まだ日記がありません！", fg="red")

# ✐ 書出機能
def export_diary():
    with open("diary.txt", "r") as diary_file:
        diary_content = diary_file.read()

    with open("export.txt", "w") as export_file:
        export_file.write(diary_content)

    result_label.config(text="📂 日記を書き出しました！（export.txt）", fg="blue")

# ボタンの設定
save_button = tk.Button(root, text="💾 保存", command=save_diary, font=("Comic Sans MS", 12))
save_button.pack(pady=5)

recall_button = tk.Button(root, text="📖 回想", command=show_diary, font=("Comic Sans MS", 12))
recall_button.pack(pady=5)

export_button = tk.Button(root, text="✐書出", command=export_diary, font=("Comic Sans MS", 12))
export_button.pack(pady=5)

result_label = tk.Label(root, text="", font=("Comic Sans MS", 12))
result_label.pack(pady=10)

apply_theme()  # 初期テーマ適用
root.mainloop()
