from rest_framework import mixins, viewsets


class GetListViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet для метода List"""


class CreateModelViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet для метода Create"""
