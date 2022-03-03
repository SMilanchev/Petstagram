from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from petstagram.common.forms import CommentForm
from petstagram.common.models import Comment
from petstagram.pets.forms import PetCreateForm, EditPetForm
from petstagram.pets.models import Pet, Like


class CreatePetView(LoginRequiredMixin, CreateView):
    form_class = PetCreateForm
    template_name = 'pets/pet_create.html'
    success_url = reverse_lazy('all pets')

    def form_valid(self, form):
        pet = form.save(commit=False)
        pet.user = self.request.user
        pet.save()
        return super().form_valid(form)


class ListPetsView(ListView):
    template_name = 'pets/pet_list.html'
    model = Pet
    context_object_name = 'pets'


class PetDetailsView(DetailView):
    model = Pet
    template_name = 'pets/pet_detail.html'
    context_object_name = 'pet'

    def get_context_data(self, **kwargs):
        result = super().get_context_data(**kwargs)
        self.object.likes_count = self.object.like_set.count()
        result['is_liked'] = self.object.like_set.filter(user_id=self.request.user.id).exists()
        result['is_owner'] = self.object.user == self.request.user
        result['comment_form'] = CommentForm(initial={'pet_pk': self.object.pk})
        result['comments'] = self.object.comment_set.all()
        return result


class UpdatePetView(LoginRequiredMixin, UpdateView):
    model = Pet
    form_class = EditPetForm
    template_name = 'pets/pet_edit.html'
    success_url = reverse_lazy('all pets')


class CommentPetView(LoginRequiredMixin, View):
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        pet = Pet.objects.get(pk=self.kwargs['pk'])
        comment = Comment(
            text=form.cleaned_data['text'],
            pet=pet,
            user=self.request.user
        )

        comment.save()

        return redirect('pet details', pet.id)

    def form_invalid(self, form):
        pass


class LikePetView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pet = Pet.objects.get(pk=self.kwargs['pk'])
        liked_object_by_user = pet.like_set.filter(user_id=self.request.user.id).first()
        if liked_object_by_user:
            liked_object_by_user.delete()
        else:
            like = Like(
                pet=pet,
                user=self.request.user,
            )
            like.save()
        return redirect('pet details', pet.id)


class DeletePetView(LoginRequiredMixin, DeleteView):
    model = Pet
    success_url = reverse_lazy('all pets')
    template_name = 'pets/pet_delete.html'
