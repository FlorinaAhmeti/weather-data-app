from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Station
from .serializers import StationSerializer

class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Handles PATCH requests to activate or deactivate a station and update the API key."""
        station = self.queryset.get(pk=pk)
        
        serializer = self.get_serializer(station, data=request.data, partial=True)
        if serializer.is_valid():
            station = serializer.save()
            # Customize the response based on the new status
            if station.status == "active":
                return Response(
                    {"api_key": station.api_key},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"status": "Station deactivated successfully"},
                    status=status.HTTP_200_OK
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
