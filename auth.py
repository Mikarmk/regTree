import streamlit as st
import hashlib
import sqlite3

# Это пока бд
def create_database():
    conn = sqlite3.connect('users.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT UNIQUE, password TEXT)''')
    conn.commit()
    conn.close()

create_database()

# добавлям в хеш пароль, который пользователь ввел
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Добавляем в бд
def add_user(username, hashed_password):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()

# Проверка!
def check_credentials(username, hashed_password):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
    result = c.fetchone()
    conn.close()
    return result is not None

def show_auth():
    st.sidebar.title("Аутентификация")
    username = st.sidebar.text_input("Имя пользователя", key="login_user")
    password = st.sidebar.text_input("Пароль", type="password", key="login_pass")
    
    if st.sidebar.button("Зарегистрироваться"):
        if not username or not password:
            st.sidebar.error("Введите имя пользователя и пароль")
        else:
            hashed_password = hash_password(password)
            add_user(username, hashed_password)
            st.sidebar.success("Пользователь создан успешно. Теперь войдите в систему.")
    
    elif st.sidebar.button("Войти"):
        if not username or not password:
            st.sidebar.error("Введите имя пользователя и пароль")
        else:
            hashed_password = hash_password(password)
            if check_credentials(username, hashed_password):
                st.session_state['authenticated'] = True
                st.session_state['username'] = username
                st.experimental_rerun()
            else:
                st.sidebar.error("Неверные учетные данные")

    if st.sidebar.button("Выйти"):
        if 'authenticated' in st.session_state:
            del st.session_state['authenticated']
        if 'username' in st.session_state:
            del st.session_state['username']
            
    if 'authenticated' in st.session_state and st.session_state['authenticated']:
        st.sidebar.success(f"Вы вошли как {st.session_state['username']}")
        return True
    else:
        return False
