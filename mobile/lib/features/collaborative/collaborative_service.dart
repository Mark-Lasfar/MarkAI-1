// mobile/lib/features/collaborative/collaborative_service.dart
import 'package:markai/core/api/api_service.dart';
import 'package:markai/models/improvement.dart';
import 'package:markai/models/similar_user.dart';

class CollaborativeService {
  static Future<List<SimilarUser>> getSimilarUsers(String userId) async {
    final response = await ApiService.get(
      '/collaborative/similar-users',
      params: {'count': 5},
    );
    return (response.data as List)
        .map((e) => SimilarUser.fromJson(e))
        .toList();
  }

  static Future<void> shareImprovement(
    String userId,
    Improvement improvement,
  ) async {
    await ApiService.post(
      '/collaborative/share-improvement',
      data: improvement.toJson(),
    );
  }

  static Future<List<Improvement>> getSharedImprovements(String userId) async {
    final response = await ApiService.get('/collaborative/shared-improvements');
    return (response.data as List)
        .map((e) => Improvement.fromJson(e))
        .toList();
  }
}