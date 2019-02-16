from django.conf.urls import url

from account.views import AccountCreateAPIView, AccountEditAPIView

urlpatterns = [
	url(r'^create/?$', AccountCreateAPIView.as_view()),
	url(r'^edit/?$', AccountEditAPIView.as_view())
]
