// mobile/lib/features/collaborative/similar_users_view.dart
import 'package:flutter/material.dart';
import 'package:markai/models/similar_user.dart';

class SimilarUsersView extends StatelessWidget {
  final List<SimilarUser> users;

  const SimilarUsersView({super.key, required this.users});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'مستخدمون مشابهون لك',
          style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 10),
        SizedBox(
          height: 120,
          child: ListView.builder(
            scrollDirection: Axis.horizontal,
            itemCount: users.length,
            itemBuilder: (ctx, index) {
              final user = users[index];
              return Container(
                width: 100,
                margin: const EdgeInsets.only(right: 10),
                child: Column(
                  children: [
                    CircleAvatar(
                      child: Text(user.userId.substring(0, 2)),
                    ),
                    Text('تشابه ${(user.similarity * 100).toStringAsFixed(0)}%'),
                  ],
                ),
              );
            },
          ),
        ),
      ],
    );
  }
}