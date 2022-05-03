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
        for index in range(len(trudy)-1):
            t.append(round(trudy[index]/val_price_by_raw[index],3))
            f.append(round(fondy[index] / val_price_by_raw[index], 3))
        st.dataframe(pd.DataFrame(t))
        st.dataframe(pd.DataFrame(f))

        col_names, itogo_by_row, dob_st, val_price_by_raw, trud, fondy = read.readByCol(sheet)
        st.dataframe(pd.DataFrame(val_price_by_raw))
        for i in range(len(t)):
            t[i] = val_price_by_raw[i] * t[i]
            f[i] = val_price_by_raw[i] * f[i]

        st.dataframe(pd.DataFrame(t))
        st.dataframe(pd.DataFrame(f))






def app():
    buildMain()