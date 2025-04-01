// mobile/lib/core/utils/app_updater.dart
import 'package:flutter_inapp_update/flutter_inapp_update.dart';

class AppUpdater {
  static Future<void> checkForUpdate() async {
    final update = await InAppUpdate.checkForUpdate();
    if (update.updateAvailability == UpdateAvailability.updateAvailable) {
      await InAppUpdate.performImmediateUpdate();
    }
  }
}