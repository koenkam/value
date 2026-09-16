import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';

/// Result of resolving the current Firebase user against the `users`
/// allowlist collection.
sealed class AuthState {
  const AuthState();
}

class SignedOut extends AuthState {
  const SignedOut();
}

class Authorised extends AuthState {
  const Authorised(this.user);

  final User user;
}

/// Signed in with Google, but the email has no document in `users`.
class NotAllowlisted extends AuthState {
  const NotAllowlisted(this.email);

  final String email;
}

/// Google-only authentication against a Firestore allowlist.
///
/// There is no self-service registration: an email only gains access once a
/// document with that email as its ID exists in the `users` collection.
class AuthService {
  AuthService({FirebaseAuth? auth, FirebaseFirestore? firestore})
      : _auth = auth ?? FirebaseAuth.instance,
        _firestore = firestore ?? FirebaseFirestore.instance;

  static const usersCollection = 'users';

  final FirebaseAuth _auth;
  final FirebaseFirestore _firestore;

  /// Emits whenever the signed-in user changes. The allowlist is re-checked on
  /// each change, so removing a user takes effect on their next sign-in or
  /// page reload.
  Stream<AuthState> get authState =>
      _auth.authStateChanges().asyncMap(_resolve);

  Future<AuthState> _resolve(User? user) async {
    final email = user?.email?.toLowerCase();
    if (user == null || email == null) return const SignedOut();

    final doc = await _firestore.collection(usersCollection).doc(email).get();
    if (!doc.exists) return NotAllowlisted(email);
    return Authorised(user);
  }

  /// Opens the Google sign-in popup. Returns silently if the user dismisses it.
  Future<void> signInWithGoogle() async {
    final provider = GoogleAuthProvider()
      ..setCustomParameters({'prompt': 'select_account'});
    try {
      await _auth.signInWithPopup(provider);
    } on FirebaseAuthException catch (e) {
      if (e.code == 'popup-closed-by-user' || e.code == 'cancelled-popup-request') {
        return;
      }
      rethrow;
    }
  }

  Future<void> signOut() => _auth.signOut();
}
