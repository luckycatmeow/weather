import datetime
from posixpath import split
import requests

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.pyplot import figure

from tkinter import*
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

apiKey = "1512563abe8c4f2fb5403ab506bd7205"
url = "http://api.openweathermap.org/data/2.5/forecast?"
urlWeather = "http://api.openweathermap.org/data/2.5/weather?"

def GetWeather(city):
    apiUrl = f"{urlWeather}q={city}&APPID={apiKey}"
    response = requests.get(apiUrl, timeout=5)
    return response.json()

def Get5Weather(city):
    apiUrl = f"{url}q={city}&APPID={apiKey}"
    response = requests.get(apiUrl, timeout=5)
    return response.json()

def DisplayWeather(data): # для показа погоды
    if comboBox.current() == 0:
        label["text"] = "Температура: " + str(data["main"]["temp"]-273.15)+ " C"
    else:
        label["text"] = "Температура: " + str(data["main"]["temp"] - 459.67) + " F"
    label1["text"] = "Облачность: " + str(data['clouds']['all']) + "%"
    label2["text"] = "Осадки: " + str(data["weather"][0]["description"])
    label3["text"] ="Скорость ветра: " + str(data['wind']['speed']) + " м/с"
    label4["text"] = "Влажность: " + str(data['main']['humidity'])+ "%"
    label5["text"] = "Давление: " + str(data['main']['pressure'])+" гПа"
    label6["text"] = [str(num)+":"+buffer[num]+'\n' for num in range(len(buffer))]

def Graphic():
    global cityInput, comboBox, canvas, buffer
    city = cityInput.get()

    buffer.insert(0,str(city))
    if len(buffer)>5:
        buffer.pop()

    data = GetWeather(city)
    if data['cod'] == 200:
        DisplayWeather(data)

    data = Get5Weather(city)
    if data['cod'] == '200':
        temp = []
        if comboBox.current() == 0:
            temp = [i["main"]["temp"] - 273.15 for i in data['list']]
        else:
            temp = [i["main"]["temp"] - 459.67 for i in data['list']]
        temp = [sum(temp[i:i + 8]) / 8 for i in range(0, len(temp), 8)]

        clouds = [i['clouds']['all'] for i in data['list']]
        clouds = [sum(clouds[i:i + 8]) / 8 for i in range(0, len(clouds), 8)]

        windSpeed = [i['wind']['speed'] for i in data['list']]
        windSpeed = [sum(windSpeed[i:i + 8]) / 8 for i in range(0, len(windSpeed), 8)]

        humidity = [i['main']['humidity'] for i in data['list']]
        humidity = [sum(humidity[i:i + 8]) / 8 for i in range(0, len(humidity), 8)]

        pressure = [i['main']['pressure'] for i in data['list']]
        pressure = [sum(pressure[i:i + 8]) / 8 for i in range(0, len(pressure), 8)]

        list2 = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]
        time = [i['dt_txt'] for i in data['list']]
        time = [time[i] for i in range(0, len(time), 8)]
        time = [datetime.datetime.strptime(i, '%Y-%m-%d %H:%M:%S') for i in time]
        time = [list2[i.weekday()] for i in time]

        fig, ax = plt.subplots(2, 3)
        ax[0, 0].plot(time, temp)
        ax[0, 0].set_xlabel('День недели')
        if comboBox.current() == 0:
            ax[0, 0].set_ylabel('Средняя температура за день, C')
        else:
            ax[0, 0].set_ylabel('Средняя температура за день, F')
        print(time)

        ax[0, 1].plot(time, clouds)
        ax[0, 1].set_xlabel('День недели')
        ax[0, 1].set_ylabel('Облачность, %')
        print(clouds)

        ax[0, 2].plot(time, windSpeed)
        ax[0, 2].set_xlabel('День недели')
        ax[0, 2].set_ylabel('Скорость ветра, м/с')

        ax[1, 0].plot(time, humidity)
        ax[1, 0].set_xlabel('День недели')
        ax[1, 0].set_ylabel('Влажность, %')

        ax[1, 1].plot(time, pressure)
        ax[1, 1].set_xlabel('День недели')
        ax[1, 1].set_ylabel('Давление, гПа')

        if 'canvas' in globals() and canvas is not None:
            canvas.get_tk_widget().grid_forget()
            del canvas

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=2, column=0, columnspan=10, sticky="nsew")

buffer = []

root = Tk()
root.title("Прогноз погоды")
root.geometry("1920x1080")

cityInput = ttk.Entry()
cityInput.grid(row = 0, column = 0)

t = ["Цельсий", "Фаренгейт"]

comboBox = ttk.Combobox(values = t, state="readonly")
comboBox.current(0)
comboBox.grid(row = 0, column = 1)

cityButton = ttk.Button(text = "show", command = Graphic)
cityButton.grid(row = 1, column = 0)

label = ttk.Label(text="")
label.grid(row = 0, column = 2)

label1 = ttk.Label(text="")
label1.grid(row = 0, column = 3)

label2 = ttk.Label(text="")
label2.grid(row = 1, column = 2)

label3 = ttk.Label(text="")
label3.grid(row = 1, column = 3)

label4 = ttk.Label(text="")
label4.grid(row = 0, column = 4)

label5 = ttk.Label(text="")
label5.grid(row = 1, column = 4)

label6 = ttk.Label(text="")
label6.grid(row = 0, column =5)

for i in range(6):
    root.grid_columnconfigure(i, weight=1)
root.grid_rowconfigure(2, weight=1)

figr = Figure(figsize=(2,3))
canvas = FigureCanvasTkAgg(figr, master=root)
canvas.get_tk_widget().grid(row=2, column=0, columnspan=5, sticky="nsew")

root.mainloop()


