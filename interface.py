import tkinter as tk
from tkinter import messagebox
import json
import matplotlib.pyplot as plt
from pathlib import Path
from PIL import Image, ImageTk
from main_py import plot_total_listen_time
from log_parser import plot_day_period_pie
import turtle
import math
import threading
import time

window = tk.Tk()
window.title("La Musica")
window.geometry("500x400")
import main_py

# Основні кольори
BG_COLOR = "#FFB6C1"  # рожевий
TEXT_COLOR = "#4B2E05"  # темно-коричневий

window.configure(bg=BG_COLOR)

label = tk.Label(window, text="Write 1 to start the program!!!\nWrite 2 to exit the program!!!",
                 font=("Arial", 14), bg=BG_COLOR, fg=TEXT_COLOR)
label.pack(pady=10)

entry = tk.Entry(window, width=30)
entry.pack(pady=5)

# --- кнопка з округлими краями ---
button_style = {"bg": "white", "fg": TEXT_COLOR, "height": 2, "width": 20,
                "relief": "groove", "bd": 3}


def say_hello(event=None):
    user_choice = entry.get().strip()
    if user_choice == "1":
        start_program()
    elif user_choice == "2":
        window.destroy()


    else:
        messagebox.showerror("Error", "Please write 1 - 4!")


entry.bind('<Return>', say_hello)


def start_program():
    label = tk.Label(window, text="Select song",
                     font=("Arial", 14), bg=BG_COLOR, fg=TEXT_COLOR)
    label.pack(pady=10)
    # Фрейм для тексту і картинок
    songs_frame = tk.Frame(window, bg=BG_COLOR)
    songs_frame.pack(pady=10, fill="x")

    # Entry для вибору
    select_song = tk.Entry(songs_frame, width=30)
    select_song.pack(pady=5)

    # Фрейм для картинок
    album_frame = tk.Frame(songs_frame, width=150, height=150, bg=BG_COLOR)
    album_frame.pack(pady=5)
    album_frame.pack_propagate(False)  # важливо, щоб розмір не змінювався
    album_label = tk.Label(album_frame, bg=BG_COLOR)
    album_label.pack(fill="both", expand=True)

    # Завантажуємо картинки один раз
    album_images = {
        "1": "static/images/beat_it.jpg",
        "2": "static/images/hey_baby.jpg",
        "3": "static/images/on_the_floor.jpg",
        "4": "static/images/tears.jpg"
    }
    loaded_images = {}
    for key, path in album_images.items():
        img = Image.open(path)
        img = img.resize((150, 150))
        loaded_images[key] = ImageTk.PhotoImage(img)

    # Функції для hover
    def show_album(n):
        album_label.config(image=loaded_images[n])

    def hide_album():
        album_label.config(image="")

    # Створюємо Label для кожної пісні
    songs = [("1: Beat It", "1"), ("2: Hey Baby", "2"), ("3: On The Floor", "3"), ("4: Tears", "4")]
    for text, num in songs:
        song_label = tk.Label(songs_frame, text=text, font=("Arial", 14),
                              bg=BG_COLOR, fg=TEXT_COLOR, cursor="hand2")
        song_label.pack(anchor="w", padx=50)
        song_label.bind("<Enter>", lambda e, n=num: show_album(n))
        song_label.bind("<Leave>", lambda e: hide_album())
    def confirm_song(event=None):
        try:
            song_num = int(select_song.get())
            if song_num not in range(1, 5):
                raise ValueError
            messagebox.showinfo("OK", f"You selected song #{song_num}")
            main_py.song = song_num
            select_speed()
            with open("info.json", "r") as f:
                data = json.load(f)
            data.append(song_num)
            with open("info.json", "w") as f:
                json.dump(data, f)
        except ValueError:
            messagebox.showerror("Error", "Enter number 1-4!")

        select_song.bind('<Return>', confirm_song)
        tk.Button(window, text="OK", command=confirm_song, **button_style).pack(pady=5)


def select_speed():
    for widget in window.winfo_children():
        widget.destroy()

    label_speed = tk.Label(window, text="Enter speed (0.1x - 2.5x):",
                           font=("Arial", 14), bg=BG_COLOR, fg=TEXT_COLOR)
    label_speed.pack(pady=10)
    select_speed_entry = tk.Entry(window, width=30)
    select_speed_entry.pack(pady=5)

    def confirm_speed(event=None):
        try:
            speed = float(select_speed_entry.get())
            if not 0.1 <= speed <= 2.5:
                raise ValueError
            messagebox.showinfo("OK", f"Speed set to {speed}x")
            select_volume()
        except ValueError:
            messagebox.showerror("Error", "Enter number between 0.1 and 2.5!")

    select_speed_entry.bind('<Return>', confirm_speed)
    tk.Button(window, text="OK", command=confirm_speed, **button_style).pack(pady=5)


def select_volume():
    for widget in window.winfo_children():
        widget.destroy()

    label_volume = tk.Label(window, text="Enter volume (1-100%):",
                            font=("Arial", 14), bg=BG_COLOR, fg=TEXT_COLOR)
    label_volume.pack(pady=10)
    select_volume_entry = tk.Entry(window, width=30)
    select_volume_entry.pack(pady=5)

    def confirm_volume(event=None):
        try:
            volume = float(select_volume_entry.get())
            if not 1 <= volume <= 100:
                raise ValueError
            messagebox.showinfo("OK", f"Volume set to {volume}%")
            select_repeat()
        except ValueError:
            messagebox.showerror("Error", "Enter number between 1 and 100!")

    select_volume_entry.bind('<Return>', confirm_volume)
    tk.Button(window, text="OK", command=confirm_volume, **button_style).pack(pady=5)


def select_repeat():
    for widget in window.winfo_children():
        widget.destroy()

    label_repeat = tk.Label(window,
                            text="Would you like to listen on repeat?\n Print Yes or No",
                            font=("Arial", 14), bg=BG_COLOR, fg=TEXT_COLOR)
    label_repeat.pack(pady=10)

    select_repeat_entry = tk.Entry(window, width=30)
    select_repeat_entry.pack(pady=5)

    def heart_loader(duration=4):
        def draw_heart():
            screen = turtle.Screen()
            screen.bgcolor("black")
            t = turtle.Turtle()
            t.hideturtle()
            t.speed(0)  # максимально швидко малює
            t.color("white")
            t.penup()

            start_time = time.time()
            k = 0
            t.goto(0, 0)

            while time.time() - start_time < duration:
                x = 15 * math.sin(k)
                3 * 20
                y = (12 * math.cos(k) - 5 * math.cos(2 * k) - 2 * math.cos(3 * k) - math.cos(4 * k)) * 20
                if k == 0:
                    t.goto(x, y)
                    t.pendown()
                else:
                    t.goto(x, y)
                k += 0.05  # менший крок → плавніша лінія

            t.penup()
            t.goto(0, 0)
            screen.bye()  # закриває вікно turtle

        thread = threading.Thread(target=draw_heart)
        thread.start()
        thread.join()

    def confirm_repeat(event=None):
        try:
            repeat_choice = (select_repeat_entry.get()).lower()
            if repeat_choice == "yes":
                for widget in window.winfo_children():
                    widget.destroy()

                label_count = tk.Label(window, text="How many times (1-2)?",
                                       font=("Arial", 14), bg=BG_COLOR, fg=TEXT_COLOR)
                label_count.pack(pady=10)

                count_entry = tk.Entry(window, width=30)
                count_entry.pack(pady=5)
                count_entry.bind('<Return>', confirm_repeat)

                def confirm_count(event=None):
                    try:
                        count = int(count_entry.get())
                        if count in range(1, 3):
                            messagebox.showinfo("Repeat", f"OK! It will repeat {count} times")
                            try:
                                song_path = main_py.get_song_path(main_py.song)
                                heart_loader(duration=4)  # показати лоадер 8 секунд
                                main_py.start_webpage(song_path)
                            except Exception as e:
                                messagebox.showerror("Error", f"Cannot open webpage: {e}")
                            window.destroy()
                        else:
                            raise ValueError
                    except ValueError:
                        messagebox.showerror("Error", "Enter number 1-2!")

                count_entry.bind('<Return>', confirm_count)
                tk.Button(window, text="OK", command=confirm_count, **button_style).pack(pady=5)

            elif repeat_choice == "no":
                messagebox.showinfo("Repeat", "Ok! It won't repeat.")
                try:
                    song_path = main_py.get_song_path(main_py.song)
                    heart_loader(duration=8)  # показати лоадер 8 секунд
                    main_py.start_webpage(song_path)
                except Exception as e:
                    messagebox.showerror("Error", f"Cannot open webpage: {e}")
                window.destroy()
            else:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter Yes or No!")

    select_repeat_entry.bind('<Return>', confirm_repeat)
    tk.Button(window, text="OK", command=confirm_repeat, **button_style).pack(pady=5)


def graphic():
    hours = Path("info.json")
    with open(hours, "r") as f:
        file = json.load(f)

    fig, ax = plt.subplots(figsize=(9, 9))
    ax.hist(file, bins=range(min(file), max(file) + 2),
            edgecolor="black", color="skyblue", rwidth=0.9, align="left")
    ax.set_xticks(range(min(file), max(file) + 1))
    ax.set_yticks(range(0, int(max(ax.get_ylim())) + 1))
    ax.set_xlim(min(file) - 0.5, max(file) + 0.5)
    ax.set_title("Top Ratings", fontsize=18, fontweight="bold")
    ax.set_xlabel("Songs", fontsize=14)
    ax.set_ylabel("Amount", fontsize=14)
    ax.grid(axis="y", linestyle="--", alpha=0.6)
    Path("static").mkdir(exist_ok=True)
    plt.savefig("static/graph.png", bbox_inches="tight")
    plt.show()


# Перше вікно
button = tk.Button(window, text="OK", command=say_hello, **button_style)
button.pack(pady=10)

window.mainloop()
