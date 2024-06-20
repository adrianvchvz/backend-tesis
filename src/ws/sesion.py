from flask import Blueprint, request, jsonify
from ..models.sesion import Sesion
import json

#Generar un blueprint para el inicio de sesión.
ws_sesion = Blueprint('ws_sesion', __name__)

#Crear un ruta (endpoint)
@ws_sesion.route('/login', methods = ['POST'])
def login():
    if request.method == 'POST':
        if 'usuario' not in request.json or 'clave' not in request.json:
            return jsonify({'status': False, 'data': None, 'message': "Falta parámetros"}), 400
        
        #Recoger las credenciales ingresadas mediante POST.
        usuario = request.json['usuario']       
        clave = request.json['clave']

        #Instanciar a la clase Sesión.
        obj = Sesion(usuario, clave)

        #Ejecutar el método iniciarSesión() y recoger el resultado.
        resultadoJSON = obj.iniciarSesion()

        #Convertir el resultadoJSON de cadena a objeto (object).
        resultadoJSONobj = json.loads(resultadoJSON)

        if resultadoJSONobj['status'] == True:
            return jsonify(resultadoJSONobj), 200  # OK
        else:
            return jsonify(resultadoJSONobj), 400
    else:
        return jsonify(resultadoJSONobj), 401  # No autorizado

        