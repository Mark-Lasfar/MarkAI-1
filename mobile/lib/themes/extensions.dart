// mobile/lib/themes/extensions.dart
import 'package:flutter/material.dart';

class AppColors extends ThemeExtension<AppColors> {
  final Color primary;
  final Color secondary;
  final Color success;
  final Color danger;

  const AppColors({
    required this.primary,
    required this.secondary,
    required this.success,
    required this.danger,
  });

  @override
  ThemeExtension<AppColors> copyWith({
    Color? primary,
    Color? secondary,
    Color? success,
    Color? danger,
  }) {
    return AppColors(
      primary: primary ?? this.primary,
      secondary: secondary ?? this.secondary,
      success: success ?? this.success,
      danger: danger ?? this.danger,
    );
  }

  @override
  ThemeExtension<AppColors> lerp(ThemeExtension<AppColors>? other, double t) {
    if (other is! AppColors) return this;
    
    return AppColors(
      primary: Color.lerp(primary, other.primary, t)!,
      secondary: Color.lerp(secondary, other.secondary, t)!,
      success: Color.lerp(success, other.success, t)!,
      danger: Color.lerp(danger, other.danger, t)!,
    );
  }
}

// تطبيق التصميم في الموبايل
final appTheme = ThemeData(
  extensions: <ThemeExtension<dynamic>>[
    AppColors(
      primary: const Color(0xFF4361EE),
      secondary: const Color(0xFF3F37C9),
      success: const Color(0xFF4CC9F0),
      danger: const Color(0xFFF72585),
    ),
  ],
);