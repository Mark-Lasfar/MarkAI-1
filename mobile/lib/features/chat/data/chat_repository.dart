// mobile/lib/features/chat/data/chat_repository.dart
import 'package:dio/dio.dart';
import 'package:markai/core/api/api_client.dart';
import 'package:markai/core/models/chat_message.dart';

class ChatRepository {
  final ApiClient _client;

  ChatRepository(this._client);

  Future<List<ChatMessage>> sendMessage({
    required String conversationId,
    required String message,
    List<ChatMessage> history = const [],
  }) async {
    try {
      final response = await _client.post(
        '/api/v1/chat',
        data: {
          'conversation_id': conversationId,
          'message': message,
          'history': history.map((m) => m.toJson()).toList(),
        },
      );

      return (response.data['messages'] as List)
          .map((json) => ChatMessage.fromJson(json))
          .toList();
    } on DioException catch (e) {
      throw Exception('Failed to send message: ${e.message}');
    }
  }
}