import random
from guizero import App, PushButton, Text, TextBox, Combo

def q_library():
    i = random.randint(1,5)
    with open ('C:/tekst/questions.txt') as f:
        content = f.readlines()
        print(content[i])
app = App(title="Müügiautomaat v.1")
tere_tulemast = Text(app, text="Tere tulemast mängu", size=30, font="Times New Roman", color="blue")
tekst_1 = Text(app, text="Sisesta oma vanus:", size=20, font="Times New Roman", color="blue")
vali_vanus = Combo(app, options=["1-13", "14-20", "21-100"])
vastuse_kast = TextBox(app, width=15)
give_question = PushButton(app, command=q_library, text="Genereeri küsimus")
app.display()
