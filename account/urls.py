from django.conf.urls import url

from account.views import AccountListView, AccountDetailsView

urlpatterns = [
	url(r'^$', AccountListView.as_view()),
	url(r'^edit/?$', AccountDetailsView.as_view())
]
