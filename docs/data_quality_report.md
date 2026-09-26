# Data Quality & Governance Report

Every cleaning rule applied to the raw CRM export, in order, so the pipeline is auditable.

## Cleaning log

1. Loaded raw customers: 6240 rows | raw interactions: 42630 rows
2. Rule 1: Trimmed whitespace and standardized casing on full_name, city.
3. Rule 2: Lower-cased emails; flagged & nulled 0 malformed email addresses.
4. Rule 3: Normalized phone numbers to +91XXXXXXXXXX format (4938 valid numbers retained).
5. Rule 4: Standardized opt-in flag to boolean; 765 missing values defaulted to opt-out (False) per data-governance principle 'no consent on file = no marketing contact'.
6. Rule 5: De-duplicated on exact email match, then on a composite match key (normalized name + city + signup date) to avoid falsely merging different people who share a common name. Removed 535 duplicate customer records (8.6% of raw file).
7. Rule 5b: Found and removed 1 record(s) with a duplicate customer_id after the above de-dup passes — a genuine ID-collision bug (two different people assigned the same primary key upstream). Left unfixed, this would have broken the primary-key constraint when loading into a real SQL database.
8. Rule 6: Parsed signup_date across 3 inconsistent source formats (YYYY-MM-DD, DD/MM/YYYY, MM-DD-YYYY); 0 unparseable dates flagged for manual review.
9. Rule 7: 287 customers with no segment tagged 'Unclassified' rather than dropped, so downstream reports don't silently lose them.
10. Rule 7b: Found 48 records where segment='Swiggy One Member' but the membership flag disagreed (a classic two-systems-of-record problem) — reconciled the flag to match the segment label rather than leaving contradictory fields live in the same table.
11. Rule 8: Computed field-level completeness scorecard (see data_quality_report.md).
12. Rule 9: Removed 630 exact-duplicate interaction rows caused by a pipeline re-send bug.
13. Rule 10: Referential-integrity check — removed 3009 interactions referencing customer_ids that don't exist in the cleaned CRM table (orphaned records).

## Field completeness (post-clean)

| Field | % Populated |
|---|---|
| email | 100.0% |
| phone | 79.1% |
| city | 95.0% |
| segment | 95.0% |

## Summary

- Raw customer records: **6240**
- Clean, de-duplicated customer records: **5704**
- Raw interaction records: **42630**
- Clean interaction records: **38991**
