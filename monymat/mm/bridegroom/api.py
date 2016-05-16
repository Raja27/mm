__author__ = 'rajaprasanna'

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from . import serializer
from . import models


class BrideGroomsListApi(ListAPIView):

    serializer_class = serializer.BrideGroomListSerializer
    paginator_class = serializer.LimitTenPaginator
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.family.looking_for is 'Bride':
            return models.BrideGroom.objects.filter(is_active=True, gender=False).exclude(family=self.request.user.family)
        elif self.request.user.family.looking_for is 'Groom':
            return models.BrideGroom.objects.filter(is_active=True, gender=True).exclude(family=self.request.user.family)
        else:
            return models.BrideGroom.objects.filter(is_active=True).exclude(family=self.request.user.family)


class BrideGroomsAPIView(APIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = serializer.BrideGroomDetailSerializer

    def get(self, request, *arg, **kwarg):
        status_messege = 'Failed'
        code = status.HTTP_400_BAD_REQUEST
        response = dict()
        try:
            id = request.GET.get('id')
            if models.BrideGroom.objects.filter(id=id, is_active=True).exists():
                result = models.BrideGroom.objects.get(id=id)
                response.update({'object': self.serializer_class(result).data})
                status_messege = 'Success'
                code = status.HTTP_200_OK
        except Exception as e:
            print(e)
        response.update({'status_messege': status_messege})
        return Response(response, code)

    def post(self, request, *arg, **kwarg):
        status_messege = 'Failed'
        code = status.HTTP_400_BAD_REQUEST
        response = dict()
        data = request.data.copy()
        try:
            family_data = data.pop('family')
            family_serializer = serializer.FamilySerializer(data=family_data)
            if family_serializer.is_valid():
                family = family_serializer.save()
                data.update({'family': family.id})
                data_serializer = serializer.BrideGroomSerializer(data=data)
                if data_serializer.is_valid():
                    data_serializer.save()
                    status_messege = 'Success'
                    code = status.HTTP_201_CREATED
                else:
                    response.update({'errors': data_serializer.errors})
            else:
                response.update({'errors': family_serializer.errors})
        except Exception as e:
            print(e)
        response.update({'status_messege': status_messege})
        return Response(response, code)

    def put(self, request, *arg, **kwarg):
        status_messege = 'Failed'
        code = status.HTTP_400_BAD_REQUEST
        response = dict()
        data = request.data.copy()
        try:
            id = request.data.get('id', None)
            if id is not None:
                if models.BrideGroom.objects.filter(id=id).exists():
                    result = models.BrideGroom.objects.get(id=id)
                    data_serializer = serializer.BrideGroomSerializer(result, data=data)
                    if data_serializer.is_valid():
                        data_serializer.save()
                        family_data = data.pop('family')
                        id = family_data.get('id', None)
                        if id is not None:
                            if models.Family.objects.filter(id=id).exists():
                                result = models.Family.objects.get(id=id)
                                family_serializer = serializer.FamilySerializer(result, data=family_data)
                                if family_serializer.is_valid():
                                    family_serializer.save()

                                    status_messege = 'Success'
                                    code = status.HTTP_201_CREATED
                                else:
                                    response.update({'errors': family_serializer.errors})
                    else:
                        response.update({'errors': data_serializer.errors})
        except Exception as e:
            print(e)
        response.update({'status_messege': status_messege})
        return Response(response, code)