import random
from guizero import App, PushButton, Text, TextBox, Combo
import Excel_read as Excel
import os
from os import system, name

#hangib küsimuse question class-ina.


def proov(vanus):
    Kysimus=Excel.get_question(vanus)
    print(Kysimus.text)
    ekraanile = Text(app, text = Kysimus.text, size= 15, font="Didot", color="blue", grid=[160,400])

app = App(title="Müügiautomaat v.1", layout="grid", bg = (255,255,255))
tere_tulemast = Text(app, text="Tere tulemast mängu", size=45, font="Didot", color="blue", grid= [160,200])
tekst_1 = Text(app, text="Vali oma vanus ja genereeri küsimus:", size=45, font="Didot", color="blue", grid= [160,201])
#vali_vanus = Combo(app, options=["1-12", "13-18", ">=19"], grid= [0,200])

vastuse_kast = TextBox(app, width=60, grid= [160,410])
nooruk =     PushButton(app, command = proov, args = [1], width = 30, height = 10, grid= [150,400],text ="<12")
keskealine =    PushButton(app, command = proov, args = [2], width = 30, height = 10, grid= [150,401],text ="13-18")
vanur =         PushButton(app, command = proov, args = [3], width = 30, height = 10, grid= [150,800],text =">=19")

#give_question = PushButton(app, command = proov, args = [], text="Genereeri küsimus", grid= [0,400])
#puhasta = PushButton (app, command = clear, args = [1], text="puhasta küsimus", grid= [0,400])
app.set_full_screen()
app.display()
