import 'stock.dart';

enum CompareOp {
  greaterThan,
  lessThan;

  String get symbol => this == CompareOp.greaterThan ? '>' : '<';
}

/// A greater-than / less-than constraint on one numeric document field.
class NumericFilter {
  const NumericFilter({
    required this.field,
    required this.op,
    required this.value,
  });

  final String field;
  final CompareOp op;
  final double value;

  bool matches(Stock stock) {
    final actual = stock.numericValue(field);
    if (actual == null) return false;
    return switch (op) {
      CompareOp.greaterThan => actual > value,
      CompareOp.lessThan => actual < value,
    };
  }

  String get label {
    var name = field;
    for (final item in filterableFields) {
      if (item.key == field) {
        name = item.label;
        break;
      }
    }
    return '$name ${op.symbol} ${_formatValue(value)}';
  }
}

class FilterableField {
  const FilterableField(this.key, this.label);

  final String key;
  final String label;
}

/// Fields the dropdown offers. Extra numeric keys found on loaded documents
/// are appended so newly retrieved parameters show up without a code change.
const filterableFields = [
  FilterableField('share_price', 'Price'),
  FilterableField('market_cap', 'Market cap'),
  FilterableField('dividend', 'Dividend'),
  FilterableField('dividend_pct', 'Div %'),
  FilterableField('eps', 'EPS'),
  FilterableField('revenue_per_share', 'Rev / sh'),
  FilterableField('week_52_high', '52w high'),
  FilterableField('week_52_low', '52w low'),
];

const _skipKeys = {
  'name',
  'currency',
  'indices',
  'updated_at',
  'symbol',
};

List<FilterableField> filterableFieldsFor(Iterable<Stock> stocks) {
  final known = {for (final field in filterableFields) field.key};
  final extras = <String>{};
  for (final stock in stocks) {
    for (final key in stock.fields.keys) {
      if (known.contains(key) || _skipKeys.contains(key)) continue;
      if (stock.numericValue(key) != null) extras.add(key);
    }
  }
  final extraKeys = extras.toList()..sort();
  return [
    ...filterableFields,
    for (final key in extraKeys) FilterableField(key, key.replaceAll('_', ' ')),
  ];
}

/// Parses a threshold. Accepts plain numbers, scientific notation, and
/// suffixes k/m/b/t (1.5b = 1_500_000_000).
double? parseFilterValue(String raw) {
  final text = raw.trim().toLowerCase().replaceAll(',', '');
  if (text.isEmpty) return null;
  const suffixes = {'k': 1e3, 'm': 1e6, 'b': 1e9, 't': 1e12};
  final last = text[text.length - 1];
  final factor = suffixes[last];
  final number = factor == null ? text : text.substring(0, text.length - 1);
  final parsed = double.tryParse(number.trim());
  if (parsed == null) return null;
  return parsed * (factor ?? 1);
}

String _formatValue(double value) {
  if (value.abs() >= 1e12) return '${_trim(value / 1e12)}T';
  if (value.abs() >= 1e9) return '${_trim(value / 1e9)}B';
  if (value.abs() >= 1e6) return '${_trim(value / 1e6)}M';
  if (value.abs() >= 1e3) return '${_trim(value / 1e3)}K';
  return _trim(value);
}

String _trim(double value) {
  if (value == value.roundToDouble()) return value.toStringAsFixed(0);
  return value.toString();
}
