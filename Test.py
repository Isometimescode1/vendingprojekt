import random
from guizero import App, PushButton, Text, TextBox, Combo
import Excel_read as Excel


#hangib küsimuse question class-ina.
def proov(vanus):
    Kysimus=Excel.get_question(vanus)
    print(Kysimus.text)


app = App(title="Müügiautomaat v.1", layout="grid", bg = (3,252,144))
tere_tulemast = Text(app, text="Tere tulemast mängu", size=90, font="Times New Roman", color="blue", grid= [200,200])
tekst_1 = Text(app, text="Vali oma vanus:", size=60, font="Times New Roman", color="blue", grid= [200,201])
#vali_vanus = Combo(app, options=["1-12", "13-18", ">=19"], grid= [0,200])
#vastuse_kast = TextBox(app, width=15, grid= [0,300])

nooruk =        PushButton(app, width = 60, height = 10, grid= [200,400], text ="<12")
keskealine =    PushButton(app, width = 60, height = 10, grid= [200,401], text ="13-18")
vanur =         PushButton(app, width = 60, height = 10, grid= [200,800], text =">=19")

give_question = PushButton(app, command = proov, args = [2], text="Genereeri küsimus", grid= [0,400])

app.set_full_screen()
app.display()
