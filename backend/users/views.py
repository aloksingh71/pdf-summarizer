from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import UserSerializer, UploadedFileSerializer, SummarySerializer, QuestionAnswerSerializer
from .services.auth_service import AuthService
from .services.file_service import FileService
from .services.summary_service import SummaryService
from .utils.exceptions import SummarizationError, FileProcessingError, TextExtractionError, APIRequestError
from rest_framework.generics import ListAPIView

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        auth_service = AuthService()
        return auth_service.register(request.data)

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        auth_service = AuthService()
        return auth_service.login(request.data)

class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        file_service = FileService()
        file_instance = file_service.upload_file(request.data, request.FILES, request.user)
        return Response(UploadedFileSerializer(file_instance).data, status=status.HTTP_201_CREATED)

class GenerateSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        summary_service = SummaryService()
        try:
            summary = summary_service.generate_summary(
                uploaded_file_id=request.data.get("uploaded_file_id"),
                user=request.user,
                summary_type=request.data.get("summary_type", "paragraph"),
                num_points=request.data.get("num_points", 5),
                paragraph_length=request.data.get("paragraph_length", 100)
            )
            return Response(SummarySerializer(summary).data, status=status.HTTP_201_CREATED)
        except FileProcessingError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except TextExtractionError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except APIRequestError as e:
            return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except SummarizationError as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AskQuestionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        summary_service = SummaryService()
        try:
            result = summary_service.answer_question(
                summary_id=request.data.get("summary_id"),
                user=request.user,
                question=request.data.get("question")
            )
            return Response(result, status=status.HTTP_200_OK)
        except SummarizationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HistoryView(ListAPIView):
    serializer_class = SummarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        from .repositories.summary_repository import SummaryRepository
        repo = SummaryRepository()
        return repo.get_user_summaries(self.request.user)

class DeleteSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, summary_id, *args, **kwargs):
        from .repositories.summary_repository import SummaryRepository
        repo = SummaryRepository()
        success = repo.delete_summary(summary_id, request.user)
        if success:
            return Response({'message': 'Summary deleted successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'Summary not found or already deleted'}, status=status.HTTP_404_NOT_FOUND)