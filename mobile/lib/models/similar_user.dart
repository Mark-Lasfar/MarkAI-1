// mobile/lib/models/similar_user.dart
class SimilarUser {
  final String userId;
  final double similarity;
  final Map<String, dynamic> preferences;

  SimilarUser({
    required this.userId,
    required this.similarity,
    required this.preferences,
  });

  factory SimilarUser.fromJson(Map<String, dynamic> json) {
    return SimilarUser(
      userId: json['user_id'],
      similarity: (json['similarity'] as num).toDouble(),
      preferences: Map<String, dynamic>.from(json['preferences']),
    );
  }
}

// mobile/lib/models/improvement.dart
class Improvement {
  final String id;
  final Map<String, dynamic> data;
  final String sharedBy;
  final DateTime timestamp;

  Improvement({
    required this.id,
    required this.data,
    required this.sharedBy,
    required this.timestamp,
  });

  factory Improvement.fromJson(Map<String, dynamic> json) {
    return Improvement(
      id: json['id'],
      data: Map<String, dynamic>.from(json['data']),
      sharedBy: json['shared_by'],
      timestamp: DateTime.parse(json['timestamp']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'data': data,
      'shared_by': sharedBy,
      'timestamp': timestamp.toIso8601String(),
    };
  }
}