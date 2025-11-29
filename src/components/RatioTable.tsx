import React, { useState, useMemo } from 'react';
import { LendingRecord } from '../utils/dataProcessor';
import { getRatioColor, getGapColor, getTextColor, NCRC_COLORS } from '../utils/ncrcColors';

interface RatioTableProps {
  data: LendingRecord[];
  onRowClick?: (record: LendingRecord) => void;
}

type SortField = 'county' | 'metric' | 'year' | 'ratio' | 'gap' | 'bank_share' | 'peer_share';
type SortDirection = 'asc' | 'desc';

export const RatioTable: React.FC<RatioTableProps> = ({ data, onRowClick }) => {
  const [sortField, setSortField] = useState<SortField>('county');
  const [sortDirection, setSortDirection] = useState<SortDirection>('asc');

  const sortedData = useMemo(() => {
    const sorted = [...data].sort((a, b) => {
      let aVal: any = a[sortField as keyof LendingRecord];
      let bVal: any = b[sortField as keyof LendingRecord];

      // Handle null/undefined values
      if (aVal === null || aVal === undefined) aVal = sortDirection === 'asc' ? Infinity : -Infinity;
      if (bVal === null || bVal === undefined) bVal = sortDirection === 'asc' ? Infinity : -Infinity;

      // String comparison
      if (typeof aVal === 'string' && typeof bVal === 'string') {
        return sortDirection === 'asc' 
          ? aVal.localeCompare(bVal)
          : bVal.localeCompare(aVal);
      }

      // Numeric comparison
      const comparison = (aVal as number) - (bVal as number);
      return sortDirection === 'asc' ? comparison : -comparison;
    });

    return sorted;
  }, [data, sortField, sortDirection]);

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('asc');
    }
  };

  const SortIcon: React.FC<{ field: SortField }> = ({ field }) => {
    if (sortField !== field) return <span>↕️</span>;
    return <span>{sortDirection === 'asc' ? '↑' : '↓'}</span>;
  };

  if (data.length === 0) {
    return (
      <div style={{ padding: '2rem', textAlign: 'center', color: NCRC_COLORS.GRAY }}>
        No data available for the selected filters.
      </div>
    );
  }

  return (
    <div style={{ overflowX: 'auto' }}>
      <table style={{
        width: '100%',
        borderCollapse: 'collapse',
        fontFamily: 'Calibri, Arial, sans-serif',
        fontSize: '0.9rem'
      }}>
        <thead>
          <tr style={{ backgroundColor: NCRC_COLORS.GRAY }}>
            <th 
              onClick={() => handleSort('county')}
              style={{
                padding: '0.75rem',
                textAlign: 'left',
                fontWeight: 600,
                color: 'white',
                cursor: 'pointer',
                userSelect: 'none',
                border: `1px solid ${NCRC_COLORS.DARK_BLUE}`
              }}
            >
              County <SortIcon field="county" />
            </th>
            <th 
              onClick={() => handleSort('state')}
              style={{
                padding: '0.75rem',
                textAlign: 'left',
                fontWeight: 600,
                color: 'white',
                cursor: 'pointer',
                userSelect: 'none',
                border: `1px solid ${NCRC_COLORS.DARK_BLUE}`
              }}
            >
              State
            </th>
            <th 
              onClick={() => handleSort('metric')}
              style={{
                padding: '0.75rem',
                textAlign: 'left',
                fontWeight: 600,
                color: 'white',
                cursor: 'pointer',
                userSelect: 'none',
                border: `1px solid ${NCRC_COLORS.DARK_BLUE}`
              }}
            >
              Metric <SortIcon field="metric" />
            </th>
            <th 
              onClick={() => handleSort('year')}
              style={{
                padding: '0.75rem',
                textAlign: 'center',
                fontWeight: 600,
                color: 'white',
                cursor: 'pointer',
                userSelect: 'none',
                border: `1px solid ${NCRC_COLORS.DARK_BLUE}`
              }}
            >
              Year <SortIcon field="year" />
            </th>
            <th 
              onClick={() => handleSort('ratio')}
              style={{
                padding: '0.75rem',
                textAlign: 'center',
                fontWeight: 600,
                color: 'white',
                cursor: 'pointer',
                userSelect: 'none',
                border: `1px solid ${NCRC_COLORS.DARK_BLUE}`
              }}
            >
              Ratio (Peer/Bank) <SortIcon field="ratio" />
            </th>
            <th 
              onClick={() => handleSort('bank_share')}
              style={{
                padding: '0.75rem',
                textAlign: 'center',
                fontWeight: 600,
                color: 'white',
                cursor: 'pointer',
                userSelect: 'none',
                border: `1px solid ${NCRC_COLORS.DARK_BLUE}`
              }}
            >
              Bank % <SortIcon field="bank_share" />
            </th>
            <th 
              onClick={() => handleSort('peer_share')}
              style={{
                padding: '0.75rem',
                textAlign: 'center',
                fontWeight: 600,
                color: 'white',
                cursor: 'pointer',
                userSelect: 'none',
                border: `1px solid ${NCRC_COLORS.DARK_BLUE}`
              }}
            >
              Peer % <SortIcon field="peer_share" />
            </th>
            <th 
              onClick={() => handleSort('gap')}
              style={{
                padding: '0.75rem',
                textAlign: 'center',
                fontWeight: 600,
                color: 'white',
                cursor: 'pointer',
                userSelect: 'none',
                border: `1px solid ${NCRC_COLORS.DARK_BLUE}`
              }}
            >
              Gap (pp) <SortIcon field="gap" />
            </th>
            <th style={{
              padding: '0.75rem',
              textAlign: 'center',
              fontWeight: 600,
              color: 'white',
              border: `1px solid ${NCRC_COLORS.DARK_BLUE}`
            }}>
              Loans
            </th>
          </tr>
        </thead>
        <tbody>
          {sortedData.map((record, idx) => {
            const ratioColor = getRatioColor(record.ratio);
            const gapColor = getRatioColor(record.gap);
            const ratioTextColor = getTextColor(ratioColor);
            const gapTextColor = getTextColor(gapColor);

            return (
              <tr
                key={idx}
                onClick={() => onRowClick?.(record)}
                style={{
                  cursor: onRowClick ? 'pointer' : 'default',
                  borderBottom: `1px solid ${NCRC_COLORS.GRAY}`,
                  transition: 'background 0.2s'
                }}
                onMouseEnter={(e) => {
                  if (onRowClick) e.currentTarget.style.backgroundColor = '#F9FAFB';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.backgroundColor = 'white';
                }}
              >
                <td style={{ padding: '0.75rem' }}>{record.county}</td>
                <td style={{ padding: '0.75rem' }}>{record.state}</td>
                <td style={{ padding: '0.75rem' }}>{record.metric}</td>
                <td style={{ padding: '0.75rem', textAlign: 'center' }}>{record.year}</td>
                <td style={{
                  padding: '0.75rem',
                  textAlign: 'center',
                  backgroundColor: ratioColor,
                  color: ratioTextColor,
                  fontWeight: 600
                }}>
                  {record.ratio !== null && record.ratio !== undefined 
                    ? record.ratio.toFixed(2) 
                    : 'N/A'}
                </td>
                <td style={{ padding: '0.75rem', textAlign: 'center' }}>
                  {record.bank_share !== null && record.bank_share !== undefined
                    ? `${record.bank_share.toFixed(1)}%`
                    : 'N/A'}
                </td>
                <td style={{ padding: '0.75rem', textAlign: 'center' }}>
                  {record.peer_share !== null && record.peer_share !== undefined
                    ? `${record.peer_share.toFixed(1)}%`
                    : 'N/A'}
                </td>
                <td style={{
                  padding: '0.75rem',
                  textAlign: 'center',
                  backgroundColor: gapColor,
                  color: gapTextColor,
                  fontWeight: 600
                }}>
                  {record.gap !== null && record.gap !== undefined
                    ? `${record.gap > 0 ? '+' : ''}${record.gap.toFixed(1)}pp`
                    : 'N/A'}
                </td>
                <td style={{ padding: '0.75rem', textAlign: 'center' }}>
                  {record.bank_count.toLocaleString()}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

