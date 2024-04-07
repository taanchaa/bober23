# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'set_budgetraIHjH.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Dialog_set_budget(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(453, 300)
        Dialog.setMaximumSize(QSize(16777215, 1000004))
        Dialog.setStyleSheet(u"background-color: rgb(61, 61, 61);")
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMaximumSize(QSize(16777215, 1000))
        self.frame.setStyleSheet(u"font-family: Georgia;\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(160, 32, 240, 255));\n"
"border: 1px solid rgba(255,255,255,30);\n"
"border-radius: 5px;")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 10000))
        font = QFont()
        font.setFamilies([u"Georgia"])
        font.setPointSize(15)
        font.setBold(False)
        self.label.setFont(font)
        self.label.setLayoutDirection(Qt.LeftToRight)
        self.label.setStyleSheet(u"color: yellow;\n"
"font-weigth bold;\n"
"font-size: 15pt;\n"
"backgroung-color: none;\n"
"border: none;")
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.bdg_day = QLineEdit(self.frame)
        self.bdg_day.setObjectName(u"bdg_day")
        self.bdg_day.setStyleSheet(u"font-size: 18pt;\n"
"color: white;\n"
"padding-left: 10px;")

        self.verticalLayout.addWidget(self.bdg_day)

        self.bdg_week = QLineEdit(self.frame)
        self.bdg_week.setObjectName(u"bdg_week")
        self.bdg_week.setStyleSheet(u"font-size: 18pt;\n"
"color: white;\n"
"padding-left: 10px;")

        self.verticalLayout.addWidget(self.bdg_week)

        self.bdg_month = QLineEdit(self.frame)
        self.bdg_month.setObjectName(u"bdg_month")
        self.bdg_month.setStyleSheet(u"font-size: 18pt;\n"
"color: white;\n"
"padding-left: 10px;")

        self.verticalLayout.addWidget(self.bdg_month)

        self.pushButton = QPushButton(self.frame)
        self.pushButton.setObjectName(u"pushButton")
        font1 = QFont()
        font1.setFamilies([u"Georgia"])
        font1.setPointSize(14)
        self.pushButton.setFont(font1)
        self.pushButton.setStyleSheet(u"QPushButton {\n"
"color: pink;\n"
"background-color: rgba(255,255,255,30);\n"
"border: 1px solid rgba(255,255,255,40);\n"
"border-radius: 7px;\n"
"width: 150px;\n"
"height: 40px;\n"
"}\n"
"QPushButton:hover {\n"
"color: white;\n"
"background-color: rgba(255,255,255,40);\n"
"}\n"
"QPushButton:pressed {\n"
"color: white;\n"
"background-color: rgba(255,255,255,70);\n"
"}")

        self.verticalLayout.addWidget(self.pushButton)


        self.verticalLayout_2.addWidget(self.frame)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\u0423\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c \u0431\u044e\u0434\u0436\u0435\u0442", None))
        self.bdg_day.setPlaceholderText(QCoreApplication.translate("Dialog", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u0431\u044e\u0434\u0436\u0435\u0442 \u043d\u0430 \u0434\u0435\u043d\u044c", None))
        self.bdg_week.setPlaceholderText(QCoreApplication.translate("Dialog", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u0431\u044e\u0434\u0436\u0435\u0442 \u043d\u0430 \u043d\u0435\u0434\u0435\u043b\u044e", None))
        self.bdg_month.setPlaceholderText(QCoreApplication.translate("Dialog", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u0431\u044e\u0434\u0436\u0435\u0442 \u043d\u0430 \u043c\u0435\u0441\u044f\u0446", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
    # retranslateUi

