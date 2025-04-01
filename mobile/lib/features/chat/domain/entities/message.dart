// lib/features/chat/domain/entities/message.dart
class Message {
  final String id;
  final String content;
  final bool isUser;
  final DateTime timestamp;
  final PlatformFile? file;

  Message({
    required this.id,
    required this.content,
    required this.isUser,
    required this.timestamp,
    this.file,
  });

  factory Message.fromJson(Map<String, dynamic> json) {
    return Message(
      id: json['id'],
      content: json['content'],
      isUser: json['isUser'],
      timestamp: DateTime.parse(json['timestamp']),
    );
  }
}