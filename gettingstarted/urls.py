from django.urls import path, include
from django.contrib import admin
from register import views as v

admin.autodiscover()

import hello.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", hello.views.index, name="index"),
    path("db/", hello.views.db, name="db"),
    path("admin/", admin.site.urls),
    path("register/", v.register, name = "register"),
    path("v1/<int:id>", hello.views.v1, name="v one"),
    path("create/", hello.views.create, name="create"),
    path("", include("django.contrib.auth.urls")),
    path("ma/", hello.views.memeber_area, name="member area"),
    path("new/", hello.views.new_repo, name="new repository"),
    path("new-datasheet/", hello.views.new_datasheet, name="new datasheet"),
    path("new-datasheet/<repo_name>", hello.views.new_datasheet_name, name="new repo"),

    path("new/<repo_name>", hello.views.new_repo_name, name="new repo"),

    path("new-subsetfeature/<repo_name>", hello.views.new_subsetfeature, name="new subsetfeature"),

    path("check-repo-name/", hello.views.check_name_availability, name="check repo name"),


]
