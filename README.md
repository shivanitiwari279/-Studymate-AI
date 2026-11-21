# AI Study Assistant

A beginner-friendly AI chatbot web application built with Flask, JavaScript, HTML, CSS, and an OpenAI-compatible chat API.

## Features

- Chat interface for study questions
- AI-generated answers through an API
- Suggested starter questions
- Loading state and basic error messages
- Clear-chat button
- Responsive layout for desktop and mobile
- API key stored in an environment file rather than browser code

## Requirements

- Python 3.10 or newer
- An API key for a supported OpenAI API account
- Internet access while using the AI feature

API usage may cost money depending on your provider/account. Check the provider's current pricing and limits before use.

## Run locally

1. Extract the ZIP file and open the project folder in VS Code.
2. Open a terminal in that folder.
3. Create a virtual environment:

   **Windows PowerShell**
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use Command Prompt:
   ```bat
   .venv\Scripts\activate.bat
   ```

4. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

5. Copy `.env.example` to a new file named `.env`.
6. Add your own API key to `.env`. Do not share or commit this file.
7. Start the app:
   ```bash
   python app.py
   ```
8. Open `http://127.0.0.1:5000` in your browser.

## Troubleshooting

- **API key not configured:** confirm that `.env` is in the same folder as `app.py` and contains a valid key.
- **API request failed:** check internet access, account access, billing/usage limits, and model availability.
- **Module not found:** activate the virtual environment and run `python -m pip install -r requirements.txt`.

## GitHub safety

Never commit `.env` or publish your API key. The `.gitignore` file excludes `.env` by default. If a key is accidentally exposed, revoke it and create a new one.

## Before adding this project to a resume

Run the application, test successful and failed requests, understand the Python route and JavaScript `fetch()` call, and make any improvements you can explain in an interview. Describe only the features you personally verified.
