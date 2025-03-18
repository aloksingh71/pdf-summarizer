from ..models import UploadedFile

class FileRepository:
    def save_file(self, validated_data, user):
        validated_data['user'] = user
        return UploadedFile.objects.create(**validated_data)

    def get_file(self, file_id, user):
        return UploadedFile.objects.get(id=file_id, user=user)