# 🤖 Personal Research & Task Assistant AI Agent

### A Model-Native AI Agent using OpenAI Function Calling + Web Search

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge\&logo=python)
![OpenAI](https://img.shields.io/badge/OpenAI-API-green?style=for-the-badge\&logo=openai)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-red?style=for-the-badge\&logo=streamlit)
![DuckDuckGo](https://img.shields.io/badge/DuckDuckGo-Web%20Search-yellow?style=for-the-badge)

---

# 📌 Overview

This project is a **model-native AI research assistant** built using:

* OpenAI Function Calling
* DuckDuckGo Search
* Streamlit UI
* Python

The agent can:

✅ Answer questions using LLM reasoning
✅ Search the web in real-time when needed
✅ Use function calling tools dynamically
✅ Display answers in a clean Streamlit interface
✅ Run iterative reasoning loops with tool usage

---

# 🧠 Features

* 🔍 Real-time web search using DuckDuckGo
* 🤖 OpenAI function calling agent
* 🌐 Streamlit frontend
* 🔄 Multi-step reasoning loop
* 🧩 Tool orchestration architecture
* 📚 Source-aware responses
* ⚡ Lightweight and beginner-friendly

---

# 🛠️ Tech Stack

| Technology               | Purpose                          |
| ------------------------ | -------------------------------- |
| Python                   | Core programming language        |
| OpenAI API               | LLM reasoning + function calling |
| Streamlit                | Web app frontend                 |
| DuckDuckGo Search (DDGS) | Real-time web search             |
| python-dotenv            | Environment variable management  |
| JSON                     | Tool argument parsing            |

---

# 📂 Project Structure

```bash
project/
│
├── app.py
├── .env
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation Guide

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/ai-agent-project.git

cd ai-agent-project
```

---

## 2️⃣ Create a Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

---

# 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install streamlit openai python-dotenv ddgs
```

---

# 🔑 OpenAI API Setup

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Get your API key from:

https://platform.openai.com/api-keys

---

# ▶️ Running the Application

```bash
streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

---

# 🧩 How the AI Agent Works

## Step 1 — User Input

The user enters a question in Streamlit.

## Step 2 — OpenAI Agent Reasoning

The model decides whether:

* it can answer directly
* or it should call a tool

## Step 3 — Function Calling

If current information is needed:

```python
web_search(query)
```

is executed using DuckDuckGo Search.

## Step 4 — Tool Results Returned

Search results are returned to the model.

## Step 5 — Final Answer Generation

The LLM synthesizes the final response.

---

# 🔧 Core Components

## OpenAI Function Calling

```python
tools = [...]
```

## Web Search Tool

```python
def web_search(query: str, max_results: int = 5):
```

## Agent Loop

```python
while iteration < max_iterations:
```

---

# 📜 Example Queries

```text
What are the latest developments in AI agents in 2024?

Compare GPT-4 vs Claude 3 Opus for building agents

Explain what a model-native agent is
```

---

# 🚀 Future Improvements

* Memory support
* Multi-tool orchestration
* File upload support
* PDF summarization
* Vector database integration
* RAG pipelines
* Streaming responses
* Async tool execution
* Multi-agent workflows

---

# 🧪 Recommended Python Version

```text
Python 3.10+
```

---

# 📋 Example requirements.txt

```txt
streamlit
openai
python-dotenv
ddgs
```

---

# 🔐 Environment Variables

| Variable       | Description         |
| -------------- | ------------------- |
| OPENAI_API_KEY | Your OpenAI API key |

---

# 🤝 Contributing

Pull requests are welcome.

---

# 📄 License

MIT License

---

# ⭐ Support

If you found this project useful, consider giving it a star on GitHub.
