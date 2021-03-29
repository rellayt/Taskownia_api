from django.urls import path
from .views import RegisterView, LoginView, UserView, NewProjectView, TakeProjectView, MyProjectView, \
    MyAuthorProjectView, ProjectsView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('newProject', NewProjectView.as_view()),
    path('takeProject', TakeProjectView.as_view()),
    path('myProjects', MyProjectView.as_view()),
    path('crProjects', MyAuthorProjectView.as_view()),
    path('projects', ProjectsView.as_view())
]