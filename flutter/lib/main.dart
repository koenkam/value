import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';

import 'firebase_options.dart';
import 'screens/login_screen.dart';
import 'screens/stock_table_screen.dart';
import 'services/auth_service.dart';
import 'services/stock_repository.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  runApp(const ValueApp());
}

class ValueApp extends StatefulWidget {
  const ValueApp({super.key});

  @override
  State<ValueApp> createState() => _ValueAppState();
}

class _ValueAppState extends State<ValueApp> {
  final _authService = AuthService();
  final _repository = StockRepository();

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'value',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.indigo),
        useMaterial3: true,
      ),
      home: StreamBuilder<AuthState>(
        stream: _authService.authState,
        builder: (context, snapshot) {
          if (!snapshot.hasData) {
            return const Scaffold(
              body: Center(child: CircularProgressIndicator()),
            );
          }

          return switch (snapshot.data!) {
            SignedOut() => LoginScreen(authService: _authService),
            NotAllowlisted(:final email) =>
              LoginScreen(authService: _authService, deniedEmail: email),
            Authorised(:final user) => StockTableScreen(
                authService: _authService,
                repository: _repository,
                email: user.email ?? '',
              ),
          };
        },
      ),
    );
  }
}
