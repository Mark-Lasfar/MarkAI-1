// mobile/lib/core/utils/offline_manager.dart
import 'package:hive/hive.dart';

class OfflineManager {
  static final Box _box = Hive.box('offlineData');

  static Future<void> saveRequest(String endpoint, dynamic data) async {
    await _box.add({
      'endpoint': endpoint,
      'data': data,
      'timestamp': DateTime.now(),
    });
  }

  static Future<void> syncAll() async {
    final requests = _box.values.toList();
    for (var req in requests) {
      try {
        await ApiService.post(req['endpoint'], data: req['data']);
        await req.delete();
      } catch (e) {
        print('Failed to sync: ${e.toString()}');
      }
    }
  }
}