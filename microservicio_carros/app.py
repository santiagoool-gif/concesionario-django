from flask import Flask, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI")

cliente = MongoClient(MONGO_URI)

db = cliente["concesionario"]
coleccion_carros = db["carros"]


@app.route("/carros", methods=["GET"])
def obtener_carros():
    carros = list(coleccion_carros.find({}, {"_id": 0}))

    return jsonify(carros)
@app.route("/carros/<int:anio>", methods=["GET"])
def obtener_carros_por_anio(anio):
    carros = list(
        coleccion_carros.find(
            {"anio": anio},
            {"_id": 0}
        )
    )

    return jsonify(carros)
if __name__ == "__main__":
    app.run(debug=True)