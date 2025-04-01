// mobile/lib/features/workspace/ai_workspace.dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:markai/features/chat/chat_screen.dart';
import 'package:markai/features/code/code_screen.dart';
import 'package:markai/features/media/media_screen.dart';
import 'package:markai/features/files/file_screen.dart';

class AIWorkspace extends ConsumerStatefulWidget {
  const AIWorkspace({super.key});

  @override
  ConsumerState<AIWorkspace> createState() => _AIWorkspaceState();
}

class _AIWorkspaceState extends ConsumerState<AIWorkspace> {
  int _currentIndex = 0;
  final PageController _pageController = PageController();

  final List<Widget> _screens = [
    const ChatScreen(),
    const CodeScreen(),
    const MediaScreen(),
    const FileScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    
    return Scaffold(
      appBar: AppBar(
        title: const Text('MarkAI Workspace'),
        centerTitle: true,
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.account_circle),
            onPressed: () {},
          ),
        ],
      ),
      body: PageView(
        controller: _pageController,
        physics: const NeverScrollableScrollPhysics(),
        children: _screens,
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _currentIndex,
        onDestinationSelected: (index) {
          setState(() => _currentIndex = index);
          _pageController.jumpToPage(index);
        },
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.chat),
            label: 'محادثة',
          ),
          NavigationDestination(
            icon: Icon(Icons.code),
            label: 'أكواد',
          ),
          NavigationDestination(
            icon: Icon(Icons.video_library),
            label: 'وسائط',
          ),
          NavigationDestination(
            icon: Icon(Icons.folder),
            label: 'ملفات',
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {},
        child: const Icon(Icons.add),
      ),
    );
  }
}