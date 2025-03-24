from django.urls import path
from .views import (
    PointListCreateView, PointRetrieveUpdateDeleteView,
    PolygonListCreateView, PolygonRetrieveUpdateDeleteView
)

urlpatterns = [
    path('points/', PointListCreateView.as_view(), name='get-the-list-of-points'),
    path('points/create/', PointListCreateView.as_view(), name='create-the-long-lat-points'),

    path('getpointsbyid/<int:pk>/', PointRetrieveUpdateDeleteView.as_view(), name='get-point-by-id'),
    path('updatepoints/<int:pk>/', PointRetrieveUpdateDeleteView.as_view(), name='update-point-by-id'),
    path('deletepoints/<int:pk>/', PointRetrieveUpdateDeleteView.as_view(), name='delete-point-by-id'),

    path('polygons/', PolygonListCreateView.as_view(), name='get-the-list-of-polygons'),
    path('polygons/create/', PolygonListCreateView.as_view(), name='create-the-long-lat-polygons'),

    path('getpolygonsbyid/<int:pk>/', PolygonRetrieveUpdateDeleteView.as_view(), name='get-polygons-by-id'),
    path('updatepolygons/<int:pk>/', PolygonRetrieveUpdateDeleteView.as_view(), name='update-polygons-by-id'),
    path('deletepolygons/<int:pk>/', PolygonRetrieveUpdateDeleteView.as_view(), name='delete-polygons-by-id'),
    
]
