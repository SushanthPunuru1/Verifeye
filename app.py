import streamlit as st
import google.generativeai as genai
from datetime import datetime


API_KEY_VALUE = st.secrets["API_KEY"]
genai.configure(api_key = API_KEY_VALUE)
model = genai.GenerativeModel("gemini-2.5-flash")


if "history" not in st.session_state:
    st.session_state.history = []


st.set_page_config(page_title="Verifeye", layout="centered")

st.title("Verifeye")
st.write("Analyze messages for **social engineering and phishing risks**.")


name = st.text_input("Your name")

content = st.text_area(
    "Paste the message or email you received",
    height=180
)

message_type = st.radio(
    "Message type",
    ("Email", "SMS/Text", "Social Media", "Instant Message", "Other")
)

concern = st.slider("How concerned are you?", 1, 10, 5)

st.divider()
st.header("Quick Survey")

how_received = st.text_input("How did you receive this message?")


def yes_no_question(label, placeholder):
    answer = st.radio(label, ("No", "Yes"), horizontal=True)
    details = ""
    if answer == "Yes":
        details = st.text_input(placeholder)
    return f"{answer} - {details}" if details else answer

know_sender = yes_no_question(
    "Do you know the sender?",
    "Who is the sender?"
)

claimed_account = yes_no_question(
    "Do you have an account with the claimed company?",
    "Which company/service?"
)

action_taken = yes_no_question(
    "Have you taken any action already?",
    "What action did you take?"
)

previous_comm = yes_no_question(
    "Have you communicated with this sender before?",
    "Describe previous communication"
)

device = st.text_input("Device used (phone, laptop, etc.)")
region = st.text_input("Your country/region")


st.sidebar.header("🔗 URL Checker")
phishing_url = st.sidebar.text_input("Paste a suspicious URL")

if st.sidebar.button("Check URL"):
    url_prompt = f"""
    Analyze this URL for phishing risk:

    URL: {phishing_url}

    Provide:
    - Risk level (Low/Medium/High)
    - Why it is risky or safe
    - Recommended action
    """
    url_result = model.generate_content(url_prompt)
    st.sidebar.write(url_result.text)


if st.button("Analyze Message"):
    prompt = f"""
    You are a cybersecurity analyst.

    MESSAGE:
    {content}

    CONTEXT:
    - Message type: {message_type}
    - How received: {how_received}
    - Know sender: {know_sender}
    - Claimed account: {claimed_account}
    - Action taken: {action_taken}
    - Previous communication: {previous_comm}
    - Device: {device}
    - Region: {region}
    - User concern: {concern}/10

    TASKS:
    1. Identify social engineering tactics.
    2. Identify phishing indicators.
    3. Give Social Engineering Risk (Low/Medium/High).
    4. Give Phishing Risk (Low/Medium/High).
    5. Give an overall risk score (0–100).
    6. Highlight suspicious phrases.
    7. Provide clear next steps.
    """
    
    result = model.generate_content(prompt)

    analysis = result.text
   
    st.divider()
    st.header("📊 Analysis Results")

    st.markdown(analysis)


