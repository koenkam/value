import 'package:flutter/material.dart';

import '../services/auth_service.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key, required this.authService, this.deniedEmail});

  final AuthService authService;

  /// Set when the user signed in successfully but is not on the allowlist.
  final String? deniedEmail;

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  bool _busy = false;
  String? _error;

  Future<void> _signIn() async {
    setState(() {
      _busy = true;
      _error = null;
    });
    try {
      await widget.authService.signInWithGoogle();
    } catch (e) {
      if (mounted) setState(() => _error = '$e');
    } finally {
      if (mounted) setState(() => _busy = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final denied = widget.deniedEmail;

    return Scaffold(
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 360),
          child: Card(
            margin: const EdgeInsets.all(24),
            child: Padding(
              padding: const EdgeInsets.all(32),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Text('value', style: theme.textTheme.headlineMedium),
                  const SizedBox(height: 8),
                  Text(
                    'Large-cap stock universe',
                    style: theme.textTheme.bodyMedium
                        ?.copyWith(color: theme.colorScheme.outline),
                  ),
                  const SizedBox(height: 32),
                  if (denied != null) ...[
                    _Notice(
                      icon: Icons.block,
                      colour: theme.colorScheme.error,
                      message:
                          '$denied is not authorised. Ask the administrator to '
                          'add you to the users collection.',
                    ),
                    const SizedBox(height: 16),
                    OutlinedButton(
                      onPressed: widget.authService.signOut,
                      child: const Text('Sign out'),
                    ),
                  ] else ...[
                    FilledButton.icon(
                      onPressed: _busy ? null : _signIn,
                      icon: _busy
                          ? const SizedBox.square(
                              dimension: 16,
                              child: CircularProgressIndicator(strokeWidth: 2),
                            )
                          : const Icon(Icons.login),
                      label: const Text('Sign in with Google'),
                    ),
                  ],
                  if (_error != null) ...[
                    const SizedBox(height: 16),
                    _Notice(
                      icon: Icons.error_outline,
                      colour: theme.colorScheme.error,
                      message: _error!,
                    ),
                  ],
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class _Notice extends StatelessWidget {
  const _Notice({
    required this.icon,
    required this.colour,
    required this.message,
  });

  final IconData icon;
  final Color colour;
  final String message;

  @override
  Widget build(BuildContext context) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Icon(icon, size: 18, color: colour),
        const SizedBox(width: 8),
        Expanded(
          child: Text(
            message,
            style: Theme.of(context)
                .textTheme
                .bodySmall
                ?.copyWith(color: colour),
          ),
        ),
      ],
    );
  }
}
