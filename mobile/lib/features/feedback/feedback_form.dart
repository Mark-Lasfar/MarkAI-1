// mobile/lib/features/feedback/feedback_form.dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class FeedbackForm extends ConsumerWidget {
  final String interactionId;
  final Function() onSubmitted;
  
  const FeedbackForm({
    required this.interactionId,
    required this.onSubmitted,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final feedbackController = TextEditingController();
    int? selectedRating;

    return AlertDialog(
      title: const Text('كيف كانت تجربتك؟'),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          TextField(
            controller: feedbackController,
            decoration: const InputDecoration(
              hintText: 'شاركنا ملاحظاتك...',
              border: OutlineInputBorder(),
            ),
            maxLines: 3,
          ),
          const SizedBox(height: 16),
          const Text('تقييم التجربة:'),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [1, 2, 3, 4, 5].map((rating) {
              return IconButton(
                icon: Icon(
                  selectedRating != null && rating <= selectedRating!
                      ? Icons.star
                      : Icons.star_border,
                  color: Colors.amber,
                ),
                onPressed: () {
                  selectedRating = rating;
                },
              );
            }).toList(),
          ),
        ],
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context),
          child: const Text('إلغاء'),
        ),
        ElevatedButton(
          onPressed: () async {
            if (selectedRating != null) {
              await ref.read(feedbackProvider).submitFeedback(
                interactionId: interactionId,
                rating: selectedRating!,
                comments: feedbackController.text,
              );
              onSubmitted();
              Navigator.pop(context);
            }
          },
          child: const Text('إرسال'),
        ),
      ],
    );
  }
}