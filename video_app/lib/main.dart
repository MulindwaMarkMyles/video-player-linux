import 'dart:async';
import 'package:flutter/material.dart';
import 'package:ML/video_player_screen.dart';
import 'package:media_kit/media_kit.dart';
import 'package:bitsdojo_window/bitsdojo_window.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  MediaKit.ensureInitialized();

  runApp(
    MaterialApp(
      debugShowCheckedModeBanner: false,
      home: VideoApp(),
    ),
  );

  doWhenWindowReady(() {
    const initialSize = Size(1024, 576);
    appWindow.minSize = initialSize;
    appWindow.size = initialSize;
    appWindow.alignment = Alignment.center;
    appWindow.show();
  });
}

class VideoApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          WindowContainer(),
          Expanded(child: VideoPlayerScreen()),
        ],
      ),
    );
  }
}

class WindowContainer extends StatefulWidget {
  @override
  _WindowContainerState createState() => _WindowContainerState();
}

class _WindowContainerState extends State<WindowContainer> {
  bool _showButtons = false;
  Timer? _hideTimer; // Timer to hide buttons
  Timer? _showTimer; // Timer to hide buttons

  void _startHideTimer() {
    _hideTimer?.cancel(); // Cancel any previous timers
    _hideTimer = Timer(Duration(seconds: 2), () {
      // Set a 2-second delay
      setState(() {
        _showButtons = false; // Hide buttons after delay
      });
    });
  }

  void _showButtonsTemporarily() {
    _showTimer?.cancel(); // Cancel any previous timers
    setState(() {
      _showButtons = true; // Show buttons immediately
    });
    _showTimer = Timer(Duration(seconds: 2), () {
      // Set a 2-second delay
      setState(() {
        _showButtons = false; // Hide buttons after delay
      });
    });
  }

  @override
  void dispose() {
    _hideTimer?.cancel(); // Cancel the timer when disposing
    super.dispose();
  }

  @override
  void initState() {
    super.initState();
    _showButtonsTemporarily();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      color: Colors.black,
      child: MouseRegion(
        onEnter: (_) {
          setState(() {
            _showButtons = true; // Show buttons when mouse enters
          });
          _startHideTimer(); // Start the timer to hide buttons after a delay
        },
        onExit: (_) {
          _hideTimer?.cancel(); // Cancel the timer if mouse exits quickly
          setState(() {
            _showButtons = false; // Immediately hide buttons on exit
          });
        },
        child: WindowTitleBarBox(
          child: Row(
            children: [
              Expanded(child: MoveWindow()), // Makes the window draggable
              if (_showButtons) WindowButtons(), // Shows buttons on hover
            ],
          ),
        ),
      ),
    );
  }
}

class WindowButtons extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        MinimizeWindowButton(),
        MaximizeWindowButton(),
        CloseWindowButton(),
      ],
    );
  }
}

class MinimizeWindowButton extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return IconButton(
      icon: Icon(
        Icons.remove,
        color: Colors.white,
      ),
      onPressed: () {
        appWindow.minimize();
      },
    );
  }
}

class MaximizeWindowButton extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return IconButton(
      icon: Icon(
        Icons.crop_square,
        color: Colors.white,
      ),
      onPressed: () {
        appWindow.maximizeOrRestore();
      },
    );
  }
}

class CloseWindowButton extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return IconButton(
      icon: Icon(Icons.close, color: Colors.white),
      onPressed: () {
        appWindow.close();
      },
    );
  }
}
