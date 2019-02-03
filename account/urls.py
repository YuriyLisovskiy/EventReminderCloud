from django.conf.urls import url

from account.views import AccountListView, AccountDetailsView

urlpatterns = [
	url(r'^$', AccountListView.as_view()),
	url(r'^(?P<pk>\d+)/?$', AccountDetailsView.as_view())
]
