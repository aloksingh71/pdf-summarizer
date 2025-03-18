import pytest
import os
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .models import UploadedFile, Summary
from .services.auth_service import AuthService
from .services.file_service import FileService
from .services.summary_service import SummaryService
from .repositories.file_repository import FileRepository
from .repositories.summary_repository import SummaryRepository
from django.core.files.uploadedfile import SimpleUploadedFile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # backend/users/

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="testpass", email="test@example.com")

@pytest.fixture
def auth_token(user):
    token, _ = Token.objects.get_or_create(user=user)
    return token.key

@pytest.fixture
def test_pdf_file():
    pdf_path = BASE_DIR / "test Input" / "testFile.pdf"
    if not pdf_path.exists():
        pytest.skip("Test PDF file not found")
    with open(pdf_path, "rb") as f:
        return SimpleUploadedFile("test.pdf", f.read(), content_type="application/pdf")

@pytest.fixture
def uploaded_file(user, test_pdf_file):
    return UploadedFile.objects.create(user=user, file=test_pdf_file, file_name="test.pdf")

@pytest.fixture
def summary(uploaded_file):
    return Summary.objects.create(
        uploaded_file=uploaded_file,
        summary_type="paragraph",
        paragraph_length=100,
        summary_text="Test summary"
    )

# Test Registration
@pytest.mark.django_db
def test_register_new_user(api_client):
    response = api_client.post("/api/register/", {
        "username": "newuser",
        "password": "newpass",
        "email": "new@example.com"
    }, format="json")
    assert response.status_code == 201
    assert "token" in response.data
    assert User.objects.filter(username="newuser").exists()

@pytest.mark.django_db
def test_register_existing_user(api_client, user):
    response = api_client.post("/api/register/", {
        "username": "testuser",
        "password": "testpass",
        "email": "test@example.com"
    }, format="json")
    assert response.status_code == 200
    assert response.data["message"] == "User already exists"

# Test Login
@pytest.mark.django_db
def test_login(api_client, user):
    response = api_client.post("/api/login/", {
        "username": "testuser",
        "password": "testpass"
    }, format="json")
    assert response.status_code == 200
    assert "token" in response.data

# Test File Upload
@pytest.mark.django_db
def test_upload_file(api_client, auth_token, test_pdf_file):
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {auth_token}")
    response = api_client.post("/api/upload/", {"file": test_pdf_file}, format="multipart")
    assert response.status_code == 201
    assert "id" in response.data
    assert UploadedFile.objects.filter(file_name="test.pdf").exists()

# Test Generate Summary
@pytest.mark.django_db
def test_generate_summary(api_client, auth_token, uploaded_file, mocker):
    mocker.patch("users.utils.pdf_utils.extract_text_from_pdf", return_value="Sample text from PDF")
    mocker.patch("users.utils.mistral_client.MistralClient.summarize", return_value="Summary text")
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {auth_token}")
    response = api_client.post("/api/generate-summary/", {
        "uploaded_file_id": uploaded_file.id,
        "summary_type": "paragraph",
        "paragraph_length": 100
    }, format="json")
    assert response.status_code == 201
    assert "summary_text" in response.data
    assert response.data["summary_text"] == "Summary text"

# Test Ask Question
@pytest.mark.django_db
def test_ask_question(api_client, auth_token, summary, mocker):
    mocker.patch("users.utils.mistral_client.MistralClient.answer_question", return_value="Test answer")
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {auth_token}")
    response = api_client.post("/api/ask-question/", {
        "summary_id": summary.id,
        "question": "What is this about?"
    }, format="json")
    assert response.status_code == 200
    assert "answer" in response.data
    assert response.data["answer"] == "Test answer"

# Test History Retrieval
@pytest.mark.django_db
def test_get_history(api_client, auth_token, summary):
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {auth_token}")
    response = api_client.get("/api/history/")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["id"] == summary.id

# Test Delete Summary
@pytest.mark.django_db
def test_delete_summary(api_client, auth_token, summary):
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {auth_token}")
    response = api_client.delete(f"/api/delete-summary/{summary.id}/")
    assert response.status_code == 200
    assert response.data["message"] == "Summary deleted successfully"
    assert not Summary.objects.filter(id=summary.id).exists()

#Test Non Existent summary
@pytest.mark.django_db
def test_delete_nonexistent_summary(api_client, auth_token):
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {auth_token}")
    response = api_client.delete("/api/delete-summary/999/")
    assert response.status_code == 404
    assert response.data["error"] == "Summary not found or already deleted"


#Test Summary from Cache
import time

@pytest.mark.django_db
def test_generate_summary_with_cache(api_client, auth_token, uploaded_file, mocker):
    from django.core.cache import cache
    
    cache.clear()
    
    mocker.patch("users.utils.pdf_utils.extract_text_from_pdf", return_value="Sample text from PDF")
    mocker.patch("users.utils.mistral_client.MistralClient.summarize", return_value="Cached summary text")
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {auth_token}")
    
    # First call: Measure time with cache miss
    start_time = time.time()
    response1 = api_client.post("/api/generate-summary/", {
        "uploaded_file_id": uploaded_file.id,
        "summary_type": "paragraph",
        "paragraph_length": 100
    }, format="json")
    duration1 = time.time() - start_time
    print(f"First call (cache miss): {duration1:.4f} seconds")
    assert response1.status_code == 201
    assert response1.data["summary_text"] == "Cached summary text"
    
    # Second call: Measure time with cache hit
    mocker.patch("users.utils.mistral_client.MistralClient.summarize", side_effect=Exception("Should not be called"))
    start_time = time.time()
    response2 = api_client.post("/api/generate-summary/", {
        "uploaded_file_id": uploaded_file.id,
        "summary_type": "paragraph",
        "paragraph_length": 100
    }, format="json")
    duration2 = time.time() - start_time
    print(f"Second call (cache hit): {duration2:.4f} seconds")
    assert response2.status_code == 201
    assert response2.data["summary_text"] == "Cached summary text"