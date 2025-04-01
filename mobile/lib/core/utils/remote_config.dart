// mobile/lib/core/utils/remote_config.dart
import 'package:firebase_remote_config/firebase_remote_config.dart';

class RemoteConfigService {
  static final RemoteConfig _remoteConfig = RemoteConfig.instance;

  static Future<void> init() async {
    await _remoteConfig.setConfigSettings(RemoteConfigSettings(
      fetchTimeout: const Duration(minutes: 1),
      minimumFetchInterval: const Duration(hours: 1),
    ));
    await _remoteConfig.fetchAndActivate();
  }

  static String get aiModel => _remoteConfig.getString('ai_model');
}