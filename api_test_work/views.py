from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .tasks import parse_task
from .models import HackerNews
from rest_framework import viewsets
from .serializers import HackerNewsListSerializer


class StartParser(APIView):

    def get(self, request):
        parse_task.delay() # start parser
        return Response({"Success": "parser started"}, status=status.HTTP_200_OK)


class NewsListViewSet(viewsets.ModelViewSet):

    serializer_class = HackerNewsListSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        order_by = self.request.query_params.get('order_by')
        if order_by:
            return HackerNews.objects.all().order_by(order_by)
        return HackerNews.objects.all()
