/**
 * Data processing utilities for filtering and aggregating lending data
 */

export interface LendingRecord {
  bank: string;
  lei: string;
  state: string;
  cbsa: string;
  county: string;
  year: number;
  metric: string;
  loan_purpose: string;
  kind: string;
  bank_count: number;
  bank_share: number | null;
  peer_share: number | null;
  gap: number | null;
  ratio: number | null;
  cbsa_app_percent_bucket?: string;
}

export interface FilterOptions {
  bank?: string;
  state?: string;
  cbsa?: string;
  county?: string;
  year?: number | number[];
  metrics?: string[];
  loan_purpose?: string;
  kind?: string;
}

/**
 * Filter data based on options
 */
export function filterData(
  data: LendingRecord[],
  options: FilterOptions
): LendingRecord[] {
  let filtered = [...data];

  if (options.bank) {
    filtered = filtered.filter(r => r.bank === options.bank);
  }

  if (options.state) {
    filtered = filtered.filter(r => r.state === options.state);
  }

  if (options.cbsa) {
    filtered = filtered.filter(r => r.cbsa === options.cbsa);
  }

  if (options.county) {
    filtered = filtered.filter(r => r.county === options.county);
  }

  if (options.year) {
    if (Array.isArray(options.year)) {
      filtered = filtered.filter(r => options.year!.includes(r.year));
    } else {
      filtered = filtered.filter(r => r.year === options.year);
    }
  }

  if (options.metrics && options.metrics.length > 0) {
    filtered = filtered.filter(r => options.metrics!.includes(r.metric));
  }

  if (options.loan_purpose) {
    filtered = filtered.filter(r => r.loan_purpose === options.loan_purpose);
  }

  if (options.kind) {
    filtered = filtered.filter(r => r.kind === options.kind);
  }

  return filtered;
}

/**
 * Get unique values for a field
 */
export function getUniqueValues(
  data: LendingRecord[],
  field: keyof LendingRecord
): string[] | number[] {
  const values = data.map(r => r[field]).filter(v => v !== null && v !== undefined);
  return Array.from(new Set(values)) as string[] | number[];
}

/**
 * Aggregate data by geographic level
 */
export function aggregateByGeography(
  data: LendingRecord[],
  level: 'state' | 'cbsa' | 'county'
): Record<string, LendingRecord[]> {
  const grouped: Record<string, LendingRecord[]> = {};

  data.forEach(record => {
    let key: string;
    if (level === 'state') {
      key = record.state;
    } else if (level === 'cbsa') {
      key = `${record.state}-${record.cbsa}`;
    } else {
      key = `${record.state}-${record.cbsa}-${record.county}`;
    }

    if (!grouped[key]) {
      grouped[key] = [];
    }
    grouped[key].push(record);
  });

  return grouped;
}

/**
 * Calculate summary statistics for a dataset
 */
export function calculateSummaryStats(data: LendingRecord[]) {
  const totalLoans = data.reduce((sum, r) => sum + r.bank_count, 0);
  const avgRatio = data
    .filter(r => r.ratio !== null && r.ratio !== undefined)
    .reduce((sum, r, _, arr) => sum + (r.ratio || 0) / arr.length, 0);
  const avgGap = data
    .filter(r => r.gap !== null && r.gap !== undefined)
    .reduce((sum, r, _, arr) => sum + (r.gap || 0) / arr.length, 0);
  const underperforming = data.filter(r => r.gap !== null && r.gap < -5).length;

  return {
    totalLoans,
    avgRatio,
    avgGap,
    underperformingAreas: underperforming,
    totalRecords: data.length
  };
}

