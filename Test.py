from guizero import App, PushButton, Text, Window, Picture, Box
import Excel_read as Excel
from tkinter import Message
import random


#sisaldab käesoleva mälumänguga seotud infot
class Game:
    def __init__(self, age_group):
      self.vanus = age_group
      self.skoor = 0  #idk mida siia algul määrata
      self.õigeid = 0
      self.valesid = 0
      self.õige_nupp = 0

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
    #open_window1()
    start()

#alustab mängu, vaja palju asju juurde lisada
def start():
        question_picture.hide()
        open_window1()
        rida = too_küsimus(mäng.vanus)
        disp_küsimus.configure(text=str(rida.text))     #tkinter meetod
        v1.show(), v2.show(), v3.show(), v4.show()
        
        #Segab vastused nuppudele suvalisse järjekorda
        answers=[rida.answer, rida.false1, rida.false2, rida.false3]
        random.shuffle(answers)
        v1.text = answers[0]
        v2.text = answers[1]
        v3.text = answers[2]
        v4.text = answers[3]
        #Õige vastuse kontrollimiseks
        mäng.õige_nupp = answers.index(rida.answer)+1

        # kui küsimusega on ette nähtud kaasnema pilt, siis kuvab selle (question_picture)
        if rida.image == 1:
            print("Küsimusega kaasnev pilt tuvastatud")
            path = "images/" + str(rida.age_group) + "_" + str(rida.nr) + ".jpg"
            question_picture.image = path
            #määrab pildi suuruseks faili resolutsiooni, muidu hakkab pilte moonutama. Suurim lubatud pilt 1920 x 600
            question_picture.width = int(Excel.get_reso(path)[0])
            question_picture.height = int(Excel.get_reso(path)[1])
            question_picture.show()
        else:
            print("Küsimusega ei kaasne pilti")
            question_picture.hide()

   
#hangib küsimuse question class-ina.
def too_küsimus(vanus):
    küs_rida=Excel.get_question(vanus)
    print(küs_rida.text)
    return küs_rida

#alustusnuppu vajutades kuvab vanusevaliku
def läks():
    close_window()
    open_windowage()
    alustusnupp.hide()
    splash_picture.hide()
    nooruk.show()
    keskealine.show()
    vanur.show()

#funktsioon kontrollib vastust ja avab vastava lehe
def kontrolli_vastust(vastus):
    if vastus == mäng.õige_nupp:
        open_window2()
        õige_vastus
    else:
        open_window3()
        vale_vastus
    print(v1.text)

    
#funktsioonid mis sulgevad ja avavad lehti:

#1 leht - ava
def open_window(): 
    app.show()

#2 leht - ava
def open_windowage():
    windowage.show(wait=True)

#3 leht - ava, toob ühe akna esile ja ei lase teistel ette tulla enne kui esimene sulgetakse 
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

#defineeritud erinevad leheküljed

#display the app avaleht
app = App(title="Avaleht", layout="auto", bg = "#7B4E4E")

#teine lehekülg küsimuste jaoks
windowage = Window(app, title="Kirjuta oma vanus", layout="auto", bg = "#7B4E4E")

#kolmas lehekülg vastused
window1 = Window(app, title="Küsimusteleht", layout="auto", bg = "#7B4E4E")

#neljas lehekülg vastasid õigesti + kas tahad uuesti mängida
window2 = Window(app, title="Lõpuleht", layout="auto", bg = "#7B4E4E")

#viies lehekülg vastasid valesti
window3 = Window (app, title="Lõpuleht", layout="auto", bg = "#7B4E4E")

#Boxes

buttons_box = Box(window1, width="fill", align="bottom", border=1, layout="grid")
answer_name_box = Box(window1, width="fill", align="bottom", border=1, layout="grid")

#PushButton widgets

alustusnupp =   PushButton(app, command = läks, width = 20, height = 5, align = "bottom", text ="Vajuta, et alustada")
alustusnupp.text_size = 30
nooruk =        PushButton(windowage, command = destroy_vanus, args = [1], width = 10, align= "bottom", height = 2, text ="<=12", visible=0)
nooruk.text_size = 30
keskealine =    PushButton(windowage, command = destroy_vanus, args = [2], width = 10, align= "bottom", height = 2, text ="13-18", visible=0)
keskealine.text_size = 30
vanur =         PushButton(windowage, command = destroy_vanus, args = [3], width = 10, align= "bottom", height = 2, text =">=19", visible=0)
vanur.text_size = 30

v1 =            PushButton(buttons_box, command = kontrolli_vastust, args = [1], width = 20, grid= [0,0], height = 3, visible=0)
v1.text_size = 30
v2 =            PushButton(buttons_box, command = kontrolli_vastust, args = [2], width = 21, grid= [1,0], height = 3, visible=0)
v2.text_size = 30
v3 =            PushButton(buttons_box, command = kontrolli_vastust, args = [3], width = 21, grid= [2,0], height = 3, visible=0)
v3.text_size = 30
v4 =            PushButton(buttons_box, command = kontrolli_vastust, args = [4], width = 20, grid= [3,0], height = 3, visible=0)
v4.text_size = 30

close_button1 = PushButton(app, text="Sulge leht 1", command=close_windows)
close_button2 = PushButton(windowage, text="Sulge leht 2", command=close_windows)
close_button3 = PushButton(window1, text="Sulge leht 3", command=close_windows)
close_button4 = PushButton(window2, text="Mängi uuesti", command=start)
close_button5 = PushButton(window3, text="Mängi uuesti", command=start)
close_button6 = PushButton(window2, text="Sulge mäng", command=close_windows)
close_button7 = PushButton(window3, text="Sulge mäng", command=close_windows)

#text widgets

disp_küsimus    = Message(window1.tk, text="Kui näed seda teksti, anna automaadi kantseldajale teada.", font=("Didot", 30), width=1600)
disp_küsimus.pack()
tere_tulemast   = Text(app, text="Tere tulemast mängu!", size=60, align = "top", font="Didot", color="black")
tekst_1         = Text(windowage, text="Vali oma vanus ja genereeri küsimus:", align = "top", size=60, font="Didot", color="black")
õige_vastus     = Text(window2, text="Õige vastus, võta auhind!!", size=60, align = "top", font="Didot", color="black")
vale_vastus     = Text(window3, text="Vale vastus, mine minema!!", size=60, align = "top", font="Didot", color="black")

a_vastus        = Text(answer_name_box, text="         A:                   B:                  C:                  D:",size=60, font="Didot", color="#3F3E3E", grid= [0,0])

#Picture widgets

splash_picture = Picture(app, image = "images/splash.jpg")
question_picture = Picture(window1, image ="images/placeholder.jpg")

#paneb lehed täisekraanile ja displayb esimese lehe
app.set_full_screen()
windowage.set_full_screen()
window1.set_full_screen()
window1.add_tk_widget(disp_küsimus)
window2.set_full_screen()
window3.set_full_screen()
#app.add_tk_widget(disp_küsimus)
app.display()