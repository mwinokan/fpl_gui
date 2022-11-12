
from PyQt5 import QtWidgets, QtCore, QtGui

class ComboWidget():

	def __init__(self,text,isChecked=False,showCheckbox=True):

		self._text = text
		self._isChecked = isChecked
		self._showCheckbox = showCheckbox
		self._stylesheet = None
		self._font = None

		self.init_widget()

	def init_widget(self):

		if self._showCheckbox:
			widget = QtWidgets.QCheckBox(self._text)
			if self._isChecked:
				widget.setCheckState(QtCore.Qt.CheckState(2))
			else:
				widget.setCheckState(QtCore.Qt.CheckState(0))
		else:
			if self._isChecked:
				widget = QtWidgets.QLabel(self._text)
			else:
				widget = QtWidgets.QLabel("("+self._text+")")

		if self._stylesheet is not None:
			widget.setStyleSheet(self._stylesheet)

		if self._font is not None:
			widget.setFont(self._font)

		self._widget = widget

	@property
	def widget(self):
		return self._widget

	def setStyleSheet(self,stylesheet):
		self._stylesheet = stylesheet

	def setCheckState(self,state):
		self._isChecked = state
		if not self._showCheckbox:
			if self._isChecked:
				self._widget.setText(self._text.rjust(4)+"  ")
			else:
				self._widget.setText(" ("+self._text.rjust(2)+") ")

	def setText(self,text):
		self._text = text

	def setFont(self,font):
		self._font = font

	def isChecked(self):
		return self._isChecked

	def text(self):
		return self._text
