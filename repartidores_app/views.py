from django.db.models.query import QuerySet
from .models import RepartidoresModel
from .serializers import RepartidoresSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from django.shortcuts import redirect




class Repartidores(APIView):
    def get(self, request, format=None):
        with connection.cursor() as cursor:
            cursor.execute("""SELECT COUNT(*) FROM repartidores_app_repartidoresmodel 
                WHERE activo = TRUE;""")
            row = cursor.fetchone()
            data = {'activos': row[0]}
        return Response(data)

def request_value(request):
    if request.data['data']:
        value = 1
        return value
    else:
        value = 2
        return value

class AsignarRepartidor(APIView):
    def post(self, request, format=None):
        with connection.cursor() as cursor:
            value = request_value(request)
            cursor.execute("""UPDATE repartidores_app_repartidoresmodel 
                SET activo= NOT activo WHERE iD=(case {value} 
                    WHEN 1 THEN (SELECT MAX(iD) FROM repartidores_app_repartidoresmodel 
                        WHERE activo = TRUE) 
                    WHEN 2 THEN (SELECT MIN(iD) FROM repartidores_app_repartidoresmodel  
                        WHERE activo = FALSE) END)""".format(value = value))
        return redirect('/repartidores/')

    
