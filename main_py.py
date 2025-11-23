import pygame
from pathlib import Path
import webbrowser
from flask import Flask, render_template, send_from_directory
import threading
import json
import matplotlib.pyplot as plt
import time
import os
from mutagen.mp3 import MP3
from log_parser import log_play, plot_day_period_pie


def update_play_log_with_length():
    # прочитати існуючі логи як список
    if not os.path.exists("play_log.json"):
        play_log = []
    else:
        with open("play_log.json", "r") as f:
            play_log = json.load(f)

    # знайти всі існуючі метадані, щоб не дублювати
    existing_lengths = {entry["song_name"] for entry in play_log
                        if "song_name" in entry}

    for file in mp3_files:
        song_name = file.name
        audio = MP3(file)
        length_min = round(audio.info.length / 60, 2)

        # додаємо лише якщо немає метаданих
        if song_name not in existing_lengths:
            play_log.append({
                "song_name": song_name,
                "plays": 0,
                "length_min": length_min
            })

    # і головне → НЕ стираємо, а ПЕРЕЗАПИСУЄМО той самий список
    with open("play_log.json", "w") as f:
        json.dump(play_log, f, indent=4)


music_folder = Path("./music")
mp3_files = [file for file in music_folder.glob("*.mp3")]
music_files_name = [file.name for file in music_folder.glob("*.mp3")]



lyrics_folder = Path("./music")
txt_files = [file for file in music_folder.glob("*.txt")]
lyrics_file_name = [file.name for file in music_folder.glob("*.txt")]

# MUSIC_FILES_NAME = ["beat_it.mp3", "tears.mp3", "hey_baby.mp3"]
# PATH = "./music/"

lyrics_dict = {"on_the_floor.mp3": r"D:\Users\User\PycharmProjects\PythonProject15\music\on_the_floor.txt",
               "tears.mp3": r"D:\Users\User\PycharmProjects\PythonProject15\music\tears.txt",
               "hey_baby.mp3": r"D:\Users\User\PycharmProjects\PythonProject15\music\hey_baby.txt",
               "beat_it.mp3":r"D:\Users\User\PycharmProjects\PythonProject15\music\beat_it.txt"}





def ask_select():
    while True:
        count = 1
        for music_name in music_files_name:
            print(f"{count}:", music_name.replace(".mp3", "").replace("_", " ").title())
            count += 1
        try:
            global song
            song = int(input("Choose a song number (1-4): ").strip())
        except ValueError:
            print("Enter a number!")
            continue
        if song in range(1, 5):
            chosen_song = music_files_name[song - 1]
            log_play(chosen_song)
            return mp3_files[song - 1]


        print("Choose 1-3: ")


def create_file_if_not_exists():
    if not os.path.exists("info.json"):
        with open("info.json", "w") as f:
            json.dump([], f)
    #     print("Файл створено.")
    # else:
    #     print("Файл вже існує.")

def add_number(song):
    with open("info.json", "r") as f:
        numbers = json.load(f)

    numbers.append(song)

    with open("info.json", "w") as f:
        json.dump(numbers, f)





def ask_speed():
    while True:
        try:
            speed = float(input("Enter the speed(0.1x - 2.5x): "))
            if 0.1 <= speed <= 2.5:
                return speed
            else:
                print("Speed must be between 0.1x and 2.5x!")
        except ValueError:
            print("Enter a valid number!")


def ask_loud():
    while True:
        try:
            global loud
            loud = int(input("Enter the volume(1% - 100%): "))
            if 1 <= loud <= 31:
                print("Volume is low - everything’s fine! Enjoy your listening")
                return loud

            if loud in range(32, 61):
                print("Volume is at a medium level - listen carefully, prolonged exposure may cause ear fatigue")
                return loud

            if loud in range(61, 101):
                print("It's too loud, be careful!!")

                return loud
            if loud not in range(1, 101):
                print("1-100 only")

        except ValueError:
            print("Enter a number")
def ask_repeat():
    while True:
        print("Would you like to listen on repeat?")
        try:
            repeat = input("Yes or no? ").lower()
        except ValueError:
            print("Enter yes or no")
            continue
        except TypeError:
            print("Enter a word")
            continue
        if repeat == "yes":

                try:
                    count = int(input("How many times(1-2)? "))
                    if count in range(1, 3):
                        print(f"Ok! It will repeat {count} times")
                        return count

                    if count not in range(1, 3):
                        continue


                except ValueError:
                    print("Enter a number")
                    continue
        if repeat == "no":
                    print("Ok! It won`t repeat")
                    return 0

def play_music(song_file, repeat_count, speed, volume):
            try:
                pygame.mixer.music.load(song_file)
                pygame.mixer.music.set_volume( volume * 100)
                pygame.mixer.music.play(repeat_count)

                print(f"Playing {song_file} at {speed}x speed and volume {volume}%...")
            except ValueError:
                print(f"Error playing {song_file}")

            print("Playback finished!\n")

def song_lyrics(song_path):

            song_name = song_path.name

            if song_name in lyrics_dict:
                try:
                    with open(lyrics_dict[song_name], "r", encoding="utf-8") as f:
                        lyrics = f.read()
                    print("\n---------Song lyrics----------")
                    print(lyrics)
                    print("---------------------------------\n")
                except FileNotFoundError:
                    print("lyrics are not found")



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"))


@app.route("/play/<song_name>")
def play(song_name):
    log_play(song_name)   # ← ось тут додається час
    return render_template("player.html", song=song_name)

@app.route("/music/<path:filename>")
def serve_music(filename):
    return send_from_directory(str(music_folder), filename)

@app.route("/show/<song>")
def show(song):
    lyrics = ""
    if song in lyrics_dict:
        try:
            with open(lyrics_dict[song], "r", encoding="utf-8") as f:
                lyrics = f.read()
        except FileNotFoundError:
            lyrics = " Текст пісні не знайдено."
    return render_template("song.html", song_name=song, lyrics=lyrics)
def get_song_path(song_num):
    return mp3_files[song_num - 1]  # тому що список починається з 0


import socket

def _wait_for_port(host, port, timeout=5.0):
    """Проста перевірка, чи вже слухає сервер порт (чекати до timeout сек)."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=0.5):
                return True
        except OSError:
            time.sleep(0.1)
    return False

def start_webpage(song_path):
    song_name = song_path.name

    def run_flask():

        app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)


    flask_thread = threading.Thread(target=run_flask, daemon=False)
    flask_thread.start()


    if _wait_for_port("127.0.0.1", 5000, timeout=6.0):
        webbrowser.open(f"http://127.0.0.1:5000/show/{song_name}")
    else:
        print("Помилка: сервер Flask не запустився за очікуваний час.")


# def start_webpage(song_path):
#     song_name = song_path.name
#     def run_flask():
#         app.run(port=5000, debug=False)
#     threading.Thread(target=run_flask, daemon=True).start()
#
#     time.sleep(1.5)
#     webbrowser.open(f"http://127.0.0.1:5000/show/{song_name}")




def graphic():
    hours = Path("info.json")

    with open(hours, "r") as f:
        file = json.load(f)


    fig, ax = plt.subplots(figsize=(9, 9))
    ax.hist(
        file,
        bins=range(min(file), max(file) + 2),  # щоб поділки були по 1
        edgecolor="black",
        color="skyblue",
        rwidth=0.9,
        align="left"  # ширина стовпців — трохи менше 1, щоб були проміжки
    )

    ax.set_xticks(range(min(file), max(file) + 1))
    ax.set_yticks(range(0, int(max(ax.get_ylim())) + 1))

    ax.set_xlim(min(file) - 0.5, max(file) + 0.5)

    ax.set_title("Розподіл годин", fontsize=18, fontweight="bold")
    ax.set_xlabel("Години", fontsize=14)
    ax.set_ylabel("Кількість", fontsize=14)
    ax.grid(axis="y", linestyle="--", alpha=0.6)

    Path("static").mkdir(exist_ok=True)
    plt.savefig("static/graph.png", bbox_inches="tight")

    plt.show()


def plot_total_listen_time():
    if not os.path.exists("play_log.json"):
        print("Файл play_log.json не знайдено!")
        return

    with open("play_log.json", "r") as f:
        play_log = json.load(f)

    # агрегована статистика по піснях
    stats = {}

    for entry in play_log:
        # лог типу {"song": "...", "time": "..."} → це 1 прослуховування
        if "song" in entry:
            song = entry["song"]
            if song not in stats:
                stats[song] = {"plays": 1, "length_min": 0}
            else:
                stats[song]["plays"] += 1

        # лог типу {"song_name": "...", "plays": 0, "length_min": ...}
        elif "song_name" in entry:
            song = entry["song_name"]
            if song not in stats:
                stats[song] = {
                    "plays": entry["plays"],
                    "length_min": entry["length_min"]
                }
            else:
                # переносимо length_min (бо це метадані)
                stats[song]["length_min"] = entry["length_min"]

    # списки для графіка
    songs = []
    total_minutes = []

    for song, data in stats.items():
        songs.append(song.replace(".mp3", ""))
        total_minutes.append(data["plays"] * data["length_min"])

    plt.figure(figsize=(10, 6))
    plt.bar(songs, total_minutes)
    plt.ylabel("Загальна тривалість прослуховування (хв)")
    plt.xlabel("Пісні")
    plt.title("Загальний час прослуховування кожної пісні")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("static/graph2.png", bbox_inches="tight")
    plt.show()


def main():
    pygame.init()
    pygame.mixer.init()

    print("---Welcome to the music disc!!--- \n")
    while True:
        print(
            "Write 1 to start the program!!!\nWrite 2 to exit the program!!!\nWrite 3 to show stats!!! \nWrite 4 to show listening activity!!!")
        try:
            user_option = int(input("Write your option(number): "))
            if user_option == 1:
                user_select_song = ask_select()
                create_file_if_not_exists()
                add_number(song)
                update_play_log_with_length()

                user_speed_song = ask_speed()
                user_loud_song = ask_loud()
                user_is_repeat = ask_repeat()
                graphic()

                # from length_parser import load_logs, aggregate_stats, plot_total_listen_time
                #
                # logs = load_logs()  # завантажуємо логи
                # stats = aggregate_stats(logs)  # обчислюємо статистику
                # plot_total_listen_time()
                #
                # from length_parser import log_length
                #
                # audio = MP3(user_select_song)
                # length_min = round(audio.info.length / 60, 2)
                # log_length(user_select_song.name, length_min)

                if user_is_repeat == 0:
                    a = "and it won`t repeat"

                else:
                    a = f"it will repeat {user_is_repeat} times"

                    print(f"""You selected this song: {music_files_name}\nthis speed: {user_speed_song}x\nthis volume: {user_loud_song}%\n{a}""")
                    play_music(user_select_song, user_is_repeat, user_speed_song, user_loud_song)
                    song_lyrics(user_select_song)
                    start_webpage(user_select_song)

            elif user_option == 2:
              return False

            elif user_option == 3:
              plot_total_listen_time()

            elif user_option == 4:
              plot_day_period_pie()

            else:
              print("Please write correct number!")
              continue
        except ValueError:
         print("error")

        if __name__ == "main":
            main()

