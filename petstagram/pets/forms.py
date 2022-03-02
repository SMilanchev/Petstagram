import os
from os import path

from django.conf import settings
from django import forms

from petstagram.core.forms import BootstrapFormMixin
from petstagram.pets.models import Pet


class PetCreateForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Pet
        exclude = ('user', )


class EditPetForm(PetCreateForm):
    def save(self, commit=True):
        db_pet = Pet.objects.get(pk=self.instance.id)
        if commit:
            # head = str(settings.MEDIA_ROOT).replace('\\', '/') + '/'
            head = settings.MEDIA_ROOT
            tail = str(db_pet.image)
            image_path = path.join(head, tail)
            os.remove(image_path)

        return super().save(commit)

    class Meta:
        model = Pet
        fields = '__all__'

        widgets = {
            'type': forms.TextInput(
                attrs={
                    'readonly': 'readonly',
                }
            )
        }


