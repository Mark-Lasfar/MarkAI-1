// mobile/lib/features/chat/chat_provider.dart
import 'package:flutter_riverpod/flutter_riverpod.dart';

class ChatMessage {
  final String text;
  final bool isUser;

  ChatMessage(this.text, this.isUser);
}

class ChatState {
  final List<ChatMessage> messages;

  ChatState(this.messages);
}

class ChatNotifier extends StateNotifier<ChatState> {
  ChatNotifier() : super(ChatState([]));

  Future<void> sendMessage(String text) async {
    state = ChatState([...state.messages, ChatMessage(text, true)]);
    
    final response = await ApiService.post('/ai/chat', data: {
      'messages': state.messages.map((m) => {
        'role': m.isUser ? 'user' : 'assistant',
        'content': m.text
      }).toList(),
    });

    state = ChatState([
      ...state.messages,
      ChatMessage(response.data['response'], false)
    ]);
  }
}

final chatProvider = StateNotifierProvider<ChatNotifier, ChatState>((ref) {
  return ChatNotifier();
});