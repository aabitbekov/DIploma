import os

import numpy as np
import openpyxl
from pathlib import Path


def save_uploadedfile(uploadedfile):
    with open(os.path.join(uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
    return uploadedfile.name


def readDocument(path):
    xlsx_file = Path(path)
    wb_obj = openpyxl.load_workbook(xlsx_file)
    sheet = wb_obj.active
    main_matrix = []
    var_row, total_count , kon_product, val_price = [],[], [], []
    outiter, inter = 0, 0
    for row in sheet.iter_rows(max_col=sheet.max_column, max_row=sheet.max_row):
        if outiter == 0:
            pass
        else:
            inter = 0
            for cell in row:
                if inter == 0:
                    pass
                else:
                    if inter == sheet.max_row - 1:
                        total_count.append(cell.value)
                        # print(total_count)
                    elif inter == sheet.max_row:
                        kon_product.append(cell.value)
                        # print(kon_product)
                    elif inter == sheet.max_row + 1:
                        val_price.append(cell.value)
                        # print(val_price)
                    else:
                        var_row.append(cell.value)
                inter += 1
        if var_row != []:
            main_matrix.append(var_row)
            var_row = []
        outiter += 1

    # print(main_matrix)
    col_names = []
    for column in sheet.iter_cols(1, sheet.max_column):
        col_names.append(column[0].value)
    # print(col_names)
    row_names = []
    for row in sheet.iter_rows(1, sheet.max_row):
        row_names.append(row[0].value)
    # print(row_names)
    return main_matrix, col_names, row_names, total_count, kon_product, val_price

def koef_prymyx_zatrat(main_matrix,  val_price):
    koef_prymyx_zatrat = []
    row_koef_prymyx_zatrat = []
    index = 0
    for array in main_matrix:
        for element in array:
            row_koef_prymyx_zatrat.append(round(element/val_price[index], 4))
            index += 1
        koef_prymyx_zatrat.append(row_koef_prymyx_zatrat)
        row_koef_prymyx_zatrat = []
        index = 0
    koef_prymyx_zatrat.remove(koef_prymyx_zatrat[-1])
    return koef_prymyx_zatrat



if __name__ == '__main__':
    main_matrix, col_names, row_names, total, product, val_price = readDocument()
    print(np.matrix(main_matrix))
    koef_prymyx_zatrat = koef_prymyx_zatrat(main_matrix, val_price)
    print(val_price)
    # print(koef_prymyx_zatrat)
    # print(pd.array(koef_prymyx_zatrat))
    z = np.matrix(koef_prymyx_zatrat)
    print(z)


