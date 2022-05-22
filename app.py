import streamlit as st
import streamlit_authenticator as stauth
import auth.authreader
from multiapp import MultiApp
from apps import main, trudAndFond, balans, landing, method

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


names = auth.authreader.getNames()
usernames = auth.authreader.getUsername()
passwords = auth.authreader.getPass()

hashed_passwords = stauth.Hasher(passwords).generate()
authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    'some_cookie_name', 'some_signature_key', cookie_expiry_days=30)

#
with st.sidebar:
    st.title("Научно-производственный центр «Геодезия и картография»")
    name, authentication_status, username = authenticator.login('Login', 'main')
if not st.session_state['authentication_status']:
    landing.buildMain()


if st.session_state['authentication_status']:
    app = MultiApp()
    app.add_app("Главная страница", landing.buildMain)
    app.add_app("Методология", method.buildMain)
    app.add_app("Посчитать коэффициенты прямых материальных затрат.", main.buildMain)
    app.add_app("Рассчитать коэффициенты прямых и полных затрат труда и фондов и плановую потребность в соответствующих ресурсах.", trudAndFond.app)
    app.add_app("Проследить баланс", balans.buildMain)
    app.run()
    with st.sidebar:
        st.write("")    
        st.write("")
        st.write("")
        st.write("----------")
        authenticator.logout('Выйти из системы', 'main')
elif st.session_state['authentication_status' ] == False:
    with st.sidebar:
        st.error('Неверное имя пользователя/пароль')
elif st.session_state['authentication_status'] == None:
    with st.sidebar:
        st.warning('Пожалуйста, введите имя пользователя и пароль')



