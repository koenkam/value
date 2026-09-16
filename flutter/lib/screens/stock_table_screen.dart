import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

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
  String _query = '';
  int _rowsPerPage = 25;

  @override
  void initState() {
    super.initState();
    _stocks = widget.repository.fetchAll();
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  void _reload() {
    setState(() => _stocks = widget.repository.fetchAll());
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
          final matching =
              all.where((stock) => stock.matches(_query)).toList(growable: false);

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
              Expanded(
                child: SingleChildScrollView(
                  padding: const EdgeInsets.symmetric(horizontal: 16),
                  child: PaginatedDataTable(
                    key: ValueKey(_query),
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
