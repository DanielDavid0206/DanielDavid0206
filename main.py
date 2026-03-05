import tkinter as tk
from tkinter import messagebox
import time
import datetime
import threading
import winsound  # Solo funciona en Windows

# ---------------- ESTADOS ----------------
is_24_hour = True
is_spanish = False
alarm_time = None
alarm_enabled = False

# ---------------- VENTANA ----------------
root = tk.Tk()
root.title("Reloj Digital Pro")
root.geometry("500x400")
root.configure(bg="#1e3c72")

# ---------------- FUNCIONES ----------------

def update_clock():
    global alarm_time, alarm_enabled

    now = datetime.datetime.now()
    hours = now.hour
    minutes = now.minute
    seconds = now.second

    am_pm = ""

    if not is_24_hour:
        am_pm = " PM" if hours >= 12 else " AM"
        hours = hours % 12
        hours = hours if hours != 0 else 12

    time_string = f"{hours:02}:{minutes:02}:{seconds:02}{am_pm}"
    time_label.config(text=time_string)

    # Fecha
    if is_spanish:
        days = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
        months = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
                  "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
        date_string = f"{days[now.weekday()]}, {now.day} de {months[now.month-1]} del {now.year}"
    else:
        days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        months = ["January","February","March","April","May","June",
                  "July","August","September","October","November","December"]
        date_string = f"{days[now.weekday()]}, {months[now.month-1]} {now.day}, {now.year}"

    date_label.config(text=date_string)

    # Verificar alarma
    current_alarm_check = f"{now.hour:02}:{now.minute:02}"
    if alarm_enabled and alarm_time == current_alarm_check:
        threading.Thread(target=play_alarm).start()

    root.after(1000, update_clock)


def toggle_format():
    global is_24_hour
    is_24_hour = not is_24_hour


def toggle_language():
    global is_spanish
    is_spanish = not is_spanish


def set_alarm():
    global alarm_time, alarm_enabled
    alarm_time = alarm_entry.get()
    if alarm_time:
        alarm_enabled = True
        status_label.config(text="Alarma configurada ✔", fg="lightgreen")
    else:
        messagebox.showwarning("Error", "Ingresa una hora válida")


def toggle_alarm():
    global alarm_enabled
    alarm_enabled = not alarm_enabled
    if alarm_enabled:
        status_label.config(text="Alarma Activada 🔔", fg="lightgreen")
    else:
        status_label.config(text="Alarma Desactivada ❌", fg="red")


def play_alarm():
    for _ in range(5):
        winsound.Beep(1000, 500)


# ---------------- WIDGETS ----------------

time_label = tk.Label(root, font=("Arial", 40, "bold"),
                      bg="#1e3c72", fg="white")
time_label.pack(pady=20)

date_label = tk.Label(root, font=("Arial", 16),
                      bg="#1e3c72", fg="white")
date_label.pack()

button_frame = tk.Frame(root, bg="#1e3c72")
button_frame.pack(pady=10)

format_button = tk.Button(button_frame, text="Cambiar 12h/24h",
                          command=toggle_format)
format_button.grid(row=0, column=0, padx=5)

language_button = tk.Button(button_frame, text="Cambiar Idioma",
                            command=toggle_language)
language_button.grid(row=0, column=1, padx=5)

alarm_entry = tk.Entry(root, font=("Arial", 14))
alarm_entry.pack(pady=10)
alarm_entry.insert(0, "HH:MM")

alarm_button = tk.Button(root, text="Configurar Alarma",
                         command=set_alarm)
alarm_button.pack(pady=5)

toggle_alarm_button = tk.Button(root, text="Activar/Desactivar Alarma",
                                command=toggle_alarm)
toggle_alarm_button.pack(pady=5)

status_label = tk.Label(root, text="", font=("Arial", 12),
                        bg="#1e3c72")
status_label.pack(pady=10)

# ---------------- INICIAR ----------------
update_clock()
root.mainloop()