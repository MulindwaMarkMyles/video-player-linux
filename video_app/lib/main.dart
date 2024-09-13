import 'package:flutter/material.dart';
import 'package:video_app/choose_movie.dart';
import 'package:media_kit/media_kit.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  MediaKit.ensureInitialized();
  runApp(
    const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: choose_movie(),
    ),
  );
}

