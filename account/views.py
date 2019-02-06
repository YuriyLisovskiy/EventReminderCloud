from rest_framework import (
	status,
	permissions,
	authentication
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from account.serializers import (
	AccountSerializer,
	AccountEditSerializer
)
from account.models import Account


class AccountListView(CreateAPIView):
	serializer_class = AccountSerializer


class AccountDetailsView(APIView):
	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)

	@staticmethod
	def get(request):
		pk = request.GET.get('pk', None)
		if pk is None:
			return Response({'error': 'primary key is not provided'}, status=status.HTTP_400_BAD_REQUEST)
		account = Account.get_by_id(pk)
		if account is None:
			return Response(status=status.HTTP_404_NOT_FOUND)
		if account.username != request.user.username or account.email != request.user.email:
			return Response(status=status.HTTP_403_FORBIDDEN)
		serializer = AccountSerializer(account)
		return Response(serializer.data, status=status.HTTP_200_OK)

	@staticmethod
	def post(request):
		pk = request.POST.get('pk', None)
		if pk is None:
			return Response({'error': 'primary key is not provided'}, status=status.HTTP_400_BAD_REQUEST)
		account = Account.get_by_id(pk)
		if account is None:
			return Response(status=status.HTTP_404_NOT_FOUND)
		serializer = AccountEditSerializer(instance=account, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
