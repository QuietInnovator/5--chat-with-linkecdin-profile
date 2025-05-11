import streamlit as st
from streamlit_chat import message as chat_message
import openai

from utils.pdf_utils import extract_text_from_pdf
from utils.chat_utils import chat_with_openai_stream, create_system_prompt
from config import NAME, PAGE_TITLE, PAGE_DESCRIPTION

# Set your OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

def initialize_session_state():
    """Initialize session state variables."""
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'system_prompt' not in st.session_state:
        st.session_state.system_prompt = ""

def display_profile_info(pdf_text, summary_text):
    """Display the profile and summary information."""
    st.subheader("PDF Profile Information")
    st.text_area("Profile Text", pdf_text, height=300)

    st.subheader("Summary")
    st.text_area("Summary Text", summary_text, height=150)

def handle_chat_interaction():
    """Handle the chat interaction with the user."""
    st.subheader(f"Chat with {NAME}")

    user_message = st.chat_input("Ask a question about Chadi's background...")
    if user_message:
        st.session_state.history.append({"role": "user", "content": user_message})
        with st.chat_message("user"):
            st.markdown(user_message)

        response_text = ""
        with st.chat_message("assistant"):
            response_container = st.empty()
            for chunk in chat_with_openai_stream(
                st.session_state.system_prompt,
                user_message,
                st.session_state.history
            ):
                if chunk.choices and chunk.choices[0].delta:
                    delta = chunk.choices[0].delta.content or ""
                    response_text += delta
                    response_container.markdown(response_text + "▌")
            response_container.markdown(response_text)

        st.session_state.history.append({"role": "assistant", "content": response_text})

    # Display chat history
    for message in st.session_state.history:
        if message['role'] == 'user':
            chat_message(message['content'], is_user=True)
        else:
            chat_message(message['content'])

def main():
    """Main application function."""
    st.title(PAGE_TITLE)
    st.markdown(PAGE_DESCRIPTION)

    initialize_session_state()

    pdf_file = st.file_uploader("Upload PDF Profile", type="pdf")
    txt_file = st.file_uploader("Upload Summary Text", type="txt")

    if st.button("Display Profile"):
        if pdf_file is None or txt_file is None:
            st.error("Please upload both PDF and summary text files.")
        else:
            with st.spinner("Extracting information..."):
                pdf_text = extract_text_from_pdf(pdf_file)
                summary_text = txt_file.read().decode("utf-8")

            st.success("Profile extracted successfully!")
            display_profile_info(pdf_text, summary_text)
            
            # Set up the system prompt
            st.session_state.system_prompt = create_system_prompt(
                NAME,
                summary_text,
                pdf_text
            )

    # Handle chat interaction if system prompt is set
    if st.session_state.system_prompt:
        handle_chat_interaction()

if __name__ == "__main__":
    main()
