import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QSlider, QFileDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl, Qt

class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Player")
        self.setGeometry(100, 100, 800, 600)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()

        openButton = QPushButton("Open")
        openButton.clicked.connect(self.open_file)

        playButton = QPushButton("Play")
        playButton.clicked.connect(self.play_video)

        volumeSlider = QSlider(Qt.Horizontal)
        volumeSlider.setRange(0, 100)
        volumeSlider.setValue(50)
        volumeSlider.valueChanged.connect(self.mediaPlayer.setVolume)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addWidget(openButton)
        layout.addWidget(playButton)
        layout.addWidget(volumeSlider)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.video_url = None

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "Video Files (*.mp4 *.avi *.mkv *.flv *.mov)")
        if file_name:
            self.video_url = QUrl.fromLocalFile(file_name)

    def play_video(self):
        if self.video_url:
            self.mediaPlayer.setMedia(QMediaContent(self.video_url))
            self.mediaPlayer.play()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())
