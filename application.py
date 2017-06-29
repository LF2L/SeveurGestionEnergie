#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, request, json, render_template
from datetime import date
import time
from flaskext.mysql import MySQL
import logging
from logging.handlers import RotatingFileHandler
import RPi.GPIO as GPIO
import json

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'projetLinkyByMaker'
app.config['MYSQL_DATABASE_DB'] = 'IoEDb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

feedBackFc = { "monitor" : monito,
}
    
@app.route('/')
def accueil():
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM `connected_obj`")
		IoTdata = cursor.fetchall()
		if IoTdata is None:
			info = "none"
			app.logger.error("[accueil][0] ["+time.asctime( time.localtime(time.time()) )+"] no data encountred")
		else:
			app.logger.info("[accueil][1] ["+time.asctime( time.localtime(time.time()) )+"] connexion ")
			#for row in IoTdata:	
		return render_template('accueil.html', IoTs = IoTdata)
	except:
		app.logger.error("[accueil][2] ["+time.asctime( time.localtime(time.time()) )+"] error during the access to the DB")
		return render_template('accueil.html', IoTs = IoTdata)
    
#request.remote_addr

@app.route('/settings/')
def settings():
	return render_template('settings.html')
	
@app.route('/signin/', methods=['POST'])
def signin():
#usermail = request.args.get('inputEmail')
	usermail = request.form['inputEmail']
	app.logger.info("[signin] ["+time.asctime( time.localtime(time.time()) )+"] variable email input"+usermail)
	password = request.form['inputPassword']
	app.logger.info("[signin] ["+time.asctime( time.localtime(time.time()) )+"] variable password input"+password)
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("SELECT * from user where mail='" + usermail + "' and password='" + password + "'")
		data = cursor.fetchone()
		if data is None:
			app.logger.error("[signin] ["+time.asctime( time.localtime(time.time()) )+"] wrong username or password")
			return "Username or Password is wrong"
		else:
			app.logger.info("[signin] ["+time.asctime( time.localtime(time.time()) )+"] connexion "+usermail)
			return "Logged in successfully"
	except:
		app.logger.error("[signin] ["+time.asctime( time.localtime(time.time()) )+"] error during the access to the DB")
	finally:
		cursor.close()
		conn.close()

@app.route('/dataquisition/')
def dataquisition():
	#fonction to save the information from the nRF24 chip 
	return 0
	
@app.route('/objectport/',methods=['POST'])
def objectport():
	ip = request.get_json().get('ip_address', '')
	id_oc = request.get_json().get('id', '')
	device = request.get_json().get('device_type', '')
	nb_soc = request.get_json().get('soc', '')
	data = {"ip": ip, "id": id_oc, "device": device, "nb_soc": nb_soc}
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM connected_obj WHERE ip_address='" + id_oc + "' ")
		data = cursor.fetchone()
		if data is None:
			app.logger.error("[objectport] ["+time.asctime( time.localtime(time.time()) )+"] non existing ip addres --> creation in bdd")
			query = "INSERT INTO connected_obj(ip_address,device_type,nb_soc) VALUES(%s,%s,%s)"
			args = (ip,device,nd_soc)
			cursor.execute(query, args)
			if cursor.lastrowid:
				print('last insert id', cursor.lastrowid)
			else:
				print('last insert id not found')
			conn.commit()
			return render_template('object.html', info1= data)
		else:
			app.logger.info("[objectport] ["+time.asctime( time.localtime(time.time()) )+"] connexion "+usermail)
			return render_template('object.html', info1= data)
		# feedback
		jsonFeed = feedBackFc[device]();
	except:
		app.logger.error("[objectport] ["+time.asctime( time.localtime(time.time()) )+"] error")
	finally:
		cursor.close()
		conn.close()
		return render_template('object.html', info1= data)
	


@app.route('/monitoring/')
def monitoring():
	try:
		con = mysql.connect()
		cursor = con.cursor()
		cursor.execute("SELECT * FROM `raw_histo` ORDER BY id DESC LIMIT 1")
		data = cursor.fetchone()
		if data is None:
			info = "none"
			app.logger.error("[monitoring] ["+time.asctime( time.localtime(time.time()) )+"] no data encountred")
		else:
			info = json.dumps({"IINST":data[12],"IMAX":data[13],"ISOUSC":data[3],"PTEC":data[10]})
			app.logger.info("[monitoring] ["+time.asctime( time.localtime(time.time()) )+"] connexion ")
		cursor.close()
		return render_template('monitoring.html', infoJSON = info)
	except:
		app.logger.error("[monitoring] ["+time.asctime( time.localtime(time.time()) )+"] error during the access to the DB")
		return render_template('monitoring.html', infoJSON = "DB error")

def monito():
	try:
		con = mysql.connect()
		cursor = con.cursor()
		cursor.execute("SELECT * FROM `raw_histo` ORDER BY id DESC LIMIT 1")
		data = cursor.fetchone()
		if data is None:
			info = "none"
			app.logger.error("[monito] ["+time.asctime( time.localtime(time.time()) )+"] no data encountred")
		else:
			info = json.dumps({"IINST":data[12],"IMAX":data[13],"ISOUSC":data[3],"PTEC":data[10]})
			app.logger.info("[monito] ["+time.asctime( time.localtime(time.time()) )+"] connexion ")
		cursor.close()
		return info
	except:
		app.logger.error("[monito] ["+time.asctime( time.localtime(time.time()) )+"] error during the access to the DB")
		return info
	

@app.route('/delesting/')
def delesting():
	
	return

@app.errorhandler(404)
def ma_page_erreur(error):
	return render_template('error.html', titre="Error !", code_error =error.code)


if __name__ == '__main__':
	# initialize the log handler
    logHandler = RotatingFileHandler('info.log', maxBytes=1000, backupCount=1)
    # set the log handler level
    logHandler.setLevel(logging.INFO)

    # set the app logger level
    app.logger.setLevel(logging.INFO)

    app.logger.addHandler(logHandler)
    app.run(debug=False)
    #port = 8000 #the custom port you want
    app.run(host='0.0.0.0')
    #app.run(port='5050')
