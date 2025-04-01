// mobile/lib/features/settings/help_screen.dart
import 'package:url_launcher/url_launcher.dart';

class HelpScreen extends StatelessWidget {
  Future<void> _launchEmail() async {
    final Uri params = Uri(
      scheme: 'mailto',
      path: 'support@markai.com',
      query: 'subject=دعم فني&body=وصف المشكلة هنا',
    );
    
    if (await canLaunchUrl(params)) {
      await launchUrl(params);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('المساعدة')),
      body: ListView(
        children: [
          ListTile(
            title: Text("اتصل بالدعم الفني"),
            onTap: _launchEmail,
          ),
          // عناصر أخرى...
        ],
      ),
    );
  }
}