import threading
from tkinter.ttk import Combobox
import tkinter.font as tkFont

from data_classes import *
from docx_service import DocxService
from file_services import FileService
from tk_entities.custom_entries import *


class MainPage:
    def __init__(self, root, drug_list, drug_dict, injection_methods: list, modes: list, diets: list,
                 all_surveys: list[list], docx_service: DocxService, file_service: FileService):
        root.title("Medbud Preparaty")
        root.iconbitmap(r"img1.ico")
        root.state("zoomed")
        root.option_add('*Dialog.msg.font', font_cal_12)
        combobox_cal_12 = tkFont.Font(name=font_cal_10[0], size=font_cal_10[1])
        root.option_add("*TCombobox*Listbox*Font", combobox_cal_12)
        self.root = root
        self.docx_service = docx_service
        self.file_service = file_service
        tk.Label(root, text="Введіть ПІБ пацієнта та номер палати", font=font_cal_14).place(x=40, y=20)
        tk.Label(root, text="Кнопка 'Пошук' заповнить поля призначення, якщо пацієнт існує", font=font_cal_12)\
            .place(x=40, y=50)
        self.fio_entry = tk.Entry(root, font=font_cal_14, width=43)
        self.fio_entry.place(x=43, y=85)
        self.ward_entry = tk.Entry(root, font=font_cal_14, width=7)
        self.ward_entry.place(x=501, y=85)
        self.search_btn = tk.Button(root, text="Пошук", command=self.search_patient, font=font_cal_11, bg='#B0C4DE')
        self.search_btn.place(x=595, y=83)

        tk.Label(root, text="Оберіть режим та дієту для пацієнта", font=font_cal_12).place(x=40, y=125)
        tk.Label(root, text="Режим", font=font_cal_14).place(x=40, y=150)
        self.mode_entry = Combobox(root, values=modes, font=font_cal_13, width=14)
        self.mode_entry.place(x=43, y=180)

        tk.Label(root, text="Дієта", font=font_cal_14).place(x=222, y=150)
        self.diet_entry = Combobox(root, values=diets, font=font_cal_13, width=8)
        self.diet_entry.place(x=225, y=180)

        tk.Label(root, text="Оберіть препарат, дозування, спосіб введення, кратність, тривалість", font=font_cal_12) \
            .place(x=40, y=220)
        tk.Label(root, text="та натисніть кнопку '+' щоб додати препарат до призначень", font=font_cal_12) \
            .place(x=40, y=240)
        self.prescriptions_list = tk.Listbox(root, font=font_cal_13, width=59, height=10)
        self.prescriptions_list.place(x=42, y=270)
        self.prescriptions: list[Prescription] = []
        self.add_btn = tk.Button(root, text='\u2795', command=self.add_drug_to_prescriptions, bg='white', fg='green',
                                 width=5, height=2)
        self.add_btn.place(x=595, y=270)
        self.remove_btn = tk.Button(root, text='\u274C', command=self.remove_drug_from_prescriptions, bg='white',
                                    fg='red', width=5, height=2)
        self.remove_btn.place(x=595, y=320)
        self.clean_btn = tk.Button(root, text='\U0001F5D1', command=self.clean_all_entries, bg='white',
                                   fg='red', width=5, height=2)
        self.clean_btn.place(x=595, y=370)
        self.generate_btn = tk.Button(root, text="Згенерувати", command=lambda: threading.Thread(target=self.generate_files).start(),
                                      font=font_cal_14, width=15, height=3, bg='#87A96B')
        # self.generate_btn.place(x=765, y=182)
        self.generate_btn.place(x=750, y=320)

        tk.Label(root, text="Препарати", font=font_cal_14).place(x=40, y=500)
        tk.Label(root, text="Дозування", font=font_cal_14).place(x=385, y=500)
        tk.Label(root, text="Спосіб введення", font=font_cal_14).place(x=593, y=500)
        tk.Label(root, text="Кратність", font=font_cal_14).place(x=760, y=500)
        tk.Label(root, text="Тривалість", font=font_cal_14).place(x=865, y=500)

        self.drug_entry = AutocompleteEntryWithListbox(root, sorted(set([item[0] for item in drug_list])),
                                                       43, 530, entry_width=34, listbox_width=37)
        self.dosage_entry = RelatedEntryWithListbox(root, sorted(set([item[1] for item in drug_list])), 387, 530,
                                                    self.drug_entry, drug_dict, entry_width=19, listbox_width=21)

        self.injection_method_entry = Combobox(root, values=injection_methods, font=font_cal_13, width=14)
        self.injection_method_entry.place(x=595, y=530)

        self.multiplicity_entry = Combobox(root, values=[str(i) + " р/д" for i in range(1, 4)],
                                           font=font_cal_13, width=7)
        self.multiplicity_entry.place(x=763, y=530)

        self.duration_entry = tk.Entry(root, font=font_cal_13, width=6)
        self.duration_entry.place(x=868, y=530)
        tk.Label(root, text="дні/днів", font=font_cal_13).place(x=934, y=530)

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
