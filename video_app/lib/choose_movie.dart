import 'package:flutter/material.dart';
import 'video_player_screen.dart';

class DragAndDropScreen extends StatefulWidget {
  const DragAndDropScreen({super.key});

  @override
  State<DragAndDropScreen> createState() => _DragAndDropScreenState();
}

class _DragAndDropScreenState extends State<DragAndDropScreen> {
  late DropzoneViewController _controller;
  String _filePath = '';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Drag and Drop File'),
      ),
      body: Stack(
        children: [
          // Dropzone for drag and drop
          DropzoneView(
            onCreated: (controller) => _controller = controller,
            onDrop: (file) async {
              String path = await _controller.createFileUrl(file);
              setState(() {
                _filePath = path;
              });
              _navigateToVideoPlayerScreen(path);
            },
          ),
          Center(
            child: Text(
              _filePath.isEmpty
                  ? 'Drop a video file here'
                  : 'File selected: $_filePath',
              style: const TextStyle(fontSize: 18),
            ),
          ),
        ],
      ),
    );
  }

  void _navigateToVideoPlayerScreen(String filePath) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => VideoPlayerScreen(filePath: filePath),
      ),
    );
  }
}

