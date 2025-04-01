// mobile/lib/core/utils/encryption.dart
import 'package:encrypt/encrypt.dart';

class EncryptionService {
  static final _key = Key.fromUtf8('32-char-long-encryption-key!');
  static final _iv = IV.fromLength(16);
  static final _encrypter = Encrypter(AES(_key));

  static String encrypt(String text) {
    return _encrypter.encrypt(text, iv: _iv).base64;
  }

  static String decrypt(String encrypted) {
    return _encrypter.decrypt64(encrypted, iv: _iv);
  }
}