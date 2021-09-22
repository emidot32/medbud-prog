import tkinter.font as tkFont
from tkinter.ttk import Combobox

from data_classes import *
from docx_service import DocxService
from file_services import FileService
from tk_entities.custom_entries import *


class MainPage:
    def __init__(self, root, drug_list, drug_dict, injection_methods: list, modes: list, diets: list,
                 all_surveys: list[list], config_dict, docx_service: DocxService, file_service: FileService):
        root.title("Medbud Preparaty")
        root.iconbitmap(r"img1.ico")
        root.state("zoomed")
        root.option_add('*Dialog.msg.font', (config_dict['@font_name'], int(config_dict['@dialog_window_font_size'])))
        combobox_cal_12 = tkFont.Font(name=config_dict['@font_name'], size=int(config_dict['@listbox_font_size']))
        root.option_add("*TCombobox*Listbox*Font", combobox_cal_12)
        self.root = root
        self.docx_service = docx_service
        self.file_service = file_service
        self.config_dict = config_dict
        tk.Label(root, text=config_dict['input_fio_label']['#text'], font=self.get_font_for('input_fio_label'))\
            .place(**self.get_coords_for('input_fio_label'))
        tk.Label(root, text=config_dict['search_btn_info_label']['#text'], font=self.get_font_for('search_btn_info_label'))\
            .place(**self.get_coords_for('search_btn_info_label'))
        self.fio_entry = tk.Entry(root, font=self.get_font_for('fio_entry'), width=int(config_dict['fio_entry']['@width']))
        self.fio_entry.place(**self.get_coords_for('fio_entry'))
        self.ward_entry = tk.Entry(root, font=self.get_font_for('ward_entry'), width=int(config_dict['ward_entry']['@width']))
        self.ward_entry.place(**self.get_coords_for('ward_entry'))
        self.search_btn = tk.Button(root, text=config_dict['search_btn']['#text'], command=self.search_patient,
                                    font=self.get_font_for('search_btn'), bg=config_dict['search_btn']['@bg_color'])
        self.search_btn.place(**self.get_coords_for('search_btn'))

        tk.Label(root, text=config_dict['select_mode_diet_label']['#text'], font=self.get_font_for('select_mode_diet_label'))\
            .place(**self.get_coords_for('select_mode_diet_label'))
        tk.Label(root, text=config_dict['mode_label']['#text'], font=self.get_font_for('mode_label'))\
            .place(**self.get_coords_for('mode_label'))
        self.mode_entry = Combobox(root, values=modes, font=self.get_font_for('mode_entry'), width=config_dict['mode_entry']['@width'])
        self.mode_entry.place(**self.get_coords_for('mode_entry'))
        tk.Label(root, text=config_dict['diet_label']['#text'], font=self.get_font_for('diet_label'))\
            .place(**self.get_coords_for('diet_label'))
        self.diet_entry = Combobox(root, values=diets, font=self.get_font_for('diet_entry'), width=config_dict['diet_entry']['@width'])
        self.diet_entry.place(**self.get_coords_for('diet_entry'))

        tk.Label(root, text=config_dict['select_all_label']['#text'], font=self.get_font_for('select_all_label')) \
            .place(**self.get_coords_for('select_all_label'))
        tk.Label(root, text=config_dict['press_plus_btn_label']['#text'], font=self.get_font_for('press_plus_btn_label')) \
            .place(**self.get_coords_for('press_plus_btn_label'))
        self.prescriptions_list = tk.Listbox(root, font=self.get_font_for('prescriptions_listbox'),
                                             width=config_dict['prescriptions_listbox']['@width'],
                                             height=config_dict['prescriptions_listbox']['@height'])
        self.prescriptions_list.place(**self.get_coords_for('prescriptions_listbox'))
        self.prescriptions: list[Prescription] = []
        self.add_btn = tk.Button(root, text=config_dict['add_btn']['#text'], font=self.get_font_for('add_btn'),
                                 command=self.add_drug_to_prescriptions,
                                 bg=config_dict['add_btn']['@bg_color'], fg=config_dict['add_btn']['@fg_color'],
                                 width=config_dict['add_btn']['@width'], height=config_dict['add_btn']['@height'])
        self.add_btn.place(**self.get_coords_for('add_btn'))
        self.remove_btn = tk.Button(root, text=config_dict['remove_btn']['#text'], font=self.get_font_for('remove_btn'),
                                    command=self.remove_drug_from_prescriptions,
                                    bg=config_dict['remove_btn']['@bg_color'], fg=config_dict['remove_btn']['@fg_color'],
                                    width=config_dict['remove_btn']['@width'], height=config_dict['remove_btn']['@height'])
        self.remove_btn.place(**self.get_coords_for('remove_btn'))
        self.clean_btn = tk.Button(root, text=config_dict['clean_btn']['#text'], font=self.get_font_for('clean_btn'),
                                   command=self.remove_drug_from_prescriptions,
                                   bg=config_dict['clean_btn']['@bg_color'], fg=config_dict['clean_btn']['@fg_color'],
                                   width=config_dict['clean_btn']['@width'], height=config_dict['clean_btn']['@height'])
        self.clean_btn.place(**self.get_coords_for('clean_btn'))
        self.generate_btn = tk.Button(root, text=config_dict['generate_btn']['#text'], command=self.generate_files,
                                      font=self.get_font_for('generate_btn'),
                                      bg=config_dict['generate_btn']['@bg_color'], fg=config_dict['generate_btn']['@fg_color'],
                                      width=config_dict['generate_btn']['@width'], height=config_dict['generate_btn']['@height'])
        self.generate_btn.place(**self.get_coords_for('generate_btn'))

        tk.Label(root, text=config_dict['drugs_label']['#text'], font=self.get_font_for('drugs_label'))\
            .place(**self.get_coords_for('drugs_label'))
        tk.Label(root, text=config_dict['dosage_label']['#text'], font=self.get_font_for('dosage_label')) \
            .place(**self.get_coords_for('dosage_label'))
        tk.Label(root, text=config_dict['inject_method_label']['#text'], font=self.get_font_for('inject_method_label')) \
            .place(**self.get_coords_for('inject_method_label'))
        tk.Label(root, text=config_dict['multiplicity_label']['#text'], font=self.get_font_for('multiplicity_label')) \
            .place(**self.get_coords_for('multiplicity_label'))
        tk.Label(root, text=config_dict['duration_label']['#text'], font=self.get_font_for('duration_label')) \
            .place(**self.get_coords_for('duration_label'))

        self.drug_entry = AutocompleteEntryWithListbox(root, sorted(set([item[0] for item in drug_list])),
                                                       entry_width=config_dict['drug_entry']['@entry_width'],
                                                       entry_font=self.get_font_for('drug_entry', '@entry_font_size'),
                                                       listbox_font=self.get_font_for('drug_entry', '@listbox_font_size'))
        self.drug_entry.place(**self.get_coords_for('drug_entry'))
        self.dosage_entry = RelatedEntryWithListbox(root, sorted(set([item[1] for item in drug_list])), self.drug_entry, drug_dict,
                                                    entry_width=config_dict['dosage_entry']['@entry_width'],
                                                    entry_font=self.get_font_for('dosage_entry', '@entry_font_size'),
                                                    listbox_font=self.get_font_for('dosage_entry', '@listbox_font_size'))
        self.dosage_entry.place(**self.get_coords_for('dosage_entry'))
        self.injection_method_entry = Combobox(root, values=injection_methods, 
                                               font=self.get_font_for('inject_method_entry'), 
                                               width=config_dict['inject_method_entry']['@width'])
        self.injection_method_entry.place(**self.get_coords_for('inject_method_entry'))

        self.multiplicity_entry = Combobox(root, values=[f"{i} р/д" for i in range(1, 4)],
                                           font=self.get_font_for('multiplicity_entry'),
                                           width=config_dict['multiplicity_entry']['@width'])
        self.multiplicity_entry.place(**self.get_coords_for('multiplicity_entry'))

        self.duration_entry = tk.Entry(root, font=self.get_font_for('duration_entry'), 
                                       width=config_dict['duration_entry']['@width'])
        self.duration_entry.place(**self.get_coords_for('duration_entry'))
        tk.Label(root, text=config_dict['days_label']['#text'], font=self.get_font_for('days_label'))\
            .place(**self.get_coords_for('days_label'))

        tk.Label(root, text="Обстеження та консультації", font=font_cal_15_bold).place(x=1055, y=20)
        tk.Label(root, text="Оберіть потрібні обстеження,",
                 font=font_cal_13).place(x=700, y=150)
        tk.Label(root, text="введіть в поле необхідну дату для них",
                 font=font_cal_13).place(x=700, y=173)
        tk.Label(root, text="та натисніть кнопку 'Проставити дату'",
                 font=font_cal_13).place(x=700, y=196)
        tk.Label(root, text="Формат дати: 'день'.'місяць'", font=font_cal_12).place(x=700, y=220)
        tk.Label(root, text="Дата:", font=font_cal_13).place(x=700, y=250)
        self.common_date = tk.Entry(root, font=font_cal_12, width=6)
        self.common_date.place(x=750, y=252)
        self.propagate_date = tk.Button(root, text="Проставити дату", command=self.set_date_to_surveys,
                                        font=font_cal_12, bg='#B0C4DE')
        self.propagate_date.place(x=820, y=245)

        self.survey_frame = tk.Frame(root)
        self.survey_frame.place(x=1030, y=65)
        self.surveys_check_btns: list[CheckBtnWithDateEntry] = self.create_all_surveys_checkbtns(all_surveys)
        self.surveys: list[Survey] = []

    def search_patient(self):
        try:
            patient_fio = self.get_value_with_validation(self.fio_entry, fio_empty).strip()
        except ValueError:
            return

        patient = self.file_service.find_patient(patient_fio)
        if patient is None:
            messagebox.showerror("Error", patient_not_found)
            return
        self.clean_entities_without_fio()
        self.ward_entry.insert(0, patient.ward)
        self.mode_entry.set(patient.mode)
        self.diet_entry.set(patient.diet)
        self.prescriptions = patient.prescriptions
        self.surveys = patient.surveys
        self.update_prescriptions_list()
        self.update_surveys_list()

    def add_drug_to_prescriptions(self):
        try:
            drug = self.get_value_with_validation(self.drug_entry, drug_empty)
            dosage = self.dosage_entry.get()
            injection_method = self.get_value_with_validation(self.injection_method_entry, injection_method_empty)
            multiplicity = self.get_value_with_validation(self.multiplicity_entry, multiplicity_empty)
            duration = self.get_value_with_validation(self.duration_entry, duration_empty)
        except ValueError:
            return

        drug_parts = drug.split(' + ')
        dosage_parts = dosage.split(' + ')
        if len(drug_parts) != len(dosage_parts):
            messagebox.showerror("Error", discrepancy_drugs_and_dosage)
            return
        drug_dosage_result = ' + '.join([f"{drug_parts[i]} {dosage_parts[i]}" for i in range(len(drug_parts))])
        self.prescriptions \
            .append(Prescription(drug_dosage_result, injection_method, multiplicity, int(duration)))
        self.update_prescriptions_list()

    def remove_drug_from_prescriptions(self):
        index = self.prescriptions_list.index(tk.ANCHOR)
        if index is not None and index < len(self.prescriptions):
            del self.prescriptions[index]
            self.update_prescriptions_list()

    def clean_all_entries(self):
        self.fio_entry.delete(0, 'end')
        self.ward_entry.delete(0, 'end')
        self.clean_entities_without_fio()

    def clean_entities_without_fio(self):
        self.ward_entry.delete(0, 'end')
        self.drug_entry.delete(0, 'end')
        self.dosage_entry.delete(0, 'end')
        self.injection_method_entry.set('')
        self.multiplicity_entry.set('')
        self.duration_entry.delete(0, 'end')
        self.mode_entry.set('')
        self.diet_entry.set('')
        self.common_date.delete(0, 'end')
        self.prescriptions = []
        self.update_prescriptions_list()
        self.surveys = []
        self.update_surveys_list()

    def generate_files(self):
        try:
            patient_fio = self.get_value_with_validation(self.fio_entry, fio_empty).strip()
            patient_ward = self.get_value_with_validation(self.ward_entry, ward_empty).strip()
            mode = self.mode_entry.get()
            diet = self.diet_entry.get()
            self.surveys = self.get_surveys()
        except ValueError:
            return

        if len(self.prescriptions) == 0:
            messagebox.showerror("Error", prescriptions_empty)
            return

        patient = Patient(fio=patient_fio, ward=patient_ward, mode=mode, diet=diet,
                          prescriptions=self.prescriptions, surveys=self.surveys)
        self.docx_service.generate_document(patient)
        # messagebox.showinfo("Info", f"Документ для пацієнта {patient_fio} згенерований!")
        self.file_service.save_patient(patient)

    def create_all_surveys_checkbtns(self, all_surveys: list[list]) -> list[CheckBtnWithDateEntry]:
        survey_btns: list[CheckBtnWithDateEntry] = []
        group: ToggledFrame = None
        for survey in all_surveys:
            if survey[0].endswith(":"):
                group = ToggledFrame(self.survey_frame, survey[0])
                group.pack(fill="both", pady=2, expand=1, anchor="n")
            else:
                if group is not None:
                    check_entity = CheckBtnWithDateEntry(group.sub_frame, survey[0], survey[1], survey[2], 7)
                    survey_btns.append(check_entity)
        return survey_btns

    def set_date_to_surveys(self):
        date_str = self.common_date.get()
        try:
            datetime.datetime.strptime(date_str, day_month_date_format)
        except ValueError:
            messagebox.showerror("Error", wrong_date)
            return
        for survey_btn in self.surveys_check_btns:
            if survey_btn.is_checked():
                survey_btn.set_date(date_str)

    def get_value_with_validation(self, entry: tk.Entry, error_message: str) -> str:
        entry_value = str(entry.get())
        if entry_value == '' or entry_value is None:
            messagebox.showerror("Error", error_message)
            raise ValueError(error_message)
        if entry == self.duration_entry:
            if not entry_value.isdecimal():
                messagebox.showerror("Error", duration_not_int)
                raise ValueError(duration_not_int)
        return entry_value

    def update_prescriptions_list(self):
        self.prescriptions_list.delete(0, tk.END)
        for i in range(len(self.prescriptions)):
            presc = self.prescriptions[i]
            self.prescriptions_list.insert(
                tk.END,
                f"{'%2d' % (i + 1)}. {presc.drug_with_dosage}  {presc.injection_method}  {presc.multiplicity}  {presc.duration} д.")

    def get_surveys(self) -> list[Survey]:
        return [Survey(survey_checkbtn.cget("text"), survey_checkbtn.get_date(), survey_checkbtn.row_num, survey_checkbtn.col_num)
                for survey_checkbtn in self.surveys_check_btns if survey_checkbtn.is_checked()]

    def update_surveys_list(self):
        for survey_checkbtn in self.surveys_check_btns:
            survey_checkbtn.set_checked(False)
            survey_checkbtn.set_date('')
            for survey in self.surveys:
                if survey.name == survey_checkbtn.cget("text"):
                    survey_checkbtn.set_checked(True)
                    survey_checkbtn.set_date(survey.date)

    def get_font_for(self, entity_key: str, font_key='@font_size'):
        return self.config_dict['@font_name'], int(self.config_dict[entity_key][font_key])

    def get_coords_for(self, entity_key: str):
        return {'x': self.config_dict[entity_key]['@x'], 'y': self.config_dict[entity_key]['@y']}
