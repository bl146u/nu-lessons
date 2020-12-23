from uuid import uuid4
from django.urls import reverse
from django.conf import settings
from django.views.generic import FormView
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile

from apps.plugins import ml
from apps.lessons import forms as lessons_forms


class T74View(FormView):
    form_class = lessons_forms.T74Form
    template_name = "lessons/t74.html"

    def _upload_image(self, image: InMemoryUploadedFile) -> str:
        image_uuid = uuid4()
        image_name = f"{image_uuid}.jpg"
        default_storage.save(image_name, ContentFile(image.read()))
        return str(image_uuid)

    def _predict(self, image_path) -> tuple:
        return ml.digits_model.predict(image_path)

    def get_success_url(self):
        image_uuid = self._upload_image(self.request.FILES.get("image"))
        return reverse("apps_lessons:t74_uuid", kwargs={"uuid": image_uuid})

    def get(self, request, *args, **kwargs):
        try:
            image_url = kwargs.get("uuid")
            history, digit = self._predict(image_url)
            self.extra_context = {
                "history": history,
                "digit": digit,
                "image_url": f"{settings.MEDIA_URL}{image_url}.jpg",
            }
        except:
            pass
        return super().get(request, *args, **kwargs)
