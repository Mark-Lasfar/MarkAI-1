import 'package:markai_mobile/core/api/api_service.dart';

class GenerateTextUseCase {
  Future<String> execute(String model, String prompt, int maxLength) async {
    try {
      final response = await ApiService.generateText(
        model: model,
        prompt: prompt,
        maxLength: maxLength,
      );
      return response.data['result'];
    } catch (e) {
      throw Exception('Failed to generate text: ${e.toString()}');
    }
  }
}

final generateTextUseCaseProvider = Provider((ref) => GenerateTextUseCase());