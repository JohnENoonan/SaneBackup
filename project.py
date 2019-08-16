import hou,os,sqlite3
from hutil.Qt import QtWidgets, QtCore

proj = hou.getenv("JOB") + '/'
backupDir = os.path.join(proj,"backup")

class Backup():
    def __init__(self):
        self.name = "backup.db"
        # check for database
        if self.name not in os.listdir(backupDir):
            open(os.path.join(backupDir,self.name), 'a').close()
            self.initTable()

    def saveBackup(self):
        hou.hipFile.save()
        hou.hipFile.saveAsBackup()
        # may need to catch hou.OperationFailed

    def makeCommit(self, msg):
        # get commit Message
        if len(msg) == 0:
            sendMsg("Error: backups must have a defining message.")
            return
        conn = sqlite3.connect(self.name)
        c = conn.cursor()

    def initTable(self):
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute('''CREATE TABLE stocks
                 (date text, trans text, symbol text, qty real, price real)''')
        conn.commit()
        conn.close()


class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        # create composite backup controller
        self.backup = Backup()
        # init main window ui
        self.initMainWindow()
        self.backBtn = QtWidgets.QPushButton("Back")
        self.backBtn.resize(self.backBtn.minimumSizeHint())
        self.backBtn.move(0,0)
        # init commit Window
        self.initCommitWindow()
        self.setGeometry(500, 300, 400, 200)
        self.setWindowTitle('Sane Backup')
        # set layouts and add widgets
        parentLayout = QtWidgets.QVBoxLayout()
        self.setLayout(parentLayout)
        parentLayout.addWidget(self.toggleWidget)
        parentLayout.addStretch()
        parentLayout.addWidget(self.commitWindow)
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)

    def initMainWindow(self):
        self.toggleLayout = QtWidgets.QHBoxLayout()
        self.toggleWidget = QtWidgets.QWidget()
        # setup commit toggle
        self.commitBtn = QtWidgets.QPushButton("Save a Backup",self)
        self.commitBtn.setCheckable(True)
        self.connect(self.commitBtn, QtCore.SIGNAL('clicked()'), self.handleCommitToggle)
        self.commitBtn.setChecked(True)
        # setup load toggle
        self.loadBtn = QtWidgets.QPushButton("Load a Backup",self)
        self.loadBtn.setCheckable(True)
        self.connect(self.loadBtn, QtCore.SIGNAL('clicked()'), self.handleLoadToggle)
        self.toggleLayout.addWidget(self.commitBtn)
        self.toggleLayout.addWidget(self.loadBtn)
        self.toggleWidget.setLayout(self.toggleLayout)

    # setup text box for message and submit button
    def initCommitWindow(self):
        self.commitBox = QtWidgets.QVBoxLayout()
        self.commitWindow = QtWidgets.QWidget()
        self.commitWindow.setMinimumHeight(400)
        self.commitWindow.setLayout(self.commitBox)
        self.commitMsg = QtWidgets.QTextEdit()
        self.commitMsg.setPlaceholderText("Enter Commit Message")
        self.commitMsg.setParent(self.commitWindow)
        self.commitBox.addWidget(self.commitMsg)
        okBtn = QtWidgets.QPushButton("Ok",self.commitWindow)
        okBtn.clicked.connect(lambda: self.backup.makeCommit(self.commitMsg.toPlainText()))
        self.commitBox.addWidget(okBtn)

    def handleCommitToggle(self):
        print "clicked commit toggle"
        self.commitBtn.setChecked(True)
        self.loadBtn.setChecked(False)
        self.commitWindow.setVisible(True)

    def handleLoadToggle(self):
        print "clicked load toggle"
        self.commitBtn.setChecked(False)
        self.loadBtn.setChecked(True)
        self.commitWindow.setVisible(False)


def sendMsg(text):
    hou.ui.displayMessage(text)

# execution of program called from shelf
def main():
    gui = Window()
    gui.show()
