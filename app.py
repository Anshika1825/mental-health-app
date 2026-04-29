import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import pickle
from datetime import datetime

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Mental Health App", layout="wide")

# ---------------- DB ----------------
conn = sqlite3.connect("data.db", check_same_thread=False)
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)")
c.execute("""CREATE TABLE IF NOT EXISTS records
          (user TEXT, date TEXT, q1 INT, q2 INT, q3 INT, q4 INT, q5 INT, q6 INT, q7 INT, q8 INT, q9 INT)""")
conn.commit()

# ---------------- FUNCTIONS ----------------
def login_user(u, p):
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (u,p))
    return c.fetchall()

def signup_user(u,p):
    c.execute("INSERT INTO users VALUES (?,?)",(u,p))
    conn.commit()

# ---------------- TITLE ----------------
st.markdown("<h1 style='text-align:center;color:#6C3483;'>🧠 Mental Health Tracker</h1>", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- LOGIN / SIGNUP SCREEN ----------------
if st.session_state.user is None:

    menu = st.sidebar.selectbox("Menu", ["Login","Signup"])

    if menu == "Signup":
        st.subheader("Create Account")
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")

        if st.button("Signup"):
            signup_user(user,pwd)
            st.success("Account Created!")

    elif menu == "Login":
        st.subheader("Login")
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")

        if st.button("Login"):
            result = login_user(user,pwd)

            if result:
                st.session_state.user = user
                st.success("Login Successful")
                st.rerun()
            else:
                st.error("Wrong credentials")

# ---------------- MAIN APP ----------------
else:

    user = st.session_state.user

    # Sidebar Navigation
    page = st.sidebar.selectbox("Navigation", ["Dashboard","Assessment","History","Tips","Logout"])

    st.sidebar.write(f"👤 {user}")

    # -------- DASHBOARD --------
    if page == "Dashboard":
        st.subheader("🏠 Dashboard")
        st.write("Welcome to your mental health tracker!")

        df = pd.read_sql_query(f"SELECT * FROM records WHERE user='{user}'", conn)

        if not df.empty:
            st.line_chart(df[['q1','q2','q3','q4','q5','q6','q7','q8','q9']])
        else:
            st.info("No data yet")

    # -------- ASSESSMENT --------
    elif page == "Assessment":

        st.subheader("🧠 Mental Health Assessment")

        model = pickle.load(open("model.pkl","rb"))

        q1 = st.slider("Little interest in doing things",0,3)
        q2 = st.slider("Feeling down or depressed",0,3)
        q3 = st.slider("Trouble sleeping",0,3)
        q4 = st.slider("Feeling tired",0,3)
        q5 = st.slider("Poor appetite",0,3)
        q6 = st.slider("Feeling bad about yourself",0,3)
        q7 = st.slider("Trouble concentrating",0,3)
        q8 = st.slider("Moving/speaking slowly",0,3)
        q9 = st.slider("Thoughts of self-harm",0,3)

        if st.button("Analyze"):
            data = np.array([[q1,q2,q3,q4,q5,q6,q7,q8,q9]])
            result = model.predict(data)

            if result[0] == 1:
                st.error("⚠ High Risk of Depression")
            else:
                st.success("✅ You are doing well!")

        if st.button("Save Today's Data"):
            today = datetime.now().strftime("%Y-%m-%d")
            c.execute("INSERT INTO records VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                      (user,today,q1,q2,q3,q4,q5,q6,q7,q8,q9))
            conn.commit()
            st.success("Data Saved")

    # -------- HISTORY --------
    elif page == "History":

        st.subheader("📊 History")

        df = pd.read_sql_query(f"SELECT * FROM records WHERE user='{user}'", conn)

        if not df.empty:
            st.dataframe(df)
            st.line_chart(df[['q1','q2','q3','q4','q5','q6','q7','q8','q9']])
        else:
            st.warning("No history found")

    # -------- TIPS --------
    elif page == "Tips":

        st.subheader("💡 Mental Health Tips")

        st.success("✔ Sleep properly")
        st.success("✔ Exercise daily")
        st.success("✔ Talk to friends/family")
        st.success("✔ Reduce screen time")
        st.success("✔ Practice meditation")

    # -------- LOGOUT --------
    elif page == "Logout":
        st.session_state.user = None
        st.rerun()