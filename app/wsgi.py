"""  
Diccionario de Glifos Mayas - Aplicación Flask
Instituto Politécnico Nacional
"""
import os
import logging
from flask import Flask, request, render_template, session, redirect, url_for
from flask_mysqldb import MySQL
from flask_session import Session
from flask_mail import Mail, Message
from dotenv import load_dotenv
from collections import Counter
import random
import yagmail
import base64
import io
import time
import json
from PIL import Image
import hashlib

# Cargar variables de entorno
load_dotenv()

# Configurar logging (sin información sensible)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Log de inicio sin información sensible
logger.info("Iniciando aplicación Glifos Mayas...")

# Configuración de la aplicación desde variables de entorno
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "default-secret-key-change-in-production")
app.config['SESSION_TYPE'] = os.environ.get("SESSION_TYPE", "filesystem")
app.config['MYSQL_USER'] = os.environ.get("MYSQL_USER", "root")
app.config['MYSQL_PASSWORD'] = os.environ.get("MYSQL_PASSWORD", "")
app.config['MYSQL_HOST'] = os.environ.get("MYSQL_HOST", "localhost")
app.config['MYSQL_PORT'] = int(os.environ.get("MYSQL_PORT", "3306"))
app.config['MYSQL_DB'] = os.environ.get("MYSQL_DB", "base_grigori")

# Configuración de correo
app.config['MAIL_SERVER'] = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
app.config['MAIL_PORT'] = int(os.environ.get("MAIL_PORT", "465"))
app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME", "")
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD", "")
app.config['MAIL_USE_TLS'] = os.environ.get("MAIL_USE_TLS", "False").lower() == "true"
app.config['MAIL_USE_SSL'] = os.environ.get("MAIL_USE_SSL", "True").lower() == "true"

#app.config['RECAPTCHA_ENABLED'] = True
#app.config['RECAPTCHA_SITE_KEY'] = "6LeE4ywpAAAAAJy-JLCxVHfSYf-94aWM6KYZqEFn"
#app.config['RECAPTCHA_SECRET_KEY'] = "6LeE4ywpAAAAABxZYGvHN5QWoU9vye5fr4kwl7Px"


mail = Mail(app)

Session(app)


mysql = MySQL(app)

def todos_los_datos_2(cursor,orden_datos,datos_busqueda,datos_atributes):
    if datos_atributes != "default" and datos_busqueda == "default":
        print("DAVID_SOTO_ESTOY_ENTRANDO A ESTA CONDICION, VAMOS POR BUEN CAMINO 1",flush=True)
        datos_con_id_atributos = []
        datos_con_id_atributos_final = []
        lista_atributos_resultante = []
        lista_atributos_limpio = []
        nuevo_valor_atributo = ""
        valores_dato_general_acumulada = []
        lista_atributos_resultante_repetidos = []
        total_datos = 0
        conjunto_datos = []
        print(datos_atributes,flush=True)
        print("Si entro a esta sección",flush=True)
        print(datos_atributes,flush=True)
        atributos_lista = datos_atributes.split("-")
        print(type(atributos_lista),flush=True) # Es una lista. 
        print(atributos_lista,flush=True)
        atributos_lista = atributos_lista[1:-1]
        print("ATRIBUTOS_LISTA 1")
        print(atributos_lista,flush=True)
        atributos_listas_1 = []
        for id_glifo in atributos_lista:
            cursor.execute(f"SELECT id_glifo FROM `t_distinction` WHERE `id_glifo` = '{id_glifo}';") 
            valor_atributos = cursor.fetchall()
            #print(valor_atributos,flush=True)
            atributos_listas_1.append(valor_atributos)
            
        print("RESULTADOS FINALES DE MI PRUEBA",flush=True)
        print(atributos_listas_1,flush=True)
        print(len(atributos_listas_1))

            
        atributo_final_id_glifo = []
        tamano = 0
        for atributo in atributos_listas_1:
            tamano += len(atributo)
            for atri in atributo:
                if atri not in atributo_final_id_glifo:
                    atributo_final_id_glifo.append(atri)
        
        print("Resultados conteo")
        print(tamano,flush=True)
        
        print("RESULTADOS FINALES DE MI PRUEBA 2",flush=True)
        print(atributo_final_id_glifo,flush=True)

        lista_atributos_limpio = []
        for valores in atributo_final_id_glifo:
            lista_atributos_limpio.append(valores[0])
            
        print("RESULTADOS FINALES DE MI PRUEBA 3")
        print(lista_atributos_limpio,flush=True)
    
        #Realizar la consulta a la tabla t-general 

        for id_glifo in atributos_lista:
            cursor.execute(f"SELECT * FROM `t_general` WHERE `id_glifo` = '{id_glifo}';") # Este se modifico
            valores_datos_general = cursor.fetchall()
            valores_dato_general_acumulada += valores_datos_general
            
         
            
        conjunto_datos = valores_dato_general_acumulada
    print("VARIABLE CONJUNTO DATOS")
    print(conjunto_datos)

    return conjunto_datos
        

def todos_los_datos_1(cursor,orden_datos,datos_busqueda,datos_atributes):
    conjunto_datos = []
    if orden_datos == "thomson" and datos_busqueda == "default":
        cursor.execute('SELECT * FROM `t_general` ORDER BY `th_num`')
        conjunto_datos = cursor.fetchall()

    if orden_datos == "traduccion" and datos_busqueda == "default":
        cursor.execute('SELECT * FROM `t_general` ORDER BY `des_traduccion`')
        conjunto_datos = cursor.fetchall()

    if orden_datos == "transcripcion"  and datos_busqueda == "default":
        cursor.execute('SELECT * FROM `t_general` ORDER BY `des_transcripcion`')
        conjunto_datos = cursor.fetchall()

    if datos_busqueda != "default" and orden_datos == "thomson":
        cursor.execute(f"SELECT * FROM `t_general` WHERE `th_num` = '{datos_busqueda}' ORDER BY `th_num`;") 
        conjunto_datos = cursor.fetchall()
        print("Entro en esta seccion 1 ")

    if datos_busqueda != "default" and orden_datos == "traduccion":
        cursor.execute(f"SELECT * FROM `t_general` WHERE `des_traduccion` = '{datos_busqueda}' ORDER BY `des_traduccion`;") 
        conjunto_datos = cursor.fetchall()
        print("Entro en esta seccion 2 ")
        
    if datos_busqueda != "default" and orden_datos == "transcripcion":
        cursor.execute(f"SELECT * FROM `t_general` WHERE `des_transcripcion` = '{datos_busqueda}' ORDER BY `des_transcripcion`;") 
        conjunto_datos = cursor.fetchall()
        print("Entro en esta seccion 3 ")
    
    if datos_atributes != "default" and datos_busqueda == "default":
        print("DAVID_SOTO_ESTOY_ENTRANDO A ESTA CONDICION, VAMOS POR BUEN CAMINO")
        datos_con_id_atributos = []
        datos_con_id_atributos_final = []
        lista_atributos_resultante = []
        lista_atributos_limpio = []
        nuevo_valor_atributo = ""
        valores_dato_general_acumulada = []
        lista_atributos_resultante_repetidos = []
        total_datos = 0
        conjunto_datos = []
        print("Si entro a esta sección",flush=True)
        print(datos_atributes,flush=True)
        atributos_lista = datos_atributes.split("-")
        print(type(atributos_lista),flush=True) # Es una lista. 
        print(atributos_lista,flush=True)
        
        atributos_lista = atributos_lista[1:-1]
        print("ATRIBUTOS_LISTA 1")
        print(atributos_lista,flush=True)
        
        atributos_listas_1 = []
        for atributo in atributos_lista:
            cursor.execute(f"SELECT id_glifo FROM `t_distinction` WHERE `id_attribute` = '{atributo}';") 
            valor_atributos = cursor.fetchall()
            #print(valor_atributos,flush=True)
            atributos_listas_1.append(valor_atributos)
            
        print("RESULTADOS FINALES DE MI PRUEBA",flush=True)
        print(atributos_listas_1,flush=True)
        print(len(atributos_listas_1))

            
        atributo_final_id_glifo = []
        tamano = 0
        for atributo in atributos_listas_1:
            tamano += len(atributo)
            for atri in atributo:
                if atri not in atributo_final_id_glifo:
                    atributo_final_id_glifo.append(atri)
        
        print("Resultados conteo")
        print(tamano,flush=True)
        
        print("RESULTADOS FINALES DE MI PRUEBA 2",flush=True)
        print(atributo_final_id_glifo,flush=True)

        lista_atributos_limpio = []
        for valores in atributo_final_id_glifo:
            lista_atributos_limpio.append(valores[0])
            
        print("RESULTADOS FINALES DE MI PRUEBA 3")
        print(lista_atributos_limpio,flush=True)
    
        #Realizar la consulta a la tabla t-general 

        for id_glifo in lista_atributos_limpio:
            cursor.execute(f"SELECT * FROM `t_general` WHERE `id_glifo` = '{id_glifo}';") 
            valores_datos_general = cursor.fetchall()
            valores_dato_general_acumulada += valores_datos_general
            
         
            
        conjunto_datos = valores_dato_general_acumulada
    print("VARIABLE CONJUNTO DATOS")
    print(conjunto_datos)

    return conjunto_datos

def todos_los_datos(cursor,orden_datos,datos_busqueda,datos_atributes):
    conjunto_datos = []
    if orden_datos == "thomson" and datos_busqueda == "default":
        cursor.execute('SELECT * FROM `t_general` ORDER BY `th_num`')
        conjunto_datos = cursor.fetchall()

    if orden_datos == "traduccion" and datos_busqueda == "default":
        cursor.execute('SELECT * FROM `t_general` ORDER BY `des_traduccion`')
        conjunto_datos = cursor.fetchall()

    if orden_datos == "transcripcion"  and datos_busqueda == "default":
        cursor.execute('SELECT * FROM `t_general` ORDER BY `des_transcripcion`')
        conjunto_datos = cursor.fetchall()

    if datos_busqueda != "default" and orden_datos == "thomson":
        cursor.execute(f"SELECT * FROM `t_general` WHERE `th_num` = '{datos_busqueda}' ORDER BY `th_num`;") 
        conjunto_datos = cursor.fetchall()
        print("Entro en esta seccion 1 ")

    if datos_busqueda != "default" and orden_datos == "traduccion":
        cursor.execute(f"SELECT * FROM `t_general` WHERE `des_traduccion` = '{datos_busqueda}' ORDER BY `des_traduccion`;") 
        conjunto_datos = cursor.fetchall()
        print("Entro en esta seccion 2 ")
        
    if datos_busqueda != "default" and orden_datos == "transcripcion":
        cursor.execute(f"SELECT * FROM `t_general` WHERE `des_transcripcion` = '{datos_busqueda}' ORDER BY `des_transcripcion`;") 
        conjunto_datos = cursor.fetchall()
        print("Entro en esta seccion 3 ")
    
    if datos_atributes != "default" and datos_busqueda == "default":
        datos_con_id_atributos = []
        datos_con_id_atributos_final = []
        lista_atributos_resultante = []
        lista_atributos_limpio = []
        nuevo_valor_atributo = ""
        valores_dato_general_acumulada = []
        lista_atributos_resultante_repetidos = []
        total_datos = 0
        conjunto_datos = []
        print("Si entro a esta sección",flush=True)
        print(datos_atributes,flush=True)
        atributos_lista = datos_atributes.split("-")
        print(type(atributos_lista),flush=True) # Es una lista. 
        print(atributos_lista,flush=True)
        #Recorre la tupla de los atributos seleccionados y realiza la consulta a la tabla atribute
        for id_atributo in atributos_lista:
            print(id_atributo,flush=True)
            cursor.execute(f"SELECT `id_glifo` FROM `t_distinction` WHERE `id_attribute` = '{id_atributo}';") 
            datos_con_id_atributos = cursor.fetchall()
            datos_con_id_atributos_final += datos_con_id_atributos
 
        print(datos_con_id_atributos_final,flush=True);       
        print("Todal de elementos son ",len(datos_con_id_atributos_final))

        #Elimina elementos duplicados de la lista
        print("SECCION QUE ESTAMOS PROBANDO",flush=True)
        for valor_atributo in datos_con_id_atributos_final:
            if valor_atributo not in lista_atributos_resultante: 
                lista_atributos_resultante.append(valor_atributo)
            else:
                veces_repetido = datos_con_id_atributos_final.count(valor_atributo)
                if(veces_repetido == len(atributos_lista)):
                    lista_atributos_resultante_repetidos.append(valor_atributo)
        print(lista_atributos_resultante,flush=True)
        print(lista_atributos_resultante_repetidos,flush=True)
        print("total de atributos " + str(len(atributos_lista)))

        #Elimina caracteres no necesarios   
        if lista_atributos_resultante_repetidos == [] and len(atributos_lista) == 1:
            for valor_atributo in lista_atributos_resultante:
                nuevo_valor_atributo = ""
                valor_atributo_1 = str(valor_atributo)
                for caracter in valor_atributo_1:
                    if caracter != ")" and caracter != "(" and caracter != ",":
                        nuevo_valor_atributo += caracter
                lista_atributos_limpio.append(nuevo_valor_atributo)
            print("Lista de elementos no repetidos impresa es: " + str(lista_atributos_limpio))
        
        if lista_atributos_resultante_repetidos != [] and len(atributos_lista)>1:
            for valor_atributo in lista_atributos_resultante_repetidos:
                nuevo_valor_atributo = ""
                valor_atributo_1 = str(valor_atributo)
                for caracter in valor_atributo_1:
                    if caracter != ")" and caracter != "(" and caracter != ",":
                        nuevo_valor_atributo += caracter
                lista_atributos_limpio.append(nuevo_valor_atributo)
            print("Lista de elementos repetidos impresa es: " + str(lista_atributos_limpio))

    
        #Realizar la consulta a la tabla t-general 

        for id_glifo in lista_atributos_limpio:
            cursor.execute(f"SELECT * FROM `t_general` WHERE `id_glifo` = '{id_glifo}';") 
            valores_datos_general = cursor.fetchall()
            valores_dato_general_acumulada += valores_datos_general
            
        conjunto_datos = valores_dato_general_acumulada
    print("VARIABLE CONJUNTO DATOS")
    print(conjunto_datos)

    return conjunto_datos

def total_de_campos(cursor,orden_datos,datos_busqueda,conjunto_datos,datos_atributes):
    total_datos_1 = ""
    total_datos_glifos = ""
    total_datos_glifos_1 = ""

    print("SECCION DE DATOS BUSQUEDA",flush=True)
    print("Datos busqueda: " + str(datos_busqueda),flush=True)
    print("Datos atributos: " + str(datos_atributes),flush=True)

    cursor.execute("SELECT count(num) FROM `t_general`")
    total_datos_glifos = cursor.fetchall()
    total_datos_glifos = str(total_datos_glifos)
    print("Total_datos_glifos" + str(total_datos_glifos),flush=True)
    for dato in total_datos_glifos:
            if dato != "(" and dato != ")" and dato != ",":
                total_datos_glifos_1 += dato

    if  datos_busqueda == "default":
        cursor.execute("SELECT count(num) FROM `t_general`")
        total_datos = cursor.fetchall()
        total_datos = str(total_datos)
        for dato in total_datos:
            if dato != "(" and dato != ")" and dato != ",":
                total_datos_1 += dato

    if datos_busqueda != "default":
         cursor.execute(f"SELECT count(num) FROM `t_general` WHERE `th_num` = '{datos_busqueda}'")
         total_datos = cursor.fetchall()
         total_datos = str(total_datos)
         for dato in total_datos:
            if dato != "(" and dato != ")" and dato != ",":
                total_datos_1 += dato
    
    print("DESPUES DE TODA LA LIMPIEZA",flush=True)
    
    if datos_busqueda == "default" and datos_atributes != "default":
        total_datos_1 = str(len(conjunto_datos))
        print("SE ESTA CUMPLIENDO ESTA CONDICION",flush=True)
    elif datos_busqueda != "default" and datos_atributes != "default":
        total_datos_1 = str(len(conjunto_datos))
    else:
        print("NO SE ESTA CUMPLIENDO ESTA CONDICION",flush=True)
    
    total_datos_1 = str(len(conjunto_datos))
    print("total_datos_1" + str(total_datos_1),flush=True)
    print("total_datos_glifos_1" + str(total_datos_glifos_1),flush=True)

    return total_datos_1,total_datos_glifos_1

def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16)  # Genera un valor de sal aleatorio

    # Combina la contraseña y la sal
    password_salt = password.encode() + salt

    # Crea un hash utilizando el algoritmo de hash seguro (por ejemplo, SHA-256)
    hashed_password = hashlib.sha256(password_salt).hexdigest()

    # Devuelve el hash y la sal
    return hashed_password, salt

@app.route('/')
def principal():
    session.pop('username', None)
    return render_template("inicio.html")

@app.route('/confirmacion')
def confirmacion():
    if 'username' in session:
        username = session['username']
        return f'¡Hola, {username}! <a href="/logout">Cerrar sesión</a>'
    return 'No has iniciado sesión. <a href="/login">Iniciar sesión</a>'

@app.route('/registrarse/', methods=['GET', 'POST'])
def registrarse():
    cursor = mysql.connection.cursor()
    nombre_apellidos = ""
    nombre_de_usuario = ""
    correo = ""
    universidad = ""
    password = ""
    pass_con = ""
    hashed_password = ""
    salt = ""
    mensaje = ""
    if request.method == "POST":
        nombre_apellidos = request.form["nombre"]
        nombre_de_usuario = request.form["apellidos"]
        correo = request.form["email"]
        universidad = request.form["universidad"]
        password = request.form["contrasena"]
        pass_con = request.form["con-contrasena"]
        captcha_response = "hola"
        recuperacion = ""
        hashed_password, salt = hash_password(password)
        
        hashed_password = str(hashed_password)
        salt = str(salt.hex())
        
        # Consultas parametrizadas para prevenir SQL Injection
        cursor.execute("SELECT correo FROM register_users WHERE correo = %s", (correo,))
        correo_resultado_busqueda = cursor.fetchall()
        
        cursor.execute("SELECT apellidos FROM register_users WHERE apellidos = %s", (nombre_de_usuario,))
        usuario_resultado_busqueda = cursor.fetchall()
        
        if str(nombre_apellidos) == "" or str(nombre_de_usuario) == "" or str(correo) == "" or str(universidad) == "" or str(hashed_password) == "" or str(salt) == "" or str(captcha_response) == "":
            mensaje = "Hacen falta datos para completar el registro"
            return render_template("registrarse.html",mensaje=mensaje)
        
        
        elif str(nombre_apellidos) != "" and str(nombre_de_usuario) != "" and str(correo) != "" and str(universidad) != "" and str(hashed_password) != "" and str(salt) != "":
            if captcha_response != "":
                if str(correo_resultado_busqueda) == "()" and str(usuario_resultado_busqueda) == "()":
                    logger.info("Nuevo usuario registrado")
                    # INSERT parametrizado para prevenir SQL Injection
                    cursor.execute(
                        "INSERT INTO register_users(nombre,apellidos,correo,universidad,password,salt,recuperacion) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                        (nombre_apellidos, nombre_de_usuario, correo, universidad, hashed_password, salt, recuperacion)
                    )
                    mysql.connection.commit()
                    return redirect(url_for('registro_confirmado')) 
                elif str(str(correo_resultado_busqueda)) != "()" and str(usuario_resultado_busqueda) == "()":
                    mensaje = "El correo que ingresaste ya esta registrado"
                    return render_template("registrarse.html",mensaje=mensaje)
                elif str(str(correo_resultado_busqueda)) == "()" and str(usuario_resultado_busqueda) != "()":
                    mensaje = "Alguien mas ya utilizo este nombre de usuario"
                    return render_template("registrarse.html",mensaje=mensaje)
                elif str(str(correo_resultado_busqueda)) != "()" and str(usuario_resultado_busqueda) != "()":
                    mensaje = "Este correo y usuario ya han sido registrados"
                    return render_template("registrarse.html",mensaje=mensaje)
            else: 
                mensaje = "Te falto seleccionar el captcha"
                return render_template("registrarse.html",mensaje=mensaje)
    
    return render_template("registrarse.html", nombre_apellidos = nombre_apellidos,nombre_de_usuario=nombre_de_usuario,correo=correo,mensaje = mensaje )

def comparando_datos(user_password,stored_password,salt):
    valor = 0
    # Convierte la sal y la contraseña ingresada a bytes
    salt_bytes = bytes.fromhex(salt)
    password_bytes = user_password.encode()

    # Combina la contraseña ingresada con la sal almacenada
    password_salt = password_bytes + salt_bytes

    # Calcular el hash de la contraseña ingresada
    hashed_password = hashlib.sha256(password_salt).hexdigest()

    # Verificar si el hash coincide con el almacenado en la base de datos
    if hashed_password == stored_password:
        mensaje = "Contraseña válida. Inicio de sesión exitoso."
        valor = 1
    else:
        mensaje = "Contraseña incorrecta. Inicio de sesión fallido."
        valor = 2
    
    return mensaje,valor


@app.route('/iniciar_sesion/',methods=['GET', 'POST'])
def iniciar_sesion():
    cursor = mysql.connection.cursor()
    correo = ""
    password = ""
    mensaje = ""
    valor_num = 0
    if request.method == "POST":
        correo = request.form["email"]
        password = request.form["contrasena"]
        pantalla = request.form['tamanioPantalla']
        
        dato_usuario='default'
        datos_atributes = 'default'
        datos_busqueda = 'default'
        datos_filtro = '1'
        orden_datos = 'thomson'
        busqueda = 'default'

        pantalla = pantalla.split("x")
        pantalla = [int(valor) for valor in pantalla]

        # Consulta parametrizada para prevenir SQL Injection
        cursor.execute("SELECT password,salt,nombre,apellidos FROM register_users WHERE correo = %s", (correo,))
        correo_base_datos = cursor.fetchall()
        
        if str(correo_base_datos) != "()":
            user = correo_base_datos[0][3]
            decision,valor = comparando_datos(password,correo_base_datos[0][0],correo_base_datos[0][1])
            
            if valor == 1:
                logger.info("Inicio de sesión exitoso")
                session['username'] = user
                if pantalla[0] > 768:
                    return redirect(url_for('index',orden_datos=orden_datos,datos_filtro=datos_filtro,datos_busqueda=datos_busqueda,datos_atributes=datos_atributes,dato_usuario=dato_usuario))
                if pantalla[0] <= 768:
                    return redirect(url_for('index_movil',orden_datos=orden_datos,datos_filtro=datos_filtro,busqueda=busqueda,datos_atributes=datos_atributes,dato_usuario=dato_usuario))

            else:
                mensaje = "El correo que ingresaste o registraste no son correctos."
                return render_template("inicio_sesion.html",mensaje = mensaje)
        else:
            mensaje = "El correo que ingresaste o registraste no son correctos."
            return render_template("inicio_sesion.html",mensaje = mensaje)
    return render_template("inicio_sesion.html",mensaje = mensaje)

@app.route('/contrasena_olvidada',methods=['GET', 'POST'])
def contrasena_olvidada():
    cursor = mysql.connection.cursor()
    if request.method == "POST":
            correo = request.form["email"]
            # Consulta parametrizada
            cursor.execute("SELECT correo FROM register_users WHERE correo = %s", (correo,))
            correo_resultado_busqueda = cursor.fetchall()
            if correo_resultado_busqueda == ():
                mensaje = "El correo que ingresaste no esta registrado"
                return render_template("contrasena_olvidada.html",mensaje=mensaje)
            elif correo_resultado_busqueda != ():
                
                email = app.config['MAIL_USERNAME']
                contrasena = app.config['MAIL_PASSWORD']
                numero_aleatorio = random.randint(100000, 999999)
                # UPDATE parametrizado
                cursor.execute("UPDATE register_users SET recuperacion = %s WHERE correo = %s", (numero_aleatorio, correo))
                mysql.connection.commit() 
                
                yag = yagmail.SMTP(user=email,password=contrasena)
                
                destinatarios = [correo]
                asunto = 'Recuperación de password'
                mensaje = 'Clave para recuperacion de password: ' + str(numero_aleatorio) 
                html = 'Ingresa este codigo en el sistema para actualizar tu password'
                
                yag.send(destinatarios,asunto,[mensaje,html])
                return redirect(url_for('ingresar_clave',correo=correo))            
    return render_template("contrasena_olvidada.html")

@app.route('/ingresar_clave/<string:correo>',methods=['GET', 'POST'])
def ingresar_clave(correo):
    cursor = mysql.connection.cursor()
    if request.method == "POST":
        if 'form1_submit' in request.form:
            clave = request.form["clave"]
            # Consulta parametrizada
            cursor.execute("SELECT correo,recuperacion FROM register_users WHERE correo = %s AND recuperacion = %s", (correo, clave))
            clave_busqueda = cursor.fetchall()

            if clave_busqueda and clave_busqueda[0][0] == correo and clave == clave_busqueda[0][1]:
                return redirect(url_for('cambiar_contrasena',correo=correo))
        elif 'form2_submit' in request.form:
            email = app.config['MAIL_USERNAME']
            contrasena = app.config['MAIL_PASSWORD']
            numero_aleatorio = random.randint(100000, 999999)
            # UPDATE parametrizado
            cursor.execute("UPDATE register_users SET recuperacion = %s WHERE correo = %s", (numero_aleatorio, correo))
            mysql.connection.commit() 
            
            yag = yagmail.SMTP(user=email,password=contrasena)
            
            destinatarios = [correo]
            asunto = 'Recuperación de password'
            mensaje = 'Clave para recuperacion de password: ' + str(numero_aleatorio) 
            html = 'Ingresa este codigo en el sistema para actualizar tu password'
            
            yag.send(destinatarios,asunto,[mensaje,html])
            return redirect(url_for('ingresar_clave',correo=correo)) 
            
    return render_template("ingresar_clave.html")

@app.route('/cambiar_contrasena/<string:correo>',methods=['GET', 'POST'])
def cambiar_contrasena(correo):
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        contraseña = request.form["contrasena"]
        conf_password = request.form["con-contrasena"]
        
        # Consulta parametrizada
        cursor.execute("SELECT correo FROM register_users WHERE correo = %s", (correo,))
        correo_resultado_busqueda = cursor.fetchall()
        
        
        if correo_resultado_busqueda == ():
                mensaje = "El correo que ingresaste no esta registrado"
                return render_template("contrasena_olvidada.html",mensaje=mensaje)
        elif correo_resultado_busqueda[0][0] == correo:
            hashed_password, salt = hash_password(contraseña)
            hashed_password = str(hashed_password)
            salt = str(salt.hex())
            
            recuperacion = ""
            
            cursor.execute(f"UPDATE `register_users` SET `password` = '{hashed_password}',`salt` = '{salt}',`recuperacion` = '{recuperacion}'  WHERE `correo` = '{correo_resultado_busqueda[0][0]}';")
            mysql.connection.commit() 
            
            return redirect(url_for('confirmacion_contrasena'))
    
    return render_template("cambio_contrasena.html")

@app.route('/confirmacion_contrasena',methods=['GET', 'POST'])
def confirmacion_contrasena():
    return render_template("contrasena_modificada.html")

@app.route('/registro_confirmado',methods=['GET', 'POST'])
def registro_confirmado():
    return render_template("registro_finalizado.html")

@app.route('/nuevo_atributo/<string:dispositivo>',methods=['GET','POST'])
def nuevo_atributo(dispositivo):
    if 'username' in session:
        mensaje =  ""
        cursor = mysql.connection.cursor()
        valor = str(session['username'])
        
        print("Si entro a nuevos atributos",flush=True)
        print(valor,flush=True)
        print(valor,flush=True)
        print(dispositivo,flush=True)
        
        cursor.execute(f"SELECT correo FROM `register_users` WHERE `apellidos` = '{valor}';")
        correo_resultado_busqueda = cursor.fetchall()
        
        cursor.execute(f"SELECT id_attribute,attribute FROM `t_attributes`")
        atributos = cursor.fetchall()
        
        print("Resultados atributos",flush=True)
        print(correo_resultado_busqueda,flush=True)
        print(atributos,flush=True)
        
        if request.method == 'POST':
            nombre_atributo = request.form['texto_nombre_atributo']
            checkbox_values = request.form.getlist('checkbox')
            
            print(nombre_atributo)
            print(checkbox_values,flush=True)
            # Aquí puedes realizar otras acciones según tus necesidades
            elementos_id = []
            elementos_atributos = []
            resultados_atributos_creados = []
            for valor_1 in checkbox_values:
                cursor.execute(f"SELECT id_attribute FROM `t_attributes` WHERE `id_attribute` = '{valor_1}';")
                id_attribute = cursor.fetchall()
                elementos_id.append(id_attribute[0][0])
                
                cursor.execute(f"SELECT attribute FROM `t_attributes` WHERE `id_attribute` = '{valor_1}';")
                attribute = cursor.fetchall()
                elementos_atributos.append(attribute[0][0])
                
            elementos_id = str(elementos_id)
            elementos_atributos = elementos_atributos
            import re
            # Definir una expresión regular para encontrar los caracteres no deseados
            regex_pattern = r"[\"\'\\]"

            # Aplicar la expresión regular y reemplazar los caracteres no deseados con una cadena vacía
            cleaned_strings = [re.sub(regex_pattern, "", s) for s in elementos_atributos]
            
            final = ""
            for atributos in cleaned_strings:
                final += " , " + str(atributos)
            
            saludo = "hola"
            print(elementos_id,flush=True)
            print(final,flush=True)
            
            cursor.execute(f"SELECT nombre_atributo FROM `atributos_personales` WHERE `nombre_atributo` = '{nombre_atributo}' AND `usuario` = '{valor}';")
            atributo_confirmacion = cursor.fetchall()
            
            if atributo_confirmacion == ():
                cursor.execute(f"INSERT INTO atributos_personales(usuario,nombre_atributo,id,conjuntos) VALUES ('{valor}','{nombre_atributo}','{elementos_id}','{final}')")
                mysql.connection.commit()
                return redirect(url_for("atributos_exitoso",dispositivo=dispositivo))
            elif atributo_confirmacion != ():
                mensaje = "El nombre del atributo ya existe"
                #return render_template("pestaña_nuevos_atributos_default.html",valor=valor,correo_resultado_busqueda=correo_resultado_busqueda,atributos=atributos,mensaje=mensaje)
        
        cursor.execute(f"SELECT correo FROM `register_users` WHERE `apellidos` = '{valor}';")
        correo_resultado_busqueda = cursor.fetchall()
        
        cursor.execute(f"SELECT id_attribute,attribute FROM `t_attributes`")
        atributos = cursor.fetchall()
        
        print("Resultados atributos",flush=True)
        print(correo_resultado_busqueda,flush=True)
        print(atributos,flush=True)
        
        return render_template("pestaña_nuevos_atributos_default.html",valor=valor,correo_resultado_busqueda=correo_resultado_busqueda,atributos=atributos,mensaje=mensaje)
    return render_template("usuario_no_inicio.html")


@app.route('/nuevo_atributo_personalizado/<string:dispositivo>',methods=['GET', 'POST'])
def nuevo_atributo_personalizado(dispositivo):
    if 'username' in session:
        cursor = mysql.connection.cursor()
        arreglo_imagenes_procesadas = list()
        arreglo_imagenes_image_1 = []
        mensaje = ""
        arreglo_imagenes_id_glifo = []
        valor = str(session['username'])
        arreglo_imagenes_finales = list()
        id_glifo = list()
        cursor.execute('SELECT * FROM `t_general` ORDER BY `th_num`')
        conjunto_datos = cursor.fetchall()
        
        cursor.execute('SELECT * FROM `t_glifos` ORDER BY `th_num`')
        data = cursor.fetchall()
        
        i = 0
        for elementos in range(len(data)):
            image_1 = base64.b64encode(data[elementos][1])
            id_glifo = data[elementos][0]
            
            arreglo_imagenes_image_1.append(str(image_1, 'UTF-8'))
            arreglo_imagenes_id_glifo.append(id_glifo)
            
        conteo = Counter(arreglo_imagenes_id_glifo)

        # Imprime los resultados
        for elemento, cantidad in conteo.items():
            if cantidad != 1:
                print(f'{elemento}: {cantidad} veces',flush=True)
        
        if request.method == 'POST':
            nombre_atributo = request.form['texto_nombre_atributo']
            checkbox_values = request.form.getlist('checkbox')
            print("NUEVOS ATRIBUTOS CREADOS PERSONALIZADOS:",flush=True)
            print(valor,flush=True)
            print(nombre_atributo,flush=True)
            print(checkbox_values,flush=True)
            print(type(checkbox_values),flush=True)
            
            cadena_resultante = ','.join(map(str, checkbox_values))
            
            
            cadena_resultante = f'["num",{cadena_resultante}]'
            print(cadena_resultante,flush=True)
            
            cursor.execute(f"SELECT nombre_atributo FROM `atributos_personales_por_atributos` WHERE `nombre_atributo` = '{nombre_atributo}' AND `usuario` = '{valor}';")
            atributo_confirmacion_personalizada = cursor.fetchall()
            
            if atributo_confirmacion_personalizada == ():
                cursor.execute(f"INSERT INTO atributos_personales_por_atributos(usuario,nombre_atributo,glifo_id) VALUES ('{valor}','{nombre_atributo}','{cadena_resultante}')")
                mysql.connection.commit()
                return redirect(url_for("atributos_exitoso",dispositivo=dispositivo))
            elif atributo_confirmacion_personalizada != ():
                mensaje = "El nombre del atributo ya existe"
                #return render_template("pestaña_nuevos_atributos_default.html",valor=valor,correo_resultado_busqueda=correo_resultado_busqueda,atributos=atributos,mensaje=mensaje)
        
           
                    
        return render_template("pestaña_nuevos_atributos_default_personalizados.html",conjunto_datos=conjunto_datos,arreglo_imagenes_image_1=arreglo_imagenes_image_1,arreglo_imagenes_id_glifo=arreglo_imagenes_id_glifo,mensaje=mensaje)
    
    return render_template("usuario_no_inicio.html")
    

@app.route('/atributos_exitoso/<string:dispositivo>',methods=['GET','POST'])
def atributos_exitoso(dispositivo):
    if 'username' in session:
        return render_template("atributos_guardados_exitoso.html",dispositivo=dispositivo)
    
@app.route('/index_invitado/<string:orden_datos>/<string:datos_filtro>/<string:datos_busqueda>/<string:datos_atributes>/<string:dato_usuario>/', methods=['GET', 'POST'])
def index_invitado(orden_datos,datos_filtro,datos_busqueda,datos_atributes,dato_usuario):
    arreglo_imagenes = list()
    id_glifo = list()
    total_datos_glifos = ""
    usuario_agregado = []
    atributos_de_usuario = []
    atributos_separados_1 = []
    atributos_lado_derecho = []
    total_datos = ""
    print(datos_atributes)
    arreglo_imagenes_procesadas = list()
    cursor = mysql.connection.cursor()
    conjunto_datos = todos_los_datos(cursor,orden_datos,datos_busqueda,datos_atributes)
    
    total_datos,total_datos_glifos = total_de_campos(cursor,orden_datos,datos_busqueda,conjunto_datos,datos_atributes)
    print("total_Dato" + total_datos)
    print("TOTAL DATOS" + total_datos_glifos)
    # Se sacan las imagenes de la base de datos 
    cursor.execute(f"SELECT id_glifo, graph_glifo  FROM `t_glifos`;")
    data = cursor.fetchall()

    cursor.execute(f"SELECT * FROM `t_attributes`;")
    atributos = cursor.fetchall()

    cursor.execute(f"SELECT * FROM `t_usuarios`;")
    usuarios = cursor.fetchall()

    i = 0
    total_datos_imagenes = 0
    while(i < int(total_datos_glifos)):
        arreglo_imagenes.append(data[i][1])
        id_glifo.append(data[i][0])
        image_1 = base64.b64encode(arreglo_imagenes[i])
        arreglo_imagenes_procesadas.append(str(image_1, 'UTF-8'))
        i = i+1

    ####################################################################################################
    
    if dato_usuario != "default":
        cursor.execute(f"SELECT * FROM  `t_attributes` WHERE `id_usuario` = '{dato_usuario}'")
        atributos_de_usuario = cursor.fetchall()
        print(atributos_de_usuario) 

        cursor.execute(f"SELECT * FROM `atributos_guardados` WHERE `id_usuario` = '{dato_usuario}'")
        atributos_lado_derecho = cursor.fetchall()
        print(atributos_lado_derecho)

    if request.method == "POST":
        limpiar = request.form.get("datos_eliminados")
        print(limpiar)
        if limpiar != None:
            if limpiar != "":
                usuario = limpiar.split("$eliminacion$")
                usuario_1 = usuario[0]
                print("LOS ATRIBUTOS A ELIMINAR SON DEL USUARIO: ")
                print(usuario_1)
            cursor.execute(f"DELETE FROM `atributos_guardados` WHERE `id_usuario` = '{usuario_1}';")
            mysql.connection.commit() 

    if request.method == "POST":
        guardados = request.form.get("datos_guardados")
        print("datos guardados" + str(guardados))
        id_num = ""
        id_usuario_1 = ""
        atributos_repetidos = []
        if guardados != None:

            datos_guardados_separados = guardados.split("$atributos_almacenados$")
            print(datos_guardados_separados)
            usuario_a_guardar = datos_guardados_separados[0]
            print(usuario_a_guardar)
            atributos_a_guardar = datos_guardados_separados[1]
            atributos_a_guardar_separados = atributos_a_guardar.split(",")
            print("Atributos_ agregados: " + str(atributos_a_guardar_separados))

        
            cursor.execute(f"DELETE FROM `atributos_guardados` WHERE `id_usuario` = '{usuario_a_guardar}';")
            mysql.connection.commit()  
            time.sleep(1)
            
            cursor.execute(f"SELECT id FROM `atributos_guardados`;")
            id_almacenados = cursor.fetchall()
            print("Atributos ya almacenados" + str(id_almacenados))

            for id_numero in atributos_a_guardar_separados:
                print("El numero de id_numero es: " + str(id_numero))
                for numero_id_almacenado in id_almacenados:
                    print("El numero del ciclo almacenado es" + str(numero_id_almacenado[0]))
                if str(id_numero) == str(numero_id_almacenado[0]):
                        atributos_repetidos.append(id_numero)
            

            print("Los atributos repetidos son: " + str(atributos_repetidos))

            for atributos_repetidos_1 in atributos_repetidos:
                atributos_a_guardar_separados.remove(atributos_repetidos_1)


            print("La lista resultante es: " + str(atributos_a_guardar_separados))

            if atributos_a_guardar_separados != ['']:
                for atributos in atributos_a_guardar_separados:
                    cursor.execute(f"SELECT id_attribute FROM `t_attributes` WHERE `id_attribute` = '{atributos}';")
                    id = cursor.fetchall()
                    cursor.execute(f"SELECT id_usuario FROM `t_attributes` WHERE `id_attribute` = '{atributos}';")
                    id_usuario = cursor.fetchall()
                    cursor.execute(f"SELECT attribute FROM `t_attributes` WHERE `id_attribute` = '{atributos}';")
                    atributos = cursor.fetchall()

                    print(id[0][0])
                    print(id_usuario[0][0])
                    print(atributos[0][0])
                    
                    cursor.execute(f"INSERT INTO atributos_guardados(id,id_usuario,atributo) VALUES ('{id[0][0]}','{id_usuario[0][0]}','{atributos[0][0]}')")
                    mysql.connection.commit()

    if request.method == "POST":
        usuario = request.form.get("todo")
        
        if usuario != None:
            print("EL VALOR RETORNADO ES: " + str(usuario))
            datos_usuario_separado = usuario.split("$atributos$")
            print("El valor de usuario es:" + str(datos_usuario_separado[0]))
            usuario_seleccionado = str(datos_usuario_separado[0])
            print("El valor de atributos es:" + str(datos_usuario_separado[1]))

            atributos_separados = datos_usuario_separado[1].split(",")
            print("Los atributos separados son: " + str(atributos_separados))

            for atributo in atributos_separados:
                if atributo != "":
                    atributos_separados_1.append(atributo)
            
            cursor.execute(f"SELECT * FROM `t_usuarios` WHERE `usuario` = '{usuario_seleccionado}'")
            usuario_resultado = cursor.fetchall()
            
            print("El valor del usuario es: " + str(usuario_resultado))
            usuario_resultado_1 = str(usuario_resultado)

            if(usuario_resultado_1 == "()"):
                cursor.execute(f"INSERT INTO  t_usuarios(usuario) VALUES ('{usuario_seleccionado}')")
                mysql.connection.commit()

                cursor.execute(f"SELECT * FROM `t_usuarios` WHERE `usuario` = '{usuario_seleccionado}'")
                usuario_agregado = cursor.fetchall()
                print("El usuario agregado es: " + str(usuario_agregado))

                usuario_id_2 = ""
                usuario_id = usuario_agregado[0]
                usuario_id_str = str(usuario_id).split(",")
                usuario_id_1 = usuario_id_str[0]

                for caracter in usuario_id_1:
                    if caracter != "," and caracter != "(" and caracter != ")":
                        usuario_id_2 += caracter

                print("El id de usuario seleccionado es:" + str(usuario_id_2))

                for atributo_nuevo in atributos_separados_1:
                    cursor.execute(f"INSERT INTO  t_attributes(id_usuario,attribute) VALUES ('{usuario_id_2}','{atributo_nuevo}')")
                    mysql.connection.commit()
                

    return render_template("index_invitado.html",conjunto_datos=conjunto_datos,total_datos = total_datos,id_glifo=id_glifo,arreglo_imagenes_procesadas = arreglo_imagenes_procesadas,datos_busqueda = datos_busqueda,atributos = atributos, usuarios=usuarios,atributos_de_usuario=atributos_de_usuario,atributos_lado_derecho=atributos_lado_derecho)

@app.route('/index_ingles_invitado/<string:orden_datos>/<string:datos_filtro>/<string:datos_busqueda>/<string:datos_atributes>/<string:dato_usuario>/', methods=['GET', 'POST'])
def index_ingles_invitado(orden_datos,datos_filtro,datos_busqueda,datos_atributes,dato_usuario):
    arreglo_imagenes = list()
    id_glifo = list()
    total_datos_glifos = ""
    usuario_agregado = []
    atributos_de_usuario = []
    atributos_separados_1 = []
    atributos_lado_derecho = []
    total_datos = ""
    print(datos_atributes)
    arreglo_imagenes_procesadas = list()
    cursor = mysql.connection.cursor()
    conjunto_datos = todos_los_datos(cursor,orden_datos,datos_busqueda,datos_atributes)
    
    total_datos,total_datos_glifos = total_de_campos(cursor,orden_datos,datos_busqueda,conjunto_datos,datos_atributes)
    print("total_Dato" + total_datos)
    print("TOTAL DATOS" + total_datos_glifos)
    # Se sacan las imagenes de la base de datos 
    cursor.execute(f"SELECT id_glifo, graph_glifo  FROM `t_glifos`;")
    data = cursor.fetchall()

    cursor.execute(f"SELECT * FROM `t_attributes`;")
    atributos = cursor.fetchall()

    cursor.execute(f"SELECT * FROM `t_usuarios`;")
    usuarios = cursor.fetchall()

    i = 0
    total_datos_imagenes = 0
    while(i < int(total_datos_glifos)):
        arreglo_imagenes.append(data[i][1])
        id_glifo.append(data[i][0])
        image_1 = base64.b64encode(arreglo_imagenes[i])
        arreglo_imagenes_procesadas.append(str(image_1, 'UTF-8'))
        i = i+1

    ####################################################################################################
    
    if dato_usuario != "default":
        cursor.execute(f"SELECT * FROM  `t_attributes` WHERE `id_usuario` = '{dato_usuario}'")
        atributos_de_usuario = cursor.fetchall()
        print(atributos_de_usuario) 

        cursor.execute(f"SELECT * FROM `atributos_guardados` WHERE `id_usuario` = '{dato_usuario}'")
        atributos_lado_derecho = cursor.fetchall()
        print(atributos_lado_derecho)

    if request.method == "POST":
        limpiar = request.form.get("datos_eliminados")
        print(limpiar)
        if limpiar != None:
            if limpiar != "":
                usuario = limpiar.split("$eliminacion$")
                usuario_1 = usuario[0]
                print("LOS ATRIBUTOS A ELIMINAR SON DEL USUARIO: ")
                print(usuario_1)
            cursor.execute(f"DELETE FROM `atributos_guardados` WHERE `id_usuario` = '{usuario_1}';")
            mysql.connection.commit() 

    if request.method == "POST":
        guardados = request.form.get("datos_guardados")
        print("datos guardados" + str(guardados))
        id_num = ""
        id_usuario_1 = ""
        atributos_repetidos = []
        if guardados != None:

            datos_guardados_separados = guardados.split("$atributos_almacenados$")
            print(datos_guardados_separados)
            usuario_a_guardar = datos_guardados_separados[0]
            print(usuario_a_guardar)
            atributos_a_guardar = datos_guardados_separados[1]
            atributos_a_guardar_separados = atributos_a_guardar.split(",")
            print("Atributos_ agregados: " + str(atributos_a_guardar_separados))

        
            cursor.execute(f"DELETE FROM `atributos_guardados` WHERE `id_usuario` = '{usuario_a_guardar}';")
            mysql.connection.commit()  
            time.sleep(1)
            
            cursor.execute(f"SELECT id FROM `atributos_guardados`;")
            id_almacenados = cursor.fetchall()
            print("Atributos ya almacenados" + str(id_almacenados))

            for id_numero in atributos_a_guardar_separados:
                print("El numero de id_numero es: " + str(id_numero))
                for numero_id_almacenado in id_almacenados:
                    print("El numero del ciclo almacenado es" + str(numero_id_almacenado[0]))
                if str(id_numero) == str(numero_id_almacenado[0]):
                        atributos_repetidos.append(id_numero)
            

            print("Los atributos repetidos son: " + str(atributos_repetidos))

            for atributos_repetidos_1 in atributos_repetidos:
                atributos_a_guardar_separados.remove(atributos_repetidos_1)


            print("La lista resultante es: " + str(atributos_a_guardar_separados))

            if atributos_a_guardar_separados != ['']:
                for atributos in atributos_a_guardar_separados:
                    cursor.execute(f"SELECT id_attribute FROM `t_attributes` WHERE `id_attribute` = '{atributos}';")
                    id = cursor.fetchall()
                    cursor.execute(f"SELECT id_usuario FROM `t_attributes` WHERE `id_attribute` = '{atributos}';")
                    id_usuario = cursor.fetchall()
                    cursor.execute(f"SELECT attribute FROM `t_attributes` WHERE `id_attribute` = '{atributos}';")
                    atributos = cursor.fetchall()

                    print(id[0][0])
                    print(id_usuario[0][0])
                    print(atributos[0][0])
                    
                    cursor.execute(f"INSERT INTO atributos_guardados(id,id_usuario,atributo) VALUES ('{id[0][0]}','{id_usuario[0][0]}','{atributos[0][0]}')")
                    mysql.connection.commit()

    if request.method == "POST":
        usuario = request.form.get("todo")
        
        if usuario != None:
            print("EL VALOR RETORNADO ES: " + str(usuario))
            datos_usuario_separado = usuario.split("$atributos$")
            print("El valor de usuario es:" + str(datos_usuario_separado[0]))
            usuario_seleccionado = str(datos_usuario_separado[0])
            print("El valor de atributos es:" + str(datos_usuario_separado[1]))

            atributos_separados = datos_usuario_separado[1].split(",")
            print("Los atributos separados son: " + str(atributos_separados))

            for atributo in atributos_separados:
                if atributo != "":
                    atributos_separados_1.append(atributo)
            
            cursor.execute(f"SELECT * FROM `t_usuarios` WHERE `usuario` = '{usuario_seleccionado}'")
            usuario_resultado = cursor.fetchall()
            
            print("El valor del usuario es: " + str(usuario_resultado))
            usuario_resultado_1 = str(usuario_resultado)

            if(usuario_resultado_1 == "()"):
                cursor.execute(f"INSERT INTO  t_usuarios(usuario) VALUES ('{usuario_seleccionado}')")
                mysql.connection.commit()

                cursor.execute(f"SELECT * FROM `t_usuarios` WHERE `usuario` = '{usuario_seleccionado}'")
                usuario_agregado = cursor.fetchall()
                print("El usuario agregado es: " + str(usuario_agregado))

                usuario_id_2 = ""
                usuario_id = usuario_agregado[0]
                usuario_id_str = str(usuario_id).split(",")
                usuario_id_1 = usuario_id_str[0]

                for caracter in usuario_id_1:
                    if caracter != "," and caracter != "(" and caracter != ")":
                        usuario_id_2 += caracter

                print("El id de usuario seleccionado es:" + str(usuario_id_2))

                for atributo_nuevo in atributos_separados_1:
                    cursor.execute(f"INSERT INTO  t_attributes(id_usuario,attribute) VALUES ('{usuario_id_2}','{atributo_nuevo}')")
                    mysql.connection.commit()
                

    return render_template("index_ingles_invitado.html",conjunto_datos=conjunto_datos,total_datos = total_datos,id_glifo=id_glifo,arreglo_imagenes_procesadas = arreglo_imagenes_procesadas,datos_busqueda = datos_busqueda,atributos = atributos, usuarios=usuarios,atributos_de_usuario=atributos_de_usuario,atributos_lado_derecho=atributos_lado_derecho)


@app.route('/index/<string:orden_datos>/<string:datos_filtro>/<string:datos_busqueda>/<string:datos_atributes>/<string:dato_usuario>/', methods=['GET', 'POST'])
def index(orden_datos,datos_filtro,datos_busqueda,datos_atributes,dato_usuario):
    if 'username' in session:
        username = session['username']
        valor_de_usuario = str(session['username'])
        print("Ejecucion de index " + str(username),flush=True)
        arreglo_imagenes = list()
        id_glifo = list()
        total_datos_glifos = ""
        usuario_agregado = []
        atributos_de_usuario = []
        atributos_separados_1 = []
        atributos_lado_derecho = []
        total_datos = ""
        conjunto_datos = []
        print(datos_atributes)
        arreglo_imagenes_procesadas = list()
        cursor = mysql.connection.cursor()
        print("IMPRIMIENDO LA LISTA DE DATOS ATRIBUTOS")
        
        print(datos_atributes,flush=True)
        print(type(datos_atributes),flush=True)
        #condicion para entrar a una u otra
        
        arreglo = datos_atributes.split('-')
        
        
        if arreglo[0] != "final" and arreglo[0] != "eliminar" and arreglo[0] != "num" and arreglo[0] != "eliminar1":
            try:
                print("SECCION 1",flush=True)
                conjunto_datos = todos_los_datos(cursor,orden_datos,datos_busqueda,datos_atributes)
            
                total_datos,total_datos_glifos = total_de_campos(cursor,orden_datos,datos_busqueda,conjunto_datos,datos_atributes)
                print("*********************************",flush=True)
                print(conjunto_datos,flush=True)
                print(total_datos,flush=True)
                print(total_datos_glifos,flush=True)
            except ValueError:
                 return render_template("index.html",conjunto_datos=conjunto_datos,total_datos = total_datos,id_glifo=id_glifo,arreglo_imagenes_procesadas = arreglo_imagenes_procesadas,datos_busqueda = datos_busqueda,atributos = atributos, usuarios=usuarios,atributos_de_usuario=atributos_de_usuario,atributos_lado_derecho=atributos_lado_derecho,username=username,atributos_limpios=atributos_limpios, atributos_personales_caja_derecha_limpios=atributos_personales_caja_derecha_limpios) 

        elif arreglo[0] == "final":
            print("SECCION 2",flush=True)
            conjunto_datos = todos_los_datos_1(cursor,orden_datos,datos_busqueda,datos_atributes)
            print("CONJUNTO_DATOS",flush=True)
            print(conjunto_datos)
            total_datos,total_datos_glifos = total_de_campos(cursor,orden_datos,datos_busqueda,conjunto_datos,datos_atributes)
        
        elif arreglo[0] == "num":
            print("SECCION 3")
            conjunto_datos = todos_los_datos_2(cursor,orden_datos,datos_busqueda,datos_atributes)
            print("CONJUNTO_DATOS",flush=True)
            print(conjunto_datos)
            total_datos,total_datos_glifos = total_de_campos(cursor,orden_datos,datos_busqueda,conjunto_datos,datos_atributes)
            
        elif arreglo[0] == "eliminar":
            print("SECCION 4")
            print("ENTRO EN ESTA CONDICION DE ELIMINAR",flush=True)
            print(datos_atributes,flush=True)
            arreglo = arreglo[1:]
            print("VALORES DE ARREGLO",flush=True)
            print(arreglo,flush=True)
            
            cursor.execute(f"DELETE FROM `atributos_personales` WHERE `usuario` = '{valor_de_usuario}' AND `nombre_atributo` = '{arreglo[0]}';")
            mysql.connection.commit() 
            print("ARREGLO ELIMINADO",flush=True)
            conjunto_datos = todos_los_datos_1(cursor,orden_datos,datos_busqueda,"default")
            total_datos,total_datos_glifos = total_de_campos(cursor,orden_datos,datos_busqueda,conjunto_datos,"default")
        
        elif arreglo[0] == "eliminar1":
            print("SECCION 5")
            print("ENTRO EN ESTA CONDICION DE ELIMINAR1",flush=True)
            print(datos_atributes,flush=True)
            arreglo = arreglo[1:]
            print("VALORES DE ARREGLO",flush=True)
            print(arreglo,flush=True)
            
            cursor.execute(f"DELETE FROM `atributos_personales_por_atributos` WHERE `usuario` = '{valor_de_usuario}' AND `nombre_atributo` = '{arreglo[0]}';")
            mysql.connection.commit() 
            print("ARREGLO ELIMINADO",flush=True)
            conjunto_datos = todos_los_datos_1(cursor,orden_datos,datos_busqueda,"default")
            total_datos,total_datos_glifos = total_de_campos(cursor,orden_datos,datos_busqueda,conjunto_datos,"default")
        
        print("total_Dato" + total_datos,flush=True)
        print("TOTAL DATOS" + total_datos_glifos,flush=True)
        # Se sacan las imagenes de la base de datos 
        cursor.execute(f"SELECT id_glifo, graph_glifo  FROM `t_glifos`;")  
        data = cursor.fetchall()

        cursor.execute(f"SELECT * FROM `t_attributes`;")
        atributos = cursor.fetchall()

        cursor.execute(f"SELECT * FROM `t_usuarios`;")
        usuarios = cursor.fetchall()
        
        # Procesos de la ventana de atributos personalizados
        
        print(valor_de_usuario,flush=True)
        cursor.execute(f"SELECT nombre_atributo,id FROM `atributos_personales` WHERE `usuario` = '{valor_de_usuario}' ")
        atributos_personales = cursor.fetchall()

        print("VALORES_DE_ATRIBUTOS_PERSONALES")
        print(atributos_personales,flush=True)
        
        atributos_limpios = []
        
        for atributo in atributos_personales:
            atributos_limpios.append(atributo)
        
        print("NUEVOS VALORES PROCESADOS",flush=True)
        print(atributos_limpios,flush=True)
        
        # Proceso de la ventana de atributos personalizados derecha
        
        print(valor_de_usuario,flush=True)
        cursor.execute(f"SELECT nombre_atributo,glifo_id FROM `atributos_personales_por_atributos` WHERE `usuario` = '{valor_de_usuario}' ")
        atributos_personales_caja_derecha = cursor.fetchall()

        print("VALORES_DE_ATRIBUTOS_PERSONALES DE LA CAJA DERECHA")
        print(atributos_personales_caja_derecha,flush=True)
        
        atributos_personales_caja_derecha_limpios = []
        
        for atributo in atributos_personales_caja_derecha:
            atributos_personales_caja_derecha_limpios.append(atributo)
        
        print("NUEVOS VALORES PROCESADOS",flush=True)
        print(atributos_personales_caja_derecha_limpios,flush=True)
        
        #**************************************************************************************************
    
        i = 0
        total_datos_imagenes = 0
        while(i < int(total_datos_glifos)):
            arreglo_imagenes.append(data[i][1])
            id_glifo.append(data[i][0])
            image_1 = base64.b64encode(arreglo_imagenes[i])
            arreglo_imagenes_procesadas.append(str(image_1, 'UTF-8'))
            i = i+1

        ####################################################################################################
        
        if dato_usuario != "default":
            cursor.execute(f"SELECT * FROM  `t_attributes` WHERE `id_usuario` = '{dato_usuario}'")
            atributos_de_usuario = cursor.fetchall()
            print(atributos_de_usuario) 

            cursor.execute(f"SELECT * FROM `atributos_guardados` WHERE `id_usuario` = '{dato_usuario}'")
            atributos_lado_derecho = cursor.fetchall()
            print(atributos_lado_derecho)

        if request.method == "POST":
            limpiar = request.form.get("datos_eliminados")
            print(limpiar)
            if limpiar != None:
                if limpiar != "":
                    usuario = limpiar.split("$eliminacion$")
                    usuario_1 = usuario[0]
                    print("LOS ATRIBUTOS A ELIMINAR SON DEL USUARIO: ")
                    print(usuario_1)
                cursor.execute(f"DELETE FROM `atributos_guardados` WHERE `id_usuario` = '{usuario_1}';")
                mysql.connection.commit() 

        if request.method == "POST":
            guardados = request.form.get("datos_guardados")
            print("datos guardados" + str(guardados))
            id_num = ""
            id_usuario_1 = ""
            atributos_repetidos = []
            if guardados != None:

                datos_guardados_separados = guardados.split("$atributos_almacenados$")
                print(datos_guardados_separados)
                usuario_a_guardar = datos_guardados_separados[0]
                print(usuario_a_guardar)
                atributos_a_guardar = datos_guardados_separados[1]
                atributos_a_guardar_separados = atributos_a_guardar.split(",")
                print("Atributos_ agregados: " + str(atributos_a_guardar_separados))

            
                cursor.execute(f"DELETE FROM `atributos_guardados` WHERE `id_usuario` = '{usuario_a_guardar}';")
                mysql.connection.commit()  
                time.sleep(1)
                
                cursor.execute(f"SELECT id FROM `atributos_guardados`;")
                id_almacenados = cursor.fetchall()
                print("Atributos ya almacenados" + str(id_almacenados))

                for id_numero in atributos_a_guardar_separados:
                    print("El numero de id_numero es: " + str(id_numero))
                    for numero_id_almacenado in id_almacenados:
                        print("El numero del ciclo almacenado es" + str(numero_id_almacenado[0]))
                        if str(id_numero) == str(numero_id_almacenado[0]):
                                atributos_repetidos.append(id_numero)
                

                print("Los atributos repetidos son: " + str(atributos_repetidos))

                for atributos_repetidos_1 in atributos_repetidos:
                    atributos_a_guardar_separados.remove(atributos_repetidos_1)


                print("La lista resultante es: " + str(atributos_a_guardar_separados))

                if atributos_a_guardar_separados != ['']:
                    for atributos in atributos_a_guardar_separados:
                        cursor.execute(f"SELECT id_attribute FROM `t_attributes` WHERE `id_attribute` = '{atributos}';")
                        id = cursor.fetchall()
                        cursor.execute(f"SELECT id_usuario FROM `t_attributes` WHERE `id_attribute` = '{atributos}';")
                        id_usuario = cursor.fetchall()
                        cursor.execute(f"SELECT attribute FROM `t_attributes` WHERE `id_attribute` = '{atributos}';")
                        atributos = cursor.fetchall()

                        print(id[0][0])
                        print(id_usuario[0][0])
                        print(atributos[0][0])
                        
                        cursor.execute(f"INSERT INTO atributos_guardados(id,id_usuario,atributo) VALUES ('{id[0][0]}','{id_usuario[0][0]}','{atributos[0][0]}')")
                        mysql.connection.commit()

        if request.method == "POST":
            usuario = request.form.get("todo")
            
            if usuario != None:
                print("EL VALOR RETORNADO ES: " + str(usuario))
                datos_usuario_separado = usuario.split("$atributos$")
                print("El valor de usuario es:" + str(datos_usuario_separado[0]))
                usuario_seleccionado = str(datos_usuario_separado[0])
                print("El valor de atributos es:" + str(datos_usuario_separado[1]))

                atributos_separados = datos_usuario_separado[1].split(",")
                print("Los atributos separados son: " + str(atributos_separados))

                for atributo in atributos_separados:
                    if atributo != "":
                        atributos_separados_1.append(atributo)
                
                cursor.execute(f"SELECT * FROM `t_usuarios` WHERE `usuario` = '{usuario_seleccionado}'")
                usuario_resultado = cursor.fetchall()
                
                print("El valor del usuario es: " + str(usuario_resultado))
                usuario_resultado_1 = str(usuario_resultado)

                if(usuario_resultado_1 == "()"):
                    cursor.execute(f"INSERT INTO  t_usuarios(usuario) VALUES ('{usuario_seleccionado}')")
                    mysql.connection.commit()

                    cursor.execute(f"SELECT * FROM `t_usuarios` WHERE `usuario` = '{usuario_seleccionado}'")
                    usuario_agregado = cursor.fetchall()
                    print("El usuario agregado es: " + str(usuario_agregado))

                    usuario_id_2 = ""
                    usuario_id = usuario_agregado[0]
                    usuario_id_str = str(usuario_id).split(",")
                    usuario_id_1 = usuario_id_str[0]

                    for caracter in usuario_id_1:
                        if caracter != "," and caracter != "(" and caracter != ")":
                            usuario_id_2 += caracter

                    print("El id de usuario seleccionado es:" + str(usuario_id_2))

                    for atributo_nuevo in atributos_separados_1:
                        cursor.execute(f"INSERT INTO  t_attributes(id_usuario,attribute) VALUES ('{usuario_id_2}','{atributo_nuevo}')")
                        mysql.connection.commit()
        
        print("VALOR DE ID_GLIFO_DEL ERROR QUE OBTENEMOS")
        print(id_glifo,flush=True)
        return render_template("index.html",conjunto_datos=conjunto_datos,total_datos = total_datos,id_glifo=id_glifo,arreglo_imagenes_procesadas = arreglo_imagenes_procesadas,datos_busqueda = datos_busqueda,atributos = atributos, usuarios=usuarios,atributos_de_usuario=atributos_de_usuario,atributos_lado_derecho=atributos_lado_derecho,username=username,atributos_limpios=atributos_limpios, atributos_personales_caja_derecha_limpios=atributos_personales_caja_derecha_limpios)
    return render_template("usuario_no_inicio.html")
    #'No has iniciado sesión. <a href="/iniciar_sesion/">Iniciar sesión</a>'
    #http://localhost:81/index/default/default/default/default/default/#1 

@app.route('/index_ingles/<string:orden_datos>/<string:datos_filtro>/<string:datos_busqueda>/<string:datos_atributes>/<string:dato_usuario>/', methods=['GET', 'POST'])
def index_english(orden_datos,datos_filtro,datos_busqueda,datos_atributes,dato_usuario):
    if 'username' in session:
        username = session['username']
        valor_de_usuario = str(session['username'])
        print("Ejecucion de index " + str(username),flush=True)
        arreglo_imagenes = list()
        id_glifo = list()
        total_datos_glifos = ""
        usuario_agregado = []
        atributos_de_usuario = []
        atributos_separados_1 = []
        atributos_lado_derecho = []
        total_datos = ""
        conjunto_datos = []
        print(datos_atributes)
        arreglo_imagenes_procesadas = list()
        cursor = mysql.connection.cursor()
        print("IMPRIMIENDO LA LISTA DE DATOS ATRIBUTOS")
        
        print(datos_atributes,flush=True)
        print(type(datos_atributes),flush=True)
        #condicion para entrar a una u otra
        
        arreglo = datos_atributes.split('-')

        
        if arreglo[0] != "final" and arreglo[0] != "eliminar" and arreglo[0] != "num":
            print("SECCION 1",flush=True)
            conjunto_datos = todos_los_datos(cursor,orden_datos,datos_busqueda,datos_atributes)
           
            total_datos,total_datos_glifos = total_de_campos(cursor,orden_datos,datos_busqueda,conjunto_datos,datos_atributes)
            print("*********************************",flush=True)
            print(conjunto_datos,flush=True)
            print(total_datos,flush=True)
            print(total_datos_glifos,flush=True)

        elif arreglo[0] == "final":
            print("SECCION 2",flush=True)
            conjunto_datos = todos_los_datos_1(cursor,orden_datos,datos_busqueda,datos_atributes)
            print("CONJUNTO_DATOS",flush=True)
            print(conjunto_datos)
            total_datos,total_datos_glifos = total_de_campos(cursor,orden_datos,datos_busqueda,conjunto_datos,datos_atributes)
        elif arreglo[0] == "num":
            print("SECCION 3")
            conjunto_datos = todos_los_datos_2(cursor,orden_datos,datos_busqueda,datos_atributes)
            print("CONJUNTO_DATOS",flush=True)
            print(conjunto_datos)
            total_datos,total_datos_glifos = total_de_campos(cursor,orden_datos,datos_busqueda,conjunto_datos,datos_atributes)
            
        elif arreglo[0] == "eliminar":
            print("SECCION 4")
            print("ENTRO EN ESTA CONDICION",flush=True)
            print(datos_atributes,flush=True)
            arreglo.remove("eliminar")
            for valores in arreglo:
                cursor.execute(f"DELETE FROM `atributos_personales` WHERE `usuario` = '{valor_de_usuario}' AND `nombre_atributo` = '{valores}';")
                mysql.connection.commit() 
            conjunto_datos = todos_los_datos_1(cursor,orden_datos,datos_busqueda,"default")
            total_datos,total_datos_glifos = total_de_campos(cursor,orden_datos,datos_busqueda,conjunto_datos,"default")
        
        print("total_Dato" + total_datos,flush=True)
        print("TOTAL DATOS" + total_datos_glifos,flush=True)
        # Se sacan las imagenes de la base de datos 
        cursor.execute(f"SELECT id_glifo, graph_glifo  FROM `t_glifos`;")  
        data = cursor.fetchall()

        cursor.execute(f"SELECT * FROM `t_attributes`;")
        atributos = cursor.fetchall()

        cursor.execute(f"SELECT * FROM `t_usuarios`;")
        usuarios = cursor.fetchall()
        
        # Procesos de la ventana de atributos personalizados
        
        print(valor_de_usuario,flush=True)
        cursor.execute(f"SELECT nombre_atributo,id FROM `atributos_personales` WHERE `usuario` = '{valor_de_usuario}' ")
        atributos_personales = cursor.fetchall()

        print("VALORES_DE_ATRIBUTOS_PERSONALES")
        print(atributos_personales,flush=True)
        
        atributos_limpios = []
        
        for atributo in atributos_personales:
            atributos_limpios.append(atributo)
        
        print("NUEVOS VALORES PROCESADOS",flush=True)
        print(atributos_limpios,flush=True)
        
        # Proceso de la ventana de atributos personalizados derecha
        
        print(valor_de_usuario,flush=True)
        cursor.execute(f"SELECT nombre_atributo,glifo_id FROM `atributos_personales_por_atributos` WHERE `usuario` = '{valor_de_usuario}' ")
        atributos_personales_caja_derecha = cursor.fetchall()

        print("VALORES_DE_ATRIBUTOS_PERSONALES DE LA CAJA DERECHA")
        print(atributos_personales_caja_derecha,flush=True)
        
        atributos_personales_caja_derecha_limpios = []
        
        for atributo in atributos_personales_caja_derecha:
            atributos_personales_caja_derecha_limpios.append(atributo)
        
        print("NUEVOS VALORES PROCESADOS",flush=True)
        print(atributos_personales_caja_derecha_limpios,flush=True)
        
        #**************************************************************************************************
    
        i = 0
        total_datos_imagenes = 0
        while(i < int(total_datos_glifos)):
            arreglo_imagenes.append(data[i][1])
            id_glifo.append(data[i][0])
            image_1 = base64.b64encode(arreglo_imagenes[i])
            arreglo_imagenes_procesadas.append(str(image_1, 'UTF-8'))
            i = i+1

        ####################################################################################################
        
        if dato_usuario != "default":
            cursor.execute(f"SELECT * FROM  `t_attributes` WHERE `id_usuario` = '{dato_usuario}'")
            atributos_de_usuario = cursor.fetchall()
            print(atributos_de_usuario) 

            cursor.execute(f"SELECT * FROM `atributos_guardados` WHERE `id_usuario` = '{dato_usuario}'")
            atributos_lado_derecho = cursor.fetchall()
            print(atributos_lado_derecho)

        if request.method == "POST":
            limpiar = request.form.get("datos_eliminados")
            print(limpiar)
            if limpiar != None:
                if limpiar != "":
                    usuario = limpiar.split("$eliminacion$")
                    usuario_1 = usuario[0]
                    print("LOS ATRIBUTOS A ELIMINAR SON DEL USUARIO: ")
                    print(usuario_1)
                cursor.execute(f"DELETE FROM `atributos_guardados` WHERE `id_usuario` = '{usuario_1}';")
                mysql.connection.commit() 

        if request.method == "POST":
            guardados = request.form.get("datos_guardados")
            print("datos guardados" + str(guardados))
            id_num = ""
            id_usuario_1 = ""
            atributos_repetidos = []
            if guardados != None:

                datos_guardados_separados = guardados.split("$atributos_almacenados$")
                print(datos_guardados_separados)
                usuario_a_guardar = datos_guardados_separados[0]
                print(usuario_a_guardar)
                atributos_a_guardar = datos_guardados_separados[1]
                atributos_a_guardar_separados = atributos_a_guardar.split(",")
                print("Atributos_ agregados: " + str(atributos_a_guardar_separados))

            
                cursor.execute(f"DELETE FROM `atributos_guardados` WHERE `id_usuario` = '{usuario_a_guardar}';")
                mysql.connection.commit()  
                time.sleep(1)
                
                cursor.execute(f"SELECT id FROM `atributos_guardados`;")
                id_almacenados = cursor.fetchall()
                print("Atributos ya almacenados" + str(id_almacenados))

                for id_numero in atributos_a_guardar_separados:
                    print("El numero de id_numero es: " + str(id_numero))
                    for numero_id_almacenado in id_almacenados:
                        print("El numero del ciclo almacenado es" + str(numero_id_almacenado[0]))
                        if str(id_numero) == str(numero_id_almacenado[0]):
                                atributos_repetidos.append(id_numero)
                

                print("Los atributos repetidos son: " + str(atributos_repetidos))

                for atributos_repetidos_1 in atributos_repetidos:
                    atributos_a_guardar_separados.remove(atributos_repetidos_1)


                print("La lista resultante es: " + str(atributos_a_guardar_separados))

                if atributos_a_guardar_separados != ['']:
                    for atributos in atributos_a_guardar_separados:
                        cursor.execute(f"SELECT id_attribute FROM `t_attributes` WHERE `id_attribute` = '{atributos}';")
                        id = cursor.fetchall()
                        cursor.execute(f"SELECT id_usuario FROM `t_attributes` WHERE `id_attribute` = '{atributos}';")
                        id_usuario = cursor.fetchall()
                        cursor.execute(f"SELECT attribute FROM `t_attributes` WHERE `id_attribute` = '{atributos}';")
                        atributos = cursor.fetchall()

                        print(id[0][0])
                        print(id_usuario[0][0])
                        print(atributos[0][0])
                        
                        cursor.execute(f"INSERT INTO atributos_guardados(id,id_usuario,atributo) VALUES ('{id[0][0]}','{id_usuario[0][0]}','{atributos[0][0]}')")
                        mysql.connection.commit()

        if request.method == "POST":
            usuario = request.form.get("todo")
            
            if usuario != None:
                print("EL VALOR RETORNADO ES: " + str(usuario))
                datos_usuario_separado = usuario.split("$atributos$")
                print("El valor de usuario es:" + str(datos_usuario_separado[0]))
                usuario_seleccionado = str(datos_usuario_separado[0])
                print("El valor de atributos es:" + str(datos_usuario_separado[1]))

                atributos_separados = datos_usuario_separado[1].split(",")
                print("Los atributos separados son: " + str(atributos_separados))

                for atributo in atributos_separados:
                    if atributo != "":
                        atributos_separados_1.append(atributo)
                
                cursor.execute(f"SELECT * FROM `t_usuarios` WHERE `usuario` = '{usuario_seleccionado}'")
                usuario_resultado = cursor.fetchall()
                
                print("El valor del usuario es: " + str(usuario_resultado))
                usuario_resultado_1 = str(usuario_resultado)

                if(usuario_resultado_1 == "()"):
                    cursor.execute(f"INSERT INTO  t_usuarios(usuario) VALUES ('{usuario_seleccionado}')")
                    mysql.connection.commit()

                    cursor.execute(f"SELECT * FROM `t_usuarios` WHERE `usuario` = '{usuario_seleccionado}'")
                    usuario_agregado = cursor.fetchall()
                    print("El usuario agregado es: " + str(usuario_agregado))

                    usuario_id_2 = ""
                    usuario_id = usuario_agregado[0]
                    usuario_id_str = str(usuario_id).split(",")
                    usuario_id_1 = usuario_id_str[0]

                    for caracter in usuario_id_1:
                        if caracter != "," and caracter != "(" and caracter != ")":
                            usuario_id_2 += caracter

                    print("El id de usuario seleccionado es:" + str(usuario_id_2))

                    for atributo_nuevo in atributos_separados_1:
                        cursor.execute(f"INSERT INTO  t_attributes(id_usuario,attribute) VALUES ('{usuario_id_2}','{atributo_nuevo}')")
                        mysql.connection.commit()
        
        print("VALOR DE ID_GLIFO_DEL ERROR QUE OBTENEMOS")
        print(id_glifo,flush=True)
        return render_template("index_ingles.html",conjunto_datos=conjunto_datos,total_datos = total_datos,id_glifo=id_glifo,arreglo_imagenes_procesadas = arreglo_imagenes_procesadas,datos_busqueda = datos_busqueda,atributos = atributos, usuarios=usuarios,atributos_de_usuario=atributos_de_usuario,atributos_lado_derecho=atributos_lado_derecho,username=username,atributos_limpios=atributos_limpios, atributos_personales_caja_derecha_limpios=atributos_personales_caja_derecha_limpios)
    return render_template("usuario_no_inicio.html")
    #'No has iniciado sesión. <a href="/iniciar_sesion/">Iniciar sesión</a>'
    #http://localhost:81/index/default/default/default/default/default/#1 

@app.route('/index_movil/<string:orden_datos>/<string:datos_filtro>/<string:busqueda>/<string:datos_atributes>/<string:dato_usuario>/', methods=['GET', 'POST'])
def index_movil(orden_datos,datos_filtro,busqueda,datos_atributes,dato_usuario):
    if 'username' in session:
        username = session['username']
        valor_de_usuario = str(session['username'])
        print("Ejecucion de index " + str(username),flush=True)
        arreglo_imagenes = list()
        id_glifo = list()
        dato_extra = ""
        atributos_de_usuario = []
        atributos_separados_1 = []
        atributos_lado_derecho = []
        arreglo_imagenes_procesadas = list()
        conjunto_datos = []
        cursor = mysql.connection.cursor()
        conjunto_datos = todos_los_datos(cursor,orden_datos,busqueda,datos_atributes)
        total_datos,dato_extra = total_de_campos(cursor,orden_datos,busqueda,conjunto_datos,datos_atributes)
        
        print("IMPRIMIENDO LA LISTA DE DATOS ATRIBUTOS")
        
        print(datos_atributes,flush=True)
        print(type(datos_atributes),flush=True)
        #condicion para entrar a una u otra
        
        arreglo = datos_atributes.split('-')
        
        
        if arreglo[0] != "final" and arreglo[0] != "eliminar" and arreglo[0] != "num" and arreglo[0] != "eliminar1":
            print("SECCION 1",flush=True)
            conjunto_datos = todos_los_datos(cursor,orden_datos,busqueda,datos_atributes)
           
            total_datos,total_datos_glifos = total_de_campos(cursor,orden_datos,busqueda,conjunto_datos,datos_atributes)
            print("*********************************",flush=True)
            print(conjunto_datos,flush=True)
            print(total_datos,flush=True)
            print(total_datos_glifos,flush=True)

        elif arreglo[0] == "final":
            print("SECCION 2",flush=True)
            conjunto_datos = todos_los_datos_1(cursor,orden_datos,busqueda,datos_atributes)
            print("CONJUNTO_DATOS",flush=True)
            print(conjunto_datos)
            total_datos,total_datos_glifos = total_de_campos(cursor,orden_datos,busqueda,conjunto_datos,datos_atributes)
        
        elif arreglo[0] == "num":
            print("SECCION 3")
            conjunto_datos = todos_los_datos_2(cursor,orden_datos,busqueda,datos_atributes)
            print("CONJUNTO_DATOS",flush=True)
            print(conjunto_datos)
            total_datos,total_datos_glifos = total_de_campos(cursor,orden_datos,busqueda,conjunto_datos,datos_atributes)
            
        elif arreglo[0] == "eliminar":
            print("SECCION 4")
            print("ENTRO EN ESTA CONDICION DE ELIMINAR",flush=True)
            print(datos_atributes,flush=True)
            arreglo = arreglo[1:]
            print("VALORES DE ARREGLO",flush=True)
            print(arreglo,flush=True)
            
            cursor.execute(f"DELETE FROM `atributos_personales` WHERE `usuario` = '{valor_de_usuario}' AND `nombre_atributo` = '{arreglo[0]}';")
            mysql.connection.commit() 
            print("ARREGLO ELIMINADO",flush=True)
            conjunto_datos = todos_los_datos_1(cursor,orden_datos,busqueda,"default")
            total_datos,total_datos_glifos = total_de_campos(cursor,orden_datos,busqueda,conjunto_datos,"default")
        
        elif arreglo[0] == "eliminar1":
            print("SECCION 5")
            print("ENTRO EN ESTA CONDICION DE ELIMINAR1",flush=True)
            print(datos_atributes,flush=True)
            arreglo = arreglo[1:]
            print("VALORES DE ARREGLO",flush=True)
            print(arreglo,flush=True)
            
            cursor.execute(f"DELETE FROM `atributos_personales_por_atributos` WHERE `usuario` = '{valor_de_usuario}' AND `nombre_atributo` = '{arreglo[0]}';")
            mysql.connection.commit() 
            print("ARREGLO ELIMINADO",flush=True)
            conjunto_datos = todos_los_datos_1(cursor,orden_datos,busqueda,"default")
            total_datos,total_datos_glifos = total_de_campos(cursor,orden_datos,busqueda,conjunto_datos,"default")
        
        print("total_Dato" + total_datos,flush=True)
        print("TOTAL DATOS" + total_datos_glifos,flush=True)
        
        # Se sacan las imagenes de la base de datos 
        print("El total de datos es : " + total_datos)
        cursor.execute(f"SELECT id_glifo, graph_glifo  FROM `t_glifos`;")
        data = cursor.fetchall()

        cursor.execute(f"SELECT * FROM `t_attributes`;")
        atributos = cursor.fetchall()

        cursor.execute(f"SELECT * FROM `t_usuarios`;")
        usuarios = cursor.fetchall()
        
        
        # Procesos de la ventana de atributos personalizados
        
        print(valor_de_usuario,flush=True)
        cursor.execute(f"SELECT nombre_atributo,id FROM `atributos_personales` WHERE `usuario` = '{valor_de_usuario}' ")
        atributos_personales = cursor.fetchall()

        print("VALORES_DE_ATRIBUTOS_PERSONALES")
        print(atributos_personales,flush=True)
        
        atributos_limpios = []
        
        for atributo in atributos_personales:
            atributos_limpios.append(atributo)
        
        print("NUEVOS VALORES PROCESADOS",flush=True)
        print(atributos_limpios,flush=True)
        
        # Proceso de la ventana de atributos personalizados derecha
        
        print(valor_de_usuario,flush=True)
        cursor.execute(f"SELECT nombre_atributo,glifo_id FROM `atributos_personales_por_atributos` WHERE `usuario` = '{valor_de_usuario}' ")
        atributos_personales_caja_derecha = cursor.fetchall()

        print("VALORES_DE_ATRIBUTOS_PERSONALES DE LA CAJA DERECHA")
        print(atributos_personales_caja_derecha,flush=True)
        
        atributos_personales_caja_derecha_limpios = []
        
        for atributo in atributos_personales_caja_derecha:
            atributos_personales_caja_derecha_limpios.append(atributo)
        
        print("NUEVOS VALORES PROCESADOS",flush=True)
        print(atributos_personales_caja_derecha_limpios,flush=True)
        
        #**************************************************************************************************
    
        i = 0
        total_datos_imagenes = 0
        while(i < int(dato_extra)):
            arreglo_imagenes.append(data[i][1])
            id_glifo.append(data[i][0])
            image_1 = base64.b64encode(arreglo_imagenes[i])
            arreglo_imagenes_procesadas.append(str(image_1, 'UTF-8'))
            i = i+1
            
            

        ####################################################################################
        
        if dato_usuario != "default":
            cursor.execute(f"SELECT * FROM  `t_attributes` WHERE `id_usuario` = '{dato_usuario}'")
            atributos_de_usuario = cursor.fetchall()
            print(atributos_de_usuario) 

            cursor.execute(f"SELECT * FROM `atributos_guardados` WHERE `id_usuario` = '{dato_usuario}'")
            atributos_lado_derecho = cursor.fetchall()
            print(atributos_lado_derecho)

        if request.method == "POST":
            limpiar = request.form.get("datos_eliminados")
            print(limpiar)
            if limpiar != None:
                if limpiar != "":
                    usuario = limpiar.split("$eliminacion$")
                    usuario_1 = usuario[0]
                    print("LOS ATRIBUTOS A ELIMINAR SON DEL USUARIO: ")
                    print(usuario_1)
                cursor.execute(f"DELETE FROM `atributos_guardados` WHERE `id_usuario` = '{usuario_1}';")
                mysql.connection.commit() 

        if request.method == "POST":
            guardados = request.form.get("datos_guardados")
            print("datos guardados" + str(guardados))
            id_num = ""
            id_usuario_1 = ""
            atributos_repetidos = []
            if guardados != None:

                datos_guardados_separados = guardados.split("$atributos_almacenados$")
                print(datos_guardados_separados)
                usuario_a_guardar = datos_guardados_separados[0]
                print(usuario_a_guardar)
                atributos_a_guardar = datos_guardados_separados[1]
                atributos_a_guardar_separados = atributos_a_guardar.split(",")
                print("Atributos_ agregados: " + str(atributos_a_guardar_separados))

            
                cursor.execute(f"DELETE FROM `atributos_guardados` WHERE `id_usuario` = '{usuario_a_guardar}';")
                mysql.connection.commit()  
                time.sleep(1)
                
                cursor.execute(f"SELECT id FROM `atributos_guardados`;")
                id_almacenados = cursor.fetchall()
                print("Atributos ya almacenados" + str(id_almacenados))

                for id_numero in atributos_a_guardar_separados:
                    print("El numero de id_numero es: " + str(id_numero))
                    for numero_id_almacenado in id_almacenados:
                        print("El numero del ciclo almacenado es" + str(numero_id_almacenado[0]))
                    if str(id_numero) == str(numero_id_almacenado[0]):
                            atributos_repetidos.append(id_numero)
                

                print("Los atributos repetidos son: " + str(atributos_repetidos))

                for atributos_repetidos_1 in atributos_repetidos:
                    atributos_a_guardar_separados.remove(atributos_repetidos_1)


                print("La lista resultante es: " + str(atributos_a_guardar_separados))

                if atributos_a_guardar_separados != ['']:
                    for atributos in atributos_a_guardar_separados:
                        cursor.execute(f"SELECT id_attribute FROM `t_attributes` WHERE `id_attribute` = '{atributos}';")
                        id = cursor.fetchall()
                        cursor.execute(f"SELECT id_usuario FROM `t_attributes` WHERE `id_attribute` = '{atributos}';")
                        id_usuario = cursor.fetchall()
                        cursor.execute(f"SELECT attribute FROM `t_attributes` WHERE `id_attribute` = '{atributos}';")
                        atributos = cursor.fetchall()

                        print(id[0][0])
                        print(id_usuario[0][0])
                        print(atributos[0][0])
                        
                        cursor.execute(f"INSERT INTO atributos_guardados(id,id_usuario,atributo) VALUES ('{id[0][0]}','{id_usuario[0][0]}','{atributos[0][0]}')")
                        mysql.connection.commit()

        if request.method == "POST":
            usuario = request.form.get("todo")
            
            if usuario != None:
                print("EL VALOR RETORNADO ES: " + str(usuario))
                datos_usuario_separado = usuario.split("$atributos$")
                print("El valor de usuario es:" + str(datos_usuario_separado[0]))
                usuario_seleccionado = str(datos_usuario_separado[0])
                print("El valor de atributos es:" + str(datos_usuario_separado[1]))

                atributos_separados = datos_usuario_separado[1].split(",")
                print("Los atributos separados son: " + str(atributos_separados))

                for atributo in atributos_separados:
                    if atributo != "":
                        atributos_separados_1.append(atributo)
                
                cursor.execute(f"SELECT * FROM `t_usuarios` WHERE `usuario` = '{usuario_seleccionado}'")
                usuario_resultado = cursor.fetchall()
                
                print("El valor del usuario es: " + str(usuario_resultado))
                usuario_resultado_1 = str(usuario_resultado)

                if(usuario_resultado_1 == "()"):
                    cursor.execute(f"INSERT INTO  t_usuarios(usuario) VALUES ('{usuario_seleccionado}')")
                    mysql.connection.commit()

                    cursor.execute(f"SELECT * FROM `t_usuarios` WHERE `usuario` = '{usuario_seleccionado}'")
                    usuario_agregado = cursor.fetchall()
                    print("El usuario agregado es: " + str(usuario_agregado))

                    usuario_id_2 = ""
                    usuario_id = usuario_agregado[0]
                    usuario_id_str = str(usuario_id).split(",")
                    usuario_id_1 = usuario_id_str[0]

                    for caracter in usuario_id_1:
                        if caracter != "," and caracter != "(" and caracter != ")":
                            usuario_id_2 += caracter

                    print("El id de usuario seleccionado es:" + str(usuario_id_2))

                    for atributo_nuevo in atributos_separados_1:
                        cursor.execute(f"INSERT INTO  t_attributes(id_usuario,attribute) VALUES ('{usuario_id_2}','{atributo_nuevo}')")
                        mysql.connection.commit()
                
        return render_template("index_movil.html",conjunto_datos=conjunto_datos,total_datos = total_datos,id_glifo=id_glifo,arreglo_imagenes_procesadas = arreglo_imagenes_procesadas,busqueda = busqueda,atributos = atributos,usuarios=usuarios,atributos_de_usuario=atributos_de_usuario,atributos_lado_derecho=atributos_lado_derecho,valor_de_usuario=valor_de_usuario,atributos_limpios=atributos_limpios,atributos_personales_caja_derecha_limpios=atributos_personales_caja_derecha_limpios)
    return render_template("usuario_no_inicio.html")

@app.route('/index_movil_ingles/<string:orden_datos>/<string:datos_filtro>/<string:busqueda>/<string:datos_atributes>/<string:dato_usuario>/', methods=['GET', 'POST'])
def index_movil_ingles(orden_datos,datos_filtro,busqueda,datos_atributes,dato_usuario):
    if 'username' in session:
        username = session['username']
        valor_de_usuario = str(session['username'])
        print("Ejecucion de index " + str(username),flush=True)
        arreglo_imagenes = list()
        id_glifo = list()
        dato_extra = ""
        atributos_de_usuario = []
        atributos_separados_1 = []
        atributos_lado_derecho = []
        arreglo_imagenes_procesadas = list()
        conjunto_datos = []
        cursor = mysql.connection.cursor()
        conjunto_datos = todos_los_datos(cursor,orden_datos,busqueda,datos_atributes)
        total_datos,dato_extra = total_de_campos(cursor,orden_datos,busqueda,conjunto_datos,datos_atributes)
        
        print("IMPRIMIENDO LA LISTA DE DATOS ATRIBUTOS")
        
        print(datos_atributes,flush=True)
        print(type(datos_atributes),flush=True)
        #condicion para entrar a una u otra
        
        arreglo = datos_atributes.split('-')
        
        
        if arreglo[0] != "final" and arreglo[0] != "eliminar" and arreglo[0] != "num" and arreglo[0] != "eliminar1":
            print("SECCION 1",flush=True)
            conjunto_datos = todos_los_datos(cursor,orden_datos,busqueda,datos_atributes)
           
            total_datos,total_datos_glifos = total_de_campos(cursor,orden_datos,busqueda,conjunto_datos,datos_atributes)
            print("*********************************",flush=True)
            print(conjunto_datos,flush=True)
            print(total_datos,flush=True)
            print(total_datos_glifos,flush=True)

        elif arreglo[0] == "final":
            print("SECCION 2",flush=True)
            conjunto_datos = todos_los_datos_1(cursor,orden_datos,busqueda,datos_atributes)
            print("CONJUNTO_DATOS",flush=True)
            print(conjunto_datos)
            total_datos,total_datos_glifos = total_de_campos(cursor,orden_datos,busqueda,conjunto_datos,datos_atributes)
        
        elif arreglo[0] == "num":
            print("SECCION 3")
            conjunto_datos = todos_los_datos_2(cursor,orden_datos,busqueda,datos_atributes)
            print("CONJUNTO_DATOS",flush=True)
            print(conjunto_datos)
            total_datos,total_datos_glifos = total_de_campos(cursor,orden_datos,busqueda,conjunto_datos,datos_atributes)
            
        elif arreglo[0] == "eliminar":
            print("SECCION 4")
            print("ENTRO EN ESTA CONDICION DE ELIMINAR",flush=True)
            print(datos_atributes,flush=True)
            arreglo = arreglo[1:]
            print("VALORES DE ARREGLO",flush=True)
            print(arreglo,flush=True)
            
            cursor.execute(f"DELETE FROM `atributos_personales` WHERE `usuario` = '{valor_de_usuario}' AND `nombre_atributo` = '{arreglo[0]}';")
            mysql.connection.commit() 
            print("ARREGLO ELIMINADO",flush=True)
            conjunto_datos = todos_los_datos_1(cursor,orden_datos,busqueda,"default")
            total_datos,total_datos_glifos = total_de_campos(cursor,orden_datos,busqueda,conjunto_datos,"default")
        
        elif arreglo[0] == "eliminar1":
            print("SECCION 5")
            print("ENTRO EN ESTA CONDICION DE ELIMINAR1",flush=True)
            print(datos_atributes,flush=True)
            arreglo = arreglo[1:]
            print("VALORES DE ARREGLO",flush=True)
            print(arreglo,flush=True)
            
            cursor.execute(f"DELETE FROM `atributos_personales_por_atributos` WHERE `usuario` = '{valor_de_usuario}' AND `nombre_atributo` = '{arreglo[0]}';")
            mysql.connection.commit() 
            print("ARREGLO ELIMINADO",flush=True)
            conjunto_datos = todos_los_datos_1(cursor,orden_datos,busqueda,"default")
            total_datos,total_datos_glifos = total_de_campos(cursor,orden_datos,busqueda,conjunto_datos,"default")
        
        print("total_Dato" + total_datos,flush=True)
        print("TOTAL DATOS" + total_datos_glifos,flush=True)
        
        # Se sacan las imagenes de la base de datos 
        print("El total de datos es : " + total_datos)
        cursor.execute(f"SELECT id_glifo, graph_glifo  FROM `t_glifos`;")
        data = cursor.fetchall()

        cursor.execute(f"SELECT * FROM `t_attributes`;")
        atributos = cursor.fetchall()

        cursor.execute(f"SELECT * FROM `t_usuarios`;")
        usuarios = cursor.fetchall()
        
        
        # Procesos de la ventana de atributos personalizados
        
        print(valor_de_usuario,flush=True)
        cursor.execute(f"SELECT nombre_atributo,id FROM `atributos_personales` WHERE `usuario` = '{valor_de_usuario}' ")
        atributos_personales = cursor.fetchall()

        print("VALORES_DE_ATRIBUTOS_PERSONALES")
        print(atributos_personales,flush=True)
        
        atributos_limpios = []
        
        for atributo in atributos_personales:
            atributos_limpios.append(atributo)
        
        print("NUEVOS VALORES PROCESADOS",flush=True)
        print(atributos_limpios,flush=True)
        
        # Proceso de la ventana de atributos personalizados derecha
        
        print(valor_de_usuario,flush=True)
        cursor.execute(f"SELECT nombre_atributo,glifo_id FROM `atributos_personales_por_atributos` WHERE `usuario` = '{valor_de_usuario}' ")
        atributos_personales_caja_derecha = cursor.fetchall()

        print("VALORES_DE_ATRIBUTOS_PERSONALES DE LA CAJA DERECHA")
        print(atributos_personales_caja_derecha,flush=True)
        
        atributos_personales_caja_derecha_limpios = []
        
        for atributo in atributos_personales_caja_derecha:
            atributos_personales_caja_derecha_limpios.append(atributo)
        
        print("NUEVOS VALORES PROCESADOS",flush=True)
        print(atributos_personales_caja_derecha_limpios,flush=True)
        
        #**************************************************************************************************
    
        i = 0
        total_datos_imagenes = 0
        while(i < int(dato_extra)):
            arreglo_imagenes.append(data[i][1])
            id_glifo.append(data[i][0])
            image_1 = base64.b64encode(arreglo_imagenes[i])
            arreglo_imagenes_procesadas.append(str(image_1, 'UTF-8'))
            i = i+1
            
            

        ####################################################################################
        
        if dato_usuario != "default":
            cursor.execute(f"SELECT * FROM  `t_attributes` WHERE `id_usuario` = '{dato_usuario}'")
            atributos_de_usuario = cursor.fetchall()
            print(atributos_de_usuario) 

            cursor.execute(f"SELECT * FROM `atributos_guardados` WHERE `id_usuario` = '{dato_usuario}'")
            atributos_lado_derecho = cursor.fetchall()
            print(atributos_lado_derecho)

        if request.method == "POST":
            limpiar = request.form.get("datos_eliminados")
            print(limpiar)
            if limpiar != None:
                if limpiar != "":
                    usuario = limpiar.split("$eliminacion$")
                    usuario_1 = usuario[0]
                    print("LOS ATRIBUTOS A ELIMINAR SON DEL USUARIO: ")
                    print(usuario_1)
                cursor.execute(f"DELETE FROM `atributos_guardados` WHERE `id_usuario` = '{usuario_1}';")
                mysql.connection.commit() 

        if request.method == "POST":
            guardados = request.form.get("datos_guardados")
            print("datos guardados" + str(guardados))
            id_num = ""
            id_usuario_1 = ""
            atributos_repetidos = []
            if guardados != None:

                datos_guardados_separados = guardados.split("$atributos_almacenados$")
                print(datos_guardados_separados)
                usuario_a_guardar = datos_guardados_separados[0]
                print(usuario_a_guardar)
                atributos_a_guardar = datos_guardados_separados[1]
                atributos_a_guardar_separados = atributos_a_guardar.split(",")
                print("Atributos_ agregados: " + str(atributos_a_guardar_separados))

            
                cursor.execute(f"DELETE FROM `atributos_guardados` WHERE `id_usuario` = '{usuario_a_guardar}';")
                mysql.connection.commit()  
                time.sleep(1)
                
                cursor.execute(f"SELECT id FROM `atributos_guardados`;")
                id_almacenados = cursor.fetchall()
                print("Atributos ya almacenados" + str(id_almacenados))

                for id_numero in atributos_a_guardar_separados:
                    print("El numero de id_numero es: " + str(id_numero))
                    for numero_id_almacenado in id_almacenados:
                        print("El numero del ciclo almacenado es" + str(numero_id_almacenado[0]))
                    if str(id_numero) == str(numero_id_almacenado[0]):
                            atributos_repetidos.append(id_numero)
                

                print("Los atributos repetidos son: " + str(atributos_repetidos))

                for atributos_repetidos_1 in atributos_repetidos:
                    atributos_a_guardar_separados.remove(atributos_repetidos_1)


                print("La lista resultante es: " + str(atributos_a_guardar_separados))

                if atributos_a_guardar_separados != ['']:
                    for atributos in atributos_a_guardar_separados:
                        cursor.execute(f"SELECT id_attribute FROM `t_attributes` WHERE `id_attribute` = '{atributos}';")
                        id = cursor.fetchall()
                        cursor.execute(f"SELECT id_usuario FROM `t_attributes` WHERE `id_attribute` = '{atributos}';")
                        id_usuario = cursor.fetchall()
                        cursor.execute(f"SELECT attribute FROM `t_attributes` WHERE `id_attribute` = '{atributos}';")
                        atributos = cursor.fetchall()

                        print(id[0][0])
                        print(id_usuario[0][0])
                        print(atributos[0][0])
                        
                        cursor.execute(f"INSERT INTO atributos_guardados(id,id_usuario,atributo) VALUES ('{id[0][0]}','{id_usuario[0][0]}','{atributos[0][0]}')")
                        mysql.connection.commit()

        if request.method == "POST":
            usuario = request.form.get("todo")
            
            if usuario != None:
                print("EL VALOR RETORNADO ES: " + str(usuario))
                datos_usuario_separado = usuario.split("$atributos$")
                print("El valor de usuario es:" + str(datos_usuario_separado[0]))
                usuario_seleccionado = str(datos_usuario_separado[0])
                print("El valor de atributos es:" + str(datos_usuario_separado[1]))

                atributos_separados = datos_usuario_separado[1].split(",")
                print("Los atributos separados son: " + str(atributos_separados))

                for atributo in atributos_separados:
                    if atributo != "":
                        atributos_separados_1.append(atributo)
                
                cursor.execute(f"SELECT * FROM `t_usuarios` WHERE `usuario` = '{usuario_seleccionado}'")
                usuario_resultado = cursor.fetchall()
                
                print("El valor del usuario es: " + str(usuario_resultado))
                usuario_resultado_1 = str(usuario_resultado)

                if(usuario_resultado_1 == "()"):
                    cursor.execute(f"INSERT INTO  t_usuarios(usuario) VALUES ('{usuario_seleccionado}')")
                    mysql.connection.commit()

                    cursor.execute(f"SELECT * FROM `t_usuarios` WHERE `usuario` = '{usuario_seleccionado}'")
                    usuario_agregado = cursor.fetchall()
                    print("El usuario agregado es: " + str(usuario_agregado))

                    usuario_id_2 = ""
                    usuario_id = usuario_agregado[0]
                    usuario_id_str = str(usuario_id).split(",")
                    usuario_id_1 = usuario_id_str[0]

                    for caracter in usuario_id_1:
                        if caracter != "," and caracter != "(" and caracter != ")":
                            usuario_id_2 += caracter

                    print("El id de usuario seleccionado es:" + str(usuario_id_2))

                    for atributo_nuevo in atributos_separados_1:
                        cursor.execute(f"INSERT INTO  t_attributes(id_usuario,attribute) VALUES ('{usuario_id_2}','{atributo_nuevo}')")
                        mysql.connection.commit()
                
        return render_template("index_movil_ingles.html",conjunto_datos=conjunto_datos,total_datos = total_datos,id_glifo=id_glifo,arreglo_imagenes_procesadas = arreglo_imagenes_procesadas,busqueda = busqueda,atributos = atributos,usuarios=usuarios,atributos_de_usuario=atributos_de_usuario,atributos_lado_derecho=atributos_lado_derecho,valor_de_usuario=valor_de_usuario,atributos_limpios=atributos_limpios,atributos_personales_caja_derecha_limpios=atributos_personales_caja_derecha_limpios)
    return render_template("usuario_no_inicio.html")

@app.route('/imagenes.html')
def imagenes():
    if 'username' in session:
        username = session['username']
        valor_de_usuario = str(session['username'])
        arreglo_imagenes = list()
        id_glifo = list()
        total_1 = ""
        arreglo_imagenes_procesadas = list()
        cursor = mysql.connection.cursor()
        conjunto_datos = []
        conjunto_datos_1 = []
        conjunto_datos = todos_los_datos(cursor,"thomson","default","default")
        conjunto_datos_1 = todos_los_datos(cursor,"thomson","default","default")
        total_1,total_datos = total_de_campos(cursor,"thomson","default","default","default")
        # Se sacan las imagenes de la base de datos 
        print("TOTAL DE DATOS EN IMAGENES")
        print(total_datos)
        print(conjunto_datos_1)
        cursor.execute(f"SELECT id_glifo, graph_glifo  FROM `t_glifos`;")
        data = cursor.fetchall()
        i = 0
        total_datos_imagenes = 0
        while(i < int(total_datos)):
            arreglo_imagenes.append(data[i][1])
            id_glifo.append(data[i][0])
            image_1 = base64.b64encode(arreglo_imagenes[i])
            arreglo_imagenes_procesadas.append(str(image_1, 'UTF-8'))
            i = i+1
        print(id_glifo)
        print(len(id_glifo))
        return render_template("imagenes.html",conjunto_datos=conjunto_datos,total_datos = total_datos,id_glifo=id_glifo,arreglo_imagenes_procesadas = arreglo_imagenes_procesadas)
    return render_template("usuario_no_inicio.html")

@app.route('/imagenes_invitado_ingles.html')
def imagenes_ingles():
    arreglo_imagenes = list()
    id_glifo = list()
    total_1 = ""
    arreglo_imagenes_procesadas = list()
    cursor = mysql.connection.cursor()
    conjunto_datos = todos_los_datos(cursor,"thomson","default","default")
    conjunto_datos_1 = todos_los_datos(cursor,"thomson","default","default")
    total_1,total_datos = total_de_campos(cursor,"thomson","default","default","default")
    # Se sacan las imagenes de la base de datos 
    print("TOTAL DE DATOS EN IMAGENES")
    print(total_datos)
    print(conjunto_datos_1)
    cursor.execute(f"SELECT id_glifo, graph_glifo  FROM `t_glifos`;")
    data = cursor.fetchall()
    i = 0
    total_datos_imagenes = 0
    while(i < int(total_datos)):
        arreglo_imagenes.append(data[i][1])
        id_glifo.append(data[i][0])
        image_1 = base64.b64encode(arreglo_imagenes[i])
        arreglo_imagenes_procesadas.append(str(image_1, 'UTF-8'))
        i = i+1
    print(id_glifo)
    print(len(id_glifo))
    return render_template("imagenes_invitado_ingles.html",conjunto_datos=conjunto_datos,total_datos = total_datos,id_glifo=id_glifo,arreglo_imagenes_procesadas = arreglo_imagenes_procesadas)

@app.route('/imagenes_invitado.html')
def imagenes_invitado():
    arreglo_imagenes = list()
    id_glifo = list()
    total_1 = ""
    arreglo_imagenes_procesadas = list()
    cursor = mysql.connection.cursor()
    conjunto_datos = todos_los_datos(cursor,"thomson","default","default")
    conjunto_datos_1 = todos_los_datos(cursor,"thomson","default","default")
    total_1,total_datos = total_de_campos(cursor,"thomson","default","default","default")
    # Se sacan las imagenes de la base de datos 
    print("TOTAL DE DATOS EN IMAGENES")
    print(total_datos)
    print(conjunto_datos_1)
    cursor.execute(f"SELECT id_glifo, graph_glifo  FROM `t_glifos`;")
    data = cursor.fetchall()
    i = 0
    total_datos_imagenes = 0
    while(i < int(total_datos)):
        arreglo_imagenes.append(data[i][1])
        id_glifo.append(data[i][0])
        image_1 = base64.b64encode(arreglo_imagenes[i])
        arreglo_imagenes_procesadas.append(str(image_1, 'UTF-8'))
        i = i+1
    print(id_glifo)
    print(len(id_glifo))
    return render_template("imagenes_invitado.html",conjunto_datos=conjunto_datos,total_datos = total_datos,id_glifo=id_glifo,arreglo_imagenes_procesadas = arreglo_imagenes_procesadas)


if __name__ == "__main__":
    app.run(debug=True, port=5500)  #El modelo debug nos permite actualizar nuestra consola para evitar detener el servidor, ahorra tiempo
