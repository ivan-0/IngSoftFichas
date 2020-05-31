from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import random, pdfkit, os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)
app.secret_key = "mysecretkey"
env=Environment(loader=FileSystemLoader('templates'))
template=env.get_template('ver_datos.html')

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM fichas')
    datos = cur.fetchall()
    cur.close()
    return render_template('index.html', fichas = datos)

@app.route('/agregar_cita', methods=['POST'])
def agregar_cita():
    if request.method == 'POST':
        boleta = request.form['boleta']
        hora = request.form['hora']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO fichas (boleta, hora) VALUES (%s,%s)", (boleta, hora))
        mysql.connection.commit()
        flash('Cita agendada')
        return redirect(url_for('Index'))


@app.route('/ver_cita/<boleta>', methods = ['POST', 'GET'])
def ver_cita(boleta):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM alumnos WHERE boleta={}' .format(boleta))
    datos = cur.fetchall()
    cur.execute('SELECT * FROM fichas WHERE boleta={}' .format(boleta))
    datos2 = cur.fetchall()
    cur.close()
    print(datos[0])
    print(datos2[0])
    return render_template('ver_datos.html', alumno = datos[0], ficha = datos2[0])

@app.route('/convertir_pdf/<boleta>', methods = ['POST', 'GET'])
def convertir_pdf(boleta):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM alumnos WHERE boleta={}' .format(boleta))
    datos = cur.fetchall()
    cur.execute('SELECT * FROM fichas WHERE boleta={}' .format(boleta))
    datos2 = cur.fetchall()
    cur.close()
    impresion='Nombre: '+str(datos[0][0])+' Boleta: '+str(datos[0][1])+' C.U.R.P: '+str(datos[0][2])+' Cita de reinscripcion: '+str(datos2[0][2])
    pdfkit.from_string(impresion,'cita.pdf' )
    return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(port=3000, debug=True)
