import 'dart:convert';
import 'dart:math' as math;

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:intl/intl.dart';
import 'package:timeago/timeago.dart' as timeago;
import '/flutter_flow/custom_functions.dart';
import 'package:ff_commons/flutter_flow/lat_lng.dart';
import 'package:ff_commons/flutter_flow/place.dart';
import 'package:ff_commons/flutter_flow/uploaded_file.dart';
import '/backend/backend.dart';
import "package:shadcn_u_i_kit_v48jv9/backend/schema/structs/index.dart"
    as shadcn_u_i_kit_v48jv9_data_schema;
import 'package:cloud_firestore/cloud_firestore.dart';
import '/backend/schema/structs/index.dart';
import '/backend/schema/enums/enums.dart';
import '/auth/firebase_auth/auth_util.dart';
import "package:shadcn_u_i_kit_v48jv9/backend/schema/structs/index.dart"
    as shadcn_u_i_kit_v48jv9_data_schema;
import "package:shadcn_u_i_kit_v48jv9/backend/schema/enums/enums.dart"
    as shadcn_u_i_kit_v48jv9_enums;
import 'package:shadcn_u_i_kit_v48jv9/flutter_flow/custom_functions.dart'
    as shadcn_u_i_kit_v48jv9_functions;

DocumentReference? parseCampaignRef(String? refString) {
  /// MODIFY CODE ONLY BELOW THIS LINE

  // Use a local variable 'path' initialized with the input argument 'refString'
  String? path = refString;

  if (path == null || path.isEmpty) {
    return null;
  }

  try {
    // Якщо раптом прийде формат з дужками (DocumentReference(...)), почистимо його
    if (path.contains('(') && path.contains(')')) {
      int start = path.indexOf('(') + 1;
      int end = path.lastIndexOf(')');
      path = path.substring(start, end);
    }

    // Створюємо посилання з чистого шляху
    return FirebaseFirestore.instance.doc(path!);
  } catch (e) {
    return null;
  }

  /// MODIFY CODE ONLY ABOVE THIS LINE
}
