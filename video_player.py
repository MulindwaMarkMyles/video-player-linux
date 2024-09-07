import sys
import vlc
from PyQt5 import QtWidgets, QtGui, QtCore

class VideoPlayer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize VLC player instance
        # vlc_args = ["--no-xlib", "--avcodec-hw=vaapi"] 
        self.vlc_instance = vlc.Instance()
        self.media_player = self.vlc_instance.media_player_new()

        # Set up the UI
        self.init_ui()

    def init_ui(self):
        # Create a central widget and a layout
        self.widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.widget)
        self.layout = QtWidgets.QVBoxLayout()
        self.widget.setLayout(self.layout)

        # Create a video frame to display the video
        self.video_frame = QtWidgets.QFrame(self)
        self.layout.addWidget(self.video_frame)

        # Create control buttons
        self.play_button = QtWidgets.QPushButton('Play')
        self.stop_button = QtWidgets.QPushButton('Stop')
        self.open_button = QtWidgets.QPushButton('Open File')

        # Create a horizontal layout for buttons
        self.control_layout = QtWidgets.QHBoxLayout()
        self.control_layout.addWidget(self.open_button)
        self.control_layout.addWidget(self.play_button)
        self.control_layout.addWidget(self.stop_button)

        # Add button layout to the main layout
        self.layout.addLayout(self.control_layout)

        # Connect button signals to their respective functions
        self.play_button.clicked.connect(self.play_video)
        self.stop_button.clicked.connect(self.stop_video)
        self.open_button.clicked.connect(self.open_file)

        # Set window properties
        self.setWindowTitle("Python Video Player")
        self.setGeometry(100, 100, 800, 600)
        self.show()

    def open_file(self):
        # Open a file dialog to select video
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Video")

        if filename:
            # Set the media and attach it to VLC player
            self.media = self.vlc_instance.media_new(filename)
            self.media_player.set_media(self.media)
            self.media_player.set_xwindow(int(self.video_frame.winId()))

    def play_video(self):
        # Play the video
        self.media_player.play()

    def stop_video(self):
        # Stop the video
        self.media_player.stop()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    player = VideoPlayer()
    sys.exit(app.exec_())
