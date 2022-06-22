from django.urls import path

from . import views

# We need to add the app_name so it's templates
# won't get confused with the ones of other apps when
# we use {% url %}
app_name = 'polls'

# Old views, by hand (not using generic views from django
# urlpatterns = [
#     # ex: /polls/
#     path('', views.index, name='index'),
#     # ex: /polls/5/
#     path('<int:question_id>/', views.detail, name='detail'),
#     # ex: /polls/5/results/
#     path('<int:question_id>/results/', views.results, name='results'),
#     # ex: /polls/5/vote/
#     path('<int:question_id>/vote/', views.vote, name='vote'),

#     #Path to the assignment line for autograding
#     path('owner', views.owner, name='owner'),

#     #Path to Django tutorial 4 new form#
#     path('<int:question_id>/vote/', views.vote, name='vote'),
# ]

# Django tutorial 4  generic views, question_id changes to pk.
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    #Path to the assignment line for autograding
    path('owner', views.owner, name='owner'),
]