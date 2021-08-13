from PyQt5.QtCore import QThread, pyqtSignal
import youtube_dl
from utils import get_info_box, get_error_box
from utils import STATUS, OUTPUT_FOLDER, FILE_NAME


class DownloadThread(QThread):
    """
    This class is used for handling the downloader
    and for not freezing the main window. It's able to
    download the audio in mp3 format from a youtube video.

    Attributes
    ----------
    percentage_changed : PyQt5.QtCore.pyqtSignal
        the signal for updating the percentage of downloading
    status_changed : PyQt5.QtCore.pyqtSignal
        the signal for updating the downloading status
    folder_changed : PyQt5.QtCore.pyqtSignal
        the signal for updating the folder in which saving the final file
    filename_changed : PyQt5.QtCore.pyqtSignal
        the signal for updating the final file name
    url: str
        the url from which download the audio
    path: str
        the folder in which save the downloaded audio

    Methods
    -------
    _get_youtube_options()
        Get the options dictionary used for downloading.
        
    _hook_status(info)
        Update the status of downloading, sending signals to the main window, 
        e.g. the percentage of downloading and the status. 
        
    run()
        Execute the download itself and send a feedback regarding the output (OK or KO).
    """
    
    #signals for updating the widgets in the main window
    percentage_changed = pyqtSignal(int)
    status_changed = pyqtSignal(str)
    folder_changed = pyqtSignal(str)
    filename_changed = pyqtSignal(str)
    
    
    def __init__(self, url, path, parent=None):
        QThread.__init__(self, parent)
        self.url = url
        self.path = path
        
    
    def _get_youtube_options(self):
        """
        Get the options dictionary used for downloading.

        Returns
        -------
        ydl_opts
            a dictionary with the option for downloading from youtube
        """
        ydl_opts = {
            'noplaylist':True, #stop the download of an entire playlist, download only the first song of a playlist
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3', #extracting in mp3 format
                'preferredquality': '192',
            }],
            'progress_hooks': [self._hook_status], #custom hook function that update the window
            'outtmpl': self.path + '/%(title)s.%(ext)s', #output folder choosen + song title 
        }
        return ydl_opts
    
    
    def _hook_status(self, info):
        """
        Update the status of downloading, sending signals to the main window, 
        e.g. the percentage of downloading and the status.

        Parameters
        ----------
        info : dict
            The dictionary with the information regarding the downloading status
        """
        if info['status'] == 'finished':
            #the download process has finished 
            #so set 100% as complention and finished as status
            self.percentage_changed.emit(100)
            self.status_changed.emit(STATUS.format("finished!"))
        if info['status'] == 'downloading':
            #the download process has not finished yet
            #so set the percentage as complention and downloading as status
            perc = info['_percent_str']
            self.percentage_changed.emit(int(float(perc.replace("%","").strip())))
            self.status_changed.emit(STATUS.format("downloading..."))

    
    def run(self):
        """
        Execute the download itself and send a feedback regarding the output (OK or KO).
        """
        #get download options
        ydl_opts = self._get_youtube_options()
        #update the destination folder label in the window 
        self.folder_changed.emit(OUTPUT_FOLDER.format(self.path))
        self.filename_changed.emit(FILE_NAME.format(""))
        #set percentage as 0, download just started
        self.percentage_changed.emit(0)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(self.url)
                #get the title of the video
                self.filename_changed.emit(FILE_NAME.format(info.get("title", "None")))
                message = get_info_box(info.get("title", "None"))
                #show the message that everything went well
                message.exec_()
            except Exception as e:
                self.status_changed.emit(STATUS.format("stopped!"))
                error = get_error_box(e)
                #show the message that something went wrong and show what
                error.exec_()
                
                