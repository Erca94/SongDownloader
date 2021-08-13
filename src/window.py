import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QVBoxLayout, QDialog,
                             QProgressBar, QPushButton, 
                             QLineEdit, QDesktopWidget,
                             QFileDialog, QHBoxLayout,
                             QLabel)
from utils import STATUS, OUTPUT_FOLDER, FILE_NAME
from download_thread import DownloadThread


class DownloaderWindow(QDialog):
    """
    This class is used for handling the downloader
    and for not freezing the main window. It's able to
    download the audio in mp3 format from a youtube video.

    Attributes
    ----------
    layout: PyQt5.QtWidgets.QVBoxLayout
        the external layout that contains all the widgets
    h_layout1: PyQt5.QtWidgets.QHBoxLayout
        the first internal layout that contains the first line of widgets
    url_label: PyQt5.QtWidgets.QLabel
        the label for the url
    url_box: PyQt5.QtWidgets.QLineEdit
        the text box for the url
    h_layout2: PyQt5.QtWidgets.QHBoxLayout
        the second internal layout that contains the second line of widgets
    destination_label: PyQt5.QtWidgets.QLabel
        the label for the destination folder
    directory_box: PyQt5.QtWidgets.QLineEdit
        the text box for the destination folder, uneditable
    browse_button: PyQt5.QtWidgets.QPushButton
        the button for browsing the filesystem
    download_button: PyQt5.QtWidgets.QPushButton
        the button for downloading
    progress_bar: PyQt5.QtWidgets.QProgressBar
        the bar used for tracking the downloading status
    status_l: PyQt5.QtWidgets.QLabel
        the label for the downloading status
    folder_l: PyQt5.QtWidgets.QLabel
        the label for the downloading folder
    filename_l: PyQt5.QtWidgets.QLabel
        the label for the downloading destination filename

    Methods
    -------
    _center()
        Center the window in the screen.
        
    _init_ui()
        Initialize the window and set the layout and the widgets.
        
    _browse_filesystem()
        Action executed when the button for browsing the filesystem is clicked;
        it allows to browse the filesystem and choose the destination directory.
        
    _download()
        Action executed when the button for downloading is clicked;
        it allows to start the downloading from youtube form the url pasted.
        
    _update_status(value)
        Event that allows to update the downloading status.
        
    _update_folder(value)
        Event that allows to update the destination folder label.
    
    _update_filename(value)
        Event that allows to update the output filename.
        
    _update_percentage(value)
        Event that allows to update the percentage of downloading.
    """
    
    def __init__(self):
        super().__init__()
        self._init_ui()
        
    
    def _center(self):
        """
        Center the window in the screen.
        """
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        #move the window in the center of the screen
        self.move(qt_rectangle.topLeft())
    
    
    def _init_ui(self):
        """
        Initialize the window and set the layout and the widgets.
        """
        title = 'Music Downloader'
        left = 10
        top = 10
        width = 800
        height = 270
        
        #add the two buttons on the top right of the window
        #one for closing and the other for minimizing the window
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowCloseButtonHint, True)
        self.setWindowTitle(title)
        self.setGeometry(left, top, width, height)
        #create the external layout for the window (vertical)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        #create the first internal layout for the window (horizontal) 
        self.h_layout1 = QHBoxLayout()
        self.layout.addLayout(self.h_layout1)
        
        self.url_label = QLabel("URL:")
        self.h_layout1.addWidget(self.url_label)
    
        self.url_box = QLineEdit(self)
        self.h_layout1.addWidget(self.url_box)
        #create the second internal layout for the window (horizontal) 
        self.h_layout2 = QHBoxLayout()
        self.layout.addLayout(self.h_layout2)
        
        self.destination_label = QLabel("Destination:")
        self.h_layout2.addWidget(self.destination_label)
        
        self.directory_box = QLineEdit(self)
        self.directory_box.setText(os.getcwd())
        #the text box for the destination folder must not be editable by hand
        self.directory_box.setReadOnly(True)
        
        self.h_layout2.addWidget(self.directory_box)
        #the button for choosing the directory
        self.browse_button = QPushButton('Browse', self)
        self.h_layout2.addWidget(self.browse_button)
        #the button for starting the download
        self.download_button = QPushButton('Download', self)
        self.layout.addStretch(1)
        self.layout.addWidget(self.download_button)
        #the percentage progress bar for the downloading status, it will be updated by the download thread
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.layout.addStretch(1)
        self.layout.addWidget(self.progress_bar)
        #the label for the downloading status, it will be updated by the download thread
        self.status_l = QLabel(STATUS.format(""))
        self.layout.addWidget(self.status_l)
        #the label for the destination folder, it will be updated by the download thread
        self.folder_l = QLabel(OUTPUT_FOLDER.format(""))
        self.layout.addWidget(self.folder_l)
        #the label for the output filename, it will be updated by the download thread
        self.filename_l = QLabel(FILE_NAME.format(""))
        self.layout.addWidget(self.filename_l)
        
        self.download_button.clicked.connect(self._download)
        self.browse_button.clicked.connect(self._browse_filesystem)
        self._center()
        self.show()
        
    
    def _browse_filesystem(self):
        """
        Action executed when the button for browsing the filesystem is clicked;
        it allows to browse the filesystem and choose the destination directory.
        """
        path = QFileDialog.getExistingDirectory(self, 'Choose a destination directory')
        if path:
            self.directory_box.setText(path)
                
    
    def _download(self):
        """
        Action executed when the button for downloading is clicked;
        it allows to start the downloading from youtube form the url pasted.
        """
        url = self.url_box.text().strip()
        self.downloader = DownloadThread(url, self.directory_box.text()) #the downloading thread
        #connect the widgets to the downloading thread
        self.downloader.percentage_changed.connect(self._update_percentage)
        self.downloader.status_changed.connect(self._update_status)
        self.downloader.folder_changed.connect(self._update_folder)
        self.downloader.filename_changed.connect(self._update_filename)
        #start the downloading process
        self.downloader.start()

    
    def _update_status(self, value):
        """
        Event that allows to update the downloading status.
        
        Parameters
        ----------
        value : str
            The status
        """
        self.status_l.setText(value)
        
    
    def _update_folder(self, value):
        """
        Event that allows to update the destination folder label.
        
        Parameters
        ----------
        value : str
            The destination folder
        """
        self.folder_l.setText(value)
        
    
    def _update_filename(self, value):
        """
        Event that allows to update the output filename.
        
        Parameters
        ----------
        value : str
            The output filename
        """
        self.filename_l.setText(value)
    
    def _update_percentage(self, value):
        """
        Event that allows to update the percentage of downloading.
        
        Parameters
        ----------
        value : int
            The current percentage
        """
        self.progress_bar.setValue(value)
        
        