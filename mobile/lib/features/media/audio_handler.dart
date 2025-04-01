// mobile/lib/features/media/audio_handler.dart
import 'package:just_audio/just_audio.dart';

class AudioService {
  final AudioPlayer _player = AudioPlayer();

  Future<void> playGeneratedAudio(String url) async {
    await _player.setUrl(url);
    _player.play();
  }

  Future<void> stopAudio() async {
    await _player.stop();
  }
}