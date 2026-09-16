import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

import '../models/numeric_filter.dart';
import '../models/stock.dart';
import '../services/auth_service.dart';
import '../services/stock_repository.dart';

class StockTableScreen extends StatefulWidget {
  const StockTableScreen({
    super.key,
    required this.authService,
    required this.repository,
    required this.email,
  });

  final AuthService authService;
  final StockRepository repository;
  final String email;

  @override
  State<StockTableScreen> createState() => _StockTableScreenState();
}

class _StockTableScreenState extends State<StockTableScreen> {
  late Future<List<Stock>> _stocks;
  final _searchController = TextEditingController();
  final _filterValueController = TextEditingController();
  String _query = '';
  int _rowsPerPage = 25;
  final _filters = <NumericFilter>[];
  String _filterField = filterableFields.first.key;
  CompareOp _filterOp = CompareOp.greaterThan;

  @override
  void initState() {
    super.initState();
    _stocks = widget.repository.fetchAll();
  }

  @override
  void dispose() {
    _searchController.dispose();
    _filterValueController.dispose();
    super.dispose();
  }

  void _reload() {
    setState(() => _stocks = widget.repository.fetchAll());
  }

  void _addFilter() {
    final value = parseFilterValue(_filterValueController.text);
    if (value == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Enter a number. Suffixes k, m, b, t work (e.g. 100b).'),
        ),
      );
      return;
    }
    setState(() {
      _filters.add(
        NumericFilter(field: _filterField, op: _filterOp, value: value),
      );
      _filterValueController.clear();
    });
  }

  List<Stock> _applyFilters(List<Stock> stocks) {
    return stocks
        .where((stock) {
          if (!stock.matches(_query)) return false;
          for (final filter in _filters) {
            if (!filter.matches(stock)) return false;
          }
          return true;
        })
        .toList(growable: false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('value'),
        actions: [
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 16),
            child: Center(child: Text(widget.email)),
          ),
          IconButton(
            onPressed: _reload,
            icon: const Icon(Icons.refresh),
            tooltip: 'Reload',
          ),
          IconButton(
            onPressed: widget.authService.signOut,
            icon: const Icon(Icons.logout),
            tooltip: 'Sign out',
          ),
          const SizedBox(width: 8),
        ],
      ),
      body: FutureBuilder<List<Stock>>(
        future: _stocks,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            return _ErrorPane(error: '${snapshot.error}', onRetry: _reload);
          }

          final all = snapshot.data ?? const <Stock>[];
          final matching = _applyFilters(all);
          final fields = filterableFieldsFor(all);
          final activeField = fields.any((field) => field.key == _filterField)
              ? _filterField
              : fields.first.key;

          return Column(
            children: [
              Padding(
                padding: const EdgeInsets.all(16),
                child: TextField(
                  controller: _searchController,
                  onChanged: (value) => setState(() => _query = value.trim()),
                  decoration: InputDecoration(
                    hintText: 'Search by symbol, name, or index',
                    prefixIcon: const Icon(Icons.search),
                    border: const OutlineInputBorder(),
                    suffixIcon: _query.isEmpty
                        ? null
                        : IconButton(
                            icon: const Icon(Icons.clear),
                            onPressed: () {
                              _searchController.clear();
                              setState(() => _query = '');
                            },
                          ),
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.fromLTRB(16, 0, 16, 8),
                child: _FilterBar(
                  fields: fields,
                  field: activeField,
                  op: _filterOp,
                  valueController: _filterValueController,
                  filters: _filters,
                  onField: (value) => setState(() => _filterField = value),
                  onOp: (value) => setState(() => _filterOp = value),
                  onAdd: _addFilter,
                  onRemove: (filter) => setState(() => _filters.remove(filter)),
                  onClear: _filters.isEmpty
                      ? null
                      : () => setState(() => _filters.clear()),
                ),
              ),
              Expanded(
                child: SingleChildScrollView(
                  padding: const EdgeInsets.symmetric(horizontal: 16),
                  child: PaginatedDataTable(
                    key: ValueKey('$_query|${_filters.map((f) => f.label).join(',')}'),
                    header: Text('${matching.length} of ${all.length} symbols'),
                    rowsPerPage: _rowsPerPage,
                    availableRowsPerPage: const [10, 25, 50, 100],
                    onRowsPerPageChanged: (value) {
                      if (value != null) setState(() => _rowsPerPage = value);
                    },
                    columns: const [
                      DataColumn(label: Text('Symbol')),
                      DataColumn(label: Text('Name')),
                      DataColumn(label: Text('Index')),
                      DataColumn(label: Text('Ccy')),
                      DataColumn(label: Text('Price'), numeric: true),
                      DataColumn(label: Text('Market cap'), numeric: true),
                      DataColumn(label: Text('Div'), numeric: true),
                      DataColumn(label: Text('Div %'), numeric: true),
                      DataColumn(label: Text('EPS'), numeric: true),
                      DataColumn(label: Text('Rev / sh'), numeric: true),
                      DataColumn(label: Text('52w high'), numeric: true),
                      DataColumn(label: Text('52w low'), numeric: true),
                    ],
                    source: _StockDataSource(matching),
                  ),
                ),
              ),
            ],
          );
        },
      ),
    );
  }
}

class _StockDataSource extends DataTableSource {
  _StockDataSource(this.stocks);

  static final _marketCap = NumberFormat.compactCurrency(
    locale: 'en_US',
    symbol: r'$',
    decimalDigits: 2,
  );
  static final _price = NumberFormat.currency(
    locale: 'en_US',
    symbol: r'$',
    decimalDigits: 2,
  );
  static final _percent = NumberFormat('0.00');

  final List<Stock> stocks;

  String _money(double? value) =>
      value == null ? Stock.missing : _price.format(value);

  String _cap(double? value) =>
      value == null ? Stock.missing : _marketCap.format(value);

  String _pct(double? value) =>
      value == null ? Stock.missing : '${_percent.format(value)}%';

  @override
  DataRow? getRow(int index) {
    if (index >= stocks.length) return null;
    final stock = stocks[index];

    return DataRow.byIndex(
      index: index,
      cells: [
        DataCell(Text(stock.symbol)),
        DataCell(Text(stock.name)),
        DataCell(SizedBox(width: 160, child: Text(stock.indicesLabel))),
        DataCell(Text(stock.currency)),
        DataCell(Text(_money(stock.sharePrice))),
        DataCell(Text(_cap(stock.marketCap))),
        DataCell(Text(_money(stock.dividend))),
        DataCell(Text(_pct(stock.dividendPct))),
        DataCell(Text(_money(stock.eps))),
        DataCell(Text(_money(stock.revenuePerShare))),
        DataCell(Text(_money(stock.week52High))),
        DataCell(Text(_money(stock.week52Low))),
      ],
    );
  }

  @override
  bool get isRowCountApproximate => false;

  @override
  int get rowCount => stocks.length;

  @override
  int get selectedRowCount => 0;
}

class _FilterBar extends StatelessWidget {
  const _FilterBar({
    required this.fields,
    required this.field,
    required this.op,
    required this.valueController,
    required this.filters,
    required this.onField,
    required this.onOp,
    required this.onAdd,
    required this.onRemove,
    required this.onClear,
  });

  final List<FilterableField> fields;
  final String field;
  final CompareOp op;
  final TextEditingController valueController;
  final List<NumericFilter> filters;
  final ValueChanged<String> onField;
  final ValueChanged<CompareOp> onOp;
  final VoidCallback onAdd;
  final ValueChanged<NumericFilter> onRemove;
  final VoidCallback? onClear;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Wrap(
          spacing: 8,
          runSpacing: 8,
          crossAxisAlignment: WrapCrossAlignment.center,
          children: [
            SizedBox(
              width: 160,
              child: InputDecorator(
                decoration: const InputDecoration(
                  labelText: 'Field',
                  border: OutlineInputBorder(),
                  isDense: true,
                ),
                child: DropdownButtonHideUnderline(
                  child: DropdownButton<String>(
                    value: field,
                    isExpanded: true,
                    isDense: true,
                    items: [
                      for (final item in fields)
                        DropdownMenuItem(
                          value: item.key,
                          child: Text(item.label),
                        ),
                    ],
                    onChanged: (value) {
                      if (value != null) onField(value);
                    },
                  ),
                ),
              ),
            ),
            SizedBox(
              width: 88,
              child: InputDecorator(
                decoration: const InputDecoration(
                  labelText: 'Op',
                  border: OutlineInputBorder(),
                  isDense: true,
                ),
                child: DropdownButtonHideUnderline(
                  child: DropdownButton<CompareOp>(
                    value: op,
                    isExpanded: true,
                    isDense: true,
                    items: const [
                      DropdownMenuItem(
                        value: CompareOp.greaterThan,
                        child: Text('>'),
                      ),
                      DropdownMenuItem(
                        value: CompareOp.lessThan,
                        child: Text('<'),
                      ),
                    ],
                    onChanged: (value) {
                      if (value != null) onOp(value);
                    },
                  ),
                ),
              ),
            ),
            SizedBox(
              width: 140,
              child: TextField(
                controller: valueController,
                keyboardType: const TextInputType.numberWithOptions(
                  decimal: true,
                  signed: true,
                ),
                onSubmitted: (_) => onAdd(),
                decoration: const InputDecoration(
                  labelText: 'Value',
                  hintText: 'e.g. 5 or 100b',
                  border: OutlineInputBorder(),
                  isDense: true,
                ),
              ),
            ),
            FilledButton.icon(
              onPressed: onAdd,
              icon: const Icon(Icons.add, size: 18),
              label: const Text('Add filter'),
            ),
            if (onClear != null)
              TextButton(onPressed: onClear, child: const Text('Clear filters')),
          ],
        ),
        if (filters.isNotEmpty) ...[
          const SizedBox(height: 8),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: [
              for (final filter in filters)
                InputChip(
                  label: Text(filter.label),
                  onDeleted: () => onRemove(filter),
                ),
            ],
          ),
        ],
      ],
    );
  }
}

class _ErrorPane extends StatelessWidget {
  const _ErrorPane({required this.error, required this.onRetry});

  final String error;
  final VoidCallback onRetry;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.error_outline,
                color: Theme.of(context).colorScheme.error),
            const SizedBox(height: 12),
            Text(error, textAlign: TextAlign.center),
            const SizedBox(height: 16),
            FilledButton(onPressed: onRetry, child: const Text('Retry')),
          ],
        ),
      ),
    );
  }
}
