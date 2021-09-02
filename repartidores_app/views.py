from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from django.shortcuts import redirect


class Repartidores(APIView):
    def get(self, request, format=None):
        with connection.cursor() as cursor:
            cursor.execute("""SELECT COUNT(*) FROM repartidores_app_repartidoresmodel 
                WHERE activo = TRUE;""")
            row = cursor.fetchone()
            
        if row[0] == 0:
            data = {"Disponibles": "ninguno"}
            return Response(data)
        else:
            data = {"Disponibles":row[0]}
            return Response(data)


class AsignarRepartidor(APIView):
    def post(self, request, format=None):
        value = request.data['data']
        with connection.cursor() as cursor:
            cursor.execute("""UPDATE repartidores_app_repartidoresmodel 
                SET activo= NOT activo WHERE iD=(case {value} 
                    WHEN TRUE THEN (SELECT MAX(iD) FROM repartidores_app_repartidoresmodel 
                        WHERE activo = TRUE) 
                    WHEN FALSE THEN (SELECT MIN(iD) FROM repartidores_app_repartidoresmodel  
                        WHERE activo = FALSE) END)""".format(value = value))
        return redirect('/repartidores/')

    
