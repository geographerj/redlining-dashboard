"""
Process BigQuery data to calculate shares, gaps, ratios, and damages
Converts the BigQuery output into the format expected by the dashboard
"""

import json
import pandas as pd
from pathlib import Path
from collections import defaultdict

# Configuration
BIGQUERY_DATA_FILE = Path(__file__).parent / "data" / "webster-bank-loan-data-from-bigquery.json"
OUTPUT_FILE = Path(__file__).parent / "data" / "webster-bank-data.json"

print("=" * 100)
print("PROCESSING BIGQUERY DATA FOR DASHBOARD")
print("=" * 100)

# Read BigQuery data
print(f"\nReading BigQuery data from: {BIGQUERY_DATA_FILE}")
with open(BIGQUERY_DATA_FILE, 'r', encoding='utf-8') as f:
    bigquery_data = json.load(f)

records = bigquery_data['records']
print(f"  Loaded {len(records)} records")

# Normalize Connecticut CBSA names to merge CBSAs with different names across years
# This handles the shift from traditional counties to planning regions
CT_CBSA_MAPPING = {
    # 2022-2023 names → 2024 names (standardized)
    'Bridgeport-Stamford-Norwalk, CT': 'Bridgeport-Stamford-Danbury, CT',
    'Hartford-East Hartford-Middletown, CT': 'Hartford-West Hartford-East Hartford, CT',
    'New Haven-Milford, CT': 'New Haven, CT',
    # Note: Norwich-New London, CT and Waterbury-Shelton, CT may need special handling
    # Torrington, CT stays the same
}

# Map Connecticut planning regions to traditional counties
# Planning regions were introduced in 2024, but we want to use traditional county names
CT_PLANNING_REGION_TO_COUNTY = {
    'Greater Bridgeport Planning Region': 'Fairfield County',
    'Capitol Planning Region': 'Hartford County',
    'South Central Connecticut Planning Region': 'New Haven County',
    'Southeastern Connecticut Planning Region': 'New London County',
    'Naugatuck Valley Planning Region': 'New Haven County',  # Primary county
    'Lower Connecticut River Valley Planning Region': 'Middlesex County',
    'Northwest Hills Planning Region': 'Litchfield County',
    'Northeastern Connecticut Planning Region': 'Tolland County',  # Primary county
    'Western Connecticut Planning Region': 'Fairfield County',  # Primary county
}

print("\nNormalizing Connecticut CBSA names...")
cbsa_normalized_count = 0
for record in records:
    if record.get('state') == 'Connecticut' and record.get('cbsa') in CT_CBSA_MAPPING:
        old_cbsa = record['cbsa']
        new_cbsa = CT_CBSA_MAPPING[old_cbsa]
        record['cbsa'] = new_cbsa
        cbsa_normalized_count += 1

if cbsa_normalized_count > 0:
    print(f"  Normalized {cbsa_normalized_count} Connecticut CBSA records")

print("\nNormalizing Connecticut county names (planning regions → traditional counties)...")
county_normalized_count = 0
for record in records:
    if record.get('state') == 'Connecticut' and record.get('county') in CT_PLANNING_REGION_TO_COUNTY:
        old_county = record['county']
        new_county = CT_PLANNING_REGION_TO_COUNTY[old_county]
        record['county'] = new_county
        county_normalized_count += 1

if county_normalized_count > 0:
    print(f"  Normalized {county_normalized_count} Connecticut county records")

# Separate subject and peer records
subject_records = [r for r in records if r['bank_type'] == 'subject']
peer_records = [r for r in records if r['bank_type'] == 'peer']

print(f"  Subject records: {len(subject_records)}")
print(f"  Peer records: {len(peer_records)}")

# Calculate total counts for each geography/year/kind/loanPurpose
# This is needed to calculate shares
print("\nCalculating total counts by geography...")
total_counts = defaultdict(lambda: {
    'bankTotal': 0,
    'peerTotal': 0
})

# Group subject records to get totals
for record in subject_records:
    key = (
        record['state'],
        record['cbsa'],
        record['county'],
        record['year'],
        record['kind'],
        record['loanPurpose']
    )
    total_counts[key]['bankTotal'] += record.get('bankCount', 0) or 0

# Group peer records to get totals
for record in peer_records:
    key = (
        record['state'],
        record['cbsa'],
        record['county'],
        record['year'],
        record['kind'],
        record['loanPurpose']
    )
    total_counts[key]['peerTotal'] += record.get('peerCount', 0) or 0

print(f"  Calculated totals for {len(total_counts)} geography/year/kind/purpose combinations")

# Merge subject and peer records and calculate metrics
print("\nMerging subject and peer data and calculating metrics...")
output_records = []

# Create lookup for peer data
peer_lookup = {}
for record in peer_records:
    key = (
        record['state'],
        record['cbsa'],
        record['county'],
        record['year'],
        record['kind'],
        record['loanPurpose'],
        record['metric']
    )
    peer_lookup[key] = record

# Process subject records
for subject in subject_records:
    key = (
        subject['state'],
        subject['cbsa'],
        subject['county'],
        subject['year'],
        subject['kind'],
        subject['loanPurpose'],
        subject['metric']
    )
    
    peer = peer_lookup.get(key, {})
    
    # Get totals for this geography/year/kind/purpose
    total_key = (
        subject['state'],
        subject['cbsa'],
        subject['county'],
        subject['year'],
        subject['kind'],
        subject['loanPurpose']
    )
    totals = total_counts.get(total_key, {'bankTotal': 0, 'peerTotal': 0})
    
    bank_count = subject.get('bankCount', 0) or 0
    peer_count = peer.get('peerCount', 0) or 0
    bank_total = totals['bankTotal']
    peer_total = totals['peerTotal']
    
    # Calculate shares
    bank_share = (bank_count / bank_total * 100) if bank_total > 0 else None
    peer_share = (peer_count / peer_total * 100) if peer_total > 0 else None
    
    # Calculate gap (subject - peer)
    gap = (bank_share - peer_share) if (peer_share is not None and bank_share is not None) else None
    
    # Calculate ratio (peer_share / bank_share)
    # Ratio > 1 means peers are doing more (adverse), ratio < 1 means bank is doing more (good)
    ratio = (peer_share / bank_share) if (bank_share is not None and bank_share > 0 and peer_share is not None) else None
    
    # Get average loan amount
    avg_loan_amount = subject.get('avgLoanAmount')
    
    # Calculate shortfall (when adverse: gap < 0 OR ratio > 1)
    # Both conditions indicate the bank is underperforming relative to peers
    shortfall = None
    is_adverse = False
    
    # Check if ratio > 1 (adverse condition)
    if ratio is not None and ratio > 1 and bank_total > 0:
        # Ratio > 1 means peer_share > bank_share (peers doing more, which is adverse)
        # Calculate shortfall: what the bank should have lent to match peer performance
        # Shortfall = (peer_share - bank_share) / 100 * bank_total
        # This will be positive when ratio > 1 (peer_share > bank_share)
        if peer_share is not None and bank_share is not None:
            shortfall = ((peer_share - bank_share) / 100.0) * bank_total
            is_adverse = True
    
    # Also check gap < 0 (traditional adverse condition)
    if gap is not None and gap < 0 and bank_total > 0:
        shortfall = (gap / 100.0) * bank_total
        is_adverse = True
    
    # Calculate damages (shortfall * avg loan amount, when adverse)
    damages = None
    if is_adverse and shortfall is not None and avg_loan_amount is not None:
        # Use absolute value of shortfall for damages calculation
        damages = abs(shortfall) * avg_loan_amount
    
    output_record = {
        'lender': 'webster-bank',
        'lenderName': 'Webster Bank',
        'state': subject['state'],
        'cbsa': subject['cbsa'],
        'county': subject['county'],
        'year': subject['year'],
        'metric': subject['metric'],
        'loanPurpose': subject['loanPurpose'],
        'kind': subject['kind'],
        'bankCount': bank_count,
        'bankShare': round(bank_share, 2) if bank_share is not None else None,
        'peerShare': round(peer_share, 2) if peer_share is not None else None,
        'gap': round(gap, 2) if gap is not None else None,
        'ratio': round(ratio, 2) if ratio is not None else None,
        'avgLoanAmount': round(avg_loan_amount, 2) if avg_loan_amount is not None else None,
        'shortfall': round(shortfall, 2) if shortfall is not None else None,
        'damages': round(damages, 0) if damages is not None else None
    }
    
    output_records.append(output_record)

print(f"  Generated {len(output_records)} output records")

# Create output structure
output_data = {
    'metadata': {
        'generated': pd.Timestamp.now().isoformat(),
        'totalRecords': len(output_records),
        'bank': 'Webster Bank',
        'lei': 'WV0OVGBTLUP1XIUJE722',
        'rssd': '761806',
        'source': 'BigQuery',
        'description': 'Processed from BigQuery loan data with calculated shares, gaps, ratios, and damages'
    },
    'records': output_records
}

# Save output
print(f"\nSaving processed data to: {OUTPUT_FILE}")
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"  ✓ File saved: {OUTPUT_FILE}")
print(f"  File size: {OUTPUT_FILE.stat().st_size / 1024:.2f} KB")

# Print summary
print("\n" + "=" * 100)
print("DATA PROCESSING COMPLETED SUCCESSFULLY")
print("=" * 100)
print(f"\nTotal records: {len(output_records)}")
print(f"\nSummary by year:")
for year in [2022, 2023, 2024]:
    year_records = [r for r in output_records if r['year'] == year]
    total_loans = sum(r['bankCount'] for r in year_records)
    print(f"  {year}: {len(year_records)} records, {total_loans:,} total loans")

print(f"\nSummary by kind:")
for kind in ['Applications', 'Originations']:
    kind_records = [r for r in output_records if r['kind'] == kind]
    if kind_records:
        total_loans = sum(r['bankCount'] for r in kind_records)
        print(f"  {kind}: {len(kind_records)} records, {total_loans:,} total loans")

print(f"\nRecords with damages calculated: {sum(1 for r in output_records if r['damages'] is not None)}")


