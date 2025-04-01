// lib/app.dart - Root Application
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:markai/config/routes.dart';
import 'package:markai/core/ai/multimodal_provider.dart';
import 'package:markai/features/auth/presentation/auth_controller.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const ProviderScope(child: MarkAIApp()));
}

class MarkAIApp extends ConsumerWidget {
  const MarkAIApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final authState = ref.watch(authControllerProvider);
    
    return MaterialApp.router(
      routerConfig: goRouter,
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      debugShowCheckedModeBanner: false,
      builder: (context, child) {
        // Initialize AI models when app starts
        ref.read(multimodalAIServiceProvider).initialize();
        return child!;
      },
    );
  }
}