# 📄 PDF Summarizer

A one-page web application that allows users to upload PDF files and generate AI-powered summaries with customizable parameters. Built with a Django REST backend and a Streamlit single-page frontend, it integrates the Mistral AI model for summarization, offering a scalable and user-friendly solution.

## Overview
This project fulfills the requirements of a one-page web application where users input parameters (summary type, length) to retrieve AI-generated summaries of uploaded PDFs. It includes user authentication, data persistence, and bonus features like caching and question answering, demonstrating a robust and thoughtful approach to design and scalability.

[## Demo Video

## Demo Video

[![Watch the video](https://raw.githubusercontent.com/aloksingh71/pdf-summarizer/main/Demo/pdf_Summarizer_demo.png)](https://drive.google.com/file/d/14TipbAxktOg1gKfOsibaHXUeo0SuMnbp)

## Features
- **User Authentication**: Register and log in to manage your PDFs and summaries.
- **PDF Upload**: Upload PDF files securely, stored with user-specific paths.
- **Summary Generation**: Generate summaries in bullet-point or paragraph format, with caching for performance.
- **Question Answering**: Ask questions about generated summaries, powered by AI.
- **History Management**: View and delete your summary history.
- **Robust Design**: Implements design patterns (Singleton, Factory, Strategy, Adapter, Decorator) and error handling.
 

---

##  Requirements Met

### **Backend (Django REST API)**
- **Language**: Python (Django, Django REST Framework)
- **AI Model**: Mistral AI API for **summarization** and **question answering**.
- **Data Processing**: Handles **PDF uploads**, **text extraction**, and **AI-driven insights**.

### **Frontend (Streamlit)**
- **Single-page application** with sections for **Upload, Summarization, History, and Q&A**.
- **Intuitive UI** with real-time interactions.

### **Product Requirements**
✔ **Authentication** – Ensures user-specific data storage with Django authentication.  
✔ **Customization** – Users can select **summary format** (bullet/paragraph) and **length**.  
✔ **AI-Powered Results** – Summaries & Q&A driven by **Mistral AI**.  
✔ **Performance Boosters** – **Caching**, **history tracking**, and **fast Q&A interactions**.  

---

##  Setup Instructions

### **1️⃣ Backend Setup**

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables** (⚠ Required: Add your **Mistral API Key**):
   - Create a `.env` file in the `backend/` directory and add:
     ```ini
     SECRET_KEY=your_django_secret_key
     DEBUG=True
     MISTRAL_API_KEY=your_mistral_api_key
     ```

4. **Apply database migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Run the backend server**:
   ```bash
   python manage.py runserver
   ```

---

### **2️⃣ Frontend Setup**

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Run Streamlit frontend**:
   ```bash
   streamlit run app.py
   ```

---

##  Running Tests

To execute test cases for the backend, run:
```bash
cd backend
pytest -v
```

---

##  Usage Guide

1. Open **http://localhost:8501** (default Streamlit interface).
2. **Register/Login** using your credentials.
3. **Upload a PDF**, select **summary format and length**.
4. Generate **summaries**, **view history**, or **ask questions** based on the text.

---

##  Technologies Used

- **Backend**: Django, Django REST Framework, SQLite
- **Frontend**: Streamlit
- **AI**: Mistral AI API for **summarization & question answering**
- **Testing**: Pytest, pytest-django, pytest-mock
- **Caching**: Django caching framework

---

##  Future Enhancements

🔹 **Celery-based Asynchronous Processing** – Handle larger files seamlessly.  
🔹 **Redis Integration** – Improve caching efficiency.  
🔹 **Support for DOCX & TXT Files** – Expand compatibility beyond PDFs.  
🔹 **Multi-language Summarization** – Summarization in different languages.  

---

##  GitHub Repository

🔗 **GitHub Repository**: [PDF Summarizer](https://github.com/aloksingh71/pdf-summarizer)

---

##  Additional Notes

**Designed for scalability** – Implements **design patterns** (*Singleton, Factory, Strategy*).  
**Robust error handling** – Ensures **high stability & reliability**.  
**Optimized API calls** – Improves speed & performance.  

---
 Developed by **[@aloksingh71](https://github.com/aloksingh71)**
