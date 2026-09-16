import 'package:flutter_test/flutter_test.dart';
import 'package:value/models/numeric_filter.dart';
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

  group('NumericFilter', () {
    test('greater than and less than compare the named field', () {
      final apple = stock({'eps': 8.68, 'market_cap': 4.8e12});

      expect(
        const NumericFilter(
          field: 'eps',
          op: CompareOp.greaterThan,
          value: 5,
        ).matches(apple),
        isTrue,
      );
      expect(
        const NumericFilter(
          field: 'eps',
          op: CompareOp.lessThan,
          value: 5,
        ).matches(apple),
        isFalse,
      );
      expect(
        const NumericFilter(
          field: 'market_cap',
          op: CompareOp.greaterThan,
          value: 1e12,
        ).matches(apple),
        isTrue,
      );
    });

    test('N/A and missing values never match', () {
      final empty = stock({'eps': 'N/A'});
      expect(
        const NumericFilter(
          field: 'eps',
          op: CompareOp.greaterThan,
          value: 0,
        ).matches(empty),
        isFalse,
      );
      expect(
        const NumericFilter(
          field: 'share_price',
          op: CompareOp.lessThan,
          value: 1000,
        ).matches(empty),
        isFalse,
      );
    });
  });

  group('parseFilterValue', () {
    test('parses suffixes and plain numbers', () {
      expect(parseFilterValue('5'), 5);
      expect(parseFilterValue('1.5b'), 1.5e9);
      expect(parseFilterValue('100T'), 1e14);
      expect(parseFilterValue('1e12'), 1e12);
      expect(parseFilterValue('nope'), isNull);
    });
  });
}
