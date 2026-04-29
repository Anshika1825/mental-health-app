import streamlit as st
import numpy as np
import pickle

st.set_page_config(page_title="Mental Health App")

st.title("🧠 Mental Health Predictor")

st.write("Fill the details below:")

# Load model
model = pickle.load(open("model.pkl","rb"))

# Inputs
q1 = st.slider("Interest in doing things",0,3)
q2 = st.slider("Feeling depressed",0,3)
q3 = st.slider("Sleep issues",0,3)
q4 = st.slider("Feeling tired",0,3)
q5 = st.slider("Appetite problems",0,3)
q6 = st.slider("Low confidence",0,3)
q7 = st.slider("Concentration issues",0,3)
q8 = st.slider("Slow movement",0,3)
q9 = st.slider("Negative thoughts",0,3)

# Prediction
if st.button("Predict"):
    data = np.array([[q1,q2,q3,q4,q5,q6,q7,q8,q9]])
    result = model.predict(data)

    if result[0] == 1:
        st.error("⚠ High Risk of Depression")
    else:
        st.success("✅ You are doing well!")