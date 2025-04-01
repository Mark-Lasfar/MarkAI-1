// test/widget_test.dart
void main() {
  testWidgets('Chat screen test', (WidgetTester tester) async {
    await tester.pumpWidget(
      ProviderScope(
        child: MaterialApp(
          home: ChatScreen(),
        ),
      ),
    );

    await tester.enterText(find.byType(TextField), 'مرحبا');
    await tester.tap(find.byIcon(Icons.send));
    await tester.pump();

    expect(find.text('مرحبا'), findsOneWidget);
  });
}