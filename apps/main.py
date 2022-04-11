import streamlit as st
import pandas as pd

import read
def buildMain():
    st.markdown("""Основным элементом матричной модели является технологический коэффициент  , который отражает технологические связи и материальные потребности между производящими и потребляющими отраслями. Коэффициент прямых  материальных затрат  показывает, сколько единиц продукции і-отрасли непосредственно затрачивается в качестве средств производства на выпуск единицы продукции j-отрасли.
    Прямыми материальными затратами называются затраты, обусловленные на последнем этапе производства.""")

    uploaded_file = st.file_uploader("Выберите таблицу", type=['xlsx','csv'])
    # main_matrix, col_names, row_names, total_count, kon_product, val_price = read.readDocument(uploaded_file)
    if uploaded_file:
        path = read.save_uploadedfile(uploaded_file)
        main_matrix, col_names, row_names, total_count, kon_product, val_price = read.readDocument(path)
        koef_pryamyx_zatrat = read.koef_prymyx_zatrat(main_matrix, val_price)
        # st.write(type(koef_pryamyx_zatrat))
        # pd.DataFrame(koef_pryamyx_zatrat)
        # dataframe = pd.read_csv(uploaded_file)
        st.dataframe(pd.DataFrame(koef_pryamyx_zatrat))



def app():
    buildMain()