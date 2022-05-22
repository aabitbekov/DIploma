import numpy as np
import streamlit as st
import pandas as pd
import read


@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')


def buildMain():
    st.markdown("""Основным элементом матричной модели является технологический коэффициент  , который отражает технологические связи и материальные потребности между производящими и потребляющими отраслями. Коэффициент прямых  материальных затрат  показывает, сколько единиц продукции і-отрасли непосредственно затрачивается в качестве средств производства на выпуск единицы продукции j-отрасли.
    Прямыми материальными затратами называются затраты, обусловленные на последнем этапе производства.""")

    uploaded_file = st.file_uploader("Выберите таблицу", type=['xlsx','csv'])
    if uploaded_file:
        path = read.save_uploadedfile(uploaded_file)
        sheet = read.readDocument(path)
        main_matrix = read.readMainMatrix(sheet)
        row_names, itogo_by_col, end_pruducts, val_price = read.readByRow(sheet)
        koef_pryamyx_zatrat = read.koef_prymyx_zatrat(main_matrix, val_price)
        if koef_pryamyx_zatrat == 0:
            st.error('Type error')
        else:
            st.write("""По формуле aij = xij / xj находим коэффициенты прямых затрат: """)
            # print(row_names)
            st.table(pd.DataFrame(koef_pryamyx_zatrat))
            st.line_chart(pd.DataFrame(koef_pryamyx_zatrat))

            st.write("Вычисляем обратную матрицу (E-A)-1")
            inv_matrix = read.getInverseMatrix(koef_pryamyx_zatrat)
            st.table(pd.DataFrame(inv_matrix))
            st.line_chart(pd.DataFrame(inv_matrix))

            st.write('''
            Введем коэффициенты прямых затрат:
    aij = xij/xj, (i,j = 1,2,...,n),
    показывающие затраты продукции i-й отрасли на производство единицы стоимости j-й отрасли.
    Находим валовой объем продукции xi;
    ''')
            filtered_list = list(filter(None, end_pruducts))
            del filtered_list[-1]
            matrixX = np.dot(inv_matrix, filtered_list)
            st.table(pd.DataFrame(matrixX))


            st.write("Величина условно чистой продукции Zi равна сумме амортизации, оплаты труда и чистого дохода отрасли j.")
            sum = np.sum(main_matrix, axis=0)
            res = []
            for i in range(len(matrixX)):
                var =  round(matrixX[i] - sum[i], 2)
                res.append(var)
            st.table(pd.DataFrame(res))


            csv = convert_df(pd.DataFrame(koef_pryamyx_zatrat))
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='large_df.csv',
                mime='text/csv',
            )
