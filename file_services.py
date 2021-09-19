import os
from abc import ABC, abstractmethod
import xml.etree.ElementTree as et
import json
from types import SimpleNamespace
from consts import *
from data_classes import *


class FileService(ABC):
    def __init__(self):
        self.patient: Patient = None

    @abstractmethod
    def get_file_type(self) -> str:
        pass

    @abstractmethod
    def save_patient(self, patient: Patient):
        pass

    def find_patient(self, fio: str) -> Patient:
        file_type = self.get_file_type()
        for file in os.listdir(f"output_files/{file_type}"):
            name = fio.replace(' ', '_')
            file_name = file.split(".")[0]
            if file_name == name:
                return self.parse_file(f"output_files/{file_type}/{file}")
        return None

    @abstractmethod
    def parse_file(self, file_name: str) -> Patient:
        pass


class JsonService(FileService):

    class PatientEncoder(JSONEncoder):
        def default(self, o): return o.__dict__

    def get_file_type(self) -> str:
        return 'json'

    def save_patient(self, patient: Patient):
        self.patient = patient
        json_str = json.dumps(patient, indent=4, cls=self.PatientEncoder, ensure_ascii=False)
        name = self.patient.fio.replace(' ', '_')
        file = open(f"output_files/json/{name}.json", mode='w', encoding='utf-8')
        file.write(json_str)

    def parse_file(self, file_name: str) -> Patient:
        file = open(file_name, mode='r', encoding='utf-8')
        json_str = file.read()
        return json.loads(json_str, object_hook=lambda d: SimpleNamespace(**d))


class XmlService(FileService):

    def get_file_type(self) -> str:
        return 'xml'

    def save_patient(self, patient: Patient):
        self.patient = patient
        root = et.Element('patient')
        root.set('fio', patient.fio)
        root.set('ward', patient.ward)
        self.set_prescriptions(root)
        self.set_surveys(root)
        tree = et.ElementTree(root)
        self.indent(root)
        name = self.patient.fio.replace(' ', '_')
        tree.write(f"output_files/xml/{name}.xml", encoding='utf-8')

    def parse_file(self, file_name: str) -> Patient:
        pass

    def set_prescriptions(self, root: et.Element):
        prescriptions_tag = et.SubElement(root, 'prescriptions')
        for prescription in self.patient.prescriptions:
            prescription_tag = et.SubElement(prescriptions_tag, 'prescription')
            prescription_tag.set('drug_dosage', prescription.drug_with_dosage)
            prescription_tag.set('injection_method', prescription.injection_method)
            prescription_tag.set('multiplicity', prescription.multiplicity)
            prescription_tag.set('duration', str(prescription.duration))

    def set_surveys(self, root: et.Element):
        surveys_tag = et.SubElement(root, 'surveys')
        for survey in self.patient.surveys:
            prescription_tag = et.SubElement(surveys_tag, 'survey')
            prescription_tag.set('name', survey.name)
            prescription_tag.set('date', survey.date)

    def indent(self, elem: et.Element, level=0):
        i = "\n" + level * "    "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "    "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
