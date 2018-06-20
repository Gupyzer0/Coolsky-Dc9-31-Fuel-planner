import sys

from PyQt5 import QtSql

db = QtSql.QSqlDatabase.addDatabase("QSQLITE","planeadorDC931")
db.setDatabaseName("performance_dc930.db")

bdatos_ok = db.open()

if not bdatos_ok:
	print("conexion fallida con la base de datos")
	sys.exit()	
	
else:
	query = QtSql.QSqlQuery(db)
	
class baseDatos():
	
	@staticmethod
	def calcularCombustibleRuta(altura, distancia, vientos):
		query.prepare(""" SELECT * FROM tiempo_combustible WHERE altura = (SELECT id FROM altura WHERE altura = ?) AND distancia = (SELECT id FROM distancia WHERE distancia = ? ORDER BY id DESC limit 1) AND vientos = (SELECT id FROM vientos WHERE velocidad = ?) """)
		query.addBindValue(altura)
		query.addBindValue(distancia)
		query.addBindValue(vientos)

		if query.exec_():
			while query.next():
				return {'combustible':query.value(2),'tiempo':query.value(1)}
		else:
			return False

	@staticmethod
	def calcularCombustibleAlterno(distanciaAlterno):
		query.prepare(""" SELECT * FROM combustible_alterno WHERE distancia >= ? ORDER BY distancia limit 1 """)
		query.addBindValue(distanciaAlterno)

		if query.exec_():
			while query.next():
				return {'combustible': query.value(4), 'nivel_optimo': query.value(2), 'tiempo': query.value(3), 'TAS': query.value(5)}
		else:
			return False
