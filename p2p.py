from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys, socket, os
import subprocess
from thread import *
 
def msg_box(title, data):
        w = QWidget()
        QMessageBox.information(w, title, data)

def update_peers():
    # ps1=subprocess.Popen(["sudo", "arp-scan", "-l", "--interface=wlp2s0"], stdout=subprocess.PIPE)
    # ps2=subprocess.Popen(["grep", "-E", '"([0-9]{1,3}\.){3}[0-9]{1,3}"',], stdin=ps1.stdout, stdout=peers_file)
    # ps3=subprocess.Popen(["cut", '-d$\'\\t\'', "-f1,2"], stdin=ps2.stdout, shell=True)
    # ps3=subprocess.Popen(["cat", '>', "peers.txt"], stdin=ps2.stdout)
    # peers_file.close()

    # f=open('peers.txt','r')
    peers_file=open("peers.txt",'r')
    for line in peers_file.readlines():
        ip,mac=line.split()
        peers[ip]=mac
    peers_file.close()

def update_list(self, data):
        # print type(data)
        self.listWidget.addItem(data)
        print "\a"
 
def server_socket(self):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 7777))
        s.listen(1)
    except socket.error, e:
        msg_box("Socket Error !!",
            "Unable To Setup Local Socket. Port In Use")
        return
 
    while 1:
        conn, addr = s.accept()
 
        incoming_ip = str(addr[0])
        current_chat_ip = self.ip_text.text()
 
        if incoming_ip != current_chat_ip:
                conn.close()
        else:
            rec=""
            while True:
                rec += conn.recv(1024)
                print rec
                rec_end = rec.find('\n')
                if rec_end != -1:
                    data = rec[:rec_end]
                    break
            data=''.join(data)
            data=QString(unicode(data))

            update_list(self, data)
            conn.close()
 
    s.close()
 
try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
 
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
 
        self.start_server()
 
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(662, 448)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.frame = QFrame(self.centralwidget)
        self.frame.setGeometry(QRect(10, 10, 651, 41))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))

        self.ip_label = QLabel(self.frame)
        self.ip_label.setGeometry(QRect(10, 10, 131, 21))
        self.ip_label.setObjectName(_fromUtf8("ip_label"))

        self.ip_text = QLineEdit(self.frame)
        self.ip_text.setGeometry(QRect(90, 10, 161, 21))
        self.ip_text.setObjectName(_fromUtf8("ip_text"))

        self.name_label = QLabel(self.frame)
        self.name_label.setGeometry(QRect(260, 10, 131, 21))
        self.name_label.setObjectName(_fromUtf8("name_label"))

        self.name_text = QLineEdit(self.frame)
        self.name_text.setGeometry(QRect(300, 10, 151, 21))
        self.name_text.setObjectName(_fromUtf8("name_text"))

        self.show_peers_btn = QPushButton(self.frame)
        self.show_peers_btn.setGeometry(QRect(460, 10, 159, 21))
        self.show_peers_btn.setObjectName(_fromUtf8("show_peers_btn"))
        self.show_peers_btn.clicked.connect(self.show_peers)

        self.chat_frame = QFrame(self.centralwidget)
        self.chat_frame.setGeometry(QRect(10, 60, 301, 321))
        self.chat_frame.setFrameShape(QFrame.StyledPanel)
        self.chat_frame.setFrameShadow(QFrame.Raised)
        self.chat_frame.setObjectName(_fromUtf8("chat_frame"))

        self.msg_box = QTextEdit(self.chat_frame)
        self.msg_box.setGeometry(QRect(10, 10, 281, 251))
        self.msg_box.setObjectName(_fromUtf8("msg_box"))

        self.send_msg_btn = QPushButton(self.chat_frame)
        self.send_msg_btn.setGeometry(QRect(10, 280, 171, 31))
        self.send_msg_btn.setObjectName(_fromUtf8("send_msg_btn"))
        self.send_msg_btn.clicked.connect(self.client_send_message)
 
        self.clear_logs_btn = QPushButton(self.chat_frame)
        self.clear_logs_btn.setGeometry(QRect(190, 280, 93, 31))
        self.clear_logs_btn.setObjectName(_fromUtf8("clear_logs_btn")) 
 
        self.log_frame = QFrame(self.centralwidget)
        self.log_frame.setGeometry(QRect(320, 60, 331, 321))
        self.log_frame.setFrameShape(QFrame.StyledPanel)
        self.log_frame.setFrameShadow(QFrame.Raised)
        self.log_frame.setObjectName(_fromUtf8("log_frame"))

        self.listWidget = QListWidget(self.log_frame)
        self.listWidget.setGeometry(QRect(10, 10, 311, 301))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
 
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)
 
    def clear_logs(self):
        self.listWidget.clear()

    def show_peers(self):
        # update_peers()
        peers_list=""
        for key in peers:
            peers_list+=key+" : "+peers[key]+"\n"
        if(len(peers)!=0) :
            msg_box("Peers",peers_list)
        else :
            msg_box("Peers","No Peers Online")


 
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QApplication.translate("MainWindow","P2P Chat", None, QApplication.UnicodeUTF8))
        self.ip_label.setText(QApplication.translate("MainWindow", "IP Address:",None, QApplication.UnicodeUTF8))
        self.name_label.setText(QApplication.translate("MainWindow", "Name: ",None, QApplication.UnicodeUTF8))
        self.show_peers_btn.setText(QApplication.translate("MainWindow","Available Peers", None, QApplication.UnicodeUTF8))
        self.send_msg_btn.setText(QApplication.translate("MainWindow","Send Message", None, QApplication.UnicodeUTF8))
        self.clear_logs_btn.setText(QApplication.translate("MainWindow","Clear Logs", None, QApplication.UnicodeUTF8))
 
    def start_server(self):
                start_new_thread(server_socket, (self,))
                msg_box("Success", "Server Started Sucessfully")
   
    def client_send_message(self):
        ip_address = self.ip_text.text()
 
        name = self.name_text.text()
        name = name.replace("#>","")
        message = self.msg_box.toPlainText()
        # print message
        message = message.replace("#>","")

        msg =  name + " #> " + message + "\n"
 
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       
        try:
            c.connect((ip_address, 7777))
        except Exception, e:
            msg_box("Connection Refused", "The Address You Are Trying To Reach Is Currently Unavailable")
            return
 
        try:
            # msg=msg.encode('utf-8')
            c.sendall(unicode(msg))
            self.listWidget.addItem(msg)
            self.msg_box.setText("")
        except Exception, e:
            msg_box("Connection Refused", "The Message Cannot Be Sent. End-Point Not Connected !!")
 
        c.close()
 
if __name__ == "__main__":
    peers=dict()
    f=open('peers.txt','r')
    for line in f.readlines():
        ip,mac=line.split()
        peers[ip]=mac
    f.close()
    # for key in peers.keys():
    #     print key
    #     print peers[key]
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
 
    sys.exit(app.exec_())