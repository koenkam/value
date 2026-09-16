// Firebase configuration for the `value` project (value-619ef).
//
// Only the web platform is configured; this app is web-only by design.
import 'package:firebase_core/firebase_core.dart' show FirebaseOptions;
import 'package:flutter/foundation.dart'
    show TargetPlatform, defaultTargetPlatform, kIsWeb;

class DefaultFirebaseOptions {
  static FirebaseOptions get currentPlatform {
    if (kIsWeb) {
      return web;
    }
    throw UnsupportedError(
      'value is a web-only app; no Firebase options exist for '
      '$defaultTargetPlatform (${TargetPlatform.values}).',
    );
  }

  static const FirebaseOptions web = FirebaseOptions(
    apiKey: 'AIzaSyD-mmx0EQ7II_1csfk6YCDLl041XANr-TM',
    appId: '1:201509019673:web:f03b0cebd5b8e01e258a88',
    messagingSenderId: '201509019673',
    projectId: 'value-619ef',
    authDomain: 'value-619ef.firebaseapp.com',
    storageBucket: 'value-619ef.firebasestorage.app',
  );
}
