from PyQt5.QtWidgets import QApplication,QLineEdit,QMainWindow,QWidget,QFormLayout,QPushButton,QRadioButton,QGridLayout,QLabel
from PyQt5.QtGui import QIntValidator,QDoubleValidator,QFont
from PyQt5.QtCore import Qt,QRect
import sys
from script import scrap, add_to_anki
import traceback
class main_window(QWidget):
        def __init__(self,parent=None):
                super().__init__(parent)
                
                self.setStyleSheet("color:#371501")
                self.word = ''
                self.noun_or_verb = ''
                self.meanings_list = []
                self.radio_list = []
                self.sentense = ''
                self.audio_link = ''
                self.error1_label=False
                self.error2_label = False
                self.success_label = False
                self.last_width = self.width()
                self.last_height = self.height()
                self.add_button = None
                self.line = QLineEdit()
                self.line.textChanged.connect(self.textchanged)
                self.flo = QGridLayout()
                self.flo.addWidget(self.line,0,1)
                self.search_button = QPushButton(self)
                self.search_button.setText("Search")
                self.search_button.clicked.connect(self.search_clicked)
                self.flo.addWidget(self.search_button,1,1)
                self.setLayout(self.flo)
                self.setWindowTitle("A&B")
                
                

        def textchanged(self,text):
            self.word = text
            
                
        def search_clicked(self):
            self.clear_widgets("search")
            self.word, self.noun_or_verb, self.meanings_list, sentenses, self.audio_link = scrap(self.word)
            if not self.word:
                
                self.error1_label = QLabel("<font color=red>Word not found or internet connection is lost</font>")
                self.flo.addWidget(self.error1_label, 2,1)
                return
            elif self.error1_label:
                self.error1_label.setParent(None)
                self.error1_label = False
            
            self.radio_list = []
            
            for l in sentenses:
                self.radio_list.append(QRadioButton(l))
                self.radio_list[-1].toggled.connect(self.onClicked)
                if len(self.radio_list) == 1:
                    self.radio_list[0].setChecked(True)
                    self.sentense = l
                self.flo.addWidget(self.radio_list[-1],  len(self.radio_list)+1,1)
                
            self.add_button = QPushButton(self)
            self.add_button.setText("Add")
            self.add_button.clicked.connect(self.addToAnki)
            self.flo.addWidget(self.add_button,len(self.radio_list)+2,1)
            
            
        def enterPress(self):
            self.search_clicked()
        
        def addToAnki(self):
            try:
                add_to_anki(self.word, self.noun_or_verb,self.meanings_list, self.sentense, self.audio_link)
                self.clear_widgets()
                self.success_label = QLabel("<font color=green>Word added succesfully</font>")
                

            except Exception as e:
                traceback.print_exc()
                self.error2_label = QLabel("<font color=red>Please Open ankiDroid</font>")
                self.flo.addWidget(self.error2_label, self.flo.rowCount(),1)
            
            
            
        def onClicked(self):
            radioButton = self.sender()
            if radioButton.isChecked():
                self.sentense = radioButton.text()
        
        def clear_widgets(self,button="add"):
            
            if button == "add":
                
                self.line.clear()
            if self.success_label:
                
                self.success_label.setParent(None)
                self.success_label = False
            if self.error1_label:
                self.error1_label.setParent(None)
                self.error1_label = False
            if self.error2_label:
                self.error2_label.setParent(None)
                self.error2_label = False
            if len(self.radio_list)>0:
                for r in self.radio_list:
                    self.flo.removeWidget(r)
                self.radio_list = [] 
            if self.add_button is not None:
                self.flo.removeWidget(self.add_button)
                self.add_button = None
            self.resize(100,50)
if __name__ == "__main__":
        app = QApplication(sys.argv)
        win = main_window()
        win.show()
        sys.exit(app.exec_())