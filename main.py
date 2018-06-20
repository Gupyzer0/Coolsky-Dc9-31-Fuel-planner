import sys

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt

from datetime import timedelta

from interfaz import Ui_MainWindow
from bdatos import baseDatos

class FuelPlanner(QtWidgets.QMainWindow):
	def __init__(self, parent = None):
		super(FuelPlanner,self).__init__(parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.msgBox = QtWidgets.QMessageBox()
		#Pesos
		self.MRW = 106000
		self.MTOW = 105000
		self.MZFW = 87000
		self.SOW = 61252
		self.MLW = 95300
		#inicializando aeronave vacia
		self.ZFW = 61252
		self.TOW = 61252
		#inicializando combustible
		self.combustible_minimo_vuelo = 8040
		self.combustible_maximo = 24649
		self.combustible_reserva_final = 4000
		
		self.tiempo_reserva_final = timedelta(minutes = 45)
		self.tiempo_extra = timedelta()

		self.ui.timeEdit_reserva_final.setTime(QtCore.QTime(0,45))
		self.ui.lineEdit_num_app.setText("650")#por defecto una sola app instrumental
		self.ui.comboBox_num_app.currentIndexChanged.connect(self.calcular_combustible_apps)
		self.ui.spinBox_extra.valueChanged.connect(self.calcular_tiempo_extra)
		self.ui.pushButton.clicked.connect(self.calcular)

	def calcular_combustible_apps(self):
		combustible_app_instrumental = int(self.ui.comboBox_num_app.currentText()) * 650
		self.ui.spinBox_num_app.setValue(combustible_app_instrumental)

	def calcular_tiempo_extra(self):
		combustible_extra = self.ui.spinBox_extra.value()
		tiempo_extra_minutos = combustible_extra * 60 / 2700
		self.tiempo_extra = timedelta(minutes = tiempo_extra_minutos)
		tiempo = QtCore.QTime(int(tiempo_extra_minutos/60), tiempo_extra_minutos % 60)
		self.ui.timeEdit_extra.setTime(tiempo)

	def calcular(self):
		#TODO obtener valores desde la interfaz
		combustible_extra = self.ui.spinBox_extra.value()
		combustible_taxeo = self.ui.spinBox_taxeo.value()
		combustible_app_instrumental = int(self.ui.comboBox_num_app.currentText()) * 650 #650 por cada app por instrumentos
		
		distancia_vuelo = self.ui.comboBox_distancia.currentText()
		distancia_alterno = self.ui.comboBox_distancia_alterno.currentText()
		altura_vuelo = self.ui.comboBox_altura.currentText()
		viento_vuelo = self.ui.comboBox_viento.currentText()
		
		carga_vuelo = self.ui.spinBox_payload.value()

		self.ZFW = self.SOW + carga_vuelo

		plan_ruta = baseDatos.calcularCombustibleRuta(altura_vuelo,distancia_vuelo,viento_vuelo)
		
		if not plan_ruta:
			self.msgBox.setWindowTitle('Error')
			self.msgBox.setText('Error: No es posible realizar esta ruta, se encuentra fuera de las gráficas')
			self.msgBox.setIcon(QtWidgets.QMessageBox.Critical)
			self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
			self.msgBox.exec_()

			self.ui.lineEdit_combustible_total.setText("")
			self.ui.lineEdit_combustible_ruta.setText("")
			self.ui.lineEdit_combustible_alterno.setText("")
			return

		plan_alterno = baseDatos.calcularCombustibleAlterno(distancia_alterno)

		combustible_total = combustible_extra + combustible_taxeo + combustible_app_instrumental + self.combustible_reserva_final + (plan_ruta['combustible']*1000) + plan_alterno['combustible']

		tiempo_ruta = plan_ruta['tiempo'].split(":")		
		tiempo_alterno = plan_alterno['tiempo'].split(":")
		tiempo_ruta_delta = timedelta(hours = int(tiempo_ruta[0]), minutes = int(tiempo_ruta[1]))
		tiempo_alterno_delta = timedelta(hours = int(tiempo_alterno[0]), minutes = int(tiempo_alterno[1]))		
		tiempo_total =  tiempo_ruta_delta + tiempo_alterno_delta + self.tiempo_extra + self.tiempo_reserva_final

		#el manual indica añadir 150 lbs de combustible por cada 5000 libras
		#que el LW supere las 85000 libras
		LW = self.ZFW + (combustible_total - ((plan_ruta['combustible']*1000) + 300 + 650))

		if LW > 85000:
			diferencia = LW - 85000
			extra = diferencia * 150 / 5000
			combustible_total = combustible_total + extra

		if combustible_total > self.combustible_maximo:
			exceso = int(combustible_total - self.combustible_maximo)
			self.msgBox.setWindowTitle('Exceso de combustible')
			self.msgBox.setText("Hay un exceso de " + str(exceso) + " libras de combustible.")
			self.msgBox.setIcon(QtWidgets.QMessageBox.Critical)
			self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
			self.msgBox.exec_()
			
			self.ui.lineEdit_combustible_total.setText("")
			return

		if combustible_total < self.combustible_minimo_vuelo:
			self.msgBox.setWindowTitle('Poco combustible')
			self.msgBox.setText("La aeronave no tiene el mínimo requerido por la FAA de " + str(self.combustible_minimo_vuelo) +  " para volar. Combustible: " + str(combustible_total))
			self.msgBox.setIcon(QtWidgets.QMessageBox.Critical)
			self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
			self.msgBox.exec_()

			self.ui.lineEdit_combustible_total.setText("")
			return
			
		self.TOW = self.ZFW + combustible_total

		#---------------- Modificando interfaz -----------------
		
		#Combustible
		self.ui.lineEdit_combustible_ruta.setText(str(plan_ruta['combustible']*1000))
		self.ui.lineEdit_combustible_alterno.setText(str(plan_alterno['combustible']))
		self.ui.lineEdit_num_app.setText(str(combustible_app_instrumental))
		self.ui.lineEdit_combustible_total.setText(str(combustible_total))

		#Tiempos
		horas, minutos = tiempo_ruta
		self.ui.timeEdit_combustible_ruta.setTime(QtCore.QTime(int(horas),int(minutos)))

		horas, minutos = tiempo_alterno
		self.ui.timeEdit_combustible_alterno.setTime(QtCore.QTime(int(horas),int(minutos)))
		
		minutos = int(tiempo_total.seconds / 60) % 60
		horas = int((tiempo_total.seconds / 60) / 60 )

		self.ui.timeEdit_tiempo_total.setTime(QtCore.QTime(horas, minutos))

		#Pesos
		self.ui.lcdNumber_ZFW.display(self.ZFW)
		self.ui.lcdNumber_TOW.display(self.TOW)
		self.ui.lcdNumber_LW.display(LW)

		paletaLcdZfw = self.ui.lcdNumber_ZFW.palette()
		paletaLcdTow = self.ui.lcdNumber_TOW.palette()

		if self.TOW > self.MTOW:
			paletaLcdTow.setColor(paletaLcdTow.WindowText, QtGui.QColor(255,45,30))

		else:
			paletaLcdTow.setColor(paletaLcdTow.WindowText, QtGui.QColor(24,28,21))

		self.ui.lcdNumber_TOW.setPalette(paletaLcdTow)
			
		if self.ZFW > self.MZFW:
			paletaLcdZfw.setColor(paletaLcdZfw.WindowText, QtGui.QColor(255,45,30))
					
		else:
			paletaLcdZfw.setColor(paletaLcdZfw.WindowText, QtGui.QColor(24,28,21))

		self.ui.lcdNumber_ZFW.setPalette(paletaLcdZfw)
		
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    aplicacion = FuelPlanner()
    aplicacion.show()
    sys.exit(app.exec_())
