from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

db = pymysql.connect(
    host="localhost",
    user="root",
    password="metas639MACM",
    database="IMPERIUMALEXANDRIAE"  )

cursor = db.cursor(pymysql.cursors.DictCursor)
listaPersonas = []
resultadoPersona = []

@app.route("/mensaje", methods=["GET"])
def mensaje ():
    return jsonify({"mensaje": "¡Hola, mundo!"})

@app.route("/listarPersonas", methods=["GET"])
def listarPersonas():
    return jsonify(listaPersonas)

@app.route("/agregarPersona", methods=["POST"])
def agregarPersona():
    nuevaPersona = request.json.get("persona")
    listaPersonas.append(nuevaPersona)
    return jsonify({"mensaje": "Persona agregada exitosamente"})


@app.route("/INGRESOS_GENERADOS", methods=["GET"])
def ingresosGenerados():
    Ingresos = [{"dia": "Lunes", "ingresos": "1.500.000"}, 
    {"dia": "Martes", "ingresos": "3.000.000"}, 
    {"dia": "Miercoles", "ingresos": "6.000.000"}, 
    {"dia": "Jueves", "ingresos": "12.000.000"}, 
    {"dia": "Viernes", "ingresos": "24.000.000"}, 
    {"dia": "Sabado", "ingresos": "10.000.000"}, 
    {"dia": "Domingo", "ingresos": "7.500.000"}]
    return jsonify(Ingresos)

@app.route("/datosDeLaBase", methods=["GET"])
def datosBase():
    cursor.execute("SELECT * FROM persona")
    resultadosPersonas = cursor.fetchall()
    print(resultadosPersonas)
    return jsonify(resultadosPersonas)

@app.route("/agregarPersonaBD", methods=["POST"])
def agregar():
    nuevaPersona = request.json.get("persona")
    resultadoPersona.append(nuevaPersona)
    cursor.execute("INSERT INTO persona(identificacion, nombre, edad) VALUES (%s, %s, %s)", 
    (nuevaPersona["identificacion"], nuevaPersona['nombre'], nuevaPersona['edad']))
    db.commit()
    return "Se ha agregado una nueva persona a la base de datos"

@app.route("/buscarPersona/<identificacion>", methods=["GET"])
def buscar(identificacion):
    cursor. execute("SELECT * FROM persona WHERE identificacion = %s", (identificacion,))
    resultadosPersonas = cursor.fetchall()
    return jsonify(resultadosPersona)

@app.route("/actualizarPersona/<identificacion>", methods=["PUT"])
def actualizar(identificacion):
    nuevaPersona = request.json.get("persona")
    resultadoPersona.append(nuevaPersona)
    cursor.execute("UPDATE persona SET nombre=%s, edad=%s WHERE identificacion=%s", 
                   (nuevaPersona["nombre"], nuevaPersona['edad'], nuevaPersona['identificacion']))
    db.commit()
    return "Persona actualizada exitosamente"

@app.route("/eliminarPersona/<identificacion>", methods=["DELETE"])
def eliminar(identificacion):
    cursor.execute("DELETE FROM persona WHERE identificacion = %s", (identificacion,))
    db.commit()
    return "Persona eliminada exitosamente"

if __name__ == "__main__":
    app.run(debug=True)
