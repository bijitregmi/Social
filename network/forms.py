from django.forms import ModelForm
from .models import Post

class NewPostForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({"class": "form-control",
                                                    "rows": 5})

    class Meta:
        model = Post
        fields = ['content']