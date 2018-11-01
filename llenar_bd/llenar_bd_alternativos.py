import sqlite3

conn = sqlite3.connect('performance_dc930.db')

c = conn.cursor()

while True:
	distancia = input("Distancia: ")
	nivel_optimo = input("nivel óptimo: ")
	tiempo = input("tiempo: ")
	combustible = input("combustible: ")
	tas = input("TAS: ")
	c.execute("INSERT INTO combustible_alterno(distancia,nivel_optimo,tiempo,combustible,true_air_speed) VALUES (?,?,?,?,?)",[distancia,nivel_optimo,tiempo,combustible,tas])
	conn.commit()
	print("------------------------")