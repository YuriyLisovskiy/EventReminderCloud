from django.conf.urls import url

from account.views import (
	AccountCreateAPIView, ResetPasswordAPIView, SendTokenAPIView, AccountDeleteAPIView, AccountEditAPIView, AccountDetailsAPIView
)


urlpatterns = [
	url(r'^edit/?$', AccountEditAPIView.as_view()),
	url(r'^user/?$', AccountDetailsAPIView.as_view()),
	url(r'^create/?$', AccountCreateAPIView.as_view()),
	url(r'^delete/?$', AccountDeleteAPIView.as_view()),
	url(r'^send/token/?$', SendTokenAPIView.as_view()),
	url(r'^password/reset/?$', ResetPasswordAPIView.as_view()),
]
