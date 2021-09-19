import csv


def get_list_from_txt(file_path: str):
    file = open(file_path, mode='r', encoding='utf-8')
    return [item.replace("\n", "") for item in file.readlines()]


def get_drug_dosage_dict(full_drug_list):
    drug_dosage_dict = {}
    i = 0
    while i < len(full_drug_list):
        dosage_list = []
        k = i
        while k < len(full_drug_list) and full_drug_list[i][0] == full_drug_list[k][0]:
            dosage_list.append(full_drug_list[k][1])
            k += 1
        drug_dosage_dict[full_drug_list[i][0]] = dosage_list
        i += (k-i)
    return drug_dosage_dict


def get_list_from_csv(file_path: str):
    csvfile = open(file_path, newline='', encoding='utf-8')
    return list(csv.reader(csvfile, delimiter=';'))
