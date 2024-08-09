import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response


st.set_page_config(page_title="MahaGPT - Your AI Chat Companion", layout="centered", page_icon="🤖")

# Custom CSS for a dark-themed look and sidebar styling
st.markdown("""
    <style>
        body {
            background-color: #121212;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .main {
            background-color: #2e2e2e;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.4);
        }
        h1 {
            color: #ffffff;
            font-size: 36px;
            text-align: center;
            margin-bottom: 20px;
        }
        h2, h3, h4 {
            color: #ffffff;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 16px;
            margin-top: 20px;
        }
        .stTextInput>div>div>input {
            background-color: #3e3e3e;
            color: white;
            border-radius: 10px;
            padding: 10px;
            font-size: 18px;
        }
        .stExpander>div {
            background-color: #1e1e1e;
        }
        .stExpander>div>div {
            color: white;
        }
        /* Sidebar Styling */
        .sidebar .sidebar-content {
            background-color: #1e1e1e;
            padding: 10px;
            border-radius: 10px;
        }
        .sidebar .sidebar-content h3 {
            color: #ffffff;
            margin-bottom: 20px;
            text-align: center;
        }
        .sidebar .sidebar-content a {
            color: #ffffff;
            text-decoration: none;
            margin: 10px 0;
            display: block;
            padding: 10px;
            border-radius: 5px;
            transition: background-color 0.3s ease;
        }
        .sidebar .sidebar-content a:hover {
            background-color: #3e3e3e;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar implementation
with st.sidebar:
    st.markdown("""
    <div class="sidebar">
        <div class="sidebar-content">
            <h3>MahaGPT Suites</h3>
            <a href="/">Home</a>
            <a href="https://piyushmahajan.vercel.app/">About Us</a>
            <a href="https://piyushmahajan.vercel.app/project/port.html">Other Apps</a>
            <a href="https://piyushmahajan.vercel.app/contact/contact.html">Contact</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.header("🤖 MahaGPT - Your AI Chat Companion")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# User input area
input = st.text_input("Ask a question:", key="input")
submit = st.button("Send")

if submit and input:
    response = get_gemini_response(input)
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", input))
    
    st.subheader("Response")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("MahaGPT", chunk.text))

# Display chat history
if st.session_state['chat_history']:
    st.subheader("Chat History")
    chat_expander = st.expander("View previous interactions")
    with chat_expander:
        for role, text in st.session_state['chat_history']:
            if role == "You":
                st.markdown(f"**{role}**: {text}")
            else:
                st.markdown(f"**{role}**: {text}")
