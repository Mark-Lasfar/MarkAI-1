// mobile/lib/features/learning/context_aware_chat.dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:markai/core/api/learning_api.dart';

class ContextAwareChat extends ConsumerStatefulWidget {
  const ContextAwareChat({super.key});

  @override
  ConsumerState<ContextAwareChat> createState() => _ContextAwareChatState();
}

class _ContextAwareChatState extends ConsumerState<ContextAwareChat> {
  final TextEditingController _controller = TextEditingController();
  final List<Map<String, dynamic>> _messages = [];
  Map<String, dynamic> _context = {};

  Future<void> _sendMessage() async {
    final text = _controller.text.trim();
    if (text.isEmpty) return;

    // تسجيل التفاعل
    await LearningApi.logInteraction(
      'chat_message',
      {'message': text, 'context': _context},
    );

    setState(() {
      _messages.add({'text': text, 'isUser': true});
      _controller.clear();
    });

    // إرسال الرسالة مع السياق
    final response = await LearningApi.sendChatMessage(text, _context);

    setState(() {
      _messages.add({'text': response['message'], 'isUser': false});
      _context = {..._context, ...response['context']};
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('المحادثة السياقية')),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              itemCount: _messages.length,
              itemBuilder: (ctx, idx) {
                final msg = _messages[idx];
                return ListTile(
                  title: Text(msg['text']),
                  leading: Icon(msg['isUser'] ? Icons.person : Icons.android),
                );
              },
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    decoration: const InputDecoration(
                      hintText: 'اكتب رسالتك...',
                      border: OutlineInputBorder(),
                    ),
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