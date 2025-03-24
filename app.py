import streamlit as st

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Callback functions
def go_to_HR():
    st.session_state.page = 'HR'

def go_to_USER():
    st.session_state.page = 'USER'

def go_to_home():
    st.session_state.page = 'home'

# Page functions
def home_page():
    st.title("Home Page")
    st.write("Welcome to the homepage!")
    col1, col2 = st.columns(2)
    with col1:
        st.button("HR", key="btn_HR", on_click=go_to_HR)
    with col2:
        st.button("User", key="btn_USER", on_click=go_to_USER)

def HR():
    st.title("Welcome to HR Portal")
    uid = st.text_input("Enter UserID")
    if st.button("Login"):
        if uid == "1234":
            st.session_state.page = File_uploader
        else:
            st.write("Login Unsuccessful")

    st.button("Back to Home", key="btn_back1", on_click=go_to_home)
def File_uploader():
    st.title("Upload your file")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

def USER():
    st.title("Welcome to USER Portal")
    st.write("This is Page 2!")
    st.button("Back to Home", key="btn_back2", on_click=go_to_home)

# Navigation logic
def main():
    if st.session_state.page == 'home':
        home_page()
    elif st.session_state.page == 'HR':
        HR()
    elif st.session_state.page == 'File_Uploader':
        File_Uploader()
    elif st.session_state.page == 'USER':
        USER()


if __name__ == "__main__":
    main()