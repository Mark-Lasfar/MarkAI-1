// mobile/lib/core/utils/background_sync.dart
import 'package:workmanager/workmanager.dart';

void callbackDispatcher() {
  Workmanager().executeTask((task, inputData) async {
    await ApiService.syncPendingTasks();
    return true;
  });
}

void initBackgroundSync() {
  Workmanager().initialize(
    callbackDispatcher,
    isInDebugMode: false,
  );
  Workmanager().registerPeriodicTask(
    'sync-task',
    'backgroundSync',
    frequency: Duration(hours: 1),
  );
}