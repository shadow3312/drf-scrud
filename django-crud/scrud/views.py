"""
ScrudViewset is an abstract class that helps building any viewset with predefined and customizable action

The class abstracting this one inherit all the actions defined here
    
    class UserViewset(ScrudViewset):
        def __init__(self):
            super().__init__(models.User, serializers.UserSerializer)

"""

from . import utils
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import permission_classes 
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.parsers import FileUploadParser
from rest_framework import mixins
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

class ScrudViewset(viewsets.ViewSet, mixins.ListModelMixin):

    """
    The class relies on built-in drf ViewSet to build action

    Each action returns a paginated json response
    """

    permission_classes_by_action = {
        'create': [AllowAny],
        'list': [AllowAny],
        'get': [AllowAny],
        'edit': [AllowAny],
        'delete': [AllowAny],
        'activate': [AllowAny],
        'deactivate': [AllowAny],
        'inactives': [AllowAny], 'search': [AllowAny]
    }
    def __init__(self, model, serializer_class,  permission_classes_by_action=permission_classes_by_action, optional_serializer=None, optional_key=None):
        self.model = model
        self.instances = model.objects.all().order_by('-id')
        self.instance = None
        self.serializer_class = serializer_class
        self.permission_classes_by_action = permission_classes_by_action
        self.optional_serializer = optional_serializer
        self.optional_key = optional_key

    

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    @permission_classes([IsAuthenticated])
    def list(self, request, format=None):
        pagination = PageNumberPagination()
        qs = pagination.paginate_queryset(self.instances, request)
        serializer = self.serializer_class(qs, many=True)
        # return JsonResponse(serializer.data, status=200, safe=False)
        return pagination.get_paginated_response(serializer.data)

    @permission_classes([IsAuthenticated])
    def get(self, request, pk, format=None):
        self.instance = get_object_or_404(self.instances, pk=pk)
        serializer = self.serializer_class(self.instance)
        return JsonResponse(serializer.data, status=200, safe=False)

    @permission_classes([IsAuthenticated])
    def create(self, request, format=None):
        parser_classes = (FileUploadParser,)
        serializer = self.serializer_class(data=request.data, context={'request':request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    @permission_classes([IsAuthenticated])
    def edit(self, request, pk, format=None):
        parser_classes = (FileUploadParser,)
        self.instance = get_object_or_404(self.instances, pk=pk)
        serializer = self.serializer_class(self.instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(pk=pk)
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    
    @permission_classes([IsAdminUser,])
    def delete(self, request, pk, forma=None):
        self.instance = get_object_or_404(self.instances, pk=pk)
        self.instance.delete()
        return JsonResponse({"message": "Element supprimé avec succès."}, status=204)

    def activate(self, request, pk):
        key = self.optional_key
        return utils.toggle_status(request, pk, self.model, key, self.serializer_class, True)

    def deactivate(self, request, pk):
        key = self.optional_key
        return utils.toggle_status(request, pk, self.model, key, self.serializer_class, False)
    @permission_classes([IsAdminUser])
    def inactives(self, request, format=None):
        self.instances = self.model.objects.inactive_rows()
        serializer = self.serializer_class(self.instances, many=True)
        return JsonResponse(serializer.data, status=200, safe=False)

    
    def search(self, request, format=None):
        pagination = PageNumberPagination()
        if request.GET.items():
            cond = Q()
            items = request.GET.items()
            for key, val in items:
                if val:
                    if key == 'page':
                        continue
                    if key == 'id':
                        cond.add(Q(**{key: val}), Q.AND)
                    cond.add(Q(**{key+'__icontains': val}), Q.AND)
            self.instances = self.instances.filter(cond)
            qs = pagination.paginate_queryset(self.instances, request)
    
        serializer = self.serializer_class(qs, many=True)
        return pagination.get_paginated_response(serializer.data)

