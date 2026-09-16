import 'package:cloud_firestore/cloud_firestore.dart';

import '../models/stock.dart';

/// Reads the `stock` collection, which holds one document per symbol: the
/// document ID is the symbol and each property is a field on that document.
///
/// The whole collection is fetched in one go (a couple of thousand small
/// documents) so that search and pagination can run locally and stay instant.
/// If the universe grows by an order of magnitude, switch to server-side paging
/// on the document ID.
class StockRepository {
  StockRepository({FirebaseFirestore? firestore})
      : _firestore = firestore ?? FirebaseFirestore.instance;

  static const collectionName = 'stock';

  final FirebaseFirestore _firestore;

  Future<List<Stock>> fetchAll() async {
    final snapshot = await _firestore
        .collection(collectionName)
        .orderBy(FieldPath.documentId)
        .get();

    return snapshot.docs
        .map((doc) => Stock(symbol: doc.id, fields: doc.data()))
        .toList(growable: false);
  }
}
