from ..serializers import UploadedFileSerializer
from ..repositories.file_repository import FileRepository

class FileService:
    def upload_file(self, data, files, user):
        data = data.copy()
        data['file_name'] = files['file'].name
        serializer = UploadedFileSerializer(data=data, context={'request': None})
        if serializer.is_valid():
            repo = FileRepository()
            return repo.save_file(serializer.validated_data, user)
        raise ValueError(serializer.errors)