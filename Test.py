import random
import time
from guizero import App, PushButton, Text, TextBox, Combo, Window
import Excel_read as Excel
import os
from os import system, name

#sisaldab käesoleva mälumänguga seotud infot
class Game:
    def __init__(self, age_group):
        self.vanus = age_group
        self.skoor = 0  #idk mida siia algul määrata
        self.õigeid = 0
        self.valesid = 0

mäng = Game(0)

#eemaldab vanuse valiku nupud ja alustab mängu
def destroy_vanus(vanus):
    #eemaldab vanuse nupud
    nooruk.hide()
    keskealine.hide()
    vanur.hide()
    #alustab ühe mälumängu, kui mäng.vanus != 0
    mäng.vanus = vanus
    start()

#alustab mängu, vaja palju asju juurde lisada
def start():
        open_window1
        rida = too_küsimus(mäng.vanus)
        disp_küsimus.show()
        disp_küsimus.append(rida.text)
        open_window2
        v1.show(), v2.show(), v3.show(), v4.show()
        v1.text = rida.answer
        v2.text = rida.false1
        v3.text = rida.false2
        v4.text = rida.false3
    
#hangib küsimuse question class-ina.
def too_küsimus(vanus):
    küs_rida=Excel.get_question(vanus)
    print(küs_rida.text)
    #ekraanile = Text(app, text = küs_rida.text, size= 15, font="Didot", color="blue", grid=[160,400])
    return küs_rida

#alustusnuppu vajutades kuvab vanusevaliku
def läks():
    open_window1
    alustusnupp.hide()
    nooruk.show()
    keskealine.show()
    vanur.show()
    close_window1

#1 leht - ava
def open_window():
    app.show(wait=True)

#2 leht - ava  //funktsioon, mis toob ühe akna esile ja ei lase teistel ette tulla enne kui esimene sulgetakse 
def open_window1():
    window1.show(wait=True)

#3 leht - ava
def open_window2():
    window2.show(wait=True)

#1 leht - sulge
def close_window():
    app.hide()

#2 leht - sulge
def close_window1():
    window1.hide()

#3 leht - sulge
def close_window2():
    window2.hide()

#display the app
app = App(title="Avaleht", layout="auto", bg = (255,255,255))

#teine lehekülg
window1 = Window(app, title="Küsimusteleht", layout="auto", bg = (255,255,255))

#kolmas lehekülg

window2 = Window(app, title="Lõpuleht", layout="auto", bg = (255,255,255))

#PushButton widgets
alustusnupp =      PushButton(app, command = läks, width = 30, height = 10, text ="Kliki, et alustada")
vastuse_kast =  TextBox(window1, width=60)
nooruk =        PushButton(app, command = destroy_vanus, args = [1], width = 30, height = 10, text ="<12", visible=0)
keskealine =    PushButton(app, command = destroy_vanus, args = [2], width = 30, height = 10, text ="13-18", visible=0)
vanur =         PushButton(app, command = destroy_vanus, args = [3], width = 30, height = 10, text =">=19", visible=0)

v1 =            PushButton(window2, width = 30, height = 10, visible=0)
v2 =            PushButton(window2, width = 30, height = 10, visible=0)
v3 =            PushButton(window2, width = 30, height = 10, visible=0)
v4 =            PushButton(window2, width = 30, height = 10, visible=0)

#open_button = PushButton(app, text="Ava leht 1", command=open_window)
close_button = PushButton(app, text="Sulge leht 1", command=close_window)
open_button = PushButton(window1, text="Ava leht 2", command=open_window1)
close_button = PushButton(window1, text="Sulge leht 2", command=close_window1)
open_button = PushButton(window2, text="Ava leht 3", command=open_window2)
close_button = PushButton(window2, text="Sulge leht 3", command=close_window2)
open_button = PushButton(app, text="Kas tahad uuesti mängida?", command=open_window)
#text widgets
disp_küsimus = Text(window1, size= 15, font="Didot", color="blue", visible=0)
tere_tulemast = Text(app, text="Tere tulemast mängu", size=45, font="Didot", color="blue")
tekst_1 =       Text(window1, text="Vali oma vanus ja genereeri küsimus", size=45, font="Didot", color="blue")

#give_question = PushButton(app, command = proov, args = [], text="Genereeri küsimus", grid= [0,400])
#puhasta = PushButton (app, command = clear, args = [1], text="puhasta küsimus", grid= [0,400])
app.set_full_screen()
app.display()

