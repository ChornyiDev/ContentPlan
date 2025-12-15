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

List<AdsRecord>? filterAdsList(
  List<AdsRecord> adsList,
  DocumentReference? selectedCampaign,
  List<String>? selectedStatuses,
  List<String>? selectedPlatforms,
  List<String>? selectedAudiences,
  List<String>? selectedFunnelSteps,
  List<String>? selectedProducts,
  List<String>? selectedMarked,
  List<TagStruct>? selectedTags,
) {
  /// MODIFY CODE ONLY BELOW THIS LINE

  return adsList.where((ad) {
    // 1. Campaign Filter
    if (selectedCampaign != null) {
      if (ad.campaignRef != selectedCampaign) {
        return false;
      }
    }

    // 2. Status Filter
    // UPDATED: ad.status is now a String, not an Enum.
    if (selectedStatuses != null && selectedStatuses.isNotEmpty) {
      final status = ad.status;
      if (status == null) {
        return false;
      }
      // Direct string comparison since status is now a String
      if (!selectedStatuses.contains(status)) {
        return false;
      }
    }

    // 3. Platform Filter
    // UPDATED: ad.platform is now a single String, not a List.
    if (selectedPlatforms != null && selectedPlatforms.isNotEmpty) {
      final adPlatform = ad.platform; // Now a String?

      // If ad has no platform, reject it if filter is active
      if (adPlatform == null || adPlatform.isEmpty) {
        return false;
      }

      // Check if the ad's single platform is in the list of selected platforms
      if (!selectedPlatforms.contains(adPlatform)) {
        return false;
      }
    }

    // 4. Audience Filter
    if (selectedAudiences != null && selectedAudiences.isNotEmpty) {
      final adAudiences = ad.audience; // List<String>?

      // If ad has no audiences, reject it if filter is active
      if (adAudiences == null || adAudiences.isEmpty) {
        return false;
      }

      // Check if at least one selected audience matches any of the ad's audiences
      bool audienceMatch = false;
      for (var selectedAudience in selectedAudiences) {
        if (adAudiences.contains(selectedAudience)) {
          audienceMatch = true;
          break;
        }
      }

      if (!audienceMatch) {
        return false;
      }
    }

    // 5. Funnel Step Filter
    if (selectedFunnelSteps != null && selectedFunnelSteps.isNotEmpty) {
      final adFunnelSteps = ad.funnelStep; // List<String>?

      // If ad has no funnel steps, reject it if filter is active
      if (adFunnelSteps == null || adFunnelSteps.isEmpty) {
        return false;
      }

      // Check if at least one selected funnel step matches any of the ad's funnel steps
      bool funnelStepMatch = false;
      for (var selectedStep in selectedFunnelSteps) {
        if (adFunnelSteps.contains(selectedStep)) {
          funnelStepMatch = true;
          break;
        }
      }

      if (!funnelStepMatch) {
        return false;
      }
    }

    // 7. Marked Filter
    // selectedMarked can be: ["Marked"], ["Unmarked"], ["Marked", "Unmarked"], or empty
    if (selectedMarked != null && selectedMarked.isNotEmpty) {
      final isMarked = ad.marked ?? false;
      
      // If only "Marked" is selected
      if (selectedMarked.contains("Marked") && !selectedMarked.contains("Unmarked")) {
        if (!isMarked) {
          return false;
        }
      }
      
      // If only "Unmarked" is selected
      if (selectedMarked.contains("Unmarked") && !selectedMarked.contains("Marked")) {
        if (isMarked) {
          return false;
        }
      }
      
      // If both "Marked" and "Unmarked" are selected, show all ads (no filter)
      // If neither is selected (shouldn't happen), show all ads
    }

    // 8. Tag Filter (Complex)
    // selectedMarked can be: ["Marked"], ["Unmarked"], ["Marked", "Unmarked"], or empty
    if (selectedMarked != null && selectedMarked.isNotEmpty) {
      final isMarked = ad.marked ?? false;
      
      // If only "Marked" is selected
      if (selectedMarked.contains("Marked") && !selectedMarked.contains("Unmarked")) {
        if (!isMarked) {
          return false;
        }
      }
      
      // If only "Unmarked" is selected
      if (selectedMarked.contains("Unmarked") && !selectedMarked.contains("Marked")) {
        if (isMarked) {
          return false;
        }
      }
      
      // If both "Marked" and "Unmarked" are selected, show all ads (no filter)
      // If neither is selected (shouldn't happen), show all ads
    }

    // 7. Tag Filter (Complex)
    if (selectedTags != null && selectedTags.isNotEmpty) {
      for (var filterTag in selectedTags) {
        if (filterTag.options.isEmpty) {
          continue;
        }

        bool categoryMatchFound = false;

        // Safe handling of ad.tags which might not be a List
        List<TagStruct> adTags = [];
        try {
          final rawTags = ad.tags;

          if (rawTags == null) {
            adTags = [];
          } else if (rawTags is List) {
            // If it's already a List, cast each element
            adTags = (rawTags as List).map((e) => e as TagStruct).toList();
          } else {
            // If it's a single TagStruct or something else, wrap in a list
            adTags = [rawTags as TagStruct];
          }
        } catch (e) {
          adTags = [];
        }

        for (var adTag in adTags) {
          if (adTag.category == filterTag.category) {
            for (var option in filterTag.options) {
              if (adTag.options.contains(option)) {
                categoryMatchFound = true;
                break;
              }
            }
          }
          if (categoryMatchFound) break;
        }

        if (!categoryMatchFound) {
          return false;
        }
      }
    }

    return true;
  }).toList();

  /// MODIFY CODE ONLY ABOVE THIS LINE
}
