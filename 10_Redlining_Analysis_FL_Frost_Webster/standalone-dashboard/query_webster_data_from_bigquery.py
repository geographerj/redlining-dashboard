"""
Query BigQuery to get loan counts and dollar volumes for BOTH subject bank and peers
Peers are lenders with 50%-200% of subject bank volume in same CBSA/year/loan_purpose_category
"""

from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import os
from pathlib import Path
import json

# Configuration
PROJECT_ID = 'hdma1-242116'
WEBSTER_LEI = 'WV0OVGBTLUP1XIUJE722'
WEBSTER_RSSD = '761806'
OUTPUT_DIR = Path(__file__).parent / "data"
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "webster-bank-loan-data-from-bigquery.json"

print("=" * 100)
print("QUERYING BIGQUERY FOR WEBSTER BANK AND PEER LOAN DATA")
print("=" * 100)

# Check for BigQuery credentials
print("\nChecking for BigQuery credentials...")
credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
credentials = None

credential_paths = [
    Path(credentials_path) if credentials_path else None,
    Path(r"C:\Users\jrichardson\OneDrive - Nat'l Community Reinvestment Coaltn\Desktop\Dream\config\credentials\hdma1-242116-74024e2eb88f.json"),
    Path.home() / ".config" / "gcloud" / "application_default_credentials.json"
]

for cred_path in credential_paths:
    if cred_path and cred_path.exists():
        print(f"  Found credentials at: {cred_path}")
        credentials = service_account.Credentials.from_service_account_file(str(cred_path))
        break

if credentials:
    client = bigquery.Client(project=PROJECT_ID, credentials=credentials)
else:
    print("  Using default credentials...")
    client = bigquery.Client(project=PROJECT_ID)

print("  ✓ BigQuery client initialized")

# Build the comprehensive query with peer calculation
query = f"""
WITH state_fips_conversion AS (
    -- Helper CTE for state code to FIPS conversion
    SELECT 
        CASE state_code
            WHEN 'AL' THEN '01' WHEN 'AK' THEN '02' WHEN 'AZ' THEN '04' WHEN 'AR' THEN '05'
            WHEN 'CA' THEN '06' WHEN 'CO' THEN '08' WHEN 'CT' THEN '09' WHEN 'DE' THEN '10'
            WHEN 'FL' THEN '12' WHEN 'GA' THEN '13' WHEN 'HI' THEN '15' WHEN 'ID' THEN '16'
            WHEN 'IL' THEN '17' WHEN 'IN' THEN '18' WHEN 'IA' THEN '19' WHEN 'KS' THEN '20'
            WHEN 'KY' THEN '21' WHEN 'LA' THEN '22' WHEN 'ME' THEN '23' WHEN 'MD' THEN '24'
            WHEN 'MA' THEN '25' WHEN 'MI' THEN '26' WHEN 'MN' THEN '27' WHEN 'MS' THEN '28'
            WHEN 'MO' THEN '29' WHEN 'MT' THEN '30' WHEN 'NE' THEN '31' WHEN 'NV' THEN '32'
            WHEN 'NH' THEN '33' WHEN 'NJ' THEN '34' WHEN 'NM' THEN '35' WHEN 'NY' THEN '36'
            WHEN 'NC' THEN '37' WHEN 'ND' THEN '38' WHEN 'OH' THEN '39' WHEN 'OK' THEN '40'
            WHEN 'OR' THEN '41' WHEN 'PA' THEN '42' WHEN 'RI' THEN '44' WHEN 'SC' THEN '45'
            WHEN 'SD' THEN '46' WHEN 'TN' THEN '47' WHEN 'TX' THEN '48' WHEN 'UT' THEN '49'
            WHEN 'VT' THEN '50' WHEN 'VA' THEN '51' WHEN 'WA' THEN '53' WHEN 'WV' THEN '54'
            WHEN 'WI' THEN '55' WHEN 'WY' THEN '56' WHEN 'DC' THEN '11'
            ELSE state_code
        END as state_fips,
        state_code
    FROM (SELECT DISTINCT state_code FROM `{PROJECT_ID}.hmda.hmda` WHERE state_code IS NOT NULL)
),
webster_assessment_areas AS (
    -- Get counties where Webster Bank has branches (assessment areas)
    -- Get ALL years from both sod25 and sod_legacy to capture all counties where Webster Bank has ever had branches
    SELECT DISTINCT CAST(geoid5 AS STRING) as geoid5
    FROM `{PROJECT_ID}.branches.sod25`
    WHERE CAST(rssd AS STRING) = '{WEBSTER_RSSD}' 
        AND geoid5 IS NOT NULL
    
    UNION DISTINCT
    
    SELECT DISTINCT CAST(geoid5 AS STRING) as geoid5
    FROM `{PROJECT_ID}.branches.sod_legacy`
    WHERE CAST(rssd AS STRING) = '{WEBSTER_RSSD}' 
        AND geoid5 IS NOT NULL
),
hmda_with_geoid5 AS (
    SELECT 
        h.*,
        CONCAT(
            LPAD(s.state_fips, 2, '0'),
            LPAD(CAST(SUBSTR(LPAD(CAST(h.county_code AS STRING), 5, '0'), -3) AS STRING), 3, '0')
        ) as geoid5
    FROM `{PROJECT_ID}.hmda.hmda` h
    LEFT JOIN state_fips_conversion s ON h.state_code = s.state_code
    WHERE h.action_taken IN ('1', '2', '3', '4', '5')
        -- Excludes: 6 (Loan purchased), 7 (Preapproval denied), 8 (Preapproval approved but not accepted)
        -- Include all loan purposes for "All Loans" (1=Home Purchase, 2=Home Purchase, 4=Refinancing, 31=Refinancing, 32=Home Improvement)
        AND h.loan_purpose IN ('1', '2', '4', '31', '32')
        AND h.activity_year IN ('2022', '2023', '2024')
        AND h.census_tract IS NOT NULL
        AND h.occupancy_type = '1'
        AND h.reverse_mortgage != '1'
        AND h.construction_method = '1'
        AND h.total_units IN ('1', '2', '3', '4')
),
hmda_with_cbsa AS (
    -- Add CBSA codes to HMDA records and filter to assessment areas
    SELECT 
        h.*,
        CAST(c.cbsa_code AS STRING) as cbsa_code,
        c.County as county_name,
        c.cbsa as cbsa_name,
        SUBSTR(c.geoid5, 1, 2) as state_code_from_cbsa,
        c.State as state_name
    FROM hmda_with_geoid5 h
    INNER JOIN webster_assessment_areas faa
        ON LPAD(CAST(h.geoid5 AS STRING), 5, '0') = LPAD(faa.geoid5, 5, '0')
    LEFT JOIN `{PROJECT_ID}.geo.cbsa_to_county` c
        ON LPAD(CAST(h.geoid5 AS STRING), 5, '0') = LPAD(CAST(c.geoid5 AS STRING), 5, '0')
),
subject_hmda AS (
    -- For action_taken = '1', create both 'Originations' and 'Applications' records
    -- For action_taken IN ('2', '3', '4', '5'), create only 'Applications' records
    SELECT 
        CAST(activity_year AS INT64) as year,
        lei,
        census_tract,
        geoid5,
        cbsa_code,
        cbsa_name,
        county_name,
        COALESCE(state_code_from_cbsa, state_code) as state_code,
        state_name,
        CAST(loan_amount AS FLOAT64) as loan_amount,
        action_taken,
        loan_purpose,
        'Originations' as kind,  -- action_taken = '1' only
        CASE
            WHEN loan_purpose = '1' THEN 'Home Purchase'
            WHEN loan_purpose IN ('2', '4', '31', '32') THEN 'All Loans'  -- All Loans includes 2, 4, 31, 32 (1 is handled separately as Home Purchase)
            ELSE 'Other'
        END as loan_purpose_category
    FROM hmda_with_cbsa
    WHERE lei = '{WEBSTER_LEI}'
        AND action_taken = '1'
    
    UNION ALL
    
    SELECT 
        CAST(activity_year AS INT64) as year,
        lei,
        census_tract,
        geoid5,
        cbsa_code,
        cbsa_name,
        county_name,
        COALESCE(state_code_from_cbsa, state_code) as state_code,
        state_name,
        CAST(loan_amount AS FLOAT64) as loan_amount,
        action_taken,
        loan_purpose,
        'Applications' as kind,  -- action_taken IN ('1', '2', '3', '4', '5') - all of them
        CASE
            WHEN loan_purpose = '1' THEN 'Home Purchase'
            WHEN loan_purpose IN ('2', '4', '31', '32') THEN 'All Loans'  -- All Loans includes 2, 4, 31, 32 (1 is handled separately as Home Purchase)
            ELSE 'Other'
        END as loan_purpose_category
    FROM hmda_with_cbsa
    WHERE lei = '{WEBSTER_LEI}'
        AND action_taken IN ('1', '2', '3', '4', '5')
),
subject_volumes AS (
    -- Calculate subject bank volumes by CBSA/year/loan_purpose_category (NO kind)
    -- Use COALESCE to handle NULL cbsa_code (rural areas)
    SELECT 
        COALESCE(cbsa_code, '99999') as cbsa_code,
        year,
        loan_purpose_category,
        COUNT(*) as subject_volume
    FROM subject_hmda
    GROUP BY COALESCE(cbsa_code, '99999'), year, loan_purpose_category
),
all_bank_volumes AS (
    -- Calculate volumes for ALL banks by CBSA/year/loan_purpose_category (NO kind)
    -- Use COALESCE to handle NULL cbsa_code (rural areas)
    SELECT 
        COALESCE(CAST(cbsa_code AS STRING), '99999') as cbsa_code,
        CAST(activity_year AS INT64) as year,
        lei,
        CASE
            WHEN loan_purpose = '1' THEN 'Home Purchase'
            WHEN loan_purpose IN ('2', '4', '31', '32') THEN 'All Loans'  -- All Loans includes 2, 4, 31, 32 (1 is handled separately as Home Purchase)
            ELSE 'Other'
        END as loan_purpose_category,
        COUNT(*) as bank_volume
    FROM hmda_with_cbsa
    WHERE lei != '{WEBSTER_LEI}'
    GROUP BY COALESCE(CAST(cbsa_code AS STRING), '99999'), year, lei, loan_purpose_category
),
peer_banks AS (
    -- Identify peer banks (50%-200% volume rule) by CBSA/year/loan_purpose_category (NO kind)
    SELECT DISTINCT
        sv.cbsa_code,
        sv.year,
        sv.loan_purpose_category,
        abv.lei as peer_lei
    FROM subject_volumes sv
    INNER JOIN all_bank_volumes abv
        ON sv.cbsa_code = abv.cbsa_code
        AND sv.year = abv.year
        AND sv.loan_purpose_category = abv.loan_purpose_category
    WHERE abv.bank_volume >= sv.subject_volume * 0.5
        AND abv.bank_volume <= sv.subject_volume * 2.0
),
peer_hmda_raw AS (
    -- Get peer bank HMDA records
    -- For action_taken = '1', create both 'Originations' and 'Applications' records
    -- For action_taken IN ('2', '3', '4', '5'), create only 'Applications' records
    SELECT 
        CAST(h.activity_year AS INT64) as year,
        h.lei,
        h.census_tract,
        h.geoid5,
        h.cbsa_code,
        h.cbsa_name,
        h.county_name,
        COALESCE(h.state_code_from_cbsa, h.state_code) as state_code,
        h.state_name,
        CAST(h.loan_amount AS FLOAT64) as loan_amount,
        h.action_taken,
        h.loan_purpose,
        'Originations' as kind,  -- action_taken = '1' only
        CASE
            WHEN h.loan_purpose = '1' THEN 'Home Purchase'
            WHEN h.loan_purpose IN ('2', '4', '31', '32') THEN 'All Loans'
            ELSE 'Other'
        END as loan_purpose_category
    FROM hmda_with_cbsa h
    INNER JOIN peer_banks pb
        ON h.lei = pb.peer_lei
        AND CAST(h.activity_year AS INT64) = pb.year
        AND COALESCE(h.cbsa_code, '99999') = pb.cbsa_code
        AND CASE
            WHEN h.loan_purpose = '1' THEN 'Home Purchase'
            WHEN h.loan_purpose IN ('2', '4', '31', '32') THEN 'All Loans'
            ELSE 'Other'
        END = pb.loan_purpose_category
    WHERE h.action_taken = '1'
    
    UNION ALL
    
    SELECT 
        CAST(h.activity_year AS INT64) as year,
        h.lei,
        h.census_tract,
        h.geoid5,
        h.cbsa_code,
        h.cbsa_name,
        h.county_name,
        COALESCE(h.state_code_from_cbsa, h.state_code) as state_code,
        h.state_name,
        CAST(h.loan_amount AS FLOAT64) as loan_amount,
        h.action_taken,
        h.loan_purpose,
        'Applications' as kind,  -- action_taken IN ('1', '2', '3', '4', '5') - all of them
        CASE
            WHEN h.loan_purpose = '1' THEN 'Home Purchase'
            WHEN h.loan_purpose IN ('2', '4', '31', '32') THEN 'All Loans'
            ELSE 'Other'
        END as loan_purpose_category
    FROM hmda_with_cbsa h
    INNER JOIN peer_banks pb
        ON h.lei = pb.peer_lei
        AND CAST(h.activity_year AS INT64) = pb.year
        AND COALESCE(h.cbsa_code, '99999') = pb.cbsa_code
        AND CASE
            WHEN h.loan_purpose = '1' THEN 'Home Purchase'
            WHEN h.loan_purpose IN ('2', '4', '31', '32') THEN 'All Loans'
            ELSE 'Other'
        END = pb.loan_purpose_category
    WHERE h.action_taken IN ('1', '2', '3', '4', '5')
),
census_demographics AS (
    -- Get census tract demographics with redlining metric flags
    -- For Connecticut: Use census_legacy (traditional county FIPS codes like 001 for Fairfield County)
    -- For other states: Use geo.census (standard format)
    SELECT 
        geoid as census_tract,
        SUBSTR(geoid, 1, 5) as geoid5,
        total_black,
        total_hispanic,
        total_white,
        total_persons,
        CASE WHEN SAFE_DIVIDE((total_black + total_hispanic + total_white), total_persons) * 100 >= 50 THEN TRUE ELSE FALSE END as is_mmct_50,
        CASE WHEN SAFE_DIVIDE(total_black, total_persons) * 100 >= 50 THEN TRUE ELSE FALSE END as is_black_50,
        CASE WHEN SAFE_DIVIDE(total_hispanic, total_persons) * 100 >= 50 THEN TRUE ELSE FALSE END as is_hispanic_50,
        CASE WHEN SAFE_DIVIDE((total_black + total_hispanic), total_persons) * 100 >= 50 THEN TRUE ELSE FALSE END as is_black_hispanic_50,
        CASE WHEN SAFE_DIVIDE((total_black + total_hispanic + total_white), total_persons) * 100 >= 80 THEN TRUE ELSE FALSE END as is_mmct_80,
        CASE WHEN SAFE_DIVIDE(total_black, total_persons) * 100 >= 80 THEN TRUE ELSE FALSE END as is_black_80,
        CASE WHEN SAFE_DIVIDE(total_hispanic, total_persons) * 100 >= 80 THEN TRUE ELSE FALSE END as is_hispanic_80,
        CASE WHEN SAFE_DIVIDE((total_black + total_hispanic), total_persons) * 100 >= 80 THEN TRUE ELSE FALSE END as is_black_hispanic_80
    FROM `{PROJECT_ID}.geo.census_legacy`
    WHERE geoid IS NOT NULL
        AND SUBSTR(geoid, 1, 2) = '09'  -- Connecticut only (traditional county FIPS)
    
    UNION ALL
    
    SELECT 
        geoid as census_tract,
        SUBSTR(geoid, 1, 5) as geoid5,
        total_black,
        total_hispanic,
        total_white,
        total_persons,
        CASE WHEN SAFE_DIVIDE((total_black + total_hispanic + total_white), total_persons) * 100 >= 50 THEN TRUE ELSE FALSE END as is_mmct_50,
        CASE WHEN SAFE_DIVIDE(total_black, total_persons) * 100 >= 50 THEN TRUE ELSE FALSE END as is_black_50,
        CASE WHEN SAFE_DIVIDE(total_hispanic, total_persons) * 100 >= 50 THEN TRUE ELSE FALSE END as is_hispanic_50,
        CASE WHEN SAFE_DIVIDE((total_black + total_hispanic), total_persons) * 100 >= 50 THEN TRUE ELSE FALSE END as is_black_hispanic_50,
        CASE WHEN SAFE_DIVIDE((total_black + total_hispanic + total_white), total_persons) * 100 >= 80 THEN TRUE ELSE FALSE END as is_mmct_80,
        CASE WHEN SAFE_DIVIDE(total_black, total_persons) * 100 >= 80 THEN TRUE ELSE FALSE END as is_black_80,
        CASE WHEN SAFE_DIVIDE(total_hispanic, total_persons) * 100 >= 80 THEN TRUE ELSE FALSE END as is_hispanic_80,
        CASE WHEN SAFE_DIVIDE((total_black + total_hispanic), total_persons) * 100 >= 80 THEN TRUE ELSE FALSE END as is_black_hispanic_80
    FROM `{PROJECT_ID}.geo.census`
    WHERE geoid IS NOT NULL
        AND SUBSTR(geoid, 1, 2) != '09'  -- All other states (standard format)
),
subject_with_metrics AS (
    SELECT 
        s.*,
        c.is_mmct_50,
        c.is_black_50,
        c.is_hispanic_50,
        c.is_black_hispanic_50,
        c.is_mmct_80,
        c.is_black_80,
        c.is_hispanic_80,
        c.is_black_hispanic_80
    FROM subject_hmda s
    LEFT JOIN census_demographics c
        ON LPAD(CAST(s.census_tract AS STRING), 11, '0') = LPAD(CAST(c.census_tract AS STRING), 11, '0')
),
peer_with_metrics AS (
    SELECT 
        p.*,
        c.is_mmct_50,
        c.is_black_50,
        c.is_hispanic_50,
        c.is_black_hispanic_50,
        c.is_mmct_80,
        c.is_black_80,
        c.is_hispanic_80,
        c.is_black_hispanic_80
    FROM peer_hmda_raw p
    LEFT JOIN census_demographics c
        ON LPAD(CAST(p.census_tract AS STRING), 11, '0') = LPAD(CAST(c.census_tract AS STRING), 11, '0')
)
-- Subject bank: Black+Hispanic Tract 50%
SELECT 
    'subject' as bank_type,
    state_name as state,
    cbsa_name as cbsa,
    county_name as county,
    year,
    kind,
    loan_purpose_category as loanPurpose,
    'Black+Hispanic Tract 50%' as metric,
    COUNT(*) as bankCount,
    SUM(loan_amount) as dollarVolume,
    AVG(loan_amount) as avgLoanAmount,
    CAST(NULL AS INT64) as peerCount,
    CAST(NULL AS FLOAT64) as peerDollarVolume,
    CAST(NULL AS FLOAT64) as peerAvgLoanAmount
FROM subject_with_metrics
WHERE is_black_hispanic_50 = TRUE
GROUP BY state_name, cbsa_name, county_name, year, kind, loan_purpose_category

UNION ALL

-- Peer banks: Black+Hispanic Tract 50%
SELECT 
    'peer' as bank_type,
    state_name as state,
    cbsa_name as cbsa,
    county_name as county,
    year,
    kind,
    loan_purpose_category as loanPurpose,
    'Black+Hispanic Tract 50%' as metric,
    CAST(NULL AS INT64) as bankCount,
    CAST(NULL AS FLOAT64) as dollarVolume,
    CAST(NULL AS FLOAT64) as avgLoanAmount,
    COUNT(*) as peerCount,
    SUM(loan_amount) as peerDollarVolume,
    AVG(loan_amount) as peerAvgLoanAmount
FROM peer_with_metrics
WHERE is_black_hispanic_50 = TRUE
GROUP BY state_name, cbsa_name, county_name, year, kind, loan_purpose_category

UNION ALL

-- Subject bank: MMCT 50%
SELECT 
    'subject' as bank_type,
    state_name as state,
    cbsa_name as cbsa,
    county_name as county,
    year,
    kind,
    loan_purpose_category as loanPurpose,
    'MMCT 50%' as metric,
    COUNT(*) as bankCount,
    SUM(loan_amount) as dollarVolume,
    AVG(loan_amount) as avgLoanAmount,
    CAST(NULL AS INT64) as peerCount,
    CAST(NULL AS FLOAT64) as peerDollarVolume,
    CAST(NULL AS FLOAT64) as peerAvgLoanAmount
FROM subject_with_metrics
WHERE is_mmct_50 = TRUE
GROUP BY state_name, cbsa_name, county_name, year, kind, loan_purpose_category

UNION ALL

-- Peer banks: MMCT 50%
SELECT 
    'peer' as bank_type,
    state_name as state,
    cbsa_name as cbsa,
    county_name as county,
    year,
    kind,
    loan_purpose_category as loanPurpose,
    'MMCT 50%' as metric,
    CAST(NULL AS INT64) as bankCount,
    CAST(NULL AS FLOAT64) as dollarVolume,
    CAST(NULL AS FLOAT64) as avgLoanAmount,
    COUNT(*) as peerCount,
    SUM(loan_amount) as peerDollarVolume,
    AVG(loan_amount) as peerAvgLoanAmount
FROM peer_with_metrics
WHERE is_mmct_50 = TRUE
GROUP BY state_name, cbsa_name, county_name, year, kind, loan_purpose_category

UNION ALL

-- Subject bank: Black Tract 50%
SELECT 
    'subject' as bank_type,
    state_name as state,
    cbsa_name as cbsa,
    county_name as county,
    year,
    kind,
    loan_purpose_category as loanPurpose,
    'Black Tract 50%' as metric,
    COUNT(*) as bankCount,
    SUM(loan_amount) as dollarVolume,
    AVG(loan_amount) as avgLoanAmount,
    CAST(NULL AS INT64) as peerCount,
    CAST(NULL AS FLOAT64) as peerDollarVolume,
    CAST(NULL AS FLOAT64) as peerAvgLoanAmount
FROM subject_with_metrics
WHERE is_black_50 = TRUE
GROUP BY state_name, cbsa_name, county_name, year, kind, loan_purpose_category

UNION ALL

-- Peer banks: Black Tract 50%
SELECT 
    'peer' as bank_type,
    state_name as state,
    cbsa_name as cbsa,
    county_name as county,
    year,
    kind,
    loan_purpose_category as loanPurpose,
    'Black Tract 50%' as metric,
    CAST(NULL AS INT64) as bankCount,
    CAST(NULL AS FLOAT64) as dollarVolume,
    CAST(NULL AS FLOAT64) as avgLoanAmount,
    COUNT(*) as peerCount,
    SUM(loan_amount) as peerDollarVolume,
    AVG(loan_amount) as peerAvgLoanAmount
FROM peer_with_metrics
WHERE is_black_50 = TRUE
GROUP BY state_name, cbsa_name, county_name, year, kind, loan_purpose_category

UNION ALL

-- Subject bank: Hispanic Tract 50%
SELECT 
    'subject' as bank_type,
    state_name as state,
    cbsa_name as cbsa,
    county_name as county,
    year,
    kind,
    loan_purpose_category as loanPurpose,
    'Hispanic Tract 50%' as metric,
    COUNT(*) as bankCount,
    SUM(loan_amount) as dollarVolume,
    AVG(loan_amount) as avgLoanAmount,
    CAST(NULL AS INT64) as peerCount,
    CAST(NULL AS FLOAT64) as peerDollarVolume,
    CAST(NULL AS FLOAT64) as peerAvgLoanAmount
FROM subject_with_metrics
WHERE is_hispanic_50 = TRUE
GROUP BY state_name, cbsa_name, county_name, year, kind, loan_purpose_category

UNION ALL

-- Peer banks: Hispanic Tract 50%
SELECT 
    'peer' as bank_type,
    state_name as state,
    cbsa_name as cbsa,
    county_name as county,
    year,
    kind,
    loan_purpose_category as loanPurpose,
    'Hispanic Tract 50%' as metric,
    CAST(NULL AS INT64) as bankCount,
    CAST(NULL AS FLOAT64) as dollarVolume,
    CAST(NULL AS FLOAT64) as avgLoanAmount,
    COUNT(*) as peerCount,
    SUM(loan_amount) as peerDollarVolume,
    AVG(loan_amount) as peerAvgLoanAmount
FROM peer_with_metrics
WHERE is_hispanic_50 = TRUE
GROUP BY state_name, cbsa_name, county_name, year, kind, loan_purpose_category

UNION ALL

-- Subject bank: Black+Hispanic Tract 80%
SELECT 
    'subject' as bank_type,
    state_name as state,
    cbsa_name as cbsa,
    county_name as county,
    year,
    kind,
    loan_purpose_category as loanPurpose,
    'Black+Hispanic Tract 80%' as metric,
    COUNT(*) as bankCount,
    SUM(loan_amount) as dollarVolume,
    AVG(loan_amount) as avgLoanAmount,
    CAST(NULL AS INT64) as peerCount,
    CAST(NULL AS FLOAT64) as peerDollarVolume,
    CAST(NULL AS FLOAT64) as peerAvgLoanAmount
FROM subject_with_metrics
WHERE is_black_hispanic_80 = TRUE
GROUP BY state_name, cbsa_name, county_name, year, kind, loan_purpose_category

UNION ALL

-- Peer banks: Black+Hispanic Tract 80%
SELECT 
    'peer' as bank_type,
    state_name as state,
    cbsa_name as cbsa,
    county_name as county,
    year,
    kind,
    loan_purpose_category as loanPurpose,
    'Black+Hispanic Tract 80%' as metric,
    CAST(NULL AS INT64) as bankCount,
    CAST(NULL AS FLOAT64) as dollarVolume,
    CAST(NULL AS FLOAT64) as avgLoanAmount,
    COUNT(*) as peerCount,
    SUM(loan_amount) as peerDollarVolume,
    AVG(loan_amount) as peerAvgLoanAmount
FROM peer_with_metrics
WHERE is_black_hispanic_80 = TRUE
GROUP BY state_name, cbsa_name, county_name, year, kind, loan_purpose_category

UNION ALL

-- Subject bank: MMCT 80%
SELECT 
    'subject' as bank_type,
    state_name as state,
    cbsa_name as cbsa,
    county_name as county,
    year,
    kind,
    loan_purpose_category as loanPurpose,
    'MMCT 80%' as metric,
    COUNT(*) as bankCount,
    SUM(loan_amount) as dollarVolume,
    AVG(loan_amount) as avgLoanAmount,
    CAST(NULL AS INT64) as peerCount,
    CAST(NULL AS FLOAT64) as peerDollarVolume,
    CAST(NULL AS FLOAT64) as peerAvgLoanAmount
FROM subject_with_metrics
WHERE is_mmct_80 = TRUE
GROUP BY state_name, cbsa_name, county_name, year, kind, loan_purpose_category

UNION ALL

-- Peer banks: MMCT 80%
SELECT 
    'peer' as bank_type,
    state_name as state,
    cbsa_name as cbsa,
    county_name as county,
    year,
    kind,
    loan_purpose_category as loanPurpose,
    'MMCT 80%' as metric,
    CAST(NULL AS INT64) as bankCount,
    CAST(NULL AS FLOAT64) as dollarVolume,
    CAST(NULL AS FLOAT64) as avgLoanAmount,
    COUNT(*) as peerCount,
    SUM(loan_amount) as peerDollarVolume,
    AVG(loan_amount) as peerAvgLoanAmount
FROM peer_with_metrics
WHERE is_mmct_80 = TRUE
GROUP BY state_name, cbsa_name, county_name, year, kind, loan_purpose_category

UNION ALL

-- Subject bank: Black Tract 80%
SELECT 
    'subject' as bank_type,
    state_name as state,
    cbsa_name as cbsa,
    county_name as county,
    year,
    kind,
    loan_purpose_category as loanPurpose,
    'Black Tract 80%' as metric,
    COUNT(*) as bankCount,
    SUM(loan_amount) as dollarVolume,
    AVG(loan_amount) as avgLoanAmount,
    CAST(NULL AS INT64) as peerCount,
    CAST(NULL AS FLOAT64) as peerDollarVolume,
    CAST(NULL AS FLOAT64) as peerAvgLoanAmount
FROM subject_with_metrics
WHERE is_black_80 = TRUE
GROUP BY state_name, cbsa_name, county_name, year, kind, loan_purpose_category

UNION ALL

-- Peer banks: Black Tract 80%
SELECT 
    'peer' as bank_type,
    state_name as state,
    cbsa_name as cbsa,
    county_name as county,
    year,
    kind,
    loan_purpose_category as loanPurpose,
    'Black Tract 80%' as metric,
    CAST(NULL AS INT64) as bankCount,
    CAST(NULL AS FLOAT64) as dollarVolume,
    CAST(NULL AS FLOAT64) as avgLoanAmount,
    COUNT(*) as peerCount,
    SUM(loan_amount) as peerDollarVolume,
    AVG(loan_amount) as peerAvgLoanAmount
FROM peer_with_metrics
WHERE is_black_80 = TRUE
GROUP BY state_name, cbsa_name, county_name, year, kind, loan_purpose_category

UNION ALL

-- Subject bank: Hispanic Tract 80%
SELECT 
    'subject' as bank_type,
    state_name as state,
    cbsa_name as cbsa,
    county_name as county,
    year,
    kind,
    loan_purpose_category as loanPurpose,
    'Hispanic Tract 80%' as metric,
    COUNT(*) as bankCount,
    SUM(loan_amount) as dollarVolume,
    AVG(loan_amount) as avgLoanAmount,
    CAST(NULL AS INT64) as peerCount,
    CAST(NULL AS FLOAT64) as peerDollarVolume,
    CAST(NULL AS FLOAT64) as peerAvgLoanAmount
FROM subject_with_metrics
WHERE is_hispanic_80 = TRUE
GROUP BY state_name, cbsa_name, county_name, year, kind, loan_purpose_category

UNION ALL

-- Peer banks: Hispanic Tract 80%
SELECT 
    'peer' as bank_type,
    state_name as state,
    cbsa_name as cbsa,
    county_name as county,
    year,
    kind,
    loan_purpose_category as loanPurpose,
    'Hispanic Tract 80%' as metric,
    CAST(NULL AS INT64) as bankCount,
    CAST(NULL AS FLOAT64) as dollarVolume,
    CAST(NULL AS FLOAT64) as avgLoanAmount,
    COUNT(*) as peerCount,
    SUM(loan_amount) as peerDollarVolume,
    AVG(loan_amount) as peerAvgLoanAmount
FROM peer_with_metrics
WHERE is_hispanic_80 = TRUE
GROUP BY state_name, cbsa_name, county_name, year, kind, loan_purpose_category

UNION ALL

-- Subject bank: Total (all loans regardless of tract characteristics)
SELECT 
    'subject' as bank_type,
    state_name as state,
    cbsa_name as cbsa,
    county_name as county,
    year,
    kind,
    loan_purpose_category as loanPurpose,
    'Total' as metric,
    COUNT(*) as bankCount,
    SUM(loan_amount) as dollarVolume,
    AVG(loan_amount) as avgLoanAmount,
    CAST(NULL AS INT64) as peerCount,
    CAST(NULL AS FLOAT64) as peerDollarVolume,
    CAST(NULL AS FLOAT64) as peerAvgLoanAmount
FROM subject_hmda
GROUP BY state_name, cbsa_name, county_name, year, kind, loan_purpose_category

UNION ALL

-- Peer banks: Total (all loans regardless of tract characteristics)
SELECT 
    'peer' as bank_type,
    state_name as state,
    cbsa_name as cbsa,
    county_name as county,
    year,
    kind,
    loan_purpose_category as loanPurpose,
    'Total' as metric,
    CAST(NULL AS INT64) as bankCount,
    CAST(NULL AS FLOAT64) as dollarVolume,
    CAST(NULL AS FLOAT64) as avgLoanAmount,
    COUNT(*) as peerCount,
    SUM(loan_amount) as peerDollarVolume,
    AVG(loan_amount) as peerAvgLoanAmount
FROM peer_hmda_raw
GROUP BY state_name, cbsa_name, county_name, year, kind, loan_purpose_category

ORDER BY bank_type, state, cbsa, county, metric, year, kind, loanPurpose
"""

print("\nExecuting BigQuery query...")
print("  This may take several minutes...")
print("  Calculating peers (50%-200% volume in same CBSA/year/loan_purpose_category)...")
print("  Aggregating data for all 8 metrics + Total (subject + peer)...")

try:
    query_job = client.query(query)
    results = query_job.result()
    
    print("  ✓ Query completed")
    print("  Converting results to DataFrame...")
    
    df = results.to_dataframe()
    
    print(f"  ✓ Retrieved {len(df)} records")
    print(f"  Saving to: {OUTPUT_FILE}")
    
    # Convert to JSON format
    records = df.to_dict('records')
    
    # Convert numeric types to native Python types for JSON serialization
    for record in records:
        record['year'] = int(record['year'])
        if pd.notna(record.get('bankCount')):
            record['bankCount'] = int(record['bankCount'])
        else:
            record['bankCount'] = None
        if pd.notna(record.get('dollarVolume')):
            record['dollarVolume'] = float(record['dollarVolume'])
        else:
            record['dollarVolume'] = None
        if pd.notna(record.get('avgLoanAmount')):
            record['avgLoanAmount'] = float(record['avgLoanAmount'])
        else:
            record['avgLoanAmount'] = None
        if pd.notna(record.get('peerCount')):
            record['peerCount'] = int(record['peerCount'])
        else:
            record['peerCount'] = None
        if pd.notna(record.get('peerDollarVolume')):
            record['peerDollarVolume'] = float(record['peerDollarVolume'])
        else:
            record['peerDollarVolume'] = None
        if pd.notna(record.get('peerAvgLoanAmount')):
            record['peerAvgLoanAmount'] = float(record['peerAvgLoanAmount'])
        else:
            record['peerAvgLoanAmount'] = None
    
    output_data = {
        'metadata': {
            'generated': pd.Timestamp.now().isoformat(),
            'totalRecords': len(records),
            'description': 'Loan counts and dollar volumes from BigQuery for subject bank and peers',
            'bank': 'Webster Bank',
            'lei': WEBSTER_LEI,
            'rssd': WEBSTER_RSSD,
            'peerDefinition': 'Banks with 50%-200% of subject bank volume in same CBSA/year/loan_purpose_category'
        },
        'records': records
    }
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"  ✓ File saved: {OUTPUT_FILE}")
    print(f"  File size: {OUTPUT_FILE.stat().st_size / 1024:.2f} KB")
    
    # Print summary statistics
    print("\n" + "=" * 100)
    print("QUERY COMPLETED SUCCESSFULLY")
    print("=" * 100)
    print(f"\nOutput file: {OUTPUT_FILE}")
    print(f"Total records: {len(records)}")
    
    subject_records = [r for r in records if r['bank_type'] == 'subject']
    peer_records = [r for r in records if r['bank_type'] == 'peer']
    
    print(f"\nSubject bank records: {len(subject_records)}")
    print(f"Peer bank records: {len(peer_records)}")
    
    print(f"\nSummary by year:")
    for year in [2022, 2023, 2024]:
        year_subject = [r for r in subject_records if r['year'] == year]
        year_peer = [r for r in peer_records if r['year'] == year]
        total_bank_loans = sum(r['bankCount'] for r in year_subject if r['bankCount'])
        total_peer_loans = sum(r['peerCount'] for r in year_peer if r['peerCount'])
        print(f"  {year}: Subject={len(year_subject)} records ({total_bank_loans:,} loans), Peer={len(year_peer)} records ({total_peer_loans:,} loans)")
    
    print(f"\nSummary by kind:")
    for kind in ['Applications', 'Originations']:
        kind_subject = [r for r in subject_records if r['kind'] == kind]
        kind_peer = [r for r in peer_records if r['kind'] == kind]
        if kind_subject or kind_peer:
            total_bank = sum(r['bankCount'] for r in kind_subject if r['bankCount'])
            total_peer = sum(r['peerCount'] for r in kind_peer if r['peerCount'])
            print(f"  {kind}: Subject={len(kind_subject)} records ({total_bank:,} loans), Peer={len(kind_peer)} records ({total_peer:,} loans)")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    exit(1)

