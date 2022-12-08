import random
import time
from guizero import App, PushButton, Text, TextBox, Combo, Window
import Excel_read as Excel
import os
from os import system, name, _exit


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
    close_windowage()
    open_window1()
    start()
    

#alustab mängu, vaja palju asju juurde lisada
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

#alustusnuppu vajutades kuvab vanusevaliku
def läks():
    close_window()
    open_windowage()
    alustusnupp.hide()
    nooruk.show()
    keskealine.show()
    vanur.show()

def kontrolli_vastust(vastus):
    if vastus == 1:
        open_window2()
        õige_vastus
    else:
        open_window3()
        vale_vastus
    print(v1.text)


#1 leht - ava
def open_window():
    app.show()

#2 leht - ava
def open_windowage():
    windowage.show(wait=True)

#3 leht - ava  //funktsioon, mis toob ühe akna esile ja ei lase teistel ette tulla enne kui esimene sulgetakse 
def open_window1():
    window1.show(wait=True)

#4 leht - ava
def open_window2():
    window2.show(wait=True)

#5 leht - ava
def open_window3():
    window3.show(wait=True)

#1 leht - sulge
def close_window():
    app.hide()

#2 lisaleht vanuse jaoks
def close_windowage():
    windowage.hide()

#3 leht - sulge
def close_window1():
    window1.hide()

#4 leht - sulge
def close_window2():
    window2.hide()

#5 lisaleht vanuse jaoks
def close_window3():
    window3.hide()

#6 funktsioon mis peidab kõik lehed ja sulgeb programmi
def close_windows():
    app.hide()
    windowage.hide()
    window1.hide()
    window2.hide()
    window3.hide()
    exit()
#display the app avaleht

app = App(title="Avaleht", layout="auto", bg = (255,255,255))

#teine lehekülg küsimuste jaoks

windowage = Window(app, title="Kirjuta oma vanus", layout="auto", bg = (255,255,255))

#kolmas lehekülg vastused
window1 = Window(app, title="Küsimusteleht", layout="auto", bg = (255,255,255))

#neljas lehekülg vastasid õigesti / valesti + kas tahad uuesti mängida

window2 = Window(app, title="Lõpuleht", layout="auto", bg = (255,255,255))

#viies lehekülg vastasid valesti

window3 = Window (app, title="Lõpuleht", layout="auto", bg = (255,255,255))

#PushButton widgets
alustusnupp =   PushButton(app, command = läks, width = 60, height = 30, align = "bottom", text ="vajuta, et alustada")
#vastuse_kast =  TextBox(window1, width=60)30
nooruk =        PushButton(windowage, command = destroy_vanus, args = [1], width = 30, align= "bottom", height = 10, text ="<12", visible=0)
keskealine =    PushButton(windowage, command = destroy_vanus, args = [2], width = 30, align= "bottom", height = 10, text ="13-18", visible=0)
vanur =         PushButton(windowage, command = destroy_vanus, args = [3], width = 30, align= "bottom", height = 10, text =">=19", visible=0)

v1 =            PushButton(window1, command = kontrolli_vastust, args = [1], width = 30, align= "bottom", height = 10, visible=0)
v2 =            PushButton(window1, command = kontrolli_vastust, args = [2], width = 30, align= "bottom", height = 10, visible=0)
v3 =            PushButton(window1, command = kontrolli_vastust, args = [3], width = 30, align= "bottom", height = 10, visible=0)
v4 =            PushButton(window1, command = kontrolli_vastust, args = [4], width = 30, align= "bottom", height = 10, visible=0)

#open_button = PushButton(app, text="Ava leht 1", command=open_window)
close_button = PushButton(app, text="Sulge leht 1", command=close_window)
#open_button = PushButton(windowage, text="Ava leht 2", command=open_windowage)
close_button = PushButton(windowage, text="Sulge leht 2", command=close_windowage)
#open_button = PushButton(window1, text="Ava leht 3", command=open_window1)
close_button = PushButton(window1, text="Sulge leht 3", command=close_window1)
#open_button = PushButton(window2, text="Ava leht 4", command=open_window2)
close_button = PushButton(window2, text="Mängi uuesti", command=läks)
#open_button = PushButton(window3, text="Ava leht 5", command=open_window3)
close_button = PushButton(window3, text="Mängi uuesti", command=läks)
close_button = PushButton(window2, text="Sulge mäng", command=close_windows)
close_button = PushButton(window3, text="Sulge mäng", command=close_windows)
#välju_mängust1 = PushButton(window2, text="Sulge mäng", command=close_window2) //toimis nii, et tuli sama küsimusteleht tagasi (ei tea kas vaja)
#välju_mängust2 = PushButton(window3, text="Sulge mäng", command=close_window3)

#open_button = PushButton(window2, text="Kas tahad uuesti mängida?", command=open_window)

#text widgets
disp_küsimus = Text(window1, size= 20, font="Didot", color="blue", visible=0)
tere_tulemast = Text(app, text="Tere tulemast mängu", size=60, align = "top", font="Didot", color="black")
tekst_1 =       Text(windowage, text="Vali oma vanus ja genereeri küsimus", align = "top", size=60, font="Didot", color="black")
õige_vastus = Text (window2, text="Õige vastus, võta auhind", size=60, align = "top", font="Didot", color="black")
vale_vastus = Text (window3, text="Vale vastus, võta auhind", size=60, align = "top", font="Didot", color="black")
#give_question = PushButton(app, command = proov, args = [], text="Genereeri küsimus", grid= [0,400])
#puhasta = PushButton (app, command = clear, args = [1], text="puhasta küsimus", grid= [0,400])
app.set_full_screen()
windowage.set_full_screen()
window1.set_full_screen()
window2.set_full_screen()
window3.set_full_screen()
app.display()

