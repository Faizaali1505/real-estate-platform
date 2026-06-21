from django.urls import path
from .views import MortgageCalculatorView

urlpatterns = [
    path('calculate/', MortgageCalculatorView.as_view(), name='mortgage-calculate'),
]
