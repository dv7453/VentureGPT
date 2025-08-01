# app.py

import streamlit as st
import json
import os
from dotenv import load_dotenv
from langchain.llms import OpenAI  # Replace with Groq if using it
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# Load environment variables
# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

from langchain_groq import ChatGroq

llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0.0,
    max_retries=2,
    api_key=GROQ_API_KEY,
)
# Initialize conversation memory
memory = ConversationBufferMemory(memory_key="history", return_messages=True)

# Set up conversation chain with memory
conversation = ConversationChain(llm=llm, memory=memory, verbose=False)


# Function to load the comprehensive report
@st.cache_data(show_spinner=False)
def load_report(idea_id: str) -> str:
    try:
        with open("storage/data.json", "r") as f:
            storage_data = json.load(f)
        report = storage_data.get(idea_id, {}).get("ComprehensiveReport", None)
        if report:
            return report
        else:
            st.error(f"No report found for idea_id: {idea_id}")
            return None
    except Exception as e:
        st.error(f"Error loading report: {e}")
        return None


# Initialize Streamlit app
st.set_page_config(page_title="StartupGPT Report & Chatbot", layout="wide")
st.title("📊 Comprehensive StartupGPT Report & Chatbot")

# Sidebar for user input
st.sidebar.header("Report Selection")
idea_id = st.sidebar.text_input("Enter Idea ID", value="idea_007")

# Load and display the report
report = load_report(idea_id)

if report:
    st.header("Comprehensive StartupGPT Report")

    # Format and display the report as Markdown text
    st.markdown("### Report Overview\n")
    st.markdown(report, unsafe_allow_html=True)

    # Chat interface
    st.header("💬 Ask Questions About the Report")
    user_question = st.text_input("Enter your question here:")

    if st.button("Get Answer"):
        if user_question.strip() == "":
            st.warning("Please enter a valid question.")
        else:
            with st.spinner("Generating answer..."):
                # Generate the answer based on the user question
                answer = conversation.run(input=user_question)

                # Display the answer
                st.success("**Answer:**")
                st.write(answer)