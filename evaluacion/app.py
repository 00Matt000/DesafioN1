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
        print("✅ Conexión a la base de datos establecida")
        break
    except mysql.connector.Error as err:
        print(f"⏳ Esperando conexión a la base de datos... ({attempt + 1}/{max_retries})")
        time.sleep(3)
else:
    exit(1)


@app.route('/evaluaciones', methods=['POST'])
def crear_evaluacion():
    
    data = request.json
    
    cursor.execute("SELECT * FROM estudiantes WHERE rut = %s", (data['rut_estudiante'],))
    
    if cursor.fetchone() is None:
        return {
            'error': 'Estudiante no encontrado'
            }, 400
    
    cursor.execute("INSERT INTO evaluaciones (rut_estudiante, semestre, asignatura, evaluacion) VALUES (%s, %s, %s, %s)", 
                  (data['rut_estudiante'], data['semestre'], data['asignatura'], data['evaluacion']))
    
    db.commit()
    
    return {
        'mensaje': 'Evaluación creada'
        }, 201

@app.route('/evaluaciones', methods=['GET'])
def obtener_evaluaciones():
    
    cursor.execute("SELECT * FROM evaluaciones")
    return jsonify(cursor.fetchall())

@app.route('/evaluaciones/<int:id>', methods=['GET'])
def obtener_evaluacion(id):
    
    cursor.execute("SELECT * FROM evaluaciones WHERE id = %s", (id,))
    return jsonify(cursor.fetchone())

if __name__ == '__main__':
    app.run(host='0.0.0.0')
