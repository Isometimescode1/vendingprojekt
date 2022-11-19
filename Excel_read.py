import pandas
import random

excel_file_name = 'Küsimused.xlsx'
excel_sheet_group1 = 'Grupp_1'
excel_sheet_group2 = 'Grupp_2'
excel_sheet_group3 = 'Grupp_3'
Group1_data = pandas.read_excel (excel_file_name, excel_sheet_group1)
Group2_data = pandas.read_excel (excel_file_name, excel_sheet_group2)
Group3_data = pandas.read_excel (excel_file_name, excel_sheet_group3)

#ühte konkreetset küsimust kirjeldav class
class Question:
    def __init__(self, text, age_group, answer):
        self.text = text
        self.age_group=age_group
        self.answer=answer

#küsimuste faili kirjeldav class        
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
            kysimus = Question(Group1_data.at[i,'Küssa'],Group1_data.at[i,'Vanusegrupp'],Group1_data.at[i,'Vastus'])
        case 2:
            q_max=Group2_data.shape[0]-1
            i=random.randint(0,q_max)
            #print(i)
            kysimus = Question(Group2_data.at[i,'Küssa'],Group2_data.at[i,'Vanusegrupp'],Group2_data.at[i,'Vastus'])
        case 3:
            q_max=Group3_data.shape[0]-1
            i=random.randint(0,q_max)
            kysimus = Question(Group3_data.at[i,'Küssa'],Group3_data.at[i,'Vanusegrupp'],Group3_data.at[i,'Vastus'])
        case _:
            print("Terror: vanusegrupp valimata")

    return kysimus


#get_question(2)



#print(excel_data.shape)

#print(excel_data)

#print(Group2_data.at[0,'Küssa'])
