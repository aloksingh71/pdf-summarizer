# import streamlit as st
# import requests

# API_URL = "http://127.0.0.1:8000/api"

# if "auth_token" not in st.session_state:
#     st.session_state.auth_token = None
# if "uploaded_file_id" not in st.session_state:
#     st.session_state.uploaded_file_id = None

# def register_user(username, email, password):
#     response = requests.post(f"{API_URL}/register/", json={"username": username, "email": email, "password": password})
#     return response.json()

# def login_user(username, password):
#     response = requests.post(f"{API_URL}/login/", json={"username": username, "password": password})
#     return response.json()

# def upload_pdf(file):
#     if st.session_state.auth_token:
#         files = {"file": file}
#         headers = {"Authorization": f"Token {st.session_state.auth_token}"}
#         response = requests.post(f"{API_URL}/upload/", files=files, headers=headers)
#         return response.json()
#     st.error("❌ You must log in first.")
#     return None

# def generate_summary(file_id, summary_type, num_points=None, paragraph_length=None):
#     headers = {"Authorization": f"Token {st.session_state.auth_token}", "Content-Type": "application/json"}
#     data = {"uploaded_file_id": file_id, "summary_type": summary_type}
#     if summary_type == "bullet":
#         data["num_points"] = num_points
#     elif summary_type == "paragraph":
#         data["paragraph_length"] = paragraph_length
#     response = requests.post(f"{API_URL}/generate-summary/", json=data, headers=headers)
#     return response.json()

# def get_summary_history():
#     headers = {"Authorization": f"Token {st.session_state.auth_token}"}
#     response = requests.get(f"{API_URL}/history/", headers=headers)
#     return response.json()

# def ask_question(summary_id, question):
#     headers = {"Authorization": f"Token {st.session_state.auth_token}", "Content-Type": "application/json"}
#     data = {"summary_id": summary_id, "question": question}
#     response = requests.post(f"{API_URL}/ask-question/", json=data, headers=headers)
#     return response.json()

# def delete_summary(summary_id):
#     headers = {"Authorization": f"Token {st.session_state.auth_token}"}
#     response = requests.delete(f"{API_URL}/delete-summary/{summary_id}/", headers=headers)
#     return response.status_code == 200

# st.title("📄 AI-Powered PDF Summarizer")

# st.sidebar.title("🔑 Authentication")
# option = st.sidebar.radio("Choose an option", ["Login", "Register"])

# if option == "Register":
#     st.sidebar.subheader("Register")
#     username = st.sidebar.text_input("Username")
#     email = st.sidebar.text_input("Email")
#     password = st.sidebar.text_input("Password", type="password")
#     if st.sidebar.button("Register"):
#         result = register_user(username, email, password)
#         if "token" in result:
#             st.sidebar.success(f"✅ User registered successfully!")
#         elif "message" in result and result["message"] == "User already exists":
#             st.sidebar.info("ℹ️ User already exists. Please log in or choose a different username.")
#         else:
#             st.sidebar.error(f"❌ Registration failed: {result.get('error', 'Unknown error')}")

# if option == "Login":
#     st.sidebar.subheader("Login")
#     username = st.sidebar.text_input("Username", key="login_username")
#     password = st.sidebar.text_input("Password", type="password", key="login_password")
#     if st.sidebar.button("Login"):
#         result = login_user(username, password)
#         if "token" in result:
#             st.session_state.auth_token = result["token"]
#             st.sidebar.success("✅ Logged in successfully!")
#         else:
#             st.sidebar.error("❌ Invalid credentials.")

# if st.session_state.auth_token:
#     st.sidebar.subheader("Logout")
#     if st.sidebar.button("Logout"):
#         st.session_state.auth_token = None
#         st.session_state.uploaded_file_id = None
#         st.sidebar.success("✅ Logged out successfully.")

# if st.session_state.auth_token:
#     tab1, tab2, tab3, tab4 = st.tabs(["📤 Upload", "📃 Summarize", "📜 History", "❓ Ask Questions"])

#     with tab1:
#         st.subheader("Upload PDF")
#         uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
#         if uploaded_file and st.button("Upload"):
#             result = upload_pdf(uploaded_file)
#             if "id" in result:
#                 st.session_state.uploaded_file_id = result["id"]
#                 st.success(f"✅ Uploaded: {result['file_name']}")
#             else:
#                 st.error(f"❌ Upload failed: {result.get('error')}")

#     if st.session_state.uploaded_file_id:
#         with tab2:
#             st.subheader("Generate Summary")
#             summary_type = st.radio("Choose summary type:", ["Bullet Points", "Paragraph"])
#             if summary_type == "Bullet Points":
#                 num_points = st.slider("Number of bullet points:", min_value=1, max_value=10, value=5)
#                 summary_type_value = "bullet"
#             else:
#                 paragraph_length = st.slider("Paragraph word limit:", min_value=50, max_value=500, value=100)
#                 summary_type_value = "paragraph"

#             if st.button("Generate Summary"):
#                 response = generate_summary(
#                     file_id=st.session_state.uploaded_file_id,
#                     summary_type=summary_type_value,
#                     num_points=num_points if summary_type_value == "bullet" else None,
#                     paragraph_length=paragraph_length if summary_type_value == "paragraph" else None
#                 )
#                 if "summary_text" in response:
#                     st.subheader("📜 Summary")
#                     st.text_area("Generated Summary:", response["summary_text"], height=250)
#                 else:
#                     st.error(f"❌ Summary generation failed: {response.get('error')}")

#     with tab3:
#             st.subheader("Summary History")
#             history = get_summary_history()
#             if history:
#                 for item in history:
#                     st.write(f"**ID:** {item['id']} | **Type:** {item['summary_type']} | **Generated At:** {item['generated_at']}")
#                     st.text_area("Summary:", item["summary_text"], height=100, key=f"summary_{item['id']}")
#                     if st.button(f"❌ Delete {item['id']}", key=f"delete_{item['id']}"):
#                         if delete_summary(item["id"]):
#                             st.success("✅ Summary deleted successfully!")
#                             st.rerun()
#                         else:
#                             st.error("❌ Summary not found or already deleted.")
#                     st.divider()
#             else:
#                 st.info("📜 No summaries found.")

#     with tab4:
#         st.subheader("Ask Questions on Summary")
#         history = get_summary_history()
#         if history:
#             summary_options = {f"ID {item['id']} | {item['summary_type'].capitalize()} | {item['summary_text'][:50]}...": item["id"] for item in history}
#             selected_summary_label = st.selectbox("Select a summary:", list(summary_options.keys()))
#             selected_summary_id = summary_options[selected_summary_label]
#             question = st.text_input("Enter your question")
#             if st.button("Ask"):
#                 result = ask_question(selected_summary_id, question)
#                 if "answer" in result:
#                     st.success(f"**Answer:** {result['answer']}")
#                 else:
#                     st.error(f"❌ Failed to retrieve answer: {result.get('error')}")
#         else:
#             st.info("📜 No summaries found. Upload a file and generate a summary first.")
# else:
#     st.warning("⚠️ Please log in to continue.")

import streamlit as st
import requests

# Backend API Base URL
API_URL = "http://127.0.0.1:8000/api"

# Store authentication token
if "auth_token" not in st.session_state:
    st.session_state.auth_token = None
if "uploaded_file_id" not in st.session_state:
    st.session_state.uploaded_file_id = None

# --- Authentication Functions ---
def register_user(username, email, password):
    response = requests.post(f"{API_URL}/register/", json={"username": username, "email": email, "password": password})
    return response.json()

def login_user(username, password):
    response = requests.post(f"{API_URL}/login/", json={"username": username, "password": password})
    return response.json()

# --- File & Summary Functions ---
def upload_pdf(file):
    if st.session_state.auth_token:
        files = {"file": file}
        headers = {"Authorization": f"Token {st.session_state.auth_token}"}
        response = requests.post(f"{API_URL}/upload/", files=files, headers=headers)
        return response.json()
    st.error("You must log in first.")
    return None

def generate_summary(file_id, summary_type, num_points=None, paragraph_length=None):
    headers = {"Authorization": f"Token {st.session_state.auth_token}", "Content-Type": "application/json"}
    data = {"uploaded_file_id": file_id, "summary_type": summary_type}
    if summary_type == "bullet":
        data["num_points"] = num_points
    elif summary_type == "paragraph":
        data["paragraph_length"] = paragraph_length
    response = requests.post(f"{API_URL}/generate-summary/", json=data, headers=headers)
    return response.json()

def get_summary_history():
    headers = {"Authorization": f"Token {st.session_state.auth_token}"}
    response = requests.get(f"{API_URL}/history/", headers=headers)
    return response.json()

def ask_question(summary_id, question):
    headers = {"Authorization": f"Token {st.session_state.auth_token}", "Content-Type": "application/json"}
    data = {"summary_id": summary_id, "question": question}
    response = requests.post(f"{API_URL}/ask-question/", json=data, headers=headers)
    return response.json()

def delete_summary(summary_id):
    headers = {"Authorization": f"Token {st.session_state.auth_token}"}
    response = requests.delete(f"{API_URL}/delete-summary/{summary_id}/", headers=headers)
    return response.status_code == 200

# --- UI Starts Here ---
st.title("AI-Powered PDF Summarizer")

# Sidebar for authentication
st.sidebar.title("Authentication")
option = st.sidebar.radio("Choose an option", ["Login", "Register"])

if option == "Register":
    st.sidebar.subheader("Register")
    username = st.sidebar.text_input("Username")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Register"):
        result = register_user(username, email, password)
        if "token" in result:
            st.sidebar.success("User registered successfully!")
        elif "message" in result and result["message"] == "User already exists":
            st.sidebar.info("User already exists. Please log in or choose a different username.")
        else:
            st.sidebar.error(f"Registration failed: {result.get('error', 'Unknown error')}")

if option == "Login":
    st.sidebar.subheader("Login")
    username = st.sidebar.text_input("Username", key="login_username")
    password = st.sidebar.text_input("Password", type="password", key="login_password")
    if st.sidebar.button("Login"):
        result = login_user(username, password)
        if "token" in result:
            st.session_state.auth_token = result["token"]
            st.sidebar.success("Logged in successfully!")
        else:
            st.sidebar.error("Invalid credentials.")

if st.session_state.auth_token:
    st.sidebar.subheader("Logout")
    if st.sidebar.button("Logout"):
        st.session_state.auth_token = None
        st.session_state.uploaded_file_id = None
        st.sidebar.success("Logged out successfully.")

# --- Main UI for Authenticated Users ---
if st.session_state.auth_token:
    tab1, tab2, tab3, tab4 = st.tabs(["Upload", "Summarize", "History", "Ask Questions"])

    # Upload PDF
    with tab1:
        st.subheader("Upload PDF")
        uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
        if uploaded_file and st.button("Upload"):
            result = upload_pdf(uploaded_file)
            if "id" in result:
                st.session_state.uploaded_file_id = result["id"]
                st.success(f"Uploaded: {result['file_name']}")
            else:
                st.error(f"Upload failed: {result.get('error')}")

    # Generate Summary
    if st.session_state.uploaded_file_id:
        with tab2:
            st.subheader("Generate Summary")
            summary_type = st.radio("Choose summary type:", ["Bullet Points", "Paragraph"])
            if summary_type == "Bullet Points":
                num_points = st.slider("Number of bullet points:", min_value=1, max_value=10, value=5)
                summary_type_value = "bullet"
            else:
                paragraph_length = st.slider("Paragraph word limit:", min_value=50, max_value=500, value=100)
                summary_type_value = "paragraph"

            if st.button("Generate Summary"):
                response = generate_summary(
                    file_id=st.session_state.uploaded_file_id,
                    summary_type=summary_type_value,
                    num_points=num_points if summary_type_value == "bullet" else None,
                    paragraph_length=paragraph_length if summary_type_value == "paragraph" else None
                )
                if "summary_text" in response:
                    st.subheader("Summary")
                    st.text_area("Generated Summary:", response["summary_text"], height=250)
                else:
                    st.error(f"Summary generation failed: {response.get('error')}")

    # Summary History
    with tab3:
        st.subheader("Summary History")
        history = get_summary_history()
        if history:
            for item in history:
                st.write(f"ID: {item['id']} | Type: {item['summary_type']} | Generated At: {item['generated_at']}")
                st.text_area("Summary:", item["summary_text"], height=100, key=f"summary_{item['id']}")
                if st.button(f"Delete {item['id']}", key=f"delete_{item['id']}"):
                    if delete_summary(item["id"]):
                        st.success("Summary deleted successfully!")
                        st.rerun()
                    else:
                        st.error("Summary not found or already deleted.")
                st.divider()
        else:
            st.info("No summaries found.")

    # Ask Questions
    with tab4:
        st.subheader("Ask Questions on Summary")
        history = get_summary_history()
        if history:
            summary_options = {f"ID {item['id']} | {item['summary_type'].capitalize()} | {item['summary_text'][:50]}...": item["id"] for item in history}
            selected_summary_label = st.selectbox("Select a summary:", list(summary_options.keys()))
            selected_summary_id = summary_options[selected_summary_label]
            question = st.text_input("Enter your question")
            if st.button("Ask"):
                result = ask_question(selected_summary_id, question)
                if "answer" in result:
                    st.success(f"Answer: {result['answer']}")
                else:
                    st.error(f"Failed to retrieve answer: {result.get('error')}")
        else:
            st.info("No summaries found. Upload a file and generate a summary first.")
else:
    st.warning("Please log in to continue.")
