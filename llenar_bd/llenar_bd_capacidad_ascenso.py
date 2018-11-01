import sqlite3

conn = sqlite3.connect('performance_dc930.db')

c = conn.cursor()

c.execute('SELECT * FROM altura')
alturas = c.fetchall()

c.execute('SELECT * FROM isa')
isas = c.fetchall()

while True:
	for altura in alturas:
		for isa in isas:
			print("Altura:",altura[1])
			print("ISA:",isa[1])
			peso = input('peso: ')
			c.execute("INSERT INTO capacidad_de_ascenso(altura,isa,peso) VALUES ((SELECT id FROM altura WHERE altura = ? ),(SELECT id FROM isa WHERE isa = ?),?)",[altura[1],isa[1],peso])
			conn.commit()
			print("------------------------")
