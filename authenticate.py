import base64
import streamlit as st
import sqlite3
import subprocess

st.set_page_config(page_title="Shadow Ink - Sign in", layout="centered")

def get_img_as_base64(file):
    with open(file,"rb") as f:
        data=f.read()
    return base64.b64encode(data).decode()

img=get_img_as_base64("background.png")

def get_img_as_base64(file):
    with open(file,"rb") as f:
        data=f.read()
    return base64.b64encode(data).decode()

img1=get_img_as_base64("background.png")

page_bg_img=f"""
<style>
[data-testid="stAppViewContainer"] {{
background-image:url("data:image/png;base64,{img1}");
background-size: 100% 100%; /* Sets the background image width and height */
background-repeat: no-repeat; /* Prevents the image from repeating */
background-position: center; /* Centers the image */
}}

[data-testid="stHeader"] {{
background:rgba(0,0,0,0);
}}
</style>
"""
st.markdown(page_bg_img,unsafe_allow_html=True)

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

# === App Start ===
init_db()

st.title("Welcome to Shadow Ink✒")
st.markdown("*Conceal. Reveal. Communicate in Silence.*")

# Button toggles for Sign In and Sign Up
col1, col2 = st.columns(2)
with col1:
    sign_in_clicked = st.button("Sign In")
with col2:
    sign_up_clicked = st.button("Sign Up")
# sign_in_clicked = st.button("Sign In")
# sign_up_clicked = st.button("Sign Up")
# Session state to track which form to show
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = None

if sign_in_clicked:
    st.session_state.auth_mode = "sign_in"
elif sign_up_clicked:
    st.session_state.auth_mode = "sign_up"

if st.session_state.auth_mode == "sign_in":
    st.subheader("Sign In")
    username = st.text_input("Username", key="signin_user")
    password = st.text_input("Password", type="password", key="signin_pass")
    if st.button("Proceed", key="signin_submit"):
        if username and password:
            if authenticate_user(username, password):
                st.success(f"Logged in as {username}")
                # --- Inline JS redirect to landing page ---
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
                # Note: "/landing" should match your multipage app's landing script
            else:
                st.error("Invalid username or password.")
        else:
            st.warning("Please enter both username and password.")

elif st.session_state.auth_mode == "sign_up":
    st.subheader("Sign Up")
    new_user = st.text_input("New Username", key="signup_user")
    new_pass = st.text_input("New Password", type="password", key="signup_pass")
    if st.button("Proceed", key="signup_submit"):
        if new_user and new_pass:
            try:
                add_user(new_user, new_pass)
                st.success("Account created successfully. Please sign in.")
                st.session_state.auth_mode = "sign_in"
            except sqlite3.IntegrityError:
                st.error("Username already exists.")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter both username and password.")