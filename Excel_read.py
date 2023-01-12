#
# Nimetus:      Excel_read.py
# Kirjeldus:    Loeb ette nähtud formaadiga Exceli failist küsimusi     Müügiautomaadi jaoks
# Autor:        Erik Lootus, Hardi Tambets
# Kuupäev:      12.2022
#

import pandas
import random
import PIL

excel_file_name = 'Küsimused.xlsx'
excel_sheet_group1 = 'Grupp_1'
excel_sheet_group2 = 'Grupp_2'
excel_sheet_group3 = 'Grupp_3'
Group1_data = pandas.read_excel (excel_file_name, excel_sheet_group1)
Group2_data = pandas.read_excel (excel_file_name, excel_sheet_group2)
Group3_data = pandas.read_excel (excel_file_name, excel_sheet_group3)

#ühte konkreetset küsimust kirjeldav class
class Question:
    def __init__(self, nr, text, answer, false1, false2, false3, image, input, age_group):
        self.nr = nr            #Exceli faili rea number
        self.text = text        #Küsimuse tekst
        self.answer = answer    #Küsimuse vastus
        self.false1 = false1    #Esimene vale valikuvõimaluse
        self.false2 = false2    #Teine vale valikuvõimaluse
        self.false3 = false3    #Kolmas vale valkuvõimalus
        self.image = image      #Bool kas küsimusega käib kaasas ka pilt?
        self.input = input      #Bool kas küsimusega käib kaasas numbrite sisestus?
        self.age_group = age_group  #Vanusegrupp kuhu see küssa kuulub

#küsimuste faili kirjeldav (sisaldav?) class        
class Question_file:
    def __init__(self):
        self.group1_quest_nr = Group1_data.shape[0]
        self.group2_quest_nr = Group2_data.shape[0]
        self.group3_quest_nr = Group3_data.shape[0]


def get_question(age_group):
    match age_group:
        case 1:
            q_max=Group1_data.shape[0]-1
            i=random.randint(0,q_max)
            kysimus =   Question(i+2, Group1_data.at[i,'Küssa'],Group1_data.at[i,'Vastus'],Group1_data.at[i,'Valik1'], 
                        Group1_data.at[i,'Valik2'], Group1_data.at[i,'Valik3'], Group1_data.at[i,'Pilt'], Group1_data.at[i,'Sisestus'], Group1_data.at[i,'Vanusegrupp'])
        case 2:
            q_max=Group2_data.shape[0]-1
            i=random.randint(0,q_max)
            #print(i)
            kysimus =   Question(i+2, Group2_data.at[i,'Küssa'],Group2_data.at[i,'Vastus'],Group2_data.at[i,'Valik1'], 
                        Group2_data.at[i,'Valik2'], Group2_data.at[i,'Valik3'], Group2_data.at[i,'Pilt'], Group2_data.at[i,'Sisestus'], Group2_data.at[i,'Vanusegrupp'])
        case 3:
            q_max=Group3_data.shape[0]-1
            i=random.randint(0,q_max)
            kysimus =   Question(i+2, Group3_data.at[i,'Küssa'],Group3_data.at[i,'Vastus'],Group3_data.at[i,'Valik1'], 
                        Group3_data.at[i,'Valik2'], Group3_data.at[i,'Valik3'], Group3_data.at[i,'Pilt'], Group3_data.at[i,'Sisestus'], Group3_data.at[i,'Vanusegrupp'])
        case _:
            print("Error: vanusegrupp valimata")

    return kysimus

# Prindib terve suvalise exceli rea soovitud vanusegrupist
def print_rand_rida(x):
    proov=get_question(x)
    attrs = vars(proov)
    print(', '.join("%s: %s" % item for item in attrs.items()))

# Prindib terve exceli rea kindla küsimuse kindlast vanusegrupist. i = exceli rea number. Pandase jaoks on rida null esimene data rida pealkirja rea all.
def anna_küssa(i, vanus):
    if i == 1:
        print("See on pealkirja rida, siin pole küsimusi")
    i = i - 2
    match vanus:
        case 1:
            kysimus =   Question(i+2, Group1_data.at[i,'Küssa'],Group1_data.at[i,'Vastus'],Group1_data.at[i,'Valik1'], 
                        Group1_data.at[i,'Valik2'], Group1_data.at[i,'Valik3'], Group1_data.at[i,'Pilt'], Group1_data.at[i,'Sisestus'], Group1_data.at[i,'Vanusegrupp'])
        case 2:
            kysimus =   Question(i+2, Group2_data.at[i,'Küssa'],Group2_data.at[i,'Vastus'],Group2_data.at[i,'Valik1'], 
                        Group2_data.at[i,'Valik2'], Group2_data.at[i,'Valik3'], Group2_data.at[i,'Pilt'], Group2_data.at[i,'Sisestus'], Group2_data.at[i,'Vanusegrupp'])
        case 3:
            kysimus =   Question(i+2, Group3_data.at[i,'Küssa'],Group3_data.at[i,'Vastus'],Group3_data.at[i,'Valik1'], 
                        Group3_data.at[i,'Valik2'], Group3_data.at[i,'Valik3'], Group3_data.at[i,'Pilt'], Group3_data.at[i,'Sisestus'], Group3_data.at[i,'Vanusegrupp'])
        case _:
            print("Error: vanusegrupp valimata")

    attrs = vars(kysimus)
    print(', '.join("%s: %s" % item for item in attrs.items()))
    return kysimus


#print(Group2_data.shape)
#print(excel_data)
#print(Group2_data.at[0,'Küssa'])

#piltidega maadlemine:
def get_reso(path):
    img = PIL.Image.open(path)
    # fetching the dimensions
    wid, hgt = img.size
    return[str(wid), str(hgt)]

#get_reso("/home/pi/vendingprojekt-1/Images/splash.jpg")