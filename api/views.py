from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SpatialPoint, SpatialPolygon
from django.contrib.gis.geos import Point, Polygon
import json


class PointListCreateView(APIView):
    """
    API for listing and creating spatial point data.
    """

    def get(self, request):
        points = SpatialPoint.objects.all()
        data = [{"id": point.id, "name": point.name, "location": point.location.coords} for point in points]
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            data = request.data if request.content_type == 'application/json' else request.POST
            name = data.get("name")
            coordinates = data.get("longlat")

            if not name or not coordinates:
                return Response({"error": "Name and longlat are required"}, status=status.HTTP_400_BAD_REQUEST)

            coordinates = json.loads(coordinates) if isinstance(coordinates, str) else coordinates

            if not isinstance(coordinates, list) or len(coordinates) != 2:
                return Response({"error": "Invalid longlat format, expected [longitude, latitude]"}, status=status.HTTP_400_BAD_REQUEST)

            point = SpatialPoint.objects.create(name=name, location=Point(*coordinates))
            return Response({"id": point.id, "name": point.name, "location": point.location.coords}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PointRetrieveUpdateDeleteView(APIView):
    """
    API for retrieving, updating, and deleting a spatial point.
    """

    def get(self, request, pk):
        point = get_object_or_404(SpatialPoint, pk=pk)
        return Response({"id": point.id, "name": point.name, "location": point.location.coords}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        point = get_object_or_404(SpatialPoint, pk=pk)
        try:
            data = request.data if request.content_type == 'application/json' else request.POST
            name = data.get("name", point.name)
            coordinates = data.get("longlat")

            if coordinates:
                coordinates = json.loads(coordinates) if isinstance(coordinates, str) else coordinates
                if not isinstance(coordinates, list) or len(coordinates) != 2:
                    return Response({"error": "Invalid longlat format, expected [longitude, latitude]"}, status=status.HTTP_400_BAD_REQUEST)
                point.location = Point(*coordinates)

            point.name = name
            point.save()
            return Response({"message":F"id --> {point.id} Updated Successfully","id": point.id, "name": point.name, "location": point.location.coords}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        point = get_object_or_404(SpatialPoint, pk=pk)
        point.delete()
        return Response({"message": "Point deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class PolygonListCreateView(APIView):
    """
    API for listing and creating spatial polygon data.
    """

    def get(self, request):
        polygons = SpatialPolygon.objects.all()
        data = [{"id": polygon.id, "name": polygon.name, "area": polygon.area.coords} for polygon in polygons]
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            data = request.data if request.content_type == 'application/json' else request.POST
            name = data.get("name")
            coordinates = data.get("area")

            if not name or not coordinates:
                return Response({"error": "Name and area are required"}, status=status.HTTP_400_BAD_REQUEST)

            coordinates = json.loads(coordinates) if isinstance(coordinates, str) else coordinates

            polygon = SpatialPolygon.objects.create(name=name, area=Polygon(coordinates))
            return Response({"id": polygon.id, "name": polygon.name, "area": polygon.area.coords}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PolygonRetrieveUpdateDeleteView(APIView):
    """
    API for retrieving, updating, and deleting a spatial polygon.
    """

    def get(self, request, pk):
        polygon = get_object_or_404(SpatialPolygon, pk=pk)
        return Response({"id": polygon.id, "name": polygon.name, "area": polygon.area.coords}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        polygon = get_object_or_404(SpatialPolygon, pk=pk)
        try:
            data = request.data if request.content_type == 'application/json' else request.POST
            name = data.get("name", polygon.name)
            coordinates = data.get("area")

            if coordinates:
                coordinates = json.loads(coordinates) if isinstance(coordinates, str) else coordinates
                polygon.area = Polygon(coordinates)

            polygon.name = name
            polygon.save()
            return Response({"message":f"id --> {polygon.id} Updated Successfully","id": polygon.id, "name": polygon.name, "area": polygon.area.coords}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        polygon = get_object_or_404(SpatialPolygon, pk=pk)
        polygon.delete()
        return Response({"message": "Polygon deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
