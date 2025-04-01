// mobile/lib/widgets/content_viewer.dart
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

class ContentViewer extends StatelessWidget {
  final dynamic content;

  const ContentViewer({Key? key, required this.content}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    if (content is String) {
      return Text(content);
    } else if (content is List<int>) {
      return Image.memory(Uint8List.fromList(content));
    } else if (content is String && content.startsWith('http')) {
      return InteractiveViewer(
        child: Image.network(content),
      );
    }
    return const Text('غير قادر على عرض هذا النوع من المحتوى');
  }
}