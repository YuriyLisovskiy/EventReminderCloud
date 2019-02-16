from rest_framework import (
	status,
	permissions,
	authentication
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from account.serializers import AccountSerializer
from account.models import Account


class AccountCreateAPIView(CreateAPIView):
	serializer_class = AccountSerializer

	# credentials_sender = lambda username, password: {'username': username, 'password': password}

	# def create(self, request, *args, **kwargs):
	# 	serializer = self.serializer_class

	# 	print(serializer.data)

	# 	data = serializer.data


class AccountEditAPIView(APIView):
	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)

	@staticmethod
	def post(request):
		account = Account.get_by_pk(request.user.username)
		if account is None:
			return Response(status=status.HTTP_404_NOT_FOUND)
		data = request.data.copy()
		data['username'] = request.user.username
		serializer = AccountSerializer(instance=account, data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
