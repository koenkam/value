import 'package:flutter_test/flutter_test.dart';
import 'package:value/models/stock.dart';

void main() {
  Stock stock(Map<String, dynamic> fields) =>
      Stock(symbol: 'AAPL', fields: fields);

  group('Stock', () {
    test('exposes named fields from the document field map', () {
      final apple = stock({
        'name': 'Apple',
        'currency': 'USD',
        'indices': ['S&P 500', 'Nasdaq-100'],
        'market_cap': 3500000000000,
        'share_price': 234.56,
        'dividend': 1.05,
        'dividend_pct': 0.45,
        'eps': 7.5,
      });

      expect(apple.name, 'Apple');
      expect(apple.currency, 'USD');
      expect(apple.indices, ['S&P 500', 'Nasdaq-100']);
      expect(apple.marketCap, 3500000000000);
      expect(apple.sharePrice, 234.56);
      expect(apple.dividend, 1.05);
      expect(apple.eps, 7.5);
    });

    test('treats N/A as a missing number', () {
      final apple = stock({
        'eps': 'N/A',
        'share_price': 'N/A',
        'currency': 'N/A',
      });

      expect(apple.eps, isNull);
      expect(apple.sharePrice, isNull);
      expect(apple.currency, 'N/A');
    });

    test('matches on symbol, name, and index', () {
      final apple = stock({
        'name': 'Apple',
        'indices': ['S&P 500', 'Nasdaq-100'],
      });

      expect(apple.matches(''), isTrue);
      expect(apple.matches('aapl'), isTrue);
      expect(apple.matches('nasdaq'), isTrue);
      expect(apple.matches('microsoft'), isFalse);
    });
  });
}
