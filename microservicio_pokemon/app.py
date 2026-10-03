from flask import Flask, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI")
cliente = MongoClient(MONGO_URI)
db = cliente["pokedex"]
coleccion_pokemon = db["pokemon"]


@app.route("/pokemon", methods=["GET"])
def pokemon():
    lista_pokemon = list(coleccion_pokemon.find({}, {"_id": 0}))
    return jsonify(lista_pokemon)


@app.route("/pokemon/<nombre>", methods=["GET"])
def pokemon_nombre(nombre):
    pokemon = coleccion_pokemon.find_one(
        {"nombre": nombre.capitalize()},
        {"_id": 0},
    )

    if pokemon is None:
        return jsonify({"error": "Pokemon no encontrado"}), 404

    return jsonify(pokemon)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"servicio": "microservicio-pokemon", "estado": "ok"})


if __name__ == "__main__":
    app.run(debug=True)
