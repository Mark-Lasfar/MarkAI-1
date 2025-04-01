// mobile/lib/features/file_processing/archive_utils.dart
import 'package:archive/archive.dart';
import 'dart:io';

Future<List<File>> extractZip(String zipPath, String outputDir) async {
  final bytes = await File(zipPath).readAsBytes();
  final archive = ZipDecoder().decodeBytes(bytes);
  
  final files = <File>[];
  for (final file in archive) {
    if (file.isFile) {
      final outPath = '$outputDir/${file.name}';
      await File(outPath).create(recursive: true);
      await File(outPath).writeAsBytes(file.content);
      files.add(File(outPath));
    }
  }
  
  return files;
}