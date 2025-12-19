import streamlit as st
import google.generativeai as genai


genai.configure(api_key = "AIzaSyCr-Yeq7H31VnXnk9K5ryaI8bW5hmdsh08")


model = genai.GenerativeModel("gemini-2.5-flash")


# --- App Title ---
st.title("Social Engineering & Phishing Detector")
st.write("Paste a message or URL to check for social engineering or phishing risks.")

# --- User Info ---
name = st.text_input("Enter your name:")

# --- Message Input ---
content = st.text_area("Paste the content of the message/email you received:")

# --- Survey Section ---
st.header("Survey")

howRecieved = st.text_input("How did you receive this message?")

# Yes / No + conditional inputs
youKnow = st.radio("Is the sender someone you know?", ("No", "Yes"), horizontal=True)
youKnowDetails = ""
if youKnow == "Yes":
    youKnowDetails = st.text_input("Who is the sender?")

claimedAcc = st.radio(
    "Do you have an account with the claimed sender?",
    ("No", "Yes"),
    horizontal=True
)
claimedAccDetails = ""
if claimedAcc == "Yes":
    claimedAccDetails = st.text_input("Which company or service?")

actionTaken = st.radio(
    "Did you take any action because of this message?",
    ("No", "Yes"),
    horizontal=True
)
actionTakenDetails = ""
if actionTaken == "Yes":
    actionTakenDetails = st.text_input("What action did you take?")

previousCom = st.radio(
    "Have you communicated with this sender before?",
    ("No", "Yes"),
    horizontal=True
)
previousComDetails = ""
if previousCom == "Yes":
    previousComDetails = st.text_input("Describe the prior communication")

deviceUsed = st.text_input("What device did you use?")
region = st.text_input("Your region/country?")

concernLevel = st.slider("How concerned are you (1–10)?", 1, 10, 5)

messageType = st.radio(
    "Type of message received:",
    ("Email", "SMS/Text Message", "Social Media", "Instant Message", "Other")
)

# --- Sidebar: URL Checker ---
st.sidebar.header("Phishing URL Checker")
phishingUrl = st.sidebar.text_input("Enter URL:")

if st.sidebar.button("Check URL"):
    with st.spinner("Analyzing URL..."):
        prompt = f"""
        You are an AI cybersecurity analyst.
        Analyze the following URL for phishing risks:

        URL: {phishingUrl}

        Provide:
        - Risk level (Low/Medium/High)
        - Why it may be dangerous
        - Recommended next steps
        """
        urlAnalysis = model.generate_content(prompt)
        st.sidebar.write(urlAnalysis.text)

# --- Analyze Message ---
if st.button("Analyze Message"):
    if not content.strip():
        st.warning("Please paste a message to analyze.")
    else:
        with st.spinner("Analyzing message..."):
            prompt = f"""
            You are an AI cybersecurity analyst analyzing a potentially malicious message.

            Message content:
            {content}

            Context:
            - Message type: {messageType}
            - How received: {howRecieved}
            - Know sender: {youKnow} ({youKnowDetails})
            - Claimed account: {claimedAcc} ({claimedAccDetails})
            - Action taken: {actionTaken} ({actionTakenDetails})
            - Previous communication: {previousCom} ({previousComDetails})
            - Device used: {deviceUsed}
            - Region: {region}
            - User concern level: {concernLevel}/10

            Tasks:
            1. Identify social engineering tactics.
            2. Identify phishing indicators.
            3. Give Social Engineering Risk (Low/Medium/High).
            4. Give Phishing Risk (Low/Medium/High).
            5. Highlight suspicious phrases or links.
            6. Provide clear next steps.
            """

            result = model.generate_content(prompt)
            st.subheader("Analysis Results")
            st.write(result.text)