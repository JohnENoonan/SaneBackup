import hou
from hutil.Qt import QtWidgets, QtCore

proj = hou.getenv("JOB") + '/'

class Backup(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        # init main window ui
        self.initMainWindow()
        self.backBtn = QtWidgets.QPushButton("Back")
        self.backBtn.resize(self.backBtn.minimumSizeHint())
        self.backBtn.move(0,0)
        # init commit Window
        self.initCommitWindow()
        # hbox = QtWidgets.QHBoxLayout()
        # button = QtWidgets.QPushButton('Change Font', self)
        # button.setFocusPolicy(QtCore.Qt.NoFocus)
        # button.move(20, 20)
        # self.connect(button, QtCore.SIGNAL('clicked()'), self.showDialog)
        #
        # self.label = QtWidgets.QLabel('This is some sample text', self)
        # self.label.move(130, 20)
        # hbox.addWidget(self.label, 1)


        self.setGeometry(500, 300, 400, 200)
        self.setWindowTitle('Sane Backup')
        self.setLayout(self.mainBox)
        self.mainBox.addWidget(self.commitWindow)
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)

    def initMainWindow(self):
        self.mainBox = QtWidgets.QHBoxLayout()
        # setup commit toggle
        self.commitBtn = QtWidgets.QPushButton("Save a Backup",self)
        self.commitBtn.setCheckable(True)
        self.connect(self.commitBtn, QtCore.SIGNAL('clicked()'), self.handleCommitToggle)
        self.commitBtn.setChecked(True)
        # setup load toggle
        self.loadBtn = QtWidgets.QPushButton("Load a Backup",self)
        self.loadBtn.setCheckable(True)
        self.connect(self.loadBtn, QtCore.SIGNAL('clicked()'), self.handleLoadToggle)
        self.mainBox.addWidget(self.commitBtn)
        self.mainBox.addWidget(self.loadBtn)

    def initCommitWindow(self):
        self.commitBox = QtWidgets.QVBoxLayout()
        self.commitWindow = QtWidgets.QWidget()
        self.commitWindow.setLayout(self.commitBox)
        self.commitBox.addWidget(QtWidgets.QLabel("Commit baby!",self.commitWindow))


    def handleCommitToggle(self):
        print "clicked commit toggle"
        self.commitBtn.setChecked(True)
        self.loadBtn.setChecked(False)

    def handleLoadToggle(self):
        print "clicked load toggle"
        self.commitBtn.setChecked(False)
        self.loadBtn.setChecked(True)

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.layout=QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)


        self.checkbox=QtWidgets.QCheckBox("Layouts")
        self.layout.addWidget(self.checkbox)


        self.widget1=QtWidgets.QWidget()
        self.layout.addWidget(self.widget1)

        self.layout1=QtWidgets.QVBoxLayout()
        self.widget1.setLayout(self.layout1)

        self.layout1.addWidget(QtWidgets.QLabel("First layout"))

        self.layout1.addWidget(QtWidgets.QTextEdit())


        self.widget2=QtWidgets.QWidget()
        self.layout.addWidget(self.widget2)

        self.layout2=QtWidgets.QHBoxLayout()
        self.widget2.setLayout(self.layout2)

        self.layout2.addWidget(QtWidgets.QTextEdit("Second layout"))

        self.layout2.addWidget(QtWidgets.QTextEdit())


        self.checkbox.toggled.connect(self.checkbox_toggled)
        self.checkbox.toggle()

        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)

    def checkbox_toggled(self, state):
        self.widget1.setVisible(state)
        self.widget2.setVisible(not state)

def createInterface():
    widget = QtWidgets.QLabel("I'm a label")
    widget.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)
    return widget

def saveBackup():
    hou.hipFile.save()
    hou.hipFile.saveAsBackup()
    # may need to catch hou.OperationFailed

# execution of program called from shelf
def main():
    print proj
    dialog = Backup()
    dialog.show()
    # createInterface().show()
