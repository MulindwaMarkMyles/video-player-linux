import 'package:flutter/material.dart';
import 'package:media_kit/media_kit.dart';
import 'package:media_kit_video/media_kit_video.dart';
import 'package:file_picker/file_picker.dart';

class VideoPlayerScreen extends StatefulWidget {
  @override
  State<VideoPlayerScreen> createState() => VideoPlayerScreenState();
  final String filePath;
  const VideoPlayerScreen({super.key, required this.filePath});
}

class VideoPlayerScreenState extends State<VideoPlayerScreen> {
  // Create a [Player] to control playback.
  late final player = Player();
  // Create a [VideoController] to handle video output from [Player].
  late final controller = VideoController(player);

  @override
  void initState() {
    super.initState();
    // Open file picker dialog to select a video file
    _pickAndPlayVideo();
  }

  Future<void> _pickAndPlayVideo() async {
    // Use FilePicker to pick a video file
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.video,
    );

    if (result != null && result.files.single.path != null) {
      String? filePath = result.files.single.path;
      if (filePath != null) {
        player.open(Media(filePath));
      }
    } else {
      // If no file is picked, display a message or handle the case appropriately
      print('No file selected.');
    }
  }

  @override
  void dispose() {
    player.dispose();
    // controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Video Player"),
      ),
      body: Center(
        child: SizedBox(
          width: MediaQuery.of(context).size.width,
          height: MediaQuery.of(context).size.width * 9.0 / 16.0,
          // Use [Video] widget to display video output.
          child: Video(controller: controller),
        ),
      ),
    );
  }
}
