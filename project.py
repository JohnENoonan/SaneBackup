import hou
import os, glob
from datetime import datetime
import csv
from hutil.Qt import QtWidgets, QtCore

proj = hou.getenv("JOB") # path to project file
backupDir = os.path.join(proj,"backup") # path to backup directory

class Backup():
    def __init__(self):
        self.name = "backup.csv"
        self.header = ['Filename','Date','Message']
        self.filepath = os.path.join(backupDir,self.name)
        # check for database
        if self.name not in os.listdir(backupDir):
            print "creted new table"
            self.initTable()

    def saveBackup(self):
        try:
            hou.hipFile.save()
            hou.hipFile.saveAsBackup()
        except hou.OperationFailed:
            sendMsg("Error: Houdini could not save backup")
            sys.exit()

    # return the newest file in the backup directory
    def getNewBackup(self):
        files = glob.glob(os.path.join(backupDir, "*.hip*").replace("\\","/"))
        print files
        assert(len(files) != 0)
        return max(files, key=os.path.getmtime).replace("\\","/")

    # make a commit with given message
    def makeCommit(self, msg):
        # get commit Message
        if len(msg) == 0:
            sendMsg("Error: backups must have a defining message.")
            return
        print "making commit: \"" + msg + "\""
        self.saveBackup()
        try:
            newfile = self.getNewBackup()
            ftime = os.path.getmtime(newfile)
        except OSError:
            print("Path '%s' does not exists or is inaccessible" % newfile)
            sys.exit()
        self.writeToFile([newfile,ftime,msg])
        # self.select_all_tasks()

    def select_all_tasks(self):
        with open(self.filepath, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print "Column names are {}".format(", ".join(row.reverse()))
                    line_count += 1
                print "{}: {} = \"{}\".".format(row["Filename"],row["Date"],row["Message"])
                line_count += 1
            print str(line_count-1) + " commits"

    def writeToFile(self, data):
        with open(self.filepath, mode='ab') as backupfile:
            writer = csv.writer(backupfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(data)

    # create header
    def initTable(self):
        with open(self.filepath, mode='ab') as backupfile:
            writer = csv.writer(backupfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(self.header)

    def getHeaders(self):
        return self.header

    def getCommits(self):
        with open(self.filepath, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            commits = []
            for row in csv_reader:
                d = datetime.fromtimestamp(float(row["Date"])).strftime("%m/%d/%Y, %H:%M:%S")
                commits.append([d,row["Message"]])
                line_count += 1
            return commits


class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        # create composite backup controller
        self.backup = Backup()
        # init Windows
        self.initCommitWindow()
        self.initLoadWindow()
        self.setGeometry(500, 300, 400, 200)
        self.setWindowTitle('Sane Backup')
        # set layouts and add widgets
        self.numCommits = 0
        parentLayout = QtWidgets.QVBoxLayout()
        self.setLayout(parentLayout)
        # create tabs
        tabWidget = QtWidgets.QTabWidget()
        tabWidget.addTab(self.commitWindow,"Make a Commit")
        tabWidget.addTab(self.loadWindow,"Load a Backup")
        # listen for tab change
        tabWidget.currentChanged.connect(self.handleTabSelect)
        parentLayout.addWidget(tabWidget)
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)

    # on changed tab selection display either commit mode or load mode
    def handleTabSelect(self, index):
        if index == 0: # commit tab
            self.handleCommitToggle()
        elif index == 1: # load tab
            self.handleLoadToggle()

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

    def initLoadWindow(self):
        self.loadBox = QtWidgets.QVBoxLayout()
        self.loadWindow = QtWidgets.QWidget()
        self.loadWindow.setLayout(self.loadBox)
        self.loadWindow.setMinimumHeight(400)
        self.loadTree = QtWidgets.QTreeWidget()
        self.loadTree.setHeaderLabels(self.backup.getHeaders()[1:])
        self.loadBox.addWidget(self.loadTree)
        self.loadWindow.setVisible(False)

    def handleCommitToggle(self):
        print "clicked commit toggle"

    def handleLoadToggle(self):
        print "clicked load toggle"
        # add commits to tree
        commits = self.backup.getCommits()
        # if there has been a commit since last checking
        if (len(commits) > self.numCommits):
            print "in if statement"
            for i in xrange(self.numCommits,len(commits)):
                el = QtWidgets.QTreeWidgetItem(self.loadTree,commits[i])
            self.numCommits = len(commits)

# display a message of supplied text
def sendMsg(text):
    hou.ui.displayMessage(text)

# execution of program called from shelf
def main():
    gui = Window()
    gui.show()
