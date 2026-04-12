# 📬 National Institute of Applied Science and Technology Academic Mail Checker

> **An AI-powered Gmail orchestrator designed for INSAT students to prioritize what matters.**

**Daily Mail Checker** is a Python-based automation tool that monitors your Gmail inbox for urgent academic updates. Using the **Gemini 2.5 Flash** model, it analyzes unread emails to detect "Rattrapage," "DS," "TP," and "Exams," providing a concise summary and urgency score so you can focus on your studies instead of your inbox.

---

## ✨ Features

- **Intelligent Triage:** Automatically detects academic keywords like `TD`, `DS`, `Exam`, and `Rattrapage`.
- **AI-Powered Summarization:** Groups up to 10 emails into a single, readable executive summary using Gemini.
- **Efficient Metadata Parsing:** Uses `format='metadata'` to fetch only essential headers (Sender, Subject, Snippet), minimizing data usage.
- **Security Minded:** Implements `.env` for API keys and `token.pickle` for session management to keep your credentials safe.

---

## 🛠️ Prerequisites

### 1. Google Cloud Credentials (`credentials.json`)
To allow the script to talk to your Gmail account:
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project named "nameasyoulike".
3. In **APIs & Services > Library**, search for "Gmail API" and click **Enable**.
4. Go to **APIs & Services > OAuth consent screen**, choose "External", and add your email as a **Test User**.
5. Go to **APIs & Services > Credentials**, click **Create Credentials > OAuth client ID**.
6. Select **Desktop App**, name it, and click **Create**.
7. Download the JSON file, rename it to `credentials.json`, and move it to your project root folder.

### 2. Gemini API Key
To power the AI summarization:
1. Visit [Google AI Studio](https://aistudio.google.com/).
2. Click on **"Get API key"** in the sidebar.
3. Click **"Create API key in new project"**.
4. Copy your key (you will need it for the `.env` file below).

---

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   cd <your-working-directory>
   git clone <repo-url>
2. **Install Dependencies**
    Ensure you have Python installed, then run the following to install all required Google and AI libraries:
    ```bash
    pip install -r requirements.txt
3. **Configure Environment Variables**
    The script uses a .env file to keep your API keys secure.
   
      1.Create a file named .env in the root directory.

      2.Paste the following inside:

            GEMINI_API_KEY=your_copied_api_key_here

## 🏃 Usage
Once your `credentials.json` is in the folder and your `.env` is set up:
1. **Run the Orchestrator:**
   ```bash
   python main.py
2. **First-Run Authentication**

   On your first execution, a Google sign-in page will open in your browser.


   Log in with your INSAT/Student account to grant the script permission to read your emails.


   This will create a token.pickle file for future use.
3. **Output**

   The script will scan for unread messages, batch them,

 
   and print an AI-generated summary of your academic priorities directly to the terminal.
