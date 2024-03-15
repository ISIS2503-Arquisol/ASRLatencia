from http.client import ResponseNotReady
import random
from django.shortcuts import render, redirect
from django.urls import reverse
from .logic import cliente_logic as cl
from django.http import HttpResponse
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
import requests
from django.conf import settings
import urllib.request
import urllib.parse

# Create your views here.
@csrf_exempt
def clientes_view(request):

    if request.method == 'GET':
            return render(request, 'cliente/index.html')


    elif request.method == 'POST':
        data = request.POST
        cliente = cl.create_cliente_from_form(data)
        
        url_api_banco = 'http://localhost:8000/api/'  # Cambia esta URL por la del API de Banco
        #headers = {'Content-Type': 'application/json'}  # Establece el tipo de contenido como JSON
        try:
            response = requests.post(url_api_banco, data=cliente, json=cliente)
            response.raise_for_status()  # Lanza una excepción si la solicitud no es exitosa
            return render(request, 'cliente/index.html')
        except requests.exceptions.RequestException as e:
            return HttpResponse(f"Error al registrar el cliente en el API de Banco: {e}")
    else:
        # Aquí se manejaría el error si la creación del cliente no es exitosa
        return HttpResponse(status=405)

@csrf_exempt
def validar_usuario(request):
    if request.method == 'POST':
        email = request.POST.get('correo')
        url_api_banco = 'http://localhost:8000/api/validar_cliente/' 

        try:
            response = requests.post(url_api_banco, data={'correo': email})
            print(response)
            response.raise_for_status  # Lanza una excepción si la solicitud no es exitosa

            if response.json().get('existe', False):
                # Si el usuario o correo existe, redirigir al paso de ingreso de contraseña
                # Aquí debes decidir cómo manejarás el siguiente paso, por ejemplo:
                telefono = response.json().get('telefono')
                request.session['correo'] = email  # Guarda en la sesión
                request.session['telefono'] = telefono
                # enviar_otp_telefono(telefono)
                return redirect(vista_ingreso_contrasena)
            else:
                # Si el usuario o correo no existe, mostrar mensaje de error
                # Ajusta según tu lógica de manejo de mensajes
                print("f")
                return redirect(iniciar_sesion)
        except requests.exceptions.RequestException as e:
            #return render(request, 'login_step_one.html', {'error': f"Error al validar el usuario: {e}"})
            pass

    # Si no es un POST o si algo más falla, redirige al formulario inicial
    return render(request, 'cliente/index.html')


def vista_ingreso_contrasena(request):
    correo = request.session.get('correo')  # Asumiendo que has guardado el correo en la sesión
    telefono = request.session.get('telefono')
    #print(telefono)
    if correo:
        context = {'correo': correo , 'telefono' : telefono}
        return render(request, 'cliente/ingresoContrasenia.html', context)
    else:
        # Redirigir al usuario si el correo no está en la sesión (indicativo de que no ha pasado por el primer paso)
        return redirect(iniciar_sesion)
    
def procesar_login(request):
    if request.method == 'POST':
        contrasena = request.POST.get('contrasena')

        print(contrasena)
        return redirect(inicio_sesion_exitoso)


# def enviar_otp_telefono(telefono):
#     url = "https://wipple-sms-verify-otp.p.rapidapi.com/send"

#     payload = {
#         "app_name": "bancoDeLosAlpes",
#         "code_length": 6,
#         "code_type": "number",
#         "expiration_second": 86000,
#         "phone_number": telefono
#     }
#     headers = {
#         "content-type": "application/json",
#         "X-RapidAPI-Key": "ef7a86e331msh3e356374590d939p14d915jsnccc6c2e4b6a7",  # Asegúrate de definir esta variable en tu settings.py o como una variable de entorno
#         "X-RapidAPI-Host": "wipple-sms-verify-otp.p.rapidapi.com"
#     }

#     response = requests.post(url, json=payload, headers=headers)

#     print(response.json())  # Imprime la respuesta para depuración
#     return response.json()

# def verificar_otp(telefono, otp):
#     url = "https://otp-authenticator.p.rapidapi.com/v1/validate"
#     headers = {
#         "content-type": "application/json",
#         "X-RapidAPI-Key": "ef7a86e331msh3e356374590d939p14d915jsnccc6c2e4b6a7",
#         "X-RapidAPI-Host": "otp-authenticator.p.rapidapi.com"
#     }
#     data = {
#         "phoneNumber": telefono,
#         "otp": otp
#     }
#     response = requests.post(url, json=data, headers=headers)
#     print(response)
#     return response.json()


def registro_cliente_view(request):
    if request.method == 'GET':
        return render(request, 'cliente/registro.html')
    
def inicio_sesion_exitoso(request):
    return render(request, 'cliente/inicio.html')

def iniciar_sesion(request):
    return render(request, 'cliente/iniciarSesion.html')
