from rest_framework import (
	status,
	permissions,
	authentication
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView

from .serializers import (
	AccountSerializer,
	AccountEditSerializer
)
from .models import Account


class AccountListView(ListCreateAPIView):
	queryset = Account.objects.all().order_by('-date_joined')
	serializer_class = AccountSerializer


class AccountDetailsView(APIView):
	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	@staticmethod
	def get(request, pk):
		if pk is None:
			return Response({'details': 'id is not provided'}, status=status.HTTP_400_BAD_REQUEST)
		account = Account.get_by_id(pk)
		if account is None:
			return Response(status=status.HTTP_404_NOT_FOUND)
		serializer = AccountSerializer(account)
		return Response(serializer.data, status=status.HTTP_200_OK)

	@staticmethod
	def post(request, pk):
		if pk is None:
			return Response({'details': 'id is not provided'}, status=status.HTTP_400_BAD_REQUEST)
		account = Account.get_by_id(pk)
		if account is None:
			return Response(status=status.HTTP_404_NOT_FOUND)
		serializer = AccountEditSerializer(instance=account, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
