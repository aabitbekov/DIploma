import streamlit as st
import streamlit_authenticator as stauth

import auth.authreader
from multiapp import MultiApp
from apps import main, trudAndFond, fours, description, balans
from PIL import Image

st.set_page_config(
     page_title="MOБ",
     page_icon="⚙️",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://www.extremelycoolapp.com/help',
         'Report a bug': "https://www.extremelycoolapp.com/bug",
         'About': "# This is a header. This is an *extremely* cool app!"
     }
 )


st.markdown("""
# Межотраслевой баланс
Межотраслевой баланс (МОБ, модель «затраты — выпуск», метод «затраты — выпуск») — экономико-математическая балансовая модель, характеризующая межотраслевые производственные взаимосвязи в экономике страны. Характеризует связи между выпуском продукции в одной отрасли и затратами, расходованием продукции всех участвующих отраслей, необходимым для обеспечения этого выпуска. Межотраслевой баланс составляется в денежной и натуральной формах.""")
st.write('')
st.write('')
col1, col2, col3 = st.columns([2,6,1])

with col1:
    st.write("")

with col2:
    st.image(image=Image.open('static/175.png'),use_column_width=False, caption='Экономико-математическая модель межотраслевого баланса')

with col3:
    st.write("")
st.markdown("""Межотраслевой баланс представлен в виде системы линейных уравнений. Межотраслевой баланс (МОБ) представляет собой таблицу, в которой отражен процесс формирования и использования совокупного общественного продукта в отраслевом разрезе. Таблица показывает структуру затрат на производство каждого продукта и структуру его распределения в экономике.""")

names = ['User', 'Admin']
usernames = auth.authreader.getUsername()
passwords = auth.authreader.getPass()

hashed_passwords = stauth.Hasher(passwords).generate()
authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    'some_cookie_name', 'some_signature_key', cookie_expiry_days=30)
name, authentication_status, username = authenticator.login('Login', 'main')


if st.session_state['authentication_status']:
    app = MultiApp()
    authenticator.logout('Logout', 'main')
    # Add all your application here
    app.add_app("Посчитать коэффициенты прямых материальных затрат.", main.app)
    app.add_app("Рассчитать коэффициенты прямых и полных затрат труда и фондов и плановую потребность в соответствующих ресурсах.", trudAndFond.app)
    # app.add_app("Проследить эффект матричного мультипликатора при дополнительном увеличении конечного продукта по какой-либо отрасли на X %.", fours.app)
    app.add_app("Проследить баланс", balans.app)
    app.run()
elif st.session_state['authentication_status' ] == False:
    st.error('Неверное имя пользователя/пароль')
elif st.session_state['authentication_status'] == None:
    st.warning('Пожалуйста, введите имя пользователя и пароль')



