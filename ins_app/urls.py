from django.urls import path
from .views import Registration, Login, PolicyCreateList, PolicyGetUpdateDestroy, ProjectedBenefits

urlpatterns = [
    path('register/', Registration.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('policy/create/', PolicyCreateList.as_view(), name='policy_create'),
    path('policy/list/', PolicyCreateList.as_view(), name='policy_list'),
    path('policy/get/<int:pk>/', PolicyGetUpdateDestroy.as_view(), name='policy_get'),
    path('policy/update/<int:pk>/', PolicyGetUpdateDestroy.as_view(), name='policy_update'),
    path('policy/delete/<int:pk>/', PolicyGetUpdateDestroy.as_view(), name='policy_delete'),
    path('policy/benefits/<int:pk>/', ProjectedBenefits.as_view(), name='benefits'),
]
