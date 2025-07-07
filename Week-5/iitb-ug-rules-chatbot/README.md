# 🎓 IIT Bombay UG Academic Rules Chatbot

This project is a conversational AI assistant designed to help IIT Bombay students with queries about the undergraduate academic rules and circulars.

It uses **Gemini 1.5 Flash** combined with Retrieval-Augmented Generation (RAG) to fetch relevant excerpts from the UG rulebook and generate clear, student-friendly answers.

---

## 🚀 Features

✅ Upload UG Rulebook PDFs  
✅ Retrieve relevant sections automatically  
✅ Conversational memory for contextual Q&A  
✅ Deployed using Streamlit  

---

## 🌐 Live Demo

👉 [View the deployed app](https://your-app-url.streamlit.app)

---

## 📸 Demo

![Chatbot Demo](demo/demo.gif)

---

## 🛠️ Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/iitb-ug-rules-chatbot.git
cd iitb-ug-rules-chatbot
```

Install Dependencies:

```bash
pip install -r requirements.txt
```

Create a .env file in the project root with your API key:

```bash
GOOGLE_API_KEY=your_api_key_here
```

Run the Streamlit app:

```bash
streamlit run rulechat.py
```


