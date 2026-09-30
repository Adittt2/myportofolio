from django.urls import path

from main.views import (
    show_main,
    show_experience,
    update_experience,
    get_experiences_json,
    delete_experience,
    show_certifications,
    create_certification,
    update_certification,
    get_certifications_json,
    delete_certification,
    register,
    login_user,
    logout_user,
    create_experience_ajax,
    toggle_star_experience,
    create_certification_ajax,
    toggle_star_certification,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("experience/", show_experience, name="show_experience"),
    path("experience/<uuid:experience_id>/edit/", update_experience, name="update_experience"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    path("api/experience/", get_experiences_json, name="get_experiences_json"),
    path("certifications/", show_certifications, name="show_certifications"),
    path("certifications/add/", create_certification, name="create_certification"),
    path("certifications/<uuid:certification_id>/edit/", update_certification, name="update_certification"),
    path("certifications/<uuid:certification_id>/delete/", delete_certification, name="delete_certification"),
    path("api/certifications/", get_certifications_json, name="get_certifications_json"),
    path("experience/add-ajax/", create_experience_ajax, name="create_experience_ajax"),
    path("experience/<uuid:experience_id>/star/", toggle_star_experience, name="toggle_star_experience"),
    path("certifications/add-ajax/", create_certification_ajax, name="create_certification_ajax"),
    path("certifications/<uuid:certification_id>/star/", toggle_star_certification, name="toggle_star_certification"),
]