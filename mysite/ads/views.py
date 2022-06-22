from ads.models import Ad
from ads.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView

#All this new imports for Django4w2
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from ads.forms import CreateForm, CommentForm
from ads.models import Comment
from django.urls import reverse

# Django4w5 for search bar
from django.db.models import Q
from django.contrib.humanize.templatetags.humanize import naturaltime

#New List view for Django4w4 based on ThingsListView from favs app
class AdListView(OwnerListView):
    model = Ad
    template_name = "ads/ad_list.html"

    #We'll override the get request
    def get(self, request) :

        #This part will add the favorite stars, Django4w4
        ad_list = Ad.objects.all()
        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            rows = request.user.favorite_ads.values('id')
            # favorites = [2, 4, ...] using list comprehension
            favorites = [ row['id'] for row in rows ]
        # ctx = {'ad_list' : ad_list, 'favorites': favorites}

        # Django4w5 We'all ad the functionality of a the SEARCH BAR here
        # We also adiotionally add the "updated at" time using naturaltime django extension.
        # strval stands for some "string value"
        strval =  request.GET.get("search", False)
        if strval :
            # Simple title-only search
            # objects = Post.objects.filter(title__contains=strval).select_related().order_by('-updated_at')[:10]

            # Multi-field search
            # __icontains for case-insensitive search
            query = Q(title__icontains=strval)
            query.add(Q(text__icontains=strval), Q.OR)

            # VER REFERENCIAS AL TERMINO DE LA CLASE sobre todo la del "OR"
            # Django4w5 we add "tags" as search criteria!
            # the problems is that tags is a list, we need a "__" method to make django look into
            # every item of the list, that's __name__in , and for some weird reason the string between brackets...
            query.add(Q(tags__name__in=[strval]), Q.OR)

            #AND for SOME odd reason, well not that add, we need more filtering, with the distinct() method
            # which is like the "unique" from numpy, the result can fullfill the 3 criteria at the same time
            # and can appear up to 3 times!
            ad_list = Ad.objects.filter(query).select_related().distinct().order_by('-updated_at')[:10]

        else :
            ad_list = Ad.objects.all().order_by('-updated_at')[:10]

        # Augment the post_list
        for obj in ad_list:
            obj.natural_updated = naturaltime(obj.updated_at)

        #Finally the whole ctx or context
        ctx = {'ad_list' : ad_list, 'favorites': favorites}
        return render(request, self.template_name, ctx)
# References

# https://docs.djangoproject.com/en/3.0/topics/db/queries/#one-to-many-relationships

# Note that the select_related() QuerySet method recursively prepopulates the
# cache of all one-to-many relationships ahead of time.

# sql “LIKE” equivalent in django query
# https://stackoverflow.com/questions/18140838/sql-like-equivalent-in-django-query

# How do I do an OR filter in a Django query?
# https://stackoverflow.com/questions/739776/how-do-i-do-an-or-filter-in-a-django-query

# https://stackoverflow.com/questions/1074212/how-can-i-see-the-raw-sql-queries-django-is-running

# class AdListView(OwnerListView):
#     model = Ad
#     # By convention:
#     # template_name = "ads/article_list.html"

#New detail view for Django4w2
class AdDetailView(OwnerDetailView):
    model = Ad
    template_name = "ads/ad_detail.html"
    def get(self, request, pk) :
        x = Ad.objects.get(id=pk)
        comments = Comment.objects.filter(ad=x).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'ad' : x, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)

# class AdDetailView(OwnerDetailView):
#     model = Ad

#We change CreateView for Django4w2
class AdCreateView(LoginRequiredMixin, View):
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:all')

    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        ad = form.save(commit=False)
        ad.owner = self.request.user
        ad.save()
        form.save_m2m() # Line to save the "tags" that are manage by external library
        return redirect(self.success_url)

# class AdCreateView(OwnerCreateView):
#     model = Ad
#     fields = ['title', 'text', 'price']

# New updateview for Django4w2
class AdUpdateView(LoginRequiredMixin, View):
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:all')

    def get(self, request, pk):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(instance=ad)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=ad)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        ad = form.save(commit=False)
        ad.save()
        form.save_m2m() # Line to save the "tags" that are manage by external library

        return redirect(self.success_url)

#Old updateView
# class AdUpdateView(OwnerUpdateView):
#     model = Ad
#     fields = ['title', 'text', 'price']


class AdDeleteView(OwnerDeleteView):
    model = Ad

# New Comment Create and delete views for Django4w2

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        f = get_object_or_404(Ad, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, ad=f)
        comment.save()
        return redirect(reverse('ads:ad_detail', args=[pk]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "ads/comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        ad = self.object.ad
        return reverse('ads:ad_detail', args=[ad.id])

# New Favorite views for Django4w4
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError
from ads.models import Fav

@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Add PK",pk)
        t = get_object_or_404(Ad, id=pk)
        fav = Fav(user=request.user, ad=t)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Delete PK",pk)
        t = get_object_or_404(Ad, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, ad=t).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()


# New stream file for Django4w2
from django.http import HttpResponse
from ads.models import Ad

def stream_file(request, pk):
    ad = get_object_or_404(Ad, id=pk)
    response = HttpResponse()
    response['Content-Type'] = ad.content_type
    response['Content-Length'] = len(ad.picture)
    response.write(ad.picture)
    return response
