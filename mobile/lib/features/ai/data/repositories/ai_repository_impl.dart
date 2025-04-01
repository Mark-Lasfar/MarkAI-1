// mobile/lib/features/ai/data/repositories/ai_repository_impl.dart
import 'package:markai/core/api/ai_api.dart';

class AIRepository {
  final AIApi _api;

  Future<String> generateText(String prompt, String model) async {
    return await _api.generateText(prompt, model);
  }

  Future<String> generateCode(String requirements) async {
    return await _api.generateCode(requirements);
  }
}