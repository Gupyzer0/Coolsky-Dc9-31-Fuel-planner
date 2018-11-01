import sys, sqlite3
from datetime import timedelta

conn = sqlite3.connect('performance_dc930.db')
c = conn.cursor()

#Variables de peso
MRW  = 106000
MTOW = 105000
MLW  = 95300
MZFW = 87000
SOW  = 61252

#Variables de combustible
combustible_taxeo = 600 #300 libras por estacion
combustible_reserva_final = 4000 # :45 minutos, FAA
combustible_minimo_vuelo = 8040 # Minimo con el que se puede despachar una aeronave
combustible_app_intrumental = 650
combustible_hora_extra = 2500 #1 hora del combustible extra es igual a 2500 libras, holding flaps up +10 Vmaniobra
tiempo_reserva_final = datetime.strptime('00:45', '%H:%M')

distancia_vuelo 	= int(input("Distancia del vuelo:"))
altura_vuelo 		= int(input("Altura del vuelo:"))
carga_vuelo     	= int(input("Carga del vuelo:"))
viento_vuelo 		= int(input("Vientos:"))
distancia_alterno 	= int(input("Distancia al alterno:"))

ZFW = SOW + carga_vuelo #peso sin combustible

if ZFW > MZFW:
	print("El ZFW calculado:", ZFW ,"es excesivo. Máximo:", MZFW)
	sys.exit()

c.execute('SELECT * FROM tiempo_combustible WHERE altura = (SELECT id FROM altura WHERE altura = ?) AND distancia = (SELECT id FROM distancia WHERE distancia >= ? ORDER BY id DESC limit 1) AND vientos = (SELECT id FROM vientos WHERE velocidad = ?)',[altura_vuelo, distancia_vuelo, viento_vuelo])
planeacion_ruta = c.fetchall()

c.execute('SELECT * FROM combustible_alterno WHERE distancia >= ? ORDER BY distancia limit 1',[distancia_alterno])
planeacion_alterno = c.fetchall()

print(planeacion_alterno)

#ruta
combustible_ruta = float(planeacion_ruta[0][2]) * 1000
tiempo_ruta = datetime.strptime(planeacion_ruta[0][1], '%H:%M')

#alterno
combustible_alterno = float(planeacion_alterno[0][4])
tiempo_alterno = datetime.strptime(planeacion_alterno[0][3], '%H:%M')

combustible_total = combustible_ruta + combustible_alterno + combustible_app_intrumental + combustible_taxeo + combustible_reserva_final

TOW = ZFW + combustible_total

if TOW > MTOW:
	print("El TOW calculado:", TOW ,"es excesivo. Maximo:",MTOW)
	sys.exit()

print("----------------------------------------------------")
print("Tiempo en ruta:", tiempo_ruta.strftime('%H:%M'))
print("Tiempo alterno:", tiempo_alterno.strftime('%H:%M'))
print("Reserva FAA:", tiempo_reserva_final.strftime('%H:%M'))
print("tiempo Combustible a bordo: TODO")
print("----------------------------------------------------")
print("Combustible para la ruta:",combustible_ruta)
print("Combustible alterno:", combustible_alterno)
print("Aproximacion instrumental:", combustible_app_intrumental)
print("Taxeo:", combustible_taxeo)
print("Reserva Final:", combustible_reserva_final)
print("Combustible Total:", combustible_total )
print("----------------------------------------------------")
print("")
