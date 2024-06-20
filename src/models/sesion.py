from conexion import obtener_conexion as db
import json

class Sesion():  
    
    def __init__(self, p_usuario=None, p_clave=None):
        self.usuario = p_usuario
        self.clave = p_clave        

    def iniciarSesion(self):

        con = db()

        cursor = con.cursor()

        sql = """
                SELECT idusuario, nombresusuario, nombresrol, estadousuario FROM usuario u INNER JOIN rol r 
                ON u.idrol=r.idrol
                WHERE usuario=%s AND clave=%s
            """
        cursor.execute(sql, [self.usuario, self.clave])

        datos = cursor.fetchone()
 
        if datos is not None:
            # Obtener los nombres de las columnas
            columnas = [description[0] for description in cursor.description]
            # Construir el diccionario
            datos_dict = {columnas[i]: datos[i] for i in range(len(columnas))}
        else:
            return json.dumps({'status': False, 'datos': None, 'message': 'El usuario no existe o las credenciales son incorrectas.'})
            
        
        cursor.close()
        con.close()
        
        if datos_dict:
        
            if datos_dict['estadousuario'] == 'A': #Estado activo.
                return json.dumps({'status': True, 'data': datos_dict, 'message': 'Credenciales correctas. Bienvenido a la aplicación'})
            else: #Estado inactivo.
                return json.dumps({'status': False, 'datos': None, 'message':'Su cuenta está inactiva. Consulte con su administrador.'})
        else:
            return json.dumps({'status': False, 'datos': None, 'message': 'El usuario no existe o sus credenciales son incorrectas.'})

