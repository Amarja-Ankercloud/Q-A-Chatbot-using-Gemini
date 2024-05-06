from dotenv import load_dotenv

load_dotenv()  # loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])


def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response


# Function to apply custom styles
def apply_custom_styles():
    st.markdown("""
    <style>
    /* Background color */
    .stApp {
        background-color: #FFF8E7;
    }

    /* Customizing buttons */
    .stButton>button {
        border: 2px solid #4CAF50;
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
        cursor: pointer;
        font-size: 18px;
    }

    /* Customizing font style */
    h1, h2, .stTextInput>div>div>input, .stMarkdown {
        font-family: 'Garamond';
    }
    </style>
    """, unsafe_allow_html=True)


# initialize our streamlit app
st.set_page_config(page_title="Q&A Demo")

# Apply the custom styles for background, buttons, and fonts
apply_custom_styles()

st.header("ChatBot Application")

# Displaying an image on the side
col1, col2 = st.columns([1, 3])
with col1:
    st.image("https://jobassistant.pl/wp-content/uploads/2020/04/Chatbot.png", caption="ChatBot")


with col2:
    st.image("https://blog.snapengage.com/wp-content/uploads/2020/04/Blog-Answer-Bot.jpg", caption="Ask me anything")


# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit and input:
    response = get_gemini_response(input)
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", input))
    st.subheader("The Response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))
st.subheader("The Chat History is")

for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
