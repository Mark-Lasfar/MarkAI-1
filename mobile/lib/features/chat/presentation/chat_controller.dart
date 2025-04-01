// mobile/lib/features/chat/presentation/chat_controller.dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:markai/core/api/chat_api.dart';
import 'package:markai/core/models/chat_message.dart';

class ChatController extends StateNotifier<ChatState> {
  final Ref ref;
  
  ChatController(this.ref) : super(ChatState.initial());

  Future<void> sendMessage(String text) async {
    state = state.copyWith(
      messages: [...state.messages, ChatMessage.user(text)],
      isLoading: true
    );

    try {
      final response = await ChatApi.sendMessage(
        context: state.messages.map((m) => m.toApiFormat()).toList(),
        newMessage: text,
        model: state.selectedModel
      );

      state = state.copyWith(
        messages: [...state.messages, ChatMessage.ai(response)],
        isLoading: false
      );
    } catch (e) {
      state = state.copyWith(
        error: e.toString(),
        isLoading: false
      );
    }
  }
}