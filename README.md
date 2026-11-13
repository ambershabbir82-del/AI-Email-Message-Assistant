# AI Email & Message Assistant

A simple web app that turns rough text into clear, professional emails and messages using AI.

Type a rough message, pick a message type and a writing tone, and get a polished version in seconds.

## Screenshot

![App screenshot](screenshot.png)

## Features

- Choose a message type (for example, Professional Email)
- Choose a writing tone: Professional, Polite or Friendly
- Generate a polished message with AI
- Copy, download, regenerate or clear the result
- Input validation (empty message, length limit of 3000 characters)
- API key stays on the server and is never exposed to the browser

## Tech Stack

- Python, Flask
- Groq API (model: `openai/gpt-oss-20b`)
- HTML, CSS, JavaScript
- python-dotenv

## Project Structure

```
app.py             Flask server and /generate route
groq_service.py    Talks to the Groq API
prompts.py         Message types, tones and prompt builder
templates/         HTML page
static/            CSS and JavaScript
requirements.txt   Python dependencies
.env.example       Sample environment file
```

## How to Run

1. Clone the repo

```
git clone https://github.com/YOUR-USERNAME/AI-Email-Message-Assistant.git
cd AI-Email-Message-Assistant
```

2. Create and activate a virtual environment

```
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies

```
pip install -r requirements.txt
```

4. Create a `.env` file (copy `.env.example`) and add your Groq API key

```
GROQ_API_KEY=your_key_here
GROQ_MODEL=openai/gpt-oss-20b
```

Get a free key from the Groq console: https://console.groq.com

5. Start the app

```
python app.py
```

6. Open `http://127.0.0.1:5000` in your browser.

## What I Learned

- Building a Flask backend with a JSON API
- Calling an AI model safely from the server
- Handling errors and retrying on connection problems
- Keeping secrets out of GitHub with `.env` and `.gitignore`

## Author

Baba
