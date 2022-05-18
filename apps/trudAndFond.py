import numpy as np
import streamlit as st
import pandas as pd

import read
def buildMain():
    st.markdown("""Рассчитать коэффициенты прямых и полных затрат труда и фондов и плановую потребность в соответствующих ресурсах.""")

    uploaded_file = st.file_uploader("Выберите таблицу", type=['xlsx','csv'])
    if uploaded_file:
        path = read.save_uploadedfile(uploaded_file)
        sheet = read.readDocument(path)
        col_names, itogo_by_row, dob_st, val_price_by_raw, trud, fond = read.readByCol(sheet)
        t, f= [], []
        trudy = list(filter(None, trud))
        fondy = list(filter(None, fond))
        val_price_by_raw = list(filter(None, val_price_by_raw))
        error = 0
        for index in range(len(trudy)-1):
            try:
                t.append(round(trudy[index]/val_price_by_raw[index], 3))
                f.append(round(fondy[index] / val_price_by_raw[index], 3))
            except IndexError:
                error = 1
                st.error("Type error")
                break
        if error == 0:
            st.write('''
            Коэффициенты прямой трудоёмкости (t{\sub j)} представляют собой прямые затраты труда на единицу j-го вида продукции.
    Определить их можно как соотношение затрат живого труда в производстве j-го продукта (Lj) к объёму производства этого продукта , т.е. к валовому выпуску (Xj).
    Воспользовавшись формулой получим:
    ''')
            st.table(pd.DataFrame(t))

            st.write('''
            Коэффициенты прямой фондоёмкости (f{\sub j)} представляют собой величину среднегодовых фондов на единицу j-го вида продукции: fj = Фj/Xj
                    ''')
            st.table(pd.DataFrame(f))

            main_matrix = read.readMainMatrix(sheet)
            row_names, itogo_by_col, end_pruducts, val_price = read.readByRow(sheet)
            koef_pryamyx_zatrat = read.koef_prymyx_zatrat(main_matrix, val_price)
            inv_matrix = read.getInverseMatrix(koef_pryamyx_zatrat)
            inv_matrix = np.array(inv_matrix)
            t = np.array(t)
            st.markdown('''Коэффициенты полных затрат труда определяются как произведение коэффициентов прямой трудоёмкости и матрицы коэффициентов полных материальных затрат:''')


            st.write('Коэффициенты полных затрат трудов')
            st.table(pd.DataFrame(inv_matrix))
            st.table(pd.DataFrame(t))
            t = t.dot(inv_matrix)
            for index in range(len(t)):
                t[index] = round(t[index],3)
            st.write('Таблица полных затрат трудов')
            st.table(pd.DataFrame(t))
            st.line_chart(pd.DataFrame(t))
            st.write('Коэффициенты полных затрат фондов ')
            st.table(pd.DataFrame(inv_matrix))
            f = np.array(f)
            st.table(pd.DataFrame(f))

            f = f.dot(inv_matrix)
            for index in range(len(t)):
                f[index] = round(f[index], 3)
            st.write('Таблица коэффициентов полных затрат фондов')
            st.table(pd.DataFrame(f))
            st.line_chart(pd.DataFrame(f))






def app():
    buildMain()