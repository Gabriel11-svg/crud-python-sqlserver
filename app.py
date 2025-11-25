from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ------------------------------------------
# CONFIGURACIÓN DE SQLITE
# ------------------------------------------
DB_NAME = "crud_estudiantes.db"

def conectar_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # para poder usar e.nombre, e.apellido, etc.
    return conn

def inicializar_db():
    # Crea la base de datos y la tabla si no existen
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Estudiantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            correo TEXT,
            telefono TEXT
        );
    """)
    conn.commit()
    conn.close()

# ------------------------------------------
# RUTA PRINCIPAL – LISTAR
# ------------------------------------------
@app.route("/")
def listar():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, apellido, correo, telefono FROM Estudiantes")
    estudiantes = cursor.fetchall()
    conn.close()
    return render_template("lista.html", estudiantes=estudiantes)

# ------------------------------------------
# CREAR
# ------------------------------------------
@app.route("/crear", methods=["GET", "POST"])
def crear():
     # Cambio pequeño para habilitar PR en feature/create-student
    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        correo = request.form["correo"]
        telefono = request.form["telefono"]

        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Estudiantes (nombre, apellido, correo, telefono)
            VALUES (?, ?, ?, ?)
        """, (nombre, apellido, correo, telefono))
        conn.commit()
        conn.close()
        return redirect("/")

    # Si es GET
    return render_template("form.html", estudiante=None)

# ------------------------------------------
# EDITAR
# ------------------------------------------
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    conn = conectar_db()
    cursor = conn.cursor()

    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        correo = request.form["correo"]
        telefono = request.form["telefono"]

        cursor.execute("""
            UPDATE Estudiantes
            SET nombre=?, apellido=?, correo=?, telefono=?
            WHERE id=?
        """, (nombre, apellido, correo, telefono, id))
        conn.commit()
        conn.close()
        return redirect("/")

    cursor.execute("SELECT id, nombre, apellido, correo, telefono FROM Estudiantes WHERE id=?", (id,))
    estudiante = cursor.fetchone()
    conn.close()
    return render_template("form.html", estudiante=estudiante)

# ------------------------------------------
# ELIMINAR
# ------------------------------------------
@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Estudiantes WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

# ------------------------------------------
# INICIO APP
# ------------------------------------------
if __name__ == "__main__":
    inicializar_db()   # crea la tabla si no existe
    app.run(debug=True)
# Cambio pequeño para habilitar PR desde feature/db-model
