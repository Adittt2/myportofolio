from django.urls import path

from main import api_views

app_name = "api"

urlpatterns = [
    path("certifications/", api_views.certification_list,
         name="certification-list"),
    path("certifications/<uuid:certification_id>/", api_views.certification_detail,
         name="certification-detail"),
    path("certifications/<uuid:certification_id>/star/", api_views.certification_star,
         name="certification-star"),
     path("experience/", api_views.experience_list,
         name="experience-list"),
    path("experience/<uuid:experience_id>/", api_views.experience_detail,
         name="experience-detail"),
    path("experience/<uuid:experience_id>/star/", api_views.experience_star,
         name="experience-star"),
]