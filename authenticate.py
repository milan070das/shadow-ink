import base64
import streamlit as st
import sqlite3
import subprocess
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Shadow Ink - Sign in", layout="centered")

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def perform_operation():
    subprocess.Popen(["streamlit", "run", "homepage.py"])

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT
                )''')
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def authenticate_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    conn.close()
    return result is not None

img = get_img_as_base64("background.png")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
background-image:url("data:image/png;base64,{img}");
background-size: 100% 100%;
background-repeat: no-repeat;
background-position: center;
}}

[data-testid="stHeader"] {{
background:rgba(0,0,0,0);
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)


# === App Start ===
init_db()

st.title("Welcome to Shadow Ink✒")
st.markdown("*Conceal. Reveal. Communicate in Silence.*")

selected = option_menu(
    menu_title=None,  # No title for the menu
    options=["Sign In", "Sign Up"],
    # Icons from Bootstrap Icons: https://icons.getbootstrap.com/ [4]
    icons=["box-arrow-in-right", "person-plus"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "rgba(0,0,0,0)"},
        "icon": {"color": "white", "font-size": "18px"},
        "nav-link": {
            "font-size": "16px",
            "text-align": "center",
            "margin": "0px",
            "--hover-color": "#555",
            "color": "#ddd",
        },
        "nav-link-selected": {"background-color": "#02ab21"},
    }
)

if selected == "Sign In":
    st.subheader("Sign In")
    with st.form("signin_form", clear_on_submit=False):
        username = st.text_input("Username", key="signin_user")
        password = st.text_input("Password", type="password", key="signin_pass")
        signin_submit = st.form_submit_button("Proceed")

    if signin_submit:
        if username and password:
            if authenticate_user(username, password):
                st.success(f"Logged in as {username}")
                perform_operation()
                st.success("Welcome to Shadow Ink! Redirecting to the main app...")
                st.markdown(
                    f"""
                    <script>
                    window.open("http://localhost:8502", "_blank");
                    </script>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.error("Invalid username or password.")
        else:
            st.warning("Please enter both username and password.")

elif selected == "Sign Up":
    st.subheader("Sign Up")
    with st.form("signup_form", clear_on_submit=True):
        new_user = st.text_input("New Username", key="signup_user")
        new_pass = st.text_input("New Password", type="password", key="signup_pass")
        signup_submit = st.form_submit_button("Proceed")
    
    if signup_submit:
        if new_user and new_pass:
            try:
                add_user(new_user, new_pass)
                st.success("Account created successfully. Please select 'Sign In' to log in.")
            except sqlite3.IntegrityError:
                st.error("Username already exists.")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter both username and password.")
