// mobile/lib/core/utils/analytics.dart
import 'package:firebase_analytics/firebase_analytics.dart';

class AnalyticsService {
  static final FirebaseAnalytics _analytics = FirebaseAnalytics.instance;

  static Future<void> logEvent(String name, Map<String, dynamic>? params) async {
    await _analytics.logEvent(
      name: name,
      parameters: params,
    );
  }

  static Future<void> trackScreen(String screenName) async {
    await _analytics.logScreenView(screenName: screenName);
  }
}