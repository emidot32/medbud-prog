from json import JSONEncoder
from dataclasses import dataclass
from docx.table import _Cell


@dataclass
class Prescription:
    drug_with_dosage: str
    injection_method: str
    multiplicity: str
    duration: int


@dataclass
class Survey:
    name: str
    date: str
    row_num: int
    col_num: int


@dataclass
class Patient:
    fio: str
    ward: str
    diet: str
    mode: str
    prescriptions: list[Prescription]
    surveys: list[Survey]


@dataclass
class CellInfo:
    cell: _Cell
    row_num: int
    col_num: int
