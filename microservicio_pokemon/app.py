from flask import Flask, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI")

cliente = MongoClient(MONGO_URI)
print(cliente.list_database_names())

db = cliente["pokedex"]
coleccion_pokemon = db["pokemon"]


@app.route("/pokemon")
def pokemon():
    lista_pokemon = list(coleccion_pokemon.find({}, {"_id": 0}))
    return jsonify(lista_pokemon)


@app.route("/pokemon/<nombre>")
def pokemon_nombre(nombre):
    pokemon = coleccion_pokemon.find_one(
        {"nombre": nombre},
        {"_id": 0}
    )

    if pokemon is None:
        return jsonify({
            "error": "Pokemon no esta"
        }), 404

    return jsonify(pokemon)


if __name__ == "__main__":
    app.run(debug=True)