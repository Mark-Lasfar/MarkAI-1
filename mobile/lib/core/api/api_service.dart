import 'package:dio/dio.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

class ApiService {
  static final Dio _dio = Dio(BaseOptions(
    baseUrl: dotenv.get('API_BASE_URL'),
    connectTimeout: const Duration(seconds: 30),
    receiveTimeout: const Duration(seconds: 30),
  ));

  static Future<Response> generateText({
    required String model,
    required String prompt,
    required int maxLength,
  }) async {
    return _dio.post('/ai/generate', data: {
      'model_name': model,
      'prompt': prompt,
      'max_length': maxLength,
    });
  }

  static Future<Response> getModels() async {
    return _dio.get('/ai/models');
  }
}