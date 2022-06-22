from django.shortcuts import render

# Create your views here.

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from cats.models import Breed, Cat

# We comment the autos.forms because it is not needed, we are gonna use
# generic forms that are class based already present in Django.
# from autos.forms import MakeForm

# Create your views here.

# THE MAINVIEW is gonna be "CatList" and it has some caviats,
# check it below at the end!

class BreedList(LoginRequiredMixin, View): #,View):
    def get(self, request):
        ml = Breed.objects.all()
        ctx = {'breed_list': ml}
        return render(request, 'cats/breed_list.html', ctx)

# We use reverse_lazy() because we are in "constructor attribute" code
# that is run before urls.py is completely loaded
class BreedCreate(LoginRequiredMixin, CreateView): #,View):
    # This code will not be used, is function based and more manual.
    # We replace it with class based like in the Autos examples below
    # which only needs some parameters
    # template = 'autos/make_form.html'
    # success_url = reverse_lazy('autos:all')

    # def get(self, request):
    #     form = MakeForm()
    #     ctx = {'form': form}
    #     return render(request, self.template, ctx)

    # def post(self, request):
    #     form = MakeForm(request.POST)
    #     if not form.is_valid():
    #         ctx = {'form': form}
    #         return render(request, self.template, ctx)

    #     make = form.save()
    #     return redirect(self.success_url)

    model = Breed
    fields = '__all__'
    success_url = reverse_lazy('cats:all')


# MakeUpdate has code to implement the get/post/validate/store flow
# AutoUpdate (below) is doing the same thing with no code
# and no form by extending UpdateView
class BreedUpdate(LoginRequiredMixin, UpdateView):
    # model = Make
    # success_url = reverse_lazy('autos:all')
    # template = 'autos/make_form.html'

    # def get(self, request, pk):
    #     make = get_object_or_404(self.model, pk=pk)
    #     form = MakeForm(instance=make)
    #     ctx = {'form': form}
    #     return render(request, self.template, ctx)

    # def post(self, request, pk):
    #     make = get_object_or_404(self.model, pk=pk)
    #     form = MakeForm(request.POST, instance=make)
    #     if not form.is_valid():
    #         ctx = {'form': form}
    #         return render(request, self.template, ctx)

    #     form.save()
    #     return redirect(self.success_url)

    model = Breed
    fields = '__all__'
    success_url = reverse_lazy('cats:all')


class BreedDelete(LoginRequiredMixin, DeleteView):
    # model = Make
    # success_url = reverse_lazy('autos:all')
    # template = 'autos/make_confirm_delete.html'

    # def get(self, request, pk):
    #     make = get_object_or_404(self.model, pk=pk)
    #     form = MakeForm(instance=make)
    #     ctx = {'make': make}
    #     return render(request, self.template, ctx)

    # def post(self, request, pk):
    #     make = get_object_or_404(self.model, pk=pk)
    #     make.delete()
    #     return redirect(self.success_url)

    model = Breed
    fields = '__all__'
    success_url = reverse_lazy('cats:all')


# Take the easy way out on the main table
# These views do not need a form because CreateView, etc.
# Build a form object dynamically based on the fields
# value in the constructor attributes

# class CatList(LoginRequiredMixin, ListView):
#     model = Cat
#     fields = '__all__'
#     success_url = reverse_lazy('cats:all')

class CatList(LoginRequiredMixin, View): #,View):
    def get(self, request):
        ml = Cat.objects.all()

        # We need to add a variable with a method that counts the breeds
        # in the CatList view which is the mainview.
        # We'll call it bc, and add it to the ctx dictionary so we can use
        # it as a "variable" in the html templates.
        bc= Breed.objects.all().count()
        # We add this functions to the ctx dictionary
        ctx = {'cat_list': ml, 'breed_count': bc}
        return render(request, 'cats/cat_list.html', ctx)

class CatCreate(LoginRequiredMixin, CreateView):
    model = Cat
    fields = '__all__'
    success_url = reverse_lazy('cats:all')


class CatUpdate(LoginRequiredMixin, UpdateView):
    model = Cat
    fields = '__all__'
    success_url = reverse_lazy('cats:all')


class CatDelete(LoginRequiredMixin, DeleteView):
    model = Cat
    fields = '__all__'
    success_url = reverse_lazy('cats:all')

# We use reverse_lazy rather than reverse in the class attributes
# because views.py is loaded by urls.py and in urls.py as_view() causes
# the constructor for the view class to run before urls.py has been
# completely loaded and urlpatterns has been processed.

# References

# https://docs.djangoproject.com/en/3.0/ref/class-based-views/generic-editing/#createview