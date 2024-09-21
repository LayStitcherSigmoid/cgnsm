from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.

class Administrarion(AbstractUser):

    pass

    def __str__(self):
        return self.username

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()


class Pragmon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_created = models.ForeignKey(Administrarion, on_delete=models.RESTRICT, related_name="user_created")
    user_last_updated = models.ForeignKey(Administrarion, on_delete=models.RESTRICT, related_name="user_last_updated")
    time_created = models.DateTimeField(auto_now_add=True)
    time_last_updated = models.DateTimeField(auto_now=True)
    ip_created = models.GenericIPAddressField()
    ip_last_updated = models.GenericIPAddressField()
    is_active = models.BooleanField()


class Ontologion(Pragmon):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class OntologicalRelationType(Pragmon):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


class OntologicalRelation(Pragmon):
    kind = models.ForeignKey(OntologicalRelationType, on_delete=models.RESTRICT)
    source = models.ForeignKey(Ontologion, on_delete=models.RESTRICT, related_name="source")
    target = models.ForeignKey(Ontologion, on_delete=models.RESTRICT)

    class Meta:
        unique_together = ('source', 'target', 'kind')  # Ensure unique relation types between source and target

    def __str__(self):
        return f"{self.source} - {self.kind} -> {self.target}"
