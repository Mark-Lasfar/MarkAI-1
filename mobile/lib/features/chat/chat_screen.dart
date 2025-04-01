import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:markai/core/api/chat_api.dart';
import 'package:markai/core/models/chat_message.dart';
import 'package:markai/core/providers/chat_provider.dart';
import 'package:markai/core/utils/analytics.dart';

class ChatScreen extends ConsumerStatefulWidget {
  const ChatScreen({super.key});

  @override
  ConsumerState<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends ConsumerState<ChatScreen> {
  final TextEditingController _controller = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  String _selectedModel = 'bloom';

  @override
  void initState() {
    super.initState();
    // تسجيل تحليل لصفحة المحادثة
    AnalyticsService.trackScreenView('Chat Screen');
  }

  @override
  void dispose() {
    _controller.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  Future<void> _sendMessage() async {
    if (_controller.text.trim().isEmpty) return;

    final message = _controller.text;
    _controller.clear();

    // إضافة رسالة المستخدم
    ref.read(chatProvider.notifier).addMessage(
          ChatMessage(
            text: message,
            isUser: true,
            timestamp: DateTime.now(),
          ),
        );

    // تسجيل تفاعل المستخدم
    await AnalyticsService.logEvent(
      'message_sent',
      {
        'text': message,
        'model': _selectedModel,
        'length': message.length,
      },
    );

    // إظهار مؤشر تحميل
    ref.read(chatProvider.notifier).setLoading(true);
    _scrollToBottom();

    try {
      final response = await ChatApi.sendMessage(
        messages: ref.read(chatProvider).messages
            .map((m) => {
                  'role': m.isUser ? 'user' : 'assistant',
                  'content': m.text,
                })
            .toList(),
        model: _selectedModel,
      );

      // إضافة رد الذكاء الاصطناعي
      ref.read(chatProvider.notifier).addMessage(
            ChatMessage(
              text: response,
              isUser: false,
              timestamp: DateTime.now(),
            ),
          );

      // تسجيل استجابة الذكاء الاصطناعي
      await AnalyticsService.logEvent(
        'ai_response',
        {
          'input_length': message.length,
          'output_length': response.length,
          'model': _selectedModel,
        },
      );
    } catch (e) {
      // إضافة رسالة خطأ
      ref.read(chatProvider.notifier).addMessage(
            ChatMessage(
              text: 'حدث خطأ أثناء المعالجة. يرجى المحاولة لاحقاً.',
              isUser: false,
              timestamp: DateTime.now(),
            ),
          );
    } finally {
      ref.read(chatProvider.notifier).setLoading(false);
      _scrollToBottom();
    }
  }

  @override
  Widget build(BuildContext context) {
    final chatState = ref.watch(chatProvider);
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('المحادثة الذكية'),
        actions: [
          DropdownButton<String>(
            value: _selectedModel,
            icon: const Icon(Icons.arrow_drop_down),
            underline: Container(),
            items: const [
              DropdownMenuItem(
                value: 'bloom',
                child: Text('BLOOM (العربية)'),
              ),
              DropdownMenuItem(
                value: 'falcon',
                child: Text('Falcon (الإنجليزية)'),
              ),
              DropdownMenuItem(
                value: 'gpt-j',
                child: Text('GPT-J (متعدد)'),
              ),
            ],
            onChanged: (value) {
              if (value != null) {
                setState(() => _selectedModel = value);
              }
            },
          ),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              controller: _scrollController,
              padding: const EdgeInsets.all(8),
              itemCount: chatState.messages.length,
              itemBuilder: (context, index) {
                final message = chatState.messages[index];
                return ChatBubble(
                  message: message,
                  isDark: theme.brightness == Brightness.dark,
                );
              },
            ),
          ),
          if (chatState.isLoading)
            const Padding(
              padding: EdgeInsets.all(8.0),
              child: CircularProgressIndicator(),
            ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    decoration: InputDecoration(
                      hintText: 'اكتب رسالتك...',
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(20),
                      ),
                      contentPadding: const EdgeInsets.symmetric(
                        horizontal: 16,
                        vertical: 12,
                      ),
                    ),
                    onSubmitted: (_) => _sendMessage(),
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.send),
                  onPressed: _sendMessage,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class ChatBubble extends StatelessWidget {
  final ChatMessage message;
  final bool isDark;

  const ChatBubble({
    super.key,
    required this.message,
    required this.isDark,
  });

  @override
  Widget build(BuildContext context) {
    return Align(
      alignment: message.isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 4),
        padding: const EdgeInsets.symmetric(
          horizontal: 16,
          vertical: 10,
        ),
        decoration: BoxDecoration(
          color: message.isUser
              ? Theme.of(context).primaryColor
              : isDark
                  ? Colors.grey[800]
                  : Colors.grey[200],
          borderRadius: BorderRadius.circular(16),
        ),
        child: Text(
          message.text,
          style: TextStyle(
            color: message.isUser ? Colors.white : null,
          ),
        ),
      ),
    );
  }
}