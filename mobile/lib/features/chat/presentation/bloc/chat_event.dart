// lib/features/chat/presentation/bloc/chat_event.dart
abstract class ChatEvent {}

class SendMessageEvent extends ChatEvent {
  final String content;
  SendMessageEvent({required this.content});
}

class SendFilesEvent extends ChatEvent {
  final String sessionId;
  final List<PlatformFile> files;
  SendFilesEvent({required this.sessionId, required this.files});
}