import sqlite3

conn = sqlite3.connect('performance_dc930.db')

c = conn.cursor()

c.execute('SELECT * FROM altura')
alturas = c.fetchall()

c.execute('SELECT * FROM distancia')
distancias = c.fetchall()

c.execute('SELECT * FROM vientos')
vientos = c.fetchall()

"""

print("------- alturas ---------")
for altura in alturas:
	print(altura[1])

print("------- distancias ---------")
for distancia in distancias:
	print(distancia[1])

print("------- vientos ---------")
for velocidad in vientos:
	print(velocidad[1])

"""


for altura in alturas:
	for distancia in distancias:
		for velocidad in reversed(vientos):
			print("Ingrese los datos para:\n*altura:",altura[1],'\n*distancia:',distancia[1],'\n*vientos,',velocidad[1])
			tiempo = input("Tiempo de vuelo en formato HH:MM o N: ")
			if len(tiempo) > 1:
				combustible = input("Ingrese el combustible \"x 1000\": ")
				c.execute("INSERT INTO tiempo_combustible (tiempo, combustible, altura, distancia, vientos) VALUES(?,?,(SELECT id FROM altura WHERE altura = ?),(SELECT id FROM distancia WHERE distancia = ?),(SELECT id from vientos WHERE velocidad = ?))",[tiempo, combustible,altura[1],distancia[1],velocidad[1]])
				conn.commit()

print("completado")
