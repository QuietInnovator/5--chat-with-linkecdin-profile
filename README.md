# PDF Profile Chat Application

This Streamlit application allows users to upload a PDF profile and a summary text file, then chat with an AI that represents the person in the profile.

## Features

- PDF profile upload and text extraction
- Summary text file upload
- Interactive chat interface with AI
- Streaming responses for better user experience

## Project Structure

```
.
├── app.py              # Main application file
├── config.py           # Configuration settings
├── requirements.txt    # Project dependencies
└── utils/
    ├── pdf_utils.py    # PDF processing utilities
    └── chat_utils.py   # Chat-related utilities
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your OpenAI API key in Streamlit secrets:
   - Create a `.streamlit/secrets.toml` file
   - Add your API key: `OPENAI_API_KEY = "your-api-key"`

3. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Upload a PDF profile file
2. Upload a summary text file
3. Click "Display Profile" to process the files
4. Start chatting with the AI representation of the profile 