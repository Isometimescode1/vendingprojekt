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
    def __init__(self, nr, text, answer, false1, false2, false3, image, age_group):
        self.nr = nr            #Exceli faili rea number
        self.text = text        #Küsimuse tekst
        self.answer = answer    #Küsimuse vastus
        self.false1 = false1    #Esimene vale valikuvõimaluse
        self.false2 = false2    #Teine vale valikuvõimaluse
        self.false3 = false3    #Kolmas vale valkuvõimalus
        self.image = image      #Bool kas küsimusega käib kaasas ka pilt?
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
            kysimus = Question(i+2, Group1_data.at[i,'Küssa'],Group1_data.at[i,'Vastus'],Group1_data.at[i,'Valik1'], Group1_data.at[i,'Valik2'], Group1_data.at[i,'Valik3'], Group1_data.at[i,'Pilt'], Group1_data.at[i,'Vanusegrupp'])
        case 2:
            q_max=Group2_data.shape[0]-1
            i=random.randint(0,q_max)
            #print(i)
            kysimus = Question(i+2, Group2_data.at[i,'Küssa'],Group2_data.at[i,'Vastus'],Group2_data.at[i,'Valik1'], Group2_data.at[i,'Valik2'], Group2_data.at[i,'Valik3'], Group2_data.at[i,'Pilt'], Group2_data.at[i,'Vanusegrupp'])
        case 3:
            q_max=Group3_data.shape[0]-1
            i=random.randint(0,q_max)
            kysimus = Question(i+2, Group3_data.at[i,'Küssa'],Group3_data.at[i,'Vastus'],Group3_data.at[i,'Valik1'], Group3_data.at[i,'Valik2'], Group3_data.at[i,'Valik3'], Group3_data.at[i,'Pilt'], Group3_data.at[i,'Vanusegrupp'])
        case _:
            print("Terror: vanusegrupp valimata")

    return kysimus


#proov=get_question(2)
#attrs = vars(proov)
#print(', '.join("%s: %s" % item for item in attrs.items()))

#print(Group2_data.shape)

#print(excel_data)

#print(Group2_data.at[0,'Küssa'])

#piltidega maadlemine:
def get_reso(path):
    img = PIL.Image.open(path)
    # fetching the dimensions
    wid, hgt = img.size
    return[str(wid), str(hgt)]
