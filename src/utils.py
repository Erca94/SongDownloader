from PyQt5.QtWidgets import QMessageBox


STATUS = "Status: {}"
OUTPUT_FOLDER = "Output folder: {}"
FILE_NAME = "File name: {}"


def get_info_box(title):
    """
    Get the message box for download (everything ok)

    Parameters
    ----------
    title : str
        the title of the song

    Returns
    -------
    message
        the message window that reports everything went well
    """
    message = QMessageBox()
    message.setIcon(QMessageBox.Information)
    message.setText("Song downloaded")
    message.setInformativeText(FILE_NAME.format(title))
    message.setWindowTitle("Downloaded")
    return message


def get_error_box(e):
    """
    Get the error box for download (something went wrong)

    Parameters
    ----------
    e : Exception
        the exception returned from the downloading process;
        something went wrong

    Returns
    -------
    error
        the error window that reports something went wrong
    """
    error = QMessageBox()
    error.setIcon(QMessageBox.Critical)
    error.setText("Something went wrong...")
    error.setInformativeText(str(e))
    error.setWindowTitle("Error")
    return error

