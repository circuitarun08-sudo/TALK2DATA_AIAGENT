import streamlit as st
from agent_orchestrator import orchestrate_content_creation

# App configuration

st.set_page_config(
    page_title="Simple Content Creation Agent 🤖",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar

st.sidebar.title("Navigate - Content Creation Agent")

page = st.sidebar.radio("Go to", ["Home", "About"])

# Home Page

if page == "Home":
    st.title("Simple Content Creation Agent 🤖")
    st.write("This is a simple content creation agent that generates content based on user input and iteratively improves it based on feedback.")

    logs = st.container()

    # User input for the topic
    user_prompt = st.text_area("Enter the topic you want to create content about:", height=150)

    if st.button("Generate Content"):
        if user_prompt.strip() == "":
            st.warning("Please enter a topic to generate content.")
        else:
            with st.spinner("Generating content..."):
                app_status = st.empty()
                orchestrate_content_creation(user_prompt, app_status=app_status)
    

# About Page

elif page == "About":
    st.title("About This App")
    st.write("""
        This app is a simple content creation agent that generates content based on user input and iteratively improves it based on feedback.
        
        **How it works:**
        1. Enter a topic in the text area on the Home page.
        2. Click the "Generate Content" button.
        3. The agent will generate content based on your input and review it.
        4. If the content quality is unsatisfactory, it will use feedback to improve the content in the next iteration.
        
        **Note:** The agent will perform a maximum of 3 iterations to improve the content quality.
    """)
    st.write("Developed by Arunprasath Suresh.")