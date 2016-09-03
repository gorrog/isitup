from django.forms import ModelForm
from .models import Submission

class SubmissionForm(ModelForm):
    class Meta:
        model = Submission
        fields = ['url', 'site_name', 'responsible_account', 'submitter_email']