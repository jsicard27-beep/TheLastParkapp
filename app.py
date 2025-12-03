from flask import Flask, render_template, request, redirect, url_for, jsonify
from utils.excel_manager import (
    leer_parques,
    agregar_parque,
    obtener_parque_por_id,
    editar_parque,
    eliminar_parque
)

parques = [
    {"id":1, "nombre":"Parque Simón Bolívar", "lat":4.655, "lng":-74.093,
     "localidad":"Teusaquillo", "area_m2":114000,
     "descripcion":"El principal parque de la ciudad, con lagos y zonas verdes.",
     "direccion": "Av. 68"},

    {"id":2, "nombre":"Parque El Virrey", "lat":4.678, "lng":-74.050,
     "localidad":"Chapinero", "area_m2":20000,
     "descripcion":"Abarrotado de corredores y áreas para perros.",
     "direccion": "Cra 15"},

    {"id":3, "nombre":"Parque de los Novios", "lat":4.652, "lng":-74.065,
     "localidad":"Barrios Unidos", "area_m2":48000,
     "descripcion":"Hermosas zonas para picnic y eventos.",
     "direccion": "Calle 63"},

    {"id":4, "nombre":"Parque Nacional Enrique Olaya Herrera", "lat":4.636, "lng":-74.073,
     "localidad":"Santa Fe", "area_m2":30000,
     "descripcion":"Parque tradicional con senderos y esculturas.",
     "direccion": "Cra 7"},

    {"id":5, "nombre":"Parque El Tunal", "lat":4.598, "lng":-74.136,
     "localidad":"Tunjuelito", "area_m2":60000,
     "descripcion":"Gran parque recreativo con canchas deportivas.",
     "direccion": "Av Boyacá"}
]

app = Flask(__name__)

# ------------------------
#   HOME (MAPA)
# ------------------------
@app.route("/")
def inicio():
    return render_template("index.html")


# ------------------------
#   API PARA EL MAPA
# ------------------------
@app.route("/api/parks")
def api_parks():
    df = leer_parques()
    parques = df.to_dict(orient="records")
    return jsonify(parques)

@app.route("/api/parques")
def api_parques():
    return jsonify(parques)

# ------------------------
#   LISTAR PARQUES (CRUD)
# ------------------------
@app.route("/parques")
def listar_parques():
    return render_template("listar_parques.html", parques=parques)



# ------------------------
#   AGREGAR PARQUE (CRUD)
# ------------------------
@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    if request.method == "POST":
        datos = {
            "Nombre": request.form["nombre"],
            "Localidad": request.form["localidad"],
            "Direccion": request.form["direccion"],
            "Tamano_m2": request.form["tamano"],
            "Tipo": request.form["tipo"],
            "Estado": request.form["estado"],
            "Canchas": request.form["canchas"],
            "Juegos": request.form["juegos"],
            "Ultimo_mantenimiento": request.form["mantenimiento"]
        }
        agregar_parque(datos)
        return redirect(url_for("listar_parques"))

    return render_template("agregar_parque.html")


# ------------------------
#   EDITAR PARQUE (CRUD)
# ------------------------
@app.route("/editar/<int:id_parque>", methods=["GET", "POST"])
def editar(id_parque):
    if request.method == "POST":
        datos_modificados = {
            "Nombre": request.form["nombre"],
            "Localidad": request.form["localidad"],
            "Direccion": request.form["direccion"],
            "Tamano_m2": request.form["tamano"],
            "Tipo": request.form["tipo"],
            "Estado": request.form["estado"],
            "Canchas": request.form["canchas"],
            "Juegos": request.form["juegos"],
            "Ultimo_mantenimiento": request.form["mantenimiento"]
        }
        editar_parque(id_parque, datos_modificados)
        return redirect(url_for("listar_parques"))

    parque = obtener_parque_por_id(id_parque)
    return render_template("editar_parque.html", parque=parque)


# ------------------------
#   ELIMINAR PARQUE (CRUD)
# ------------------------
@app.route("/eliminar/<int:id_parque>")
def eliminar(id_parque):
    eliminar_parque(id_parque)
    return redirect(url_for("listar_parques"))


# ------------------------
#   EJECUTAR APP
# ------------------------
if __name__ == "__main__":
    app.run(debug=True)
