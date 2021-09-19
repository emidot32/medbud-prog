import tkinter as tk

from docx_service import DocxService
from file_services import *
from files_utils import *
from tk_entities.main_page import MainPage

full_drug_list = get_list_from_csv(r"input_files\drug_dosage.csv")
drug_dosage_dict = get_drug_dosage_dict(full_drug_list)
injection_methods = get_list_from_txt(r"input_files\injection_methods.txt")
modes = get_list_from_txt(r"input_files\modes.txt")
diets = get_list_from_txt(r"input_files\diets.txt")
all_surveys = get_list_from_txt(r"input_files\all_surveys.txt")
multiplicity_times_dict = dict(get_list_from_csv(r"input_files\multiplicity_times.csv"))

docx_service = DocxService(r"input_files\blank_example.docx", multiplicity_times_dict)
xml_service = XmlService()
json_service = JsonService()

root = tk.Tk()
MainPage(root, full_drug_list, drug_dosage_dict, injection_methods, modes, diets, all_surveys, docx_service, json_service)
root.mainloop()
