// mobile/lib/features/learning/user_learning.dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:markai/core/api/learning_api.dart';

class UserLearningNotifier extends StateNotifier<AsyncValue<List<String>>> {
  UserLearningNotifier(this.ref) : super(const AsyncValue.loading()) {
    loadRecommendations();
  }

  final Ref ref;

  Future<void> loadRecommendations() async {
    state = const AsyncValue.loading();
    try {
      final recs = await LearningApi.getRecommendations();
      state = AsyncValue.data(recs);
    } catch (e) {
      state = AsyncValue.error(e, StackTrace.current);
    }
  }

  Future<void> logInteraction(
    String interactionType,
    Map<String, dynamic> metadata,
  ) async {
    await LearningApi.logInteraction(interactionType, metadata);
    await loadRecommendations(); // تحديث التوصيات بعد التسجيل
  }
}

final userLearningProvider = StateNotifierProvider<
  UserLearningNotifier,
  AsyncValue<List<String>>
>((ref) {
  return UserLearningNotifier(ref);
});