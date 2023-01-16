#
# Nimetus:      Test.py
# Kirjeldus:    Juhib müügiautomaadi mälumängu ja graafilist kasutajaliidest
# Autor:        Erik Lootus, Hardi Tambets
# Kuupäev:      12.2022
#


from guizero import App, PushButton, Text, Box, TextBox, Window, Picture
import Excel_read as Excel
from tkinter import Message
import random
import hardware as hw
from time import sleep

 
#sisaldab käesoleva mälumänguga seotud infot
class Game:
    def __init__(self, age_group):
      self.vanus = age_group
      self.skoor = 0  #idk mida siia algul määrata
      self.õigeid = 0
      self.valesid = 0
      self.õige_nupp = 0
      self.mängu_pikkus = 5
      self.valitud_str = "Error: Koogel moogel!"
      self.digit = 0
      self.full_input = 0
      self.vajutatud_nupp = 0
      self.kasutatud_küssad = []
    
    Q_TIMEOUT = 120 #kui kaua küsimuse vastust oodatakse, sekundites
    Q_POLL_PERIOD = 0.1 #kui tihti nupuvautus kontrollitakse, sekundites
    VALE_VASTUS = "Vale vastus!"
    ÕIGE_VASTUS = "Õige, tubli laps!"

mäng = Game(0)

#alustab mängu, vaja palju asju juurde lisada

def start(age=None):
    
    if age != None:
        mäng.vanus = age

    question_picture.hide()
    open_window1()
    rida = too_küsimus(mäng.vanus)
    disp_küsimus.configure(text=str(rida.text))     #tkinter meetod
    v1.show(), v2.show(), v3.show(), v4.show()

    close_windowage()
    
    #Segab vastused nuppudele suvalisse järjekorda
    answers=[rida.answer, rida.false1, rida.false2, rida.false3]
    random.shuffle(answers)
    v1.text = answers[0]
    v2.text = answers[1]
    v3.text = answers[2]
    v4.text = answers[3]
    #Õige vastuse kontrollimiseks jätab õige "nupu" numbri meelde
    mäng.õige_nupp = answers.index(rida.answer)+1

    # kui küsimusega on ette nähtud kaasnema pilt, siis kuvab selle (question_picture)
    if rida.image == 1:
        print("Pilt: Küsimusega kaasnev pilt tuvastatud")
        path = "/home/pi/vendingprojekt-1/Images/" + str(rida.age_group) + "_" + str(rida.nr) + ".jpg"
        question_picture.image = path
        #määrab pildi suuruseks faili resolutsiooni, muidu hakkab pilte moonutama. Suurim lubatud pilt 1920 x 600
        print(path)
        question_picture.width = int(Excel.get_reso(path)[0])
        question_picture.height = int(Excel.get_reso(path)[1])
        question_picture.show()
    else:
        print("Pilt: Küsimusega ei kaasne pilti")
        question_picture.hide()

    #kui küsimus nõuab numbrilist sisendit siis kuvab sisestuskasti ja tegeleb selle sisendiga:
    if rida.input == 1:
        print("Sisestus: küsimusega kaasenb numbrite sisestus")
        a_vastus.hide()
        #input_text_box.show()
        input_textbox.clear()
        input_textbox.show()
        input_textbox.focus()
        window2.update()

        hw.clear_fifo()     #Puhastab numpadi puhvri
        while mäng.digit != "#":
            mäng.digit = hw.get_digit()     #ootame sisestust ja ei tee midagi muud
            if mäng.digit == "#":
                break
            input_textbox.append(mäng.digit)
            window2.update()
        mäng.full_input = input_textbox.value
        print("mäng.full: ", mäng.full_input)
        print("rida.answer: ", rida.answer)
        kontrolli_vastust(mäng.full_input, rida.answer)

    else:
        print("Sisestus: küsimusega ei kaasne numbrite sisestust")
        #input_text_box.hide()
        a_vastus.show()
    
    #Resetime viimase nupuvajutuse ja ootame vastust
    window1.update()
    hw.reset_button()
    print("Vastust oodates...")
    mäng.vajutatud_nupp = hw.get_input(mäng.Q_TIMEOUT, mäng.Q_POLL_PERIOD)
    print("Mängu logikasse jõudis nupuvajutus:", mäng.vajutatud_nupp)
    kontrolli_vastust(mäng.vajutatud_nupp)

   
#hangib küsimuse question class-ina. Kontrollib et ühes mängus üht küsimust mitu kporda ei tule.
def too_küsimus(vanus):
    while(1):
        küs_rida = Excel.get_question(vanus)
        if küs_rida.nr not in mäng.kasutatud_küssad:
            mäng.kasutatud_küssad.append(küs_rida.nr)
            break
    
    print("Küsimus on: ", küs_rida.text)
    return küs_rida

#alustusnuppu vajutades kuvab vanusevaliku
def läks():
    open_windowage()        #järjekord oluline
    close_window()
    alustusnupp.hide()
    splash_picture.hide()
    nooruk.show()
    keskealine.show()
    vanur.show()

    #----------------------------------------------------------------------------------------------------------------------------------------------------------------

    # ootame mingit sisendit, et saaks alustada
    print("õiges kohas")
    app.update()
    hw.reset_button()
    print("Sisendit oodates, et küsida vanust...")
    alustus_input = 0
    while alustus_input == 0:
        alustus_input = hw.get_input(mäng.Q_TIMEOUT, mäng.Q_POLL_PERIOD)
    if alustus_input > 0:
        läks()
    else:
        print("siia ei oleks tohtinud jõuda :(")

#funktsioon kontrollib vastust ja avab vastava lehe
def kontrolli_vastust(vastus, num_vastus = None):
    
    #kuvab hariliku uue küsimuse nupu igal korral kui mängu pikkus pole veel teäidetud
    uus_küsimus_button.show()
    algusesse_button.hide()

    #puhastb teksti sisu, et saaks kuvada uusi väärtusi
    vastus_tulemus.clear()
    skoor_nr_text.clear()
    valesid_nr_text.clear()
    õigeid_nr_text.clear()

    #numbrilise vastuse korral:
    if num_vastus != None:
        #muudab mõlemad int-ideks, et saaks võrrelda
        int_vastus = int(vastus)                # see oli str
        int_num_vastus = num_vastus.item()      # see oli numpy.int64

        if int_vastus == int_num_vastus:
            open_window2()
            vastus_tulemus.append(mäng.ÕIGE_VASTUS)
            mäng.õigeid += 1
            print("õige")
        else:
            vastus_tulemus.append(mäng.VALE_VASTUS)
            open_window2()
            mäng.valesid += 1 
            print("vale")
    #Surunupu vastuse korral:
    elif vastus == mäng.õige_nupp:
        open_window2()
        vastus_tulemus.append(mäng.ÕIGE_VASTUS)
        mäng.õigeid += 1
    #Küsimuse vastuse ootamise timeout
    elif vastus == 0:
        #Seda osa võiks vist täiendada
        open_window2()
    else:
        vastus_tulemus.append(mäng.VALE_VASTUS)
        open_window2()
        mäng.valesid += 1
    
    # Uuendab kuvatavas tekstis skoori
    õigeid_nr_text.append(mäng.õigeid)
    valesid_nr_text.append(mäng.valesid)
    mäng.skoor += 1
    skoor_nr_text.append(mäng.skoor)

    #v[vastus].text on valitud vastus, prindib selle silumiseks
    if num_vastus == None:
        string = "v" + str(vastus) + ".text"
        print("Valiti vastus:", eval(string))

    # kui mäng läbi saab kuvab lõpu nupu ja skoori
    if mäng.skoor >= mäng.mängu_pikkus:
        #Kuvab reseti alagatava nupu, et mängu uuesti algusest alustada
        uus_küsimus_button.hide()
        algusesse_button.show()
        open_window2()

        #Toote väljastustsükkel
        hw.väljasta()
        window2.update()
        hw.reset_button()
        algusesse_input = hw.get_input(20, 0.1)
        if algusesse_input > 0:
            full_reset()
        # kui nupuvajutuse timeout eeldame, et mängija jalutas minema ja resetime
        else:
            print("Mängija ei ole pädev ja ei vajutanud ühtki nuppu. Reset.")
            full_reset()
        return()
    
    # ootab skoori ekraanin nupuvajutust, et kuvada järgmine küssa
    window2.update()
    hw.reset_button()
    print("Sisendit oodates, et kuvada järgmine asi...")
    next_question_input = hw.get_input(mäng.Q_TIMEOUT, mäng.Q_POLL_PERIOD)
    if next_question_input > 0:
        start()
    # kui nupuvajutuse timeout eeldame, et mängija jalutas minema ja resetime
    else:
        print("Mängija ei ole pädev ja ei vajutanud ühtki nuppu. Reset.")
        full_reset()


    
def full_reset():
    mäng.skoor = 0
    mäng.õigeid = 0
    mäng.valesid = 0
    mäng.vanus = 0
    mäng.kasutatud_küssad.clear()
    open_window()


# meetodid, mis avavad ja sulgevad soovitud aknaid
#1 leht - ava
def open_window(): 
    close_window1()
    close_window2()
    close_window3()
    splash_picture.show()
    alustusnupp.show()

    app.show()
    app.focus()         #.focus() ei funka raspi peal :(
    
    # ootame mingit sisendit, et saaks alustada
    app.update()
    hw.reset_button()
    print("Sisendit oodates, et küsida vanust...")
    alustus_input = 0
    while alustus_input == 0:
        alustus_input = hw.get_input(mäng.Q_TIMEOUT, mäng.Q_POLL_PERIOD)
    if alustus_input > 0:
        läks()
    else:
        print("siia ei oleks tohtinud jõuda :(")


#2 leht - ava
def open_windowage():
    close_window1()
    close_window2()
    close_window3()
    windowage.show(wait=True)
    windowage.focus()

#3 leht - ava, toob ühe akna esile ja ei lase teistel ette tulla enne kui esimene sulgetakse 
def open_window1():
    window1.show(wait=True)     #järkekord oluline
    windowage.hide()
    close_window2()
    close_window3()

#4 leht - ava
def open_window2():
    window2.show(wait=True)
    #print(skoor_count, skoor_õigeid, skoor_valesid)

#5 leht - ava
def open_window3():
    window3.show(wait=True)
    #print(skoor_count, skoor_õigeid, skoor_valesid)

#1 leht - sulge
def close_window():
    app.hide()

#2 lisaleht vanuse jaoks
def close_windowage():
    windowage.hide()
    #mäng.vanus = vanus
    #start()

#3 leht - sulge
def close_window1():
    window1.hide()

#4 leht - sulge
def close_window2():
    window2.hide()

#5 lisaleht vanuse jaoks
def close_window3():
    window3.hide()

#6 funktsioon mis peidab kõik lehed ja sulgeb programmi, kui anda mingi parameeter, siis exit-it ei tee
def close_windows(quit=None):
    app.hide()
    windowage.hide()
    window1.hide()
    window2.hide()
    window3.hide()
    if quit is None:
        exit()


#defineeritud erinevad leheküljed

#display the app avaleht
app = App(title="Avaleht", layout="auto", bg = "#7B4E4E")

#Leht vanuse küsimiseks
windowage = Window(app, title="Kirjuta oma vanus", layout="auto", bg = "#7B4E4E")

#Leht Küsimust ja vastuste esitamiseks (põhipingutus)
window1 = Window(app, title="Küsimusteleht", layout="auto", bg = "#7B4E4E")

#Leht Küsimuste vahel tulemuste kuvamiseks
window2 = Window(app, title="Skoori vaheleht", layout="auto", bg = "#7B4E4E")

#Pole kasututses
window3 = Window(app, title="Lõpuleht", layout="auto", bg = "#7B4E4E")


#et avaleht jääks kõige ette
close_windows(1)
app.show()

#Boxes

buttons_box =           Box(window1, width="fill", align="bottom", border=1, layout="grid")
answer_name_box =       Box(window1, width="fill", align="bottom", border=1)#, layout="grid")
input_text_box =        Box(answer_name_box, width = "fill", height = "fill")#, grid = [0,0] )      #et see kuradi teksti sisestuslkast keskel püsiks
input_text_box.hide()
spacer_box1 =           Box(windowage, width ="fill", height=300, align="bottom", border=1)
age_selection_box =     Box(windowage, width="fill", height=300, align="bottom", border=1, layout="grid")
age_spacer_box =        Box(age_selection_box, width=170, grid=[0,0], border=1) #vanuse valiku nuppude tsentrisse paigutamise jaoks
age_description_box =   Box(windowage, width="fill", height=100, align="bottom", border=1)

spacer_box2 =           Box(window2, width = 1000, height=200, align="bottom", border=1)
skoor_üldine_box =      Box(window2, width = "fill", height = 600, align="bottom", border=1)
skoor_spacer_box =      Box(skoor_üldine_box, width = 200, height = "fill", align="left", border=0)
valesid_box =           Box(skoor_üldine_box, width = 1000, height=200, align="bottom", border=0, layout="grid")
õigeid_box =            Box(skoor_üldine_box, width = 1000, height=200, align="bottom", border=0, layout="grid")
skoor_box =             Box(skoor_üldine_box, width = 1000, height=200, align="bottom", border=0, layout="grid")


#PushButton widgets

alustusnupp =   PushButton(app, command = läks, width = 20, height = 5, align = "bottom", text ="Vajuta, et alustada")
alustusnupp.text_size = 30
nooruk =        PushButton(age_selection_box, command = start, args = [1], width = 20, align= "left", height = 3, text ="<=12", visible=0, grid= [1,0])
nooruk.text_size = 30
keskealine =    PushButton(age_selection_box, command = start, args = [2], width = 20, align= "left", height = 3, text ="13-18", visible=0, grid= [2,0])
keskealine.text_size = 30
vanur =         PushButton(age_selection_box, command = start, args = [3], width = 20, align= "left", height = 3, text =">=19", visible=0, grid= [3,0])
vanur.text_size = 30

v1 =            PushButton(buttons_box, command = kontrolli_vastust, args = [1], width = 18, grid= [0,0], height = 3, visible=0)
v1.text_size = 30
v1.tk.config(wraplength=440)
v2 =            PushButton(buttons_box, command = kontrolli_vastust, args = [2], width = 18, grid= [1,0], height = 3, visible=0)
v2.text_size = 30
v2.tk.config(wraplength=440)
v3 =            PushButton(buttons_box, command = kontrolli_vastust, args = [3], width = 19, grid= [2,0], height = 3, visible=0)
v3.text_size = 30
v3.tk.config(wraplength=440)
v4 =            PushButton(buttons_box, command = kontrolli_vastust, args = [4], width = 18, grid= [3,0], height = 3, visible=0)
v4.text_size = 30
v4.tk.config(wraplength=440)

close_button1       = PushButton(app, text="Sulge leht 1", command=close_windows)
close_button2       = PushButton(windowage, text="Sulge leht 2", command=close_windows)
close_button3       = PushButton(window1, text="Sulge leht 3", command=close_windows)
uus_küsimus_button  = PushButton(window2, text="Järgmine küsimus, palun", command=start)
algusesse_button    = PushButton(window2, text="Tagasi algusesse", command=full_reset, visible=0)
#close_button5      = PushButton(window3, text="Tagasi algusesse", command=full_reset)
close_button6       = PushButton(window2, text="Sulge mäng", command=close_windows)
#close_button7      = PushButton(window3, text="Sulge mäng", command=close_windows)

#text widgets

disp_küsimus    = Message(window1.tk, text="Kui näed seda teksti, anna automaadi kantseldajale teada.", font=("Didot", 30), width=1600)
disp_küsimus.pack()
tere_tulemast   = Text(app, text="Tere tulemast unikaalse müügiautomaadi juurde!", size=50, align = "top", font="Didot", color="black")
tekst_1         = Text(windowage, text="Vali sobiv vanusegrupp:", align = "top", size=60, font="Didot", color="black")
tekst_vanus_selgitus = Text(windowage, text="Kusimused on jaotatud vanuste alusel, et anda kõigile võrdne võimalus ;)", align = "top", size=30, font="Didot", color="black")
age_description_text = Text(age_description_box, text="Olen nooruk!                Keskiga juba käes!              Vanaks jäänud...", align = "top", size=30, font="Didot", color="black")
vastus_tulemus       = Text(window2, text="Initilize", size=60, align = "top", font="Didot", color="black")

a_vastus        = Text(answer_name_box, text="A:               B:               C:               D:",size=60, font="Didot", color="#3F3E3E", align = "top")

skoor_text      = Text(skoor_box, text="Küsimusi:", size=60, align="bottom", font="Didot", color="black", grid= [1,0])
õigeid_text     = Text(õigeid_box, text="Õigeid vastuseid:", size=60, align="bottom", font="Didot", color="black", grid= [1,0])
valesid_text    = Text(valesid_box, text="Valesid vastuseid:", size=60, align="bottom", font="Didot", color="black", grid= [1,0])
skoor_nr_text   = Text(skoor_box, text=mäng.skoor, size=60, align="bottom", font="Didot", color="black", grid= [2,0])
õigeid_nr_text  = Text(õigeid_box, text=mäng.õigeid, size=60, align="bottom", font="Didot", color="black", grid= [2,0])
valesid_nr_text = Text(valesid_box, text=mäng.valesid, size=60, align="bottom", font="Didot", color="black", grid= [2,0])
vajuta_text     = Text(spacer_box2, text="Jätkamiseks vajuta mõnda nuppu", size=35, font="Didot", color="black")

#TextBox widgets
input_textbox   = TextBox(answer_name_box, align = "top")
input_textbox.bg ="white"
input_textbox.font = "Didot"
input_textbox.text_size = 50
input_textbox.hide()

#Picture widgets

splash_picture = Picture(app, image = "Images/splash.jpg")
question_picture = Picture(window1, image ="Images/placeholder.jpg")

#paneb lehed täisekraanile ja displayb esimese lehe
app.set_full_screen()
windowage.set_full_screen()
window1.set_full_screen()
window1.add_tk_widget(disp_küsimus)
window2.set_full_screen()
#window3.set_full_screen()
#app.add_tk_widget(disp_küsimus)

#Mitte miskit ei tohi peale järgnevat rida olla
app.display()