from django.forms import ModelForm
from .models import Review

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields =['date', 'rating', 'comment']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)