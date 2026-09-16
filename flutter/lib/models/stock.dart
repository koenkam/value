/// A stock backed by one document in the Firestore `stock` collection: the
/// document ID is the [symbol] and every document field becomes an entry in
/// [fields].
class Stock {
  Stock({required this.symbol, required this.fields});

  static const missing = 'N/A';

  final String symbol;
  final Map<String, dynamic> fields;

  String get name => fields['name']?.toString() ?? '';

  String get currency => _asString('currency');

  List<String> get indices {
    final raw = fields['indices'];
    if (raw is List) {
      return raw.map((item) => '$item').where((item) => item.isNotEmpty).toList();
    }
    if (raw is String && raw.isNotEmpty && raw != missing) {
      return raw.split(',').map((part) => part.trim()).toList();
    }
    return const [];
  }

  String get indicesLabel => indices.isEmpty ? missing : indices.join(', ');

  double? get marketCap => _asDouble('market_cap');
  double? get sharePrice => _asDouble('share_price');
  double? get dividend => _asDouble('dividend');
  double? get dividendPct => _asDouble('dividend_pct');
  double? get eps => _asDouble('eps');
  double? get revenuePerShare => _asDouble('revenue_per_share');
  double? get week52High => _asDouble('week_52_high');
  double? get week52Low => _asDouble('week_52_low');

  /// Numeric fields are stored as Firestore numbers; the updater writes the
  /// string "N/A" when Yahoo has no value for that stock.
  double? _asDouble(String field) {
    final raw = fields[field];
    if (raw == null) return null;
    if (raw is String) {
      if (raw.toUpperCase() == missing) return null;
      return double.tryParse(raw);
    }
    if (raw is num) return raw.toDouble();
    return null;
  }

  String _asString(String field) {
    final raw = fields[field];
    if (raw == null) return missing;
    final text = '$raw';
    return text.isEmpty ? missing : text;
  }

  /// True when [query] matches the symbol, name, or an index name.
  bool matches(String query) {
    if (query.isEmpty) return true;
    final needle = query.toLowerCase();
    return symbol.toLowerCase().contains(needle) ||
        name.toLowerCase().contains(needle) ||
        indices.any((index) => index.toLowerCase().contains(needle));
  }
}
