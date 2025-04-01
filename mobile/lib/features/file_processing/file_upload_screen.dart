// mobile/lib/features/file_processing/file_upload_screen.dart
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:provider/provider.dart';

class FileUploadScreen extends StatelessWidget {
  Future<void> _uploadFile(BuildContext context) async {
    FilePickerResult? result = await FilePicker.platform.pickFiles();

    if (result != null) {
      final file = result.files.single;
      final response = await ApiService.postFile(
        endpoint: '/process-file',
        filePath: file.path!,
      );

      if (response.statusCode == 200) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('تم معالجة الملف بنجاح')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('رفع الملفات')),
      body: Center(
        child: ElevatedButton(
          onPressed: () => _uploadFile(context),
          child: Text('اختر ملف للمعالجة'),
        ),
      ),
    );
  }
}