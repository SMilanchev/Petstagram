from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from petstagram.common.forms import CommentForm
from petstagram.common.models import Comment
from petstagram.pets.forms import PetCreateForm, EditPetForm
from petstagram.pets.models import Pet, Like


def pet_details(req, pk):
    current_pet = Pet.objects.get(pk=pk)
    current_pet.likes_count = current_pet.like_set.count()
    liked_object_by_user = current_pet.like_set.filter(user_id=req.user.id).exists()

    is_owner = current_pet.user == req.user

    context = {
        'pet': current_pet,
        'comment_form': CommentForm(
            initial={
                'pet_pk': pk
            }
        ),
        'comments': current_pet.comment_set.all(),
        'is_owner': is_owner,
        'is_liked': liked_object_by_user,
    }

    return render(req, 'pets/pet_detail.html', context)

@login_required
def comment_pet(req, pk):
    form = CommentForm(req.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = req.user
        comment.save()

    return redirect('pet details', pk)


# def comment_pet(req, pk):
#     pet = Pet.objects.get(pk=pk)
#     form = CommentForm(req.POST)
#     if form.is_valid():
#         # check if comment is already in db:
#         # Comment.objects.filter(text=form.cleaned_data['text'])
#         comment = Comment(
#             text=form.cleaned_data['text'],
#             pet=pet,
#         )
#         comment.save()
#
#     return redirect('pet details', pet.id)


def list_pets(req):
    all_pets = Pet.objects.all()

    context = {
        'pets': all_pets,
    }
    return render(req, 'pets/pet_list.html', context)


@login_required
def like_pet(req, pk):
    pet = Pet.objects.get(pk=pk)
    liked_object_by_user = pet.like_set.filter(user_id=req.user.id).first()
    if liked_object_by_user:
        liked_object_by_user.delete()
    else:
        like = Like(
            pet=pet,
            user=req.user,
        )
        like.save()

    return redirect('pet details', pet.id)


@login_required
def create_pet(req):
    if req.method == "POST":
        form = PetCreateForm(req.POST, req.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.user = req.user
            pet.save()
            return redirect('all pets')
    else:
        form = PetCreateForm()

    context = {
        'form': form
    }
    return render(req, 'pets/pet_create.html', context)


@login_required
def edit_pet(req, pk):
    pet = Pet.objects.get(pk=pk)
    if req.method == "POST":
        form = EditPetForm(req.POST, req.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('all pets')
    else:
        form = EditPetForm(instance=pet)
    context = {
        'form': form
    }
    return render(req, 'pets/pet_edit.html', context)


@login_required
def delete_pet(req, pk):
    pet = Pet.objects.get(pk=pk)
    if req.method == "POST":
        pet.delete()
        return redirect('all pets')
    else:
        context = {
            'pet': pet
        }
        return render(req, 'pets/pet_delete.html', context)



