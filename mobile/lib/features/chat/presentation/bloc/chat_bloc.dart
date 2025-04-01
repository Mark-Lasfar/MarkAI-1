// lib/features/chat/presentation/bloc/chat_bloc.dart
class ChatBloc extends Bloc<ChatEvent, ChatState> {
  final ChatRepository repository;

  ChatBloc({required this.repository}) : super(ChatInitial()) {
    on<SendMessageEvent>(_onSendMessage);
    on<SendFilesEvent>(_onSendFiles);
  }

  Future<void> _onSendMessage(
    SendMessageEvent event,
    Emitter<ChatState> emit,
  ) async {
    emit(ChatLoading());
    try {
      final response = await repository.sendMessage(event.content);
      emit(ChatLoaded(messages: response));
    } catch (e) {
      emit(ChatError(message: e.toString()));
    }
  }

  Future<void> _onSendFiles(
    SendFilesEvent event,
    Emitter<ChatState> emit,
  ) async {
    emit(ChatLoading());
    try {
      final response = await repository.sendFiles(event.files);
      emit(ChatLoaded(messages: response));
    } catch (e) {
      emit(ChatError(message: e.toString()));
    }
  }
}