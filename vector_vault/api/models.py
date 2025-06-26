import uuid


from django.contrib.auth import get_user_model
from django.db import models

from pgvector.django import CosineDistance, VectorField
from sentence_transformers import SentenceTransformer

# TODO: Create a utility command to download model files
try:
    T = SentenceTransformer("./ml_models/distiluse-base-multilingual-cased-v1")
except:
    T = SentenceTransformer("distiluse-base-multilingual-cased-v1")
    T.save("./ml_models/distiluse-base-multilingual-cased-v1")


class Book(models.Model):
    """
    Stores names along with their phonetic representations and embeddings.
    """

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=1000, help_text="Book Title")

    embedding = VectorField(dimensions=512, editable=False)

    def save(self, *args, **kwargs):
        self.embedding = T.encode(self.title)
        super().save(*args, **kwargs)

    @classmethod
    def search(cls, q, dmax=0.5):
        distance = CosineDistance("embedding", T.encode(q))
        return cls.objects.alias(distance=distance).filter(distance__lt=dmax).order_by(distance)

    def __str__(self):
        return self.title
