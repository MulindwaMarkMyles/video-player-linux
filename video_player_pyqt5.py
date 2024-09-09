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
        
        # Initialize the timer to update the progress bar
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)  # Update every second
        self.timer.timeout.connect(self.update_slider)

        # Track the playback state
        self.is_playing = False
        
        # Set up the UI
        self.init_ui()

    def init_ui(self):
        # Create a central widget and a layout
        self.widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.widget)
        self.layout = QtWidgets.QVBoxLayout()
        self.widget.setLayout(self.layout)
        
        # Remove the title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        
        # Apply a style sheet to the entire window
        self.setStyleSheet("""
            QMainWindow {
                background-color: #000;
                border-radius: 20px;
            }
            QPushButton {
                background-color: #FFF;
                font-size: 20px;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #555;
            }
            QSlider::handle:horizontal {
                background: #888;
                border: 1px solid #555;
                border-radius: 10px;
                width: 10px;
                height: 10px;
                margin: -2px 0; 
            }
            QSlider::groove:horizontal {
                background: #444;
                height: 5px;
                border-radius: 5px;
            }
            QSlider::sub-page:horizontal {
                background: #00BCD4;
                border-radius: 2px;
            }
        """)
        

        # Create a video frame to display the video
        self.video_frame = QtWidgets.QFrame(self)
        self.layout.addWidget(self.video_frame)
        
        # Create a progress slider
        # Create a horizontal layout for the progress slider
        
        progress_layout = QtWidgets.QHBoxLayout()
    
        # Create an overlay widget for the controls
        self.control_widget = QtWidgets.QWidget(self.video_frame)
        # self.control_widget.setStyleSheet("background: rgba(255, 255, 255, 0.4);")  # Semi-transparent background


        # Create an overlay layout for control buttons
        self.control_layout = QtWidgets.QHBoxLayout()
        self.control_widget.setLayout(self.control_layout)
        
        # Create a progress slider
        self.progress_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.progress_slider.setRange(0, 1000)  # Placeholder range
        self.progress_slider.sliderMoved.connect(self.set_position)

        # Set fixed width for the progress slider
        self.progress_slider.setFixedWidth(400)  # Adjust the width to your desired length

        # Add stretchable space before and after the progress slider to center it
        progress_layout.addStretch(1)  # Stretch before the slider
        progress_layout.addWidget(self.progress_slider)
        progress_layout.addStretch(1)  # Stretch after the slider

        # Add the progress slider layout to the main layout
        self.layout.addLayout(progress_layout)
        
        self.progress_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #888;
                height: 10px;
                background: #555;
            }
            QSlider::handle:horizontal {
                background: #fff;
                width: 20px;
                height: 20px;
            }
            QSlider::handle:horizontal:hover {
                background: #f0f0f0;
            }
            QSlider::sub-page:horizontal {
                background: #bebdbd;
                border: 1px solid #777;
            }
            QSlider::add-page:horizontal {
                background: #333;
                border: 1px solid #333;
            }
        """)


        # Create control buttons with icons
        self.play_button = QtWidgets.QPushButton(QtGui.QIcon('/home/mulindwa/Documents/flutter/linux_video/assets/play-outline.svg'), "")
        self.pause_button = QtWidgets.QPushButton(QtGui.QIcon('/home/mulindwa/Documents/flutter/linux_video/assets/pause-outline.svg'), "")
        self.stop_button = QtWidgets.QPushButton(QtGui.QIcon('/home/mulindwa/Documents/flutter/linux_video/assets/stop-outline.svg'), "")
        self.open_button = QtWidgets.QPushButton(QtGui.QIcon('/home/mulindwa/Documents/flutter/linux_video/assets/folder-open-outline.svg'), "")

        # Set button sizes
        self.play_button.setFixedWidth(100)  
        self.pause_button.setFixedWidth(100)
        self.stop_button.setFixedWidth(100)
        self.open_button.setFixedWidth(100)
        
        
        self.control_layout.addStretch(1) 
        self.control_layout.addWidget(self.open_button)
        self.control_layout.addWidget(self.play_button)
        self.control_layout.addWidget(self.pause_button)
        self.control_layout.addWidget(self.stop_button)
        self.control_layout.addStretch(1) 


        # Connect button signals to their respective functions
        self.play_button.clicked.connect(self.play_video)
        self.pause_button.clicked.connect(self.pause_video)
        self.stop_button.clicked.connect(self.stop_video)
        self.open_button.clicked.connect(self.open_file)
        
        # Install event filter for mouse hover detection
        self.video_frame.installEventFilter(self)

        # Set window properties
        # self.setWindowTitle("Python Video Player")
        self.setGeometry(100, 100, 800, 600)
        self.show()
        
    
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space:
            if self.is_playing:
                self.pause_video()
            else:
                self.play_video()
        super().keyPressEvent(event)

    def open_file(self):
        # Open a file dialog to select video
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Video")

        if filename:
            # Set the media and attach it to VLC player
            self.media = self.vlc_instance.media_new(filename)
            self.media_player.set_media(self.media)
            self.media_player.set_xwindow(int(self.video_frame.winId()))
            self.media_player.play()  # Automatically start playing the video
            self.timer.start()

    def play_video(self):
        # Play the video
        self.media_player.play()
        self.timer.start()
        
    def pause_video(self):
        # Play the video
        self.media_player.pause()

    def stop_video(self):
        # Stop the video
        self.media_player.stop()
        self.progress_slider.setValue(0)
        self.timer.stop()
    
    def update_slider(self):
        # Update the slider position based on the current video position
        length = self.media_player.get_length()  # Get the total length of the video
        if length > 0:
            position = self.media_player.get_time()  # Get the current time of the video
            self.progress_slider.setValue(int(position * 1000 / length))  # Update slider position
    
    def set_position(self, position):
        # Set the new position in the video
        length = self.media_player.get_length()
        self.media_player.set_time(int(position * length / 1000))
        
    def eventFilter(self, obj, event):
        if obj == self.video_frame and event.type() == QtCore.QEvent.Enter:
            print("Mouse entered")
            self.control_widget.show()  # Show overlay when mouse enters the video frame
        elif obj == self.video_frame and event.type() == QtCore.QEvent.Leave:
            print("Mouse left")
            self.control_widget.hide()  # Hide overlay when mouse leaves the video frame
        return super().eventFilter(obj, event)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    player = VideoPlayer()
    sys.exit(app.exec_())
