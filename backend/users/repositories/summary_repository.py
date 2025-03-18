from ..models import Summary

class SummaryRepository:
    def save_summary(self, data):
        return Summary.objects.create(**data)

    def get_summary(self, summary_id, user):
        return Summary.objects.get(id=summary_id, uploaded_file__user=user)

    def get_user_summaries(self, user):
        return Summary.objects.filter(uploaded_file__user=user).order_by('-generated_at')

    def delete_summary(self, summary_id, user):
        try:
            summary = Summary.objects.get(id=summary_id, uploaded_file__user=user)
            summary.delete()
            return True
        except Summary.DoesNotExist:
            return False