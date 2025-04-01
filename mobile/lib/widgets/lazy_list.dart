// mobile/lib/widgets/lazy_list.dart
import 'package:flutter/material.dart';

class LazyListView extends StatelessWidget {
  final Future<List<dynamic>> Function(int) loader;
  final Widget Function(dynamic) builder;

  const LazyListView({
    required this.loader,
    required this.builder,
  });

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemBuilder: (ctx, index) {
        return FutureBuilder(
          future: loader(index),
          builder: (ctx, snapshot) {
            if (snapshot.hasData) {
              return builder(snapshot.data!);
            }
            return const CircularProgressIndicator();
          },
        );
      },
    );
  }
}