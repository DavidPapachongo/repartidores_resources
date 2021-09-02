from django.http import response
from rest_framework.test import APITestCase
from repartidores_app.models import RepartidoresModel
import json

class Repartidores(APITestCase):
    def test_get_repartidor(self):
        RepartidoresModel.objects.create(**{
            'activo': True
        })

        response = self.client.get('/repartidores/',format='json')
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data['Disponibles'] == 1

    def test_get_repartidores(self):
        RepartidoresModel.objects.create(**{
            'activo': True
        })
        RepartidoresModel.objects.create(**{
            'activo': True
        })
        RepartidoresModel.objects.create(**{
            'activo': True
        })

        response = self.client.get('/repartidores/',format='json')
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data['Disponibles'] == 3

    def test_try_get_repartidores(self):
        RepartidoresModel.objects.create(**{
            'activo': True
        })
        RepartidoresModel.objects.create(**{
            'activo': False
        })
        RepartidoresModel.objects.create(**{
            'activo': True
        })

        response = self.client.get('/repartidores/',format='json')
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data['Disponibles'] != 3

    
    def test_get_repartidores_no_disponibles(self):
        RepartidoresModel.objects.create(**{
            'activo': False
        })
        RepartidoresModel.objects.create(**{
            'activo': False
        })
        RepartidoresModel.objects.create(**{
            'activo': False
        })

        response = self.client.get('/repartidores/',format='json')
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data['Disponibles'] == 'ninguno'

class AsignarRepartidor(APITestCase):

    def test_post_asignar(self):
        RepartidoresModel.objects.create(**{
            'activo': True
        })

        data_request = {'data': True}
        

        response = self.client.post('/asignacion/',data_request,format='json')
        assert response.status_code == 302

        response = self.client.get('/repartidores/',format='json')
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data['Disponibles'] == 'ninguno'
        db = RepartidoresModel.objects.get()
        assert db.activo == False

    def test_post_desasignar(self):
        RepartidoresModel.objects.create(**{
            'activo': False
        })

        data_request = {'data': False}
        

        response = self.client.post('/asignacion/',data_request,format='json')
        assert response.status_code == 302

        response = self.client.get('/repartidores/',format='json')
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data['Disponibles'] == 1
        db = RepartidoresModel.objects.get()
        assert db.activo == True


        
