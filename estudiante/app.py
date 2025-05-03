from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)
import time

max_retries = 10
for attempt in range(max_retries):
    try:
        db = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        cursor = db.cursor(dictionary=True)
        print("Conexión a la base de datos establecida")
        break
    except mysql.connector.Error as err:
        print(f"Esperando conexión a la base de datos... ({attempt + 1}/{max_retries})")
        time.sleep(3)
else:
    exit(1)


@app.route('/estudiantes', methods=['POST'])
def crear_estudiante():
    
    data = request.json
    
    cursor.execute("INSERT INTO estudiantes (rut, nombre_completo, edad, curso) VALUES (%s, %s, %s, %s)", 
                  (data['rut'], data['nombre_completo'], data['edad'], data['curso']))
    
    db.commit()
    
    return {
        'mensaje': 'Estudiante creado'
        }, 201

@app.route('/estudiantes', methods=['GET'])
def obtener_estudiantes():
    
    cursor.execute("SELECT * FROM estudiantes")
    return jsonify(cursor.fetchall())

@app.route('/estudiantes/<rut>', methods=['GET'])
def obtener_estudiante(rut):
    
    cursor.execute("SELECT * FROM estudiantes WHERE rut = %s", (rut,))
    return jsonify(cursor.fetchone())

if __name__ == '__main__':
    app.run(host='0.0.0.0')
