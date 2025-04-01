// mobile/lib/core/api/api_client.dart
import 'package:dio/dio.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

class ApiClient {
  static final Dio _dio = Dio(BaseOptions(
    baseUrl: dotenv.env['API_BASE_URL']!,
    connectTimeout: const Duration(seconds: 30),
    receiveTimeout: const Duration(seconds: 30),
  ));

  static Future<Response> postMultimedia({
    required String endpoint,
    required String filePath,
    Map<String, dynamic>? data,
  }) async {
    FormData formData = FormData.fromMap({
      ...?data,
      'file': await MultipartFile.fromFile(filePath),
    });

    return _dio.post(endpoint, data: formData);
  }

  static Future<Response> streamResponse({
    required String endpoint,
    required Map<String, dynamic> data,
    Function(int, int)? onSendProgress,
    Function(int, int)? onReceiveProgress,
  }) {
    return _dio.post(
      endpoint,
      data: data,
      onSendProgress: onSendProgress,
      onReceiveProgress: onReceiveProgress,
      options: Options(
        responseType: ResponseType.stream,
      ),
    );
  }
}