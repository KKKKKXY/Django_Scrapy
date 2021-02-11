import openpyxl
import random

def get_cid_from_excel(path):
    print('------Start get company id from EXCEL------')
    companies_id = []
    wb_obj = openpyxl.load_workbook(path)
    sheet_obj = wb_obj.active
    max_row = sheet_obj.max_row
    for i in range(10): 
        rnum = random.randint(4, max_row)
        cell_obj = sheet_obj.cell(row = rnum, column = 2)
        print('Row: ' + str(rnum) + ' Value is ' + cell_obj.value)
        companies_id.append(cell_obj.value)     
    print(companies_id)
    return companies_id