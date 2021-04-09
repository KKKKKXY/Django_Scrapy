# import openpyxl
import random
import logging

def get_cid_from_excel(excel_path):
    print('------Start get company id from EXCEL------')
    logging.warning('------Start get company id from EXCEL------')
    companies_id = []
    wb_obj = openpyxl.load_workbook(excel_path)
    sheet_obj = wb_obj.active
    max_row = sheet_obj.max_row
    # append all values into 'companies_id' list
    for i in range(4,max_row+1,1):
        cell_obj = sheet_obj.cell(row = i, column = 2)
        logging.info('Row: ' + str(i) + ' Value is: ' + cell_obj.value)
        companies_id.append(cell_obj.value)
    return companies_id