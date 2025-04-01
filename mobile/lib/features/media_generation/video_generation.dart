// mobile/lib/features/media_generation/video_generation.dart
Future<void> generateVideoFromText(String text) async {
  final response = await ApiService.post('/media/generate-video', data: {
    'text': text,
    'model': 'bloom'
  });

  if (response.statusCode == 200) {
    final videoUrl = response.data['video_url'];
    // عرض الفيديو أو تحميله
  }
}