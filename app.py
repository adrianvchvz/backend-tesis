from flask import Flask, request, jsonify
from flask_cors import CORS

#Web Servivces
from src.ws.sesion import ws_sesion
from src.ws.cnn import ws_cnn

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})


#Registrar los módulos que contienen a los servicios web
app.register_blueprint(ws_sesion)
app.register_blueprint(ws_cnn)

@app.route("/")
def index():
    return "Servicios web en ejecución"


if __name__ == "__main__":
    app.run(debug=True)