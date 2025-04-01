// mobile/lib/features/admin/presentation/admin_panel.dart
class AdminPanel extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Consumer(
        builder: (context, ref, _) {
          final analytics = ref.watch(analyticsProvider);
          return AnalyticsDashboard(analytics);
        },
      ),
    );
  }
}