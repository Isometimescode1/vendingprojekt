import random
import time
from guizero import App, PushButton, Text, TextBox, Combo
import Excel_read as Excel
import os
from os import system, name

#sisaldab käesoleva mälumängug aseotud infor
class Game:
    def __init__(self, age_group):
        self.vanus = age_group
        self.skoor = 0  #idk mida siia algul määrata
        self.õigeid = 0
        self.valesid = 0

mäng = Game(0)

#eemaldab vanuse valiku nupud ja laustab mängu
def destroy_vanus(vanus):
    #eemaldab vanuse nupud
    nooruk.hide()
    keskealine.hide()
    vanur.hide()
    #alustab ühe mälumängu, kui mäng.vanus != 0
    mäng.vanus = vanus
    start()

#alustab mängu, vaja palju asju juurde liseada
def start():
        rida = too_küsimus(mäng.vanus)
        disp_küsimus.show()
        disp_küsimus.append(rida.text)
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

#alustusnuppu vajuatades kuvab vanusevaliku
def läks():
    alustusnupp.hide()
    nooruk.show()
    keskealine.show()
    vanur.show()

#display the app
app = App(title="Müügiautomaat v.1", layout="auto", bg = (255,255,255))

#PushBUtton widgets
alustusnupp =      PushButton(app, command = läks, width = 30, height = 10, text ="Kliki, et alustada")
vastuse_kast =  TextBox(app, width=60)
nooruk =        PushButton(app, command = destroy_vanus, args = [1], width = 30, height = 10, text ="<12", visible=0)
keskealine =    PushButton(app, command = destroy_vanus, args = [2], width = 30, height = 10, text ="13-18", visible=0)
vanur =         PushButton(app, command = destroy_vanus, args = [3], width = 30, height = 10, text =">=19", visible=0)

v1 =            PushButton(app, width = 30, height = 10, visible=0)
v2 =            PushButton(app, width = 30, height = 10, visible=0)
v3 =            PushButton(app, width = 30, height = 10, visible=0)
v4 =            PushButton(app, width = 30, height = 10, visible=0)

#text widgets
disp_küsimus = Text(app, size= 15, font="Didot", color="blue", visible=0)
tere_tulemast = Text(app, text="Tere tulemast mängu", size=45, font="Didot", color="blue")
tekst_1 =       Text(app, text="Vali oma vanus ja genereeri küsimus:", size=45, font="Didot", color="blue")

#give_question = PushButton(app, command = proov, args = [], text="Genereeri küsimus", grid= [0,400])
#puhasta = PushButton (app, command = clear, args = [1], text="puhasta küsimus", grid= [0,400])
app.set_full_screen()
app.display()

