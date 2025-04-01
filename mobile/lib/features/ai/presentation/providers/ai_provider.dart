import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:markai_mobile/features/ai/domain/usecases/generate_text.dart';

class AIState {
  final bool isLoading;
  final String generatedText;
  final String error;

  AIState({
    this.isLoading = false,
    this.generatedText = '',
    this.error = '',
  });

  AIState copyWith({
    bool? isLoading,
    String? generatedText,
    String? error,
  }) {
    return AIState(
      isLoading: isLoading ?? this.isLoading,
      generatedText: generatedText ?? this.generatedText,
      error: error ?? this.error,
    );
  }
}

class AINotifier extends StateNotifier<AIState> {
  final GenerateTextUseCase generateTextUseCase;

  AINotifier(this.generateTextUseCase) : super(AIState());

  Future<void> generateText(String model, String prompt, int maxLength) async {
    state = state.copyWith(isLoading: true, error: '');
    try {
      final result = await generateTextUseCase.execute(model, prompt, maxLength);
      state = state.copyWith(
        isLoading: false,
        generatedText: result,
      );
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: e.toString(),
      );
    }
  }
}

final aiProvider = StateNotifierProvider<AINotifier, AIState>((ref) {
  return AINotifier(ref.read(generateTextUseCaseProvider));
});