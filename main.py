# Play Icon - Icon derived from original work by Freepik - https://www.freepik.com/
# Gear Icon - Icon derived from original work by Freepik - https://www.freepik.com/
# Plus Icon - Icon derived from original work by Freepik - https://www.freepik.com/
# Minus Icon - Icon derived from original work by Freepik - https://www.freepik.com/
# Folder Icon - Icon derived from original work by Freepik - https://www.freepik.com/
# Exit Door Icon - Icon derived from original work by Freepik - https://www.freepik.com/
# History Icon - Icon derived from original work by joalfa - https://www.flaticon.com/authors/joalfa
# Feedback Icon - Icon derived from original work by Those Icons - https://www.flaticon.com/authors/those-icons
# Color Palette - https://colorhunt.co/palette/11052c3d087bf43b86ffe459

# Classix Video Manager - A lightweight video downloader to download public domain videos and those you have the rights to.
# Copyright (C) 2021 Zachary Goreczny

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from screeninfo import get_monitors
from pytube import YouTube
import tempfile
import shutil
from urllib.request import urlretrieve
import os
import ssl
import smtplib
import warnings

global copyright_var

try:
    mons = []
    for m in get_monitors():
        mons.append(m)

    width = int(int(str(mons[0].width))/4)
    height = int(int(str(mons[0].height))/5)
except:
    width = 300
    height = 200

download_list = []
hist_list = []
temp_hist_list = []

try:
    os.makedirs("App Files")
except:
    pass

try:
    with open("App Files\\output_dir.txt", "r") as file:
        output_dir = file.read()
except:
    output_dir = ""

try:
    with open("App Files\\hist_file.txt", "r", encoding="utf-8") as file:
        items = file.readlines()
        hist_list = items
except:
    pass

try:
    with open("App Files\\download_count.txt", "r") as file:
        content = file.read()
        splits = content.split(";")
        download_count = int(splits[0])
        data_count = int(splits[1])
except:
    download_count = 0
    data_count = 0

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class welcome_win(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(width,height,1000,700)
        self.setWindowTitle("Welcome to Classix Video Manager!")
        self.setWindowIcon(QIcon(r"F:\Dropbox\Python\Classix Video Manager\classix-logo.png"))
        self.setStyleSheet("background-color: #11052C; color: #FFE459")
        self.welcome_UI()
        

    def welcome_UI(self):
        self.page_one = QGridLayout()
        self.setLayout(self.page_one)

        self.page_two = QGridLayout()

        self.mone = QHBoxLayout()
        self.mtwo = QHBoxLayout()
        self.mthree = QHBoxLayout()
        self.mfour = QHBoxLayout()
### Page One Layout ###
        self.welcome_text = QLabel("Welcome to Classix Video Manager!")
        self.welcome_text.setFont(QFont("Times", 14, QFont.Bold))
        self.welcome_text.setStyleSheet("color: #F43B86")

        self.welcome_help = QLabel("'A retro style user friendly video downloader and file manager by Z Tech and Data.'")
        self.welcome_help.setStyleSheet("color: #FFE459")

        self.classix_logo = QLabel("")
        self.classix_logo.setPixmap(QPixmap(r"F:\Dropbox\Python\Classix Video Manager\classix-logo.png").scaled(300,300))

        self.start_button = QPushButton("                    Let's Begin!                    ")
        self.start_button.setStyleSheet("color: #11052C; background-color: #FFE459; border-style: outset; border-width: 2px; border-radius: 10px; border-color: #3D087B; padding: 6px")    
        self.start_button.clicked.connect(self.big_start)
### Page Two Layout ###
        self.set_dir = QLabel("First, let's set your download location.")
        self.set_dir.setFont(QFont("Times", 14, QFont.Bold))
        self.set_dir.setStyleSheet("color: #F43B86")
        self.set_dir.hide()

        self.save_loc = QLabel("Current Save Location:")
        self.save_loc.setFont(QFont("Times", 12, QFont.Bold))
        self.save_loc.setStyleSheet("color: #F43B86")
        self.save_loc.hide()

        self.set_dir_help = QLabel("Select a folder that you want your files downloaded to. You can always change this later! :)")
        self.set_dir_help.setStyleSheet("color: #FFFFFF")
        self.set_dir_help.hide()

        self.file_button = QPushButton("                Select Save Location                ")
        self.file_button.setStyleSheet("color: #11052C; background-color: #FFE459; border-style: outset; border-width: 2px; border-radius: 10px; border-color: #3D087B; padding: 6px")
        self.file_button.clicked.connect(self.get_file_dir)
        self.file_button.hide()

        self.page_three = QPushButton("             Continue ---->              ")
        self.page_three.setStyleSheet("color: #11052C; background-color: #FFE459; border-style: outset; border-width: 2px; border-radius: 10px; border-color: #3D087B; padding: 6px")
        self.page_three.clicked.connect(self.third_page)
        self.page_three.hide()
### Page Three Layout ###
        self.toolbar_text = QLabel("Great! Now here's the toolbar!")
        self.toolbar_text.setFont(QFont("Times", 14, QFont.Bold))
        self.toolbar_text.setStyleSheet("color: #F43B86")
        self.toolbar_text.hide()

        self.toolbar_help = QLabel("""
The toolbar has 8 items, only 7 work. (The Classix logo is simply there to hang out.)\n
Plus - This is how you add videos to the download list. You can choose audio or video.\n
Minus - This allows you to delete videos after you added them to the download list.\n
Folder - Clicking the folder lets you change the download location and open it easily.\n
Clock - This lets you view and manage your download history, such as deleting it.\n
Gear - Ahhh the classic settings icon lets you reset the program and see some stats.\n
Door - The door will end the program peacefully when you're done downloading.\n
Note - I love feedback and this is how to send it! All feedback is anonymous.
""")
        self.toolbar_help.setWordWrap(True)
        self.toolbar_help.setFont(QFont("Times", 11, QFont.Bold))
        self.toolbar_help.setStyleSheet("color: #FFFFFF")
        self.toolbar_help.hide()

        self.intro_toolbar = QLabel("")
        self.intro_toolbar.setPixmap(QPixmap(r"F:\Dropbox\Python\Classix Video Manager\welcome1.PNG").scaled(484,72))
        self.intro_toolbar.hide()

        self.page_four = QPushButton("             Continue ---->              ")
        self.page_four.setStyleSheet("color: #11052C; background-color: #FFE459; border-style: outset; border-width: 2px; border-radius: 10px; border-color: #3D087B; padding: 6px")
        self.page_four.clicked.connect(self.fourth_page)
        self.page_four.hide()
### Page Four Layout ###
        self.download_text = QLabel("Finally the download box!")
        self.download_text.setFont(QFont("Times", 14, QFont.Bold))
        self.download_text.setStyleSheet("color: #F43B86")
        self.download_text.hide()

        self.download_toolbar = QLabel("")
        self.download_toolbar.setPixmap(QPixmap(r"F:\Dropbox\Python\Classix Video Manager\welcome2.PNG").scaled(505,310))
        self.download_toolbar.hide()

        self.download_help = QLabel("""
And the last part is pretty self-explanatory. Seen here is the download box
and two very important buttons. After you add a download to the download
list, Classix lists the title and if you selected a video or audio download.
Of course, to start downloading your content, click 'Start Download' and the
progress bar will begin to show progress and Classix will show you what it's
currently downloading. When the download is complete, you'll see a message box
and the list will clear for the next downloads or you can quit Classix.
\n
Well... that's pretty much it. Go explore the program and make sure to send feedback!
""")
        self.download_help.setWordWrap(True)
        self.download_help.setFont(QFont("Times", 11, QFont.Bold))
        self.download_help.setStyleSheet("color: #FFFFFF")
        self.download_help.hide()

        self.onward = QPushButton("             Start Classix!              ")
        self.onward.setStyleSheet("color: #11052C; background-color: #FFE459; border-style: outset; border-width: 2px; border-radius: 10px; border-color: #3D087B; padding: 6px")
        self.onward.clicked.connect(self.onward_button)
        self.onward.hide()
        
### Layouts ###
        self.mone.addStretch()
        self.mone.addWidget(self.welcome_text)
        self.mone.addWidget(self.set_dir)
        self.mone.addWidget(self.toolbar_text)
        self.mone.addWidget(self.download_text)
        self.mone.addStretch()

        self.mtwo.addStretch()
        self.mtwo.addWidget(self.welcome_help)
        self.mtwo.addWidget(self.save_loc)
        self.mtwo.addWidget(self.intro_toolbar)
        self.mtwo.addWidget(self.download_toolbar)
        self.mtwo.addStretch()

        self.mthree.addStretch()
        self.mthree.addWidget(self.classix_logo)
        self.mthree.addWidget(self.set_dir_help)
        self.mthree.addWidget(self.toolbar_help)
        self.mthree.addWidget(self.download_help)
        self.mthree.addStretch()

        self.mfour.addStretch()
        self.mfour.addWidget(self.start_button)
        self.mfour.addWidget(self.file_button)
        self.mfour.addWidget(self.page_three)
        self.mfour.addWidget(self.page_four)
        self.mfour.addWidget(self.onward)
        self.mfour.addStretch()

        self.page_one.addLayout(self.mone,0,0)
        self.page_one.addLayout(self.mtwo,1,0)
        self.page_one.addLayout(self.mthree,2,0)
        self.page_one.addWidget(QLabel(" "),3,0)
        self.page_one.addLayout(self.mfour,4,0)
        

        self.show()

    def big_start(self):
        self.welcome_text.hide()
        self.welcome_help.hide()
        self.classix_logo.hide()
        self.start_button.hide()

        self.set_dir.show()
        self.set_dir_help.show()
        self.save_loc.show()
        self.file_button.show()
        self.page_three.show()

    def third_page(self):
        if output_dir == "":
            mbox = QMessageBox.information(self, "Please set a save location!", "You must set a save location in order to finish setup. You can always change it later.")
        else:
            self.set_dir.hide()
            self.set_dir_help.hide()
            self.save_loc.hide()
            self.file_button.hide()
            self.page_three.hide()

            self.toolbar_text.show()
            self.intro_toolbar.show()
            self.toolbar_help.show()
            self.page_four.show()

    def fourth_page(self):
        self.toolbar_text.hide()
        self.intro_toolbar.hide()
        self.toolbar_help.hide()
        self.page_four.hide()

        self.download_text.show()
        self.download_toolbar.show()
        self.download_help.show()
        self.onward.show()

    def onward_button(self):
        global wind
        self.close()
        wind = Window()

    def get_file_dir(self):
        global output_dir
        output_dir = self.file_dir = QFileDialog.getExistingDirectory()
        self.save_loc.setText("Current Save Location: {}".format(output_dir))

        with open("App Files\\output_dir.txt", "w") as file:
            file.write(output_dir)

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(width,height,1000,700)
        self.setWindowTitle("Classix Video Manager")
        self.setWindowIcon(QIcon(r"F:\Dropbox\Python\Classix Video Manager\classix-logo.png"))
        self.setStyleSheet("background-color: #11052C; color: #FFE459")
        self.UI()
        

    def UI(self):
        global main_box
        global pbar
        global curr_item
        global animation

        main_layout = QGridLayout()
        self.setLayout(main_layout)

        hbox = QHBoxLayout()

        toolbar = QToolBar()
        toolbar.setIconSize(QSize(50,50))
        toolbar.setStyleSheet("color: #11052C")
        
        classix = QAction(QIcon(r"F:\Dropbox\Python\Classix Video Manager\classix-logo.png"), "Classix", self)
        classix.triggered.connect(self.test_func)
        toolbar.addAction(classix)

        add_item = QAction(QIcon(r"F:\Dropbox\Python\Classix Video Manager\classix-plus.png"), "Add Item", self)
        add_item.triggered.connect(new_button)
        toolbar.addAction(add_item)
        
        remove_item = QAction(QIcon(r"F:\Dropbox\Python\Classix Video Manager\classix-minus.png"), "Remove Item", self)
        remove_item.triggered.connect(self.remove_button)
        toolbar.addAction(remove_item)

        open_folder = QAction(QIcon(r"F:\Dropbox\Python\Classix Video Manager\classix-folder.png"), "Open Folder", self)
        open_folder.triggered.connect(dir_button)
        toolbar.addAction(open_folder)

        c_history = QAction(QIcon(r"F:\Dropbox\Python\Classix Video Manager\classix-history.png"), "View History", self)
        c_history.triggered.connect(hist_button)
        toolbar.addAction(c_history)

        c_settings = QAction(QIcon(r"F:\Dropbox\Python\Classix Video Manager\classix-gear.png"), "Settings", self)
        c_settings.triggered.connect(settings_button)
        toolbar.addAction(c_settings)

        c_exit = QAction(QIcon(r"F:\Dropbox\Python\Classix Video Manager\classix-exit.png"), "Exit", self)
        c_exit.triggered.connect(self.exit_button)
        toolbar.addAction(c_exit)

        c_feedback = QAction(QIcon(r"F:\Dropbox\Python\Classix Video Manager\classix-feedback.png"), "Feedback", self)
        c_feedback.triggered.connect(feedback_button)
        toolbar.addAction(c_feedback)

        main_box = QListWidget()
        main_box.setFont(QFont("Times",13))
        main_box.setStyleSheet("color: #FFE459; background-color: #3D087B")

        curr_item = QLabel()
        curr_item.setStyleSheet("color: #FFE459")
        curr_item.hide()

        pbar = QProgressBar()
        pbar.setTextVisible(False)
        pbar.setFixedWidth(1000)
        pbar.setMinimum(0)
        pbar.setMaximum(100)

        start_download = QPushButton("Start Download")
        start_download.setStyleSheet("color: #11052C; background-color: #FFE459; border-style: outset; border-width: 2px; border-radius: 10px; border-color: #3D087B; padding: 6px")    
        start_download.clicked.connect(self.run_downloader)

        exit_button = QPushButton("Close Classix")
        exit_button.setStyleSheet("color: #11052C; background-color: #FFE459; border-style: outset; border-width: 2px; border-radius: 10px; border-color: #3D087B; padding: 6px")
        exit_button.clicked.connect(self.exit_button)

        hbox.addWidget(start_download)
        hbox.addWidget(exit_button)

        main_layout.addWidget(toolbar)
        main_layout.addWidget(main_box)
        main_layout.addWidget(curr_item)
        main_layout.addWidget(pbar)
        main_layout.addLayout(hbox,5,0)
        

        self.show()

    def update_pbar(self, percent):
        pbar.setValue(percent)

    def run_downloader(self):        
        self.dlworker = downloader()
        self.thread = QThread()
        self.dlworker.download_progress.connect(self.update_pbar)
        self.dlworker.moveToThread(self.thread)
        self.thread.started.connect(self.dlworker.video_downloader)
        self.dlworker.finished.connect(self.downloads_finished)
        self.thread.start()         

    def downloads_finished(self):
        global download_count, data_count
        self.thread.quit()
        mbox = QMessageBox()
        if len(download_list) == 0:
            mbox.information(self, "This is awkward...", "You should probably click the plus sign to add at least one download...")
            mbox.setStyleSheet("color: rgb(0, 0, 0)")
        else:
            mbox.information(self, "Downloads finished!", "{} files successfully downloaded!".format(len(download_list)))
            mbox.setStyleSheet("color: rgb(0, 0, 0)")
            download_count = len(download_list) + download_count
            download_list.clear()
            try:
                with open("App Files\\download_count.txt", "w") as file:
                    data = str(download_count)+";"+str(data_count)
                    file.write(data)
            except:
                pass

            try:
                with open("App Files\\download_count.txt", "w") as file:
                    data = str(download_count)+";"+str(data_count)
                    file.write(data)
            except:
                pass      

    def test_func(self):
        print("Tested!")

    def remove_button(self):
        if len(download_list) != 0:
            curr_item = main_box.currentRow()
            main_box.takeItem(curr_item)
            download_list.pop(curr_item)
            print(download_list)
        else:
            pass

    def exit_button(self):
        qApp.closeAllWindows()
        sys.exit()

def new_button():
    global new_win
    new_win = new_item()
    return new_win

def dir_button():
    global dir_win
    dir_win = directory_manager()
    return dir_win

def hist_button():
    global hist_win
    hist_win = history_window()
    return hist_win

def settings_button():
    global settings_win
    settings_win = settings_window()
    return settings_win

def feedback_button():
    global feedback_win
    feedback_win = feedback_window()
    return feedback_win


class history_window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(width,height,400,600)
        self.setWindowTitle("Download History")
        self.setWindowIcon(QIcon(r"F:\Dropbox\Python\Classix Video Manager\classix-logo.png"))
        self.setStyleSheet("color: #FFE459; background-color: #11052C")
        self.history_ui()

    def history_ui(self):
        hist_ui_layout = QGridLayout()
        self.setLayout(hist_ui_layout)

        hbox = QHBoxLayout()

        dir_label = QLabel("Download History")
        dir_label.setFont(QFont("Times", 14, QFont.Bold))
        dir_label.setStyleSheet("color: #F43B86")

        self.hist_box = QListWidget()
        
        for item in hist_list:
            self.hist_box.addItem(item)

        clear_button = QPushButton("Delete All")
        clear_button.setStyleSheet("color: #11052C; background-color: #FFE459; border-style: outset; border-width: 2px; border-radius: 10px; border-color: #3D087B; padding: 6px")
        clear_button.clicked.connect(self.clear_all)

        selected_button = QPushButton("Delete Selected")
        selected_button.setStyleSheet("color: #11052C; background-color: #FFE459; border-style: outset; border-width: 2px; border-radius: 10px; border-color: #3D087B; padding: 6px")
        selected_button.clicked.connect(self.clear_selected)

        close_button = QPushButton("Close History")
        close_button.setStyleSheet("color: #11052C; background-color: #FFE459; border-style: outset; border-width: 2px; border-radius: 10px; border-color: #3D087B; padding: 6px")
        close_button.clicked.connect(self.close_window)

        hbox.addWidget(clear_button)
        hbox.addWidget(selected_button)

        hist_ui_layout.addWidget(dir_label)
        hist_ui_layout.addWidget(self.hist_box)
        hist_ui_layout.addLayout(hbox,2,0)
        hist_ui_layout.addWidget(close_button)

        self.show()

    def close_window(self):
        self.close()

    def clear_all(self):
        try:
            self.hist_box.clear()
            os.remove("hist_file.txt")
        except:
            mbox = QMessageBox.critical(self, "Error!", "No history found or history has already been cleared.\nRestart Classix and try again.")

    def clear_selected(self):
        try:
            item = self.hist_box.currentRow()
            self.hist_box.takeItem(item)
            deleted = self.hist_box.currentItem().text()

            for item in hist_list:
                if item == deleted:
                    hist_list.remove(item)

            with open("App Files\\hist_file.txt", "w", encoding="utf-8") as file:
                for line in hist_list:
                    file.write(line)
        except:
            mbox = QMessageBox.critical(self, "Error!", "No history found or history has already been cleared.\nRestart Classix and try again.")

class settings_window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(width,height,500,700)
        self.setWindowTitle("Settings")
        self.setWindowIcon(QIcon(r"F:\Dropbox\Python\Classix Video Manager\classix-logo.png"))
        self.setStyleSheet("color: #FFE459; background-color: #11052C")
        self.settings_ui()

    def settings_ui(self):
        mb_count = str(round(data_count/1000000,2))
        gb_count = str(round((data_count/1000000)/1024,2))

        sett_ui_layout = QGridLayout()
        self.setLayout(sett_ui_layout)

        sett_text = QLabel("Settings")
        sett_text.setFont(QFont("Times", 14, QFont.Bold))
        sett_text.setStyleSheet("color: #F43B86")

        stats_text = QLabel("Stats")
        stats_text.setFont(QFont("Times", 12, QFont.Bold))

        total_downloads = QLabel("Files Downloaded: {}".format(download_count))
        total_data = QLabel("Data Downloaded: {} MB/{} GB".format(mb_count, gb_count))

        reset_text = QLabel("Reset")
        reset_text.setFont(QFont("Times", 12, QFont.Bold))

        reset_help = QLabel("""
FYI! The 'Reset Stats' button will only clear the download and data count.
If you click 'Reset All', all stats, history, and save location data will be erased.
""")
        reset_help.setWordWrap(True)

        reset_stats = QPushButton("Reset Stats")
        reset_stats.setStyleSheet("color: #11052C; background-color: #FFE459; border-style: outset; border-width: 2px; border-radius: 10px; border-color: #3D087B; padding: 6px")
        reset_stats.clicked.connect(self.reset_stats_button)

        reset_all = QPushButton("Reset All")
        reset_all.setStyleSheet("color: #11052C; background-color: #FFE459; border-style: outset; border-width: 2px; border-radius: 10px; border-color: #3D087B; padding: 6px")
        reset_all.clicked.connect(self.reset_all_button)

        about_text = QLabel("About")
        about_text.setFont(QFont("Times", 12, QFont.Bold))

        about_info = QLabel("""
Classix is an Open Source Python project created by Z Tech and Data. The intent of
this program is to provide a simple way for people to download and manage videos they
have the rights to or are using under public domain. Use of Classix means that you understand
this. More information about fair use can be found by clicking the 'Copyright Policy' button below
or visiting https://www.youtube.com/howyoutubeworks/policies/copyright/#overview.\n\nThanks for using Classix!
            """)
        about_info.setWordWrap(True)

        version_info = QLabel("Classix Version 1.0.0")

        copyright_policy = QPushButton("Copyright Policy")
        copyright_policy.setStyleSheet("color: #11052C; background-color: #FFE459; border-style: outset; border-width: 2px; border-radius: 10px; border-color: #3D087B; padding: 6px")
        copyright_policy.clicked.connect(self.copyright_policy_button)

        me_button = QPushButton("Visit Z Tech and Data")
        me_button.setStyleSheet("color: #11052C; background-color: #FFE459; border-style: outset; border-width: 2px; border-radius: 10px; border-color: #3D087B; padding: 6px")
        me_button.clicked.connect(self.me_button)

        close_sett = QPushButton("Close Settings")
        close_sett.setStyleSheet("color: #11052C; background-color: #FFE459; border-style: outset; border-width: 2px; border-radius: 10px; border-color: #3D087B; padding: 6px")
        close_sett.clicked.connect(self.close_button)

        sett_ui_layout.addWidget(sett_text)
        sett_ui_layout.addWidget(stats_text)
        sett_ui_layout.addWidget(total_downloads)
        sett_ui_layout.addWidget(total_data)
        sett_ui_layout.addWidget(reset_text)
        sett_ui_layout.addWidget(reset_help)
        sett_ui_layout.addWidget(reset_stats)
        sett_ui_layout.addWidget(reset_all)
        sett_ui_layout.addWidget(about_text)
        sett_ui_layout.addWidget(about_info)
        sett_ui_layout.addWidget(version_info)
        sett_ui_layout.addWidget(copyright_policy)
        sett_ui_layout.addWidget(me_button)
        sett_ui_layout.addWidget(close_sett)

        self.show()

    def reset_stats_button(self):
        try:
            os.remove("App Files\\download_count.txt")
            mbox = QMessageBox.information(self, "Data Erased!", "All stats have been removed!")
        except:
            mbox = QMessageBox.warning(self, "Whoops!", "No data found! It may have already been deleted. Try restarting Classix.")
    
    def reset_all_button(self):
        try:
            try:
                os.remove("App Files\\hist_file.txt")
            except:
                pass
            try:
                os.remove("App Files\\output_dir.txt")
            except:
                pass
            try:
                os.remove("App Files\\download_count.txt")
            except:
                pass
            mbox = QMessageBox.information(self, "Data Erased!", "All Classix data has been deleted!")
        except:
            mbox = QMessageBox.warning(self, "Whoops!", "No data found! It may have already been deleted. Try restarting Classix.")

    def copyright_policy_button(self):
        os.system("start https://www.youtube.com/howyoutubeworks/policies/copyright/#overview")

    def me_button(self):
        os.system("start https://www.ztdapps.com")

    def close_button(self):
        self.close()

class feedback_window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(width,height,700,500)
        self.setWindowTitle("Feedback")
        self.setWindowIcon(QIcon(r"F:\Dropbox\Python\Classix Video Manager\classix-logo.png"))
        self.setStyleSheet("color: #FFE459; background-color: #11052C")
        self.feedback_ui()

    def feedback_ui(self):
        feedback_ui_layout = QGridLayout()
        self.setLayout(feedback_ui_layout)

        hbox = QHBoxLayout()
        close_hbox = QHBoxLayout()

        feed_text = QLabel("Feedback")
        feed_text.setFont(QFont("Times", 14, QFont.Bold))
        feed_text.setStyleSheet("color: #F43B86")

        help_text = QLabel("Hi there! Hope you're enjoying Classix! Feedback is always welcome and helps me improve the app for you.\
            \nFeel free to send feature requests, bugs or words of inspiration. All messages are anonymous unless you choose to add personal info.")

        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("Subject")

        self.body_input = QTextEdit()
        self.body_input.setPlaceholderText("Use this space for comments, suggestions, and ways I can improve Classix!")

        send_button = QPushButton("Send Feedback")
        send_button.setStyleSheet("color: #11052C; background-color: #FFE459; border-style: outset; border-width: 2px; border-radius: 10px; border-color: #3D087B; padding: 6px")
        send_button.clicked.connect(self.send_feedback)

        clear_button = QPushButton("Clear All")
        clear_button.setStyleSheet("color: #11052C; background-color: #FFE459; border-style: outset; border-width: 2px; border-radius: 10px; border-color: #3D087B; padding: 6px")
        clear_button.clicked.connect(self.clear_all)

        close_button = QPushButton("        Close Feedback      ")
        close_button.setStyleSheet("color: #11052C; background-color: #FFE459; border-style: outset; border-width: 2px; border-radius: 10px; border-color: #3D087B; padding: 6px")
        close_button.clicked.connect(self.close_window)

        hbox.addWidget(send_button)
        hbox.addWidget(clear_button)

        close_hbox.addStretch()
        close_hbox.addWidget(close_button)
        close_hbox.addStretch()

        feedback_ui_layout.addWidget(feed_text)
        feedback_ui_layout.addWidget(help_text)
        feedback_ui_layout.addWidget(self.subject_input)
        feedback_ui_layout.addWidget(self.body_input)
        feedback_ui_layout.addLayout(hbox,4,0)
        feedback_ui_layout.addLayout(close_hbox,5,0)

        self.show()

    def clear_all(self):
        self.subject_input.clear()
        self.body_input.clear()

    def close_window(self):
        self.close()

    def send_feedback(self):
        warnings.simplefilter("ignore")
        port = 587
        smtp_server = "smtp.site.com"
        sender_email = "email@example.com"
        recieve_email = "email@example.com"
        password = "thisisapassword"

        subject = self.subject_input.text()
        message = self.body_input.toPlainText()

        print(subject)
        print(message)

        message = """\
Subject:Classix Feedback - {}

{}

""".format(subject, message)
        if subject and message != "":
            try:
                context = ssl.create_default_context()
                with smtplib.SMTP(smtp_server, port) as server:
                    server.starttls(context=context)
                    server.login(sender_email, password)
                    server.sendmail(sender_email, recieve_email, message)
                self.subject_input.clear()
                self.body_input.clear()
                mbox = QMessageBox.information(self, "Feedback Recieved!", "Thanks for your feedback! I'll make sure to read it as soon as possible!")
            except:
                mbox = QMessageBox.warning(self, "Feedback Not Sent!", "Make sure to include both a subject and message.")
        else:
            mbox = QMessageBox.warning(self, "Feedback Not Sent!", "Make sure to include both a subject and message.")

class directory_manager(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(width,height,300,200)
        self.setWindowTitle("Directory Manager")
        self.setWindowIcon(QIcon(r"F:\Dropbox\Python\Classix Video Manager\classix-logo.png"))
        self.setStyleSheet("color: #FFE459; background-color: #11052C")
        self.dir_ui()

    def dir_ui(self):
        dir_ui_layout = QGridLayout()
        self.setLayout(dir_ui_layout)

        dir_label = QLabel("Directory Management")
        dir_label.setFont(QFont("Times", 14, QFont.Bold))
        dir_label.setStyleSheet("color: #F43B86")

        self.current_dir = QLabel("Current Save Location: {}".format(output_dir))

        get_dir = QPushButton("Select/Change Save Location")
        get_dir.setStyleSheet("color: #11052C; background-color: #FFE459; border-style: outset; border-width: 2px; border-radius: 10px; border-color: #3D087B; padding: 6px")
        get_dir.clicked.connect(self.get_dir_name)

        goto_dir = QPushButton("Open Save Location")
        goto_dir.setStyleSheet("color: #11052C; background-color: #FFE459; border-style: outset; border-width: 2px; border-radius: 10px; border-color: #3D087B; padding: 6px")
        goto_dir.clicked.connect(self.goto_dir)

        close_button = QPushButton("Close Directory Management")
        close_button.setStyleSheet("color: #11052C; background-color: #FFE459; border-style: outset; border-width: 2px; border-radius: 10px; border-color: #3D087B; padding: 6px")
        close_button.clicked.connect(self.close_window)


        dir_ui_layout.addWidget(dir_label)
        dir_ui_layout.addWidget(self.current_dir)
        dir_ui_layout.addWidget(get_dir)
        dir_ui_layout.addWidget(goto_dir)
        dir_ui_layout.addWidget(close_button)

        self.show()

    def get_dir_name(self):
        global output_dir
        output_dir = QFileDialog.getExistingDirectory()
        self.current_dir.setText("Current Save Location: {}".format(output_dir))

        with open("App Files\\output_dir.txt", "w") as file:
            file.write(output_dir)

    def goto_dir(self):
        if output_dir != "":
            os.startfile(output_dir)
        else:
            mbox = QMessageBox()
            mbox.setStyleSheet("background-color: #F43B86; border-style: outset; border-width: 2px; border-radius: 10px; border-color: #3D087B; padding: 6px")
            mbox.warning(self, "No output folder selected!", "Please select a valid output folder.")
    
    def close_window(self):
        self.close()

class new_item(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(width,height,500,700)
        self.setWindowTitle("Add New Download")
        self.setWindowIcon(QIcon(r"F:\Dropbox\Python\Classix Video Manager\classix-logo.png"))
        self.setStyleSheet("color: #FFE459; background-color: #11052C")
        self.add_item_ui()

    def add_item_ui(self):

        new_item_layout = QGridLayout()
        self.setLayout(new_item_layout)

        hbox = QHBoxLayout()
        hbox_vid = QHBoxLayout()

        add_text = QLabel("Add Video")
        add_text.setFont(QFont("Times", 14, QFont.Bold))
        add_text.setStyleSheet("color: #F43B86")

        self.help_text = QLabel("Paste or enter an online video link and the title, description, view count, and video thumbnail will appear.\nChoose between video or audio and then click add video to add to download list.")
        self.help_text.setStyleSheet("color: #FFE459")

        self.link_entry = QLineEdit()
        self.link_entry.setStyleSheet("color: #FFE459")
        self.link_entry.setPlaceholderText("Enter or Paste (Ctrl + V) Video Link Here")
        
        search_button = QPushButton("Search")
        search_button.setStyleSheet("color: #11052C; background-color: #FFE459; border-style: outset; border-width: 2px; border-radius: 10px; border-color: #3D087B; padding: 6px")
        search_button.clicked.connect(self.get_vid_info)

        self.title_text = QLabel("Title will display here. ")
        self.title_text.setMaximumWidth(500)
        self.title_text.setWordWrap(True)
        self.title_text.setFont(QFont("Times", 14, QFont.Bold))
        self.title_text.setStyleSheet("color: #F43B86")
        self.title_text.hide()

        space = QLabel("")

        self.desc_text = QLabel("Description will display here. ")
        self.desc_text.setMaximumWidth(500)
        self.desc_text.setWordWrap(True)
        self.desc_text.setStyleSheet("color: #F43B86")
        self.desc_text.hide()

        self.thumbnail_img = QLabel("Thumbnail will display here. ")
        self.thumbnail_img.setStyleSheet("color: #F43B86")
        self.thumbnail_img.hide()

        hbox_vid.addStretch()
        hbox_vid.addWidget(self.thumbnail_img)
        hbox_vid.addStretch()

        add_button = QPushButton("Add Video")
        add_button.setStyleSheet("color: #11052C; background-color: #FFE459; border-style: outset; border-width: 2px; border-radius: 10px; border-color: #3D087B; padding: 6px")
        add_button.clicked.connect(self.download_list)

        close_button = QPushButton("Close New Video Menu")
        close_button.setStyleSheet("color: #11052C; background-color: #FFE459; border-style: outset; border-width: 2px; border-radius: 10px; border-color: #3D087B; padding: 6px")
        close_button.clicked.connect(self.close_window)

        self.radio_vid = QRadioButton("Video")
        self.radio_audio = QRadioButton("Audio Only")
        hbox.addStretch()
        hbox.addWidget(self.radio_vid)
        hbox.addWidget(self.radio_audio)
        hbox.addStretch()

        new_item_layout.addWidget(add_text)
        new_item_layout.addWidget(self.help_text)
        new_item_layout.addWidget(self.link_entry)
        new_item_layout.addWidget(search_button)
        new_item_layout.addWidget(self.title_text)
        new_item_layout.addWidget(self.desc_text)
        new_item_layout.addLayout(hbox_vid, 10, 0)
        new_item_layout.addLayout(hbox, 11 ,0)
        new_item_layout.addWidget(add_button)
        new_item_layout.addWidget(close_button)
        
        self.show()

    def close_window(self):
        self.close()

    def get_vid_info(self):
        if self.link_entry.text() != "" and (self.link_entry.text()).startswith("https"):
            self.url = self.link_entry.text()
            video = YouTube(self.url)
            dirpath = tempfile.mkdtemp()

            title = video.title
            desc = video.description
            thumbnail = video.thumbnail_url

            if len(desc) > 400:
                desc = desc[:401] + "..."

            urlretrieve(thumbnail,dirpath+"/yt_thumbnail.png")

            self.title_text.show()
            self.desc_text.show()
            self.thumbnail_img.show()
            self.help_text.hide()

            self.title_text.setText("{}".format(title))
            self.desc_text.setText("{}".format(desc))
            self.thumbnail_img.setPixmap(QPixmap(dirpath+"/yt_thumbnail.png"))
            self.thumbnail_img.setFixedSize(QSize(450,253))
            self.thumbnail_img.setAlignment(Qt.AlignCenter)

            shutil.rmtree(dirpath)
        else:
            mbox = QMessageBox()
            mbox.setStyleSheet("background-color: #F43B86; border-style: outset; border-width: 2px; border-radius: 10px; border-color: #3D087B; padding: 6px")
            mbox.warning(self, "No video URL entered!", "Please enter a valid video URL to search for a video.")

    def download_list(self):
        try:
            if self.radio_vid.isChecked():
                download_list.append("1"+self.url)
                main_box.addItem(self.title_text.text()+" - Video Download")
                self.close()
            if self.radio_audio.isChecked():
                download_list.append("2"+self.url)
                main_box.addItem(self.title_text.text()+" - Audio Download")
                self.close()
            elif self.isActiveWindow():
                mbox = QMessageBox()
                mbox.setStyleSheet("background-color: #F43B86; border-style: outset; border-width: 2px; border-radius: 10px; border-color: #3D087B; padding: 6px")
                mbox.warning(self, "No download option selected!", "Please select either video or audio.")
        except:
            mbox = QMessageBox()
            mbox.setStyleSheet("background-color: #F43B86; border-style: outset; border-width: 2px; border-radius: 10px; border-color: #3D087B; padding: 6px")
            mbox.warning(self, "Please enter a valid URL!", "Please enter a valid video URL to search for a video.")
                


class downloader(QThread):
    download_progress = pyqtSignal(int)
    finished = pyqtSignal()

    def progress_func(self, stream=None, data=None, fleft=None):
        try:
            percent = int((100*(fsize-fleft))/fsize)
            self.download_progress.emit(percent)
        except:
            pass

    @pyqtSlot()
    def video_downloader(self):
        global fsize, fname, curr_download, data_count
        curr_download = 1
        temp_size = 0
        fname = ""
        fsize = 0
        curr_item.show()

        for item in download_list:
            try:
                if str(item).startswith("1"):
                    new_url = item[1:]
                    yt = YouTube(new_url, on_progress_callback=self.progress_func)
                    videofile = yt.streams.filter(res="1080p", progressive=True).first()
                    if videofile == None:
                        videofile = yt.streams.filter(progressive=True).get_highest_resolution()
                    fsize = int(videofile.filesize)
                    fname = str(videofile.title)
                    temp_hist_list.append(fname+" - Video")
                    curr_item_text = "Downloading: {} ({}/{})".format(fname, str(curr_download), str(len(download_list)))
                    curr_item.setText(curr_item_text)
                    videofile.download(output_dir)
                    temp_size = fsize + temp_size
                if str(item).startswith("2"):
                    new_url = item[1:]
                    yt = YouTube(new_url, on_progress_callback=self.progress_func)
                    audiofile = yt.streams.filter(only_audio=True).get_audio_only()
                    fsize = int(audiofile.filesize)
                    fname = str(audiofile.title)
                    temp_hist_list.append(fname+" - Audio")
                    curr_item_text = "Downloading: {} ({}/{})".format(fname, str(curr_download), str(len(download_list)))
                    curr_item.setText(curr_item_text)
                    audiofile.download(output_dir)
                    temp_size = fsize + temp_size
                curr_download = curr_download + 1
            except:
                pass

        data_count = temp_size

        with open("App Files\\hist_file.txt", "a", encoding="utf-8") as file:
            for item in temp_hist_list:
                file.write(item+"\n")

        curr_item.hide()
        pbar.setValue(0)
        main_box.clear()
        self.finished.emit()        
        
def main():
    App = QApplication(sys.argv)
    if output_dir == "":
        welcome = welcome_win()
    else:
        win = Window()
    sys.exit(App.exec_())

if __name__ == "__main__":
    main()

#welcome window
