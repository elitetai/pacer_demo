from django.urls import include, path

from account.views import GetScoreView

app_name = 'account'

urlpatterns = [
    path('get_score/', view=GetScoreView.as_view(), name='get_score'),
]
