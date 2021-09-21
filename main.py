import tkinter as tk
import xmltodict
from docx_service import DocxService
from file_services import *
from files_utils import *
from tk_entities.main_page import MainPage

full_drug_list = get_list_from_csv("input_files/drug_dosage.csv")
drug_dosage_dict = get_drug_dosage_dict(full_drug_list)
injection_methods = get_list_from_txt("input_files/injection_methods.txt")
modes = get_list_from_txt("input_files/modes.txt")
diets = get_list_from_txt("input_files/diets.txt")
all_surveys = get_list_from_csv("input_files/all_surveys.csv")
multiplicity_times_dict = dict(get_list_from_csv("input_files/multiplicity_times.csv"))
config_dict = xmltodict.parse(open("input_files/entities_configuration.xml", mode='r', encoding='utf-8')
                              .read())['configuration']
docx_service = DocxService("input_files/blank_example.docx", multiplicity_times_dict)
json_service = JsonService()

root = tk.Tk()
MainPage(root, full_drug_list, drug_dosage_dict, injection_methods, modes, diets,
         all_surveys, config_dict, docx_service, json_service)
root.mainloop()
