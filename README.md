# GPT-4 Turbo Chat Example with Python Flask ✨

Welcome to the GPT-4 Turbo Chat Example repository! This project showcases a simple chat application built with Python, Flask, and OpenAI's GPT-4 Turbo model. The application features user registration, login, and a chat interface where users can interact with a GPT-4 powered chatbot. 💬

## Table of Contents

- [Overview](#overview) 📝
- [Features](#features) ✨
- [Setup](#setup) ⚙️
- [Running the Application](#running-the-application) ▶️
- [Contributing](#contributing) 🤝
- [License](#license) 📄

## Overview

This project demonstrates how to create a chat application using Flask and OpenAI's GPT-4 Turbo model. The application allows users to register, log in, and send messages to the chatbot, which responds using the GPT-4 Turbo model.

## ✨ Features

- User registration and login
- Chat interface with GPT-4 Turbo chatbot
- Rate limiting to prevent abuse
- CSRF protection for secure forms
- Easy local setup and running

## ⚙️ Setup

### Prerequisites

- Python 3.7 or higher
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- OpenAI API key
- Redis (for rate limiting, optional)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/DotanVG/python-flask-gpt4o-chat-example.git
    cd python-flask-gpt4o-chat-example
    ```

2. Create a virtual environment:

    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:

    Create a `.env` file in the root directory based on the provided `.env.example` file and add your own values.

    ```plaintext
    OPENAI_API_KEY=your_openai_api_key
    SECRET_KEY=your_secret_key
    DATABASE_URL=sqlite:///chatbot.db
    REDIS_URL=redis://localhost:6379/0
    DEBUG=True
    PORT=5000
    ```

### ▶️ Running the Application

1. Run the Flask application:

    ```bash
    python app.py
    ```

2. Access the application:

    Open your browser and navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000).

## 🤝 Contributing

We welcome contributions to enhance this project! If you have any suggestions, bug reports, or feature requests, feel free to open an issue or submit a pull request.

### Steps to Contribute

1. Fork the repository.
2. Create a new branch:

    ```bash
    git checkout -b feature/your-feature-name
    ```

3. Make your changes.
4. Commit your changes:

    ```bash
    git commit -m "feat: add your feature description"
    ```

5. Push to the branch:

    ```bash
    git push origin feature/your-feature-name
    ```

6. Open a pull request.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.