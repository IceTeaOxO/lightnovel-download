# coding:utf-8
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QThread, QRegExp
from PyQt5.QtGui import QIcon, QFont, QTextCursor, QPixmap, QColor,QRegExpValidator
from PyQt5.QtWidgets import QApplication, QFrame, QGridLayout, QFileDialog
from qfluentwidgets import (setTheme, Theme, PushSettingCard, SettingCardGroup, ExpandLayout, TextEdit, ImageLabel, LineEdit, PushButton, Theme, ProgressRing, setTheme, Theme, OptionsSettingCard, OptionsConfigItem, OptionsValidator, FluentWindow, SubtitleLabel, NavigationItemPosition, setThemeColor, qconfig, EditableComboBox, BoolValidator)
from qfluentwidgets import FluentIcon as FIF
import sys
import base64
import shutil
# from resource.logo import logo_base64
# from resource.book import book_base64
from lightnovel import *

font_label = QFont('微软雅黑', 18)
font_msg = QFont('微软雅黑', 11)
book_base64 = """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"""
logo_base64 = """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"""


class MainThread(QThread):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        
    def run(self):
        self.parent.clear_signal.emit('')
        try:
            book_no = self.parent.editline_book.text()
            volumn_no = self.parent.editline_volumn.text()
            downloader_router(self.parent.parent.out_path, book_no, volumn_no, True, self.parent.hang_signal, self.parent.progressring_signal, self.parent.cover_signal, self.parent.editline_hang)
            self.parent.end_signal.emit('')
        except Exception as e:
            self.parent.end_signal.emit('')
            print('错误，请检查网络情况或确认输入是否正确')
            print('错误信息：')
            print(e)
    def terminate(self) -> None:
        result = super().terminate()
        return result

class EmittingStr(QObject):
    textWritten = pyqtSignal(str)  # 定义一个发送str的信号
    def write(self, text):
        self.textWritten.emit(str(text))
    def flush(self):
        pass
    def isatty(self):
        pass

class SettingWidget(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)

        self.parent = parent
        self.expandLayout = ExpandLayout(self)
        self.setObjectName(text.replace(' ', '-'))
        self.setting_group = SettingCardGroup(self.tr("下载设置"), self)
        
        self.download_path_card = PushSettingCard(
            self.tr('选择文件夹'),
            FIF.DOWNLOAD,
            self.tr("下载目录"),
            self.parent.out_path,
            self.setting_group
        )
        self.themeMode = OptionsConfigItem(
        None, "ThemeMode", Theme.DARK, OptionsValidator(Theme), None)

        self.threadMode = OptionsConfigItem(
        None, "ThreadMode", True, BoolValidator())

        self.theme_card = OptionsSettingCard(
            self.themeMode,
            FIF.BRUSH,
            self.tr('应用主题'),
            self.tr("更改外观"),
            texts=[
                self.tr('亮'), self.tr('暗'),
                self.tr('跟随系统设置')
            ],
            parent=self.parent
        )

        self.setting_group.addSettingCard(self.download_path_card)
        self.setting_group.addSettingCard(self.theme_card)
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(20, 10, 20, 0)
        self.expandLayout.addWidget(self.setting_group)

        self.download_path_card.clicked.connect(self.download_path_changed)
        self.theme_card.optionChanged.connect(self.theme_changed)

    def download_path_changed(self):
        """ download folder card clicked slot """
        self.parent.out_path = QFileDialog.getExistingDirectory(
            self, self.tr("Choose folder"), self.parent.out_path)
        self.download_path_card.contentLabel.setText(self.parent.out_path)
    
    def theme_changed(self):
        theme_name = self.theme_card.choiceLabel.text()
        self.parent.set_theme(theme_name)
        if os.path.exists('./config'):
            shutil.rmtree('./config')


            

class HomeWidget(QFrame):

    progressring_signal = pyqtSignal(object) 
    end_signal = pyqtSignal(object) 
    hang_signal = pyqtSignal(object)
    clear_signal = pyqtSignal(object)
    cover_signal = pyqtSignal(object)

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(text)
        self.parent = parent
        self.label_book = SubtitleLabel('书号：', self)
        self.label_volumn = SubtitleLabel('卷号：', self)
        self.editline_book = LineEdit(self) 
        self.editline_volumn = LineEdit(self) 
        validator = QRegExpValidator(QRegExp("\\d+"))  # 正则表达式匹配阿拉伯数字
        self.editline_book.setValidator(validator)
        # self.editline_volumn.setValidator(validator)

        self.editline_book.setMaxLength(4)
        # self.editline_volumn.setMaxLength(2)
        
        # self.editline_book.setText('2059')
        # self.editline_volumn.setText('3')
        self.book_icon = QPixmap()
        self.book_icon.loadFromData(base64.b64decode(book_base64))
        self.cover_w, self.cover_h = 152, 230

        self.label_cover = ImageLabel(self.book_icon, self)
        self.label_cover.setBorderRadius(8, 8, 8, 8)
        self.label_cover.setFixedSize(self.cover_w, self.cover_h)

        self.text_screen = TextEdit()
        self.text_screen.setReadOnly(True)
        self.text_screen.setFixedHeight(self.cover_h)

        self.progressRing = ProgressRing(self)
        self.progressRing.setValue(0)
        self.progressRing.setTextVisible(True)
        self.progressRing.setFixedSize(50, 50)
        
        self.btn_run = PushButton('确定', self)
        self.btn_run.setShortcut(Qt.Key_Return)
        self.btn_stop = PushButton('取消', self)
        self.btn_hang = PushButton('确定', self)
        
        self.editline_hang = EditableComboBox(self)
        self.gridLayout = QGridLayout(self)
        self.screen_layout = QGridLayout()
        self.btn_layout = QGridLayout()
        self.hang_layout = QGridLayout()
        
        self.label_book.setFont(font_label)
        self.label_volumn.setFont(font_label)
        self.editline_book.setFont(font_label)
        self.editline_volumn.setFont(font_label)
        self.text_screen.setFont(font_msg)
        self.editline_hang.setFont(font_msg)

        self.gridLayout.addWidget(self.editline_book, 0, 1)
        self.gridLayout.addWidget(self.editline_volumn, 1, 1)
        self.gridLayout.addWidget(self.label_book, 0, 0)
        self.gridLayout.addWidget(self.label_volumn, 1, 0)

        self.gridLayout.addLayout(self.btn_layout, 2, 1, 1, 1)
        self.btn_layout.addWidget(self.btn_run, 2, 1)
        self.btn_layout.addWidget(self.btn_stop, 2, 2)

        self.gridLayout.addLayout(self.screen_layout, 3, 0, 2, 2)

        self.screen_layout.addWidget(self.progressRing, 0, 1, Qt.AlignLeft|Qt.AlignBottom)
        self.screen_layout.addWidget(self.text_screen, 0, 0)
        self.screen_layout.addWidget(self.label_cover, 0, 1)
        
        

        self.gridLayout.addLayout(self.hang_layout, 5, 0, 1, 2)
        self.hang_layout.addWidget(self.editline_hang, 0, 0)
        self.hang_layout.addWidget(self.btn_hang, 0, 1)

        self.screen_layout.setContentsMargins(0,0,0,0)
        self.btn_layout.setContentsMargins(0,0,0,0)
        self.gridLayout.setContentsMargins(20, 10, 20, 10)

        self.btn_run.clicked.connect(self.process_start)
        self.btn_stop.clicked.connect(self.process_stop)
        self.btn_hang.clicked.connect(self.process_continue)

        self.progressring_signal.connect(self.progressring_msg)
        self.end_signal.connect(self.process_end)
        self.hang_signal.connect(self.process_hang)
        self.clear_signal.connect(self.clear_screen)
        self.cover_signal.connect(self.display_cover)

        self.progressRing.hide()
        self.btn_hang.hide()
        self.editline_hang.hide()
        self.btn_stop.setEnabled(False)
        
        sys.stdout = EmittingStr(textWritten=self.outputWritten)
        sys.stderr = EmittingStr(textWritten=self.outputWritten)
        self.text_screen.setText(self.parent.welcome_text) 
    
    def process_start(self):
        self.label_cover.setImage(self.book_icon)
        self.label_cover.setFixedSize(self.cover_w, self.cover_h)
        self.btn_run.setEnabled(False)
        self.btn_run.setText('正在下载')
        self.btn_stop.setEnabled(True)
        self.main_thread = MainThread(self)
        self.main_thread.start()
        
    def process_end(self, input=None):
        self.btn_run.setEnabled(True)
        self.btn_run.setText('开始下载')
        self.btn_run.setShortcut(Qt.Key_Return)
        self.btn_stop.setEnabled(False)
        self.progressRing.hide()
        self.btn_hang.hide()
        self.editline_hang.clear()
        self.editline_hang.hide()
        if input=='refresh':
            self.label_cover.setImage(self.book_icon)
            self.label_cover.setFixedSize(self.cover_w, self.cover_h)
            self.clear_signal.emit('')
            self.text_screen.setText(self.parent.welcome_text) 
        
    def outputWritten(self, text):
        cursor = self.text_screen.textCursor()
        scrollbar=self.text_screen.verticalScrollBar()
        is_bottom = (scrollbar.value()>=scrollbar.maximum() - 15)
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        if is_bottom:
            self.text_screen.setTextCursor(cursor)
        # self.text_screen.ensureCursorVisible()
    
    def clear_screen(self):
        self.text_screen.clear()
    
    def display_cover(self, signal_msg):
        filepath, img_h, img_w = signal_msg
        self.label_cover.setImage(filepath)
        self.label_cover.setFixedSize(int(img_w*self.cover_h/img_h), self.cover_h)
        
    def progressring_msg(self, input):
        if input == 'start':
            self.label_cover.setImage(self.book_icon)
            self.label_cover.setFixedSize(self.cover_w, self.cover_h)
            self.progressRing.show()
        elif input == 'end':
            self.progressRing.hide()
            self.progressRing.setValue(0)
        else:
            self.progressRing.setValue(input)
    
    def process_hang(self, input=None):
        self.btn_hang.setEnabled(True)
        self.btn_hang.setShortcut(Qt.Key_Return)
        self.btn_hang.show()
        self.editline_hang.show()
    
    def process_continue(self, input=None):
        self.btn_hang.hide()
        self.btn_hang.setEnabled(False)
        self.editline_hang.hide()
        
    
    def process_stop(self):
        self.main_thread.terminate()
        self.end_signal.emit('refresh')
        
        
    

class Window(FluentWindow):
    def __init__(self):
        super().__init__()

        self.out_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        self.head = 'https://www.wenku8.net'
        split_str = '**************************************\n    '
        self.welcome_text = f'使用说明（共4条，记得下拉）：\n{split_str}1.轻小说文库{self.head}，根据书籍网址输入书号以及下载的卷号，书号最多输入4位阿拉伯数字。\n{split_str}2.例如小说网址是{self.head}/book/3138.htm，则书号输入3138。\n{split_str}3.要查询书籍卷号卷名等信息，则可以只输入书号不输入卷号，点击确定会返回书籍卷名称和对应的卷号。\n{split_str}4.根据上一步返回的信息确定自己想下载的卷号，要下载编号[2]对应卷，则卷号输入2。想下载多卷比如[1]至[3]对应卷，则卷号输入1-3或1,2,3（英文逗号分隔，编号也可以不连续）并点击确定。'
        self.homeInterface = HomeWidget('Home Interface', self)
        self.settingInterface = SettingWidget('Setting Interface', self)
        self.initNavigation()
        self.initWindow()
        
    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, '主界面')
        self.addSubInterface(self.settingInterface, FIF.SETTING, '设置', NavigationItemPosition.BOTTOM)

    def initWindow(self):
        self.resize(700, 460)
        pixmap = QPixmap()
        pixmap.loadFromData(base64.b64decode(logo_base64))
        self.setWindowIcon(QIcon(pixmap))
        self.setWindowTitle('轻小说文库EPUB下载器')
        self.setFont(font_label)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
    
    def set_theme(self, mode=None):
        if mode=='亮':
            setTheme(Theme.LIGHT)
        elif mode=='暗':
            setTheme(Theme.DARK)
        elif mode=='跟随系统设置':
            setTheme(Theme.AUTO)
        theme = qconfig.theme
        if theme == Theme.DARK:
            self.homeInterface.label_book.setTextColor(QColor(255,255,255))
            self.homeInterface.label_volumn.setTextColor(QColor(255,255,255))
        elif theme == Theme.LIGHT:
            self.homeInterface.label_book.setTextColor(QColor(0,0,0))
            self.homeInterface.label_volumn.setTextColor(QColor(0,0,0))


    
if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    setTheme(Theme.DARK)
    setThemeColor('#559DCD')
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec_()
