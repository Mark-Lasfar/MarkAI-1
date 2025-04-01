// lib/main.dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:markai/core/utils/app_theme.dart';
import 'package:markai/features/auth/presentation/auth_controller.dart';
import 'package:markai/features/auth/presentation/login_screen.dart';
import 'package:markai/features/workspace/presentation/workspace_screen.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize app dependencies (Firebase, Hive, etc.)
  await initializeDependencies();
  
  runApp(const ProviderScope(child: MarkAIApp()));
}

class MarkAIApp extends ConsumerWidget {
  const MarkAIApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return MaterialApp(
      title: 'MarkAI',
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: ThemeMode.system, // Follow system theme
      debugShowCheckedModeBanner: false,
      home: const AuthWrapper(),
    );
  }
}

class AuthWrapper extends ConsumerWidget {
  const AuthWrapper({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final authState = ref.watch(authControllerProvider);
    
    return authState.when(
      loading: () => const Scaffold(
        body: Center(
          child: CircularProgressIndicator(),
        ),
      ),
      authenticated: (user) => const WorkspaceScreen(),
      unauthenticated: () => const LoginScreen(),
      error: (error, stack) => Scaffold(
        body: Center(
          child: Text('Authentication Error: $error'),
        ),
      ),
    );
  }
}

Future<void> initializeDependencies() async {
  // Initialize all app dependencies here
  // await Firebase.initializeApp();
  // await Hive.initFlutter();
  // etc...
}