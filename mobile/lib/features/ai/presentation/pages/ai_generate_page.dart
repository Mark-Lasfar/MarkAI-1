import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';
import 'package:markai_mobile/features/ai/presentation/providers/ai_provider.dart';

class AIGeneratePage extends HookConsumerWidget {
  const AIGeneratePage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final promptController = useTextEditingController();
    final maxLength = useState(200);
    final selectedModel = useState('bloom');

    final aiState = ref.watch(aiProvider);
    final aiNotifier = ref.read(aiProvider.notifier);

    return Scaffold(
      appBar: AppBar(
        title: const Text('MarkAI Text Generation'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            DropdownButtonFormField<String>(
              value: selectedModel.value,
              items: const [
                DropdownMenuItem(value: 'bloom', child: Text('BLOOM (7B)')),
                DropdownMenuItem(value: 'falcon', child: Text('Falcon (7B)')),
                DropdownMenuItem(value: 'gpt-j', child: Text('GPT-J (6B)')),
              ],
              onChanged: (value) => selectedModel.value = value!,
              decoration: const InputDecoration(
                labelText: 'Model',
                border: OutlineInputBorder(),
                filled: true,
                fillColor: Colors.white,
              ),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: promptController,
              maxLines: 4,
              decoration: const InputDecoration(
                labelText: 'Prompt',
                border: OutlineInputBorder(),
                filled: true,
                fillColor: Colors.white,
              ),
            ),
            const SizedBox(height: 16),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    Text(
                      'Max Length: ${maxLength.value} tokens',
                      style: Theme.of(context).textTheme.titleSmall,
                    ),
                    Slider(
                      value: maxLength.value.toDouble(),
                      min: 50,
                      max: 1000,
                      divisions: 19,
                      label: maxLength.value.toString(),
                      onChanged: (value) => maxLength.value = value.toInt(),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),
            ElevatedButton(
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
              ),
              onPressed: () {
                if (promptController.text.trim().isEmpty) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Please enter a prompt')),
                  );
                  return;
                }
                
                aiNotifier.generateText(
                  selectedModel.value,
                  promptController.text,
                  maxLength.value,
                );
              },
              child: const Text(
                'Generate Text',
                style: TextStyle(fontSize: 16),
              ),
            ),
            const SizedBox(height: 24),
            if (aiState.isLoading)
              const Center(child: CircularProgressIndicator())
            else if (aiState.error.isNotEmpty)
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Theme.of(context).colorScheme.errorContainer,
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(
                  aiState.error,
                  style: TextStyle(
                    color: Theme.of(context).colorScheme.onErrorContainer,
                  ),
                ),
              )
            else if (aiState.generatedText.isNotEmpty)
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: SelectableText(
                    aiState.generatedText,
                    style: const TextStyle(fontSize: 16),
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}