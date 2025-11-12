import tkinter as tk
from tkinter import messagebox

window = tk.Tk()
window.title("La Musica")
window.geometry("500x400")
import main_py

label = tk.Label(window, text="Write 1 to start the program!!!\nWrite 2 to exit the program!!!", font=("Arial", 14))
label.pack(pady=10)

entry = tk.Entry(window, width=30)
entry.pack(pady=5)


def say_hello():
    user_choice = entry.get().strip()
    if user_choice == "1":
        start_program()
    elif user_choice == "2":
        window.destroy()
    else:
        messagebox.showerror("Error", "Please write 1 or 2!")


def start_program():
    label_song = tk.Label(window, text="Select song:\n1: Beat It\n2: Hey Baby\n3: On The Floor\n4: Tears",
                          font=("Arial", 14))
    label_song.pack(pady=10)
    select_song = tk.Entry(window, width=30)
    select_song.pack(pady=5)

    def confirm_song():
        try:
            song_num = int(select_song.get())
            if song_num not in range(1, 5):
                raise ValueError
            messagebox.showinfo("OK", f"You selected song #{song_num}")
            main_py.song = song_num
            select_speed()
        except ValueError:
            messagebox.showerror("Error", "Enter number 1-4!")

    tk.Button(window, text="OK", width=20, command=confirm_song).pack(pady=5)


def select_speed():
    for widget in window.winfo_children():
        widget.destroy()

    label_speed = tk.Label(window, text="Enter speed (0.1x - 2.5x):", font=("Arial", 14))
    label_speed.pack(pady=10)
    select_speed_entry = tk.Entry(window, width=30)
    select_speed_entry.pack(pady=5)

    def confirm_speed():
        try:
            speed = float(select_speed_entry.get())
            if not 0.1 <= speed <= 2.5:
                raise ValueError
            messagebox.showinfo("OK", f"Speed set to {speed}x")
            # main_py.ask_loud()
            select_volume()
        except ValueError:
            messagebox.showerror("Error", "Enter number between 0.1 and 2.5!")

    tk.Button(window, text="OK", width=20, command=confirm_speed).pack(pady=5)


def select_volume():
    for widget in window.winfo_children():
        widget.destroy()

    label_volume = tk.Label(window, text="Enter volume (1-100%):", font=("Arial", 14))
    label_volume.pack(pady=10)
    select_volume_entry = tk.Entry(window, width=30)
    select_volume_entry.pack(pady=5)

    def confirm_volume():
        try:
            volume = float(select_volume_entry.get())
            if not 1 <= volume <= 100:
                raise ValueError
            messagebox.showinfo("OK", f"volume set to {volume}x")
            select_repeat()

        except ValueError:
            messagebox.showerror("Error", "Enter number between 0.1 and 2.5!")

    tk.Button(window, text="OK", width=20, command=confirm_volume).pack(pady=5)


def select_repeat():
    for widget in window.winfo_children():
        widget.destroy()

    label_repeat = tk.Label(
        window,
        text="Would you like to listen on repeat?\n1 - Yes\n2 - No",
        font=("Arial", 14)
    )
    label_repeat.pack(pady=10)

    select_repeat_entry = tk.Entry(window, width=30)
    select_repeat_entry.pack(pady=5)

    def confirm_repeat():
        try:
            repeat_choice = (select_repeat_entry.get()).lower()
            if repeat_choice == "yes":

                for widget in window.winfo_children():
                    widget.destroy()

                label_count = tk.Label(
                    window,
                    text="How many times (1-2)?",
                    font=("Arial", 14)
                )
                label_count.pack(pady=10)

                count_entry = tk.Entry(window, width=30)
                count_entry.pack(pady=5)

                def confirm_count():
                    try:
                        count = int(count_entry.get())
                        if count in range(1, 3):
                            messagebox.showinfo("Repeat", f"OK! It will repeat {count} times")
                            try:
                                song_path = main_py.get_song_path(main_py.song)  # отримуємо шлях до вибраної пісні
                                main_py.start_webpage(song_path)
                            except Exception as e:
                                messagebox.showerror("Error", f"Cannot open webpage: {e}")

                            window.destroy()

                        else:
                            raise ValueError
                    except ValueError:
                        messagebox.showerror("Error", "Enter 1 or 2!")

                tk.Button(window, text="OK", width=20, command=confirm_count).pack(pady=5)

            elif repeat_choice == "no":
                messagebox.showinfo("Repeat", "Ok! It won't repeat.")
                try:
                    song_path = main_py.get_song_path(main_py.song)
                    main_py.start_webpage(song_path)
                except Exception as e:
                    messagebox.showerror("Error", f"Cannot open webpage: {e}")

                window.destroy()

            else:
                raise ValueError

        except ValueError:
            messagebox.showerror("Error", "Enter 1 for Yes or 2 for No!")

    tk.Button(window, text="OK", width=20, command=confirm_repeat).pack(pady=5)


button = tk.Button(window, text="Ok", command=say_hello)
button.pack(pady=10)

window.mainloop()
