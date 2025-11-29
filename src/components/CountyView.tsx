import React, { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useLender } from '../context/LenderContext';
import { LendingRecord, filterData } from '../utils/dataProcessor';
import { RatioTable } from './RatioTable';
import { NCRC_COLORS } from '../utils/ncrcColors';

interface CountyViewProps {
  data: LendingRecord[];
}

export const CountyView: React.FC<CountyViewProps> = ({ data }) => {
  const navigate = useNavigate();
  const { lender, state, cbsa } = useParams<{ lender: string; state: string; cbsa: string }>();
  const { lenderInfo } = useLender();
  const [selectedYear, setSelectedYear] = useState<number | 'all'>('all');

  // Filter data
  let filteredData = data;
  if (lender && lender !== 'both') {
    filteredData = filterData(data, { bank: lenderInfo[lender as 'frost' | 'webster'].name });
  }
  if (state) {
    filteredData = filterData(filteredData, { state });
  }
  if (cbsa) {
    filteredData = filterData(filteredData, { cbsa: decodeURIComponent(cbsa) });
  }
  if (selectedYear !== 'all') {
    filteredData = filterData(filteredData, { year: selectedYear });
  }

  return (
    <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '2rem' }}>
      <div style={{ marginBottom: '2rem' }}>
        <button
          onClick={() => navigate(`/cbsa/${lender || 'both'}/${state || ''}`)}
          style={{
            padding: '0.5rem 1rem',
            background: NCRC_COLORS.GRAY,
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            marginBottom: '1rem'
          }}
        >
          ← Back to CBSAs
        </button>
        <h1 style={{ 
          fontSize: '2rem', 
          color: NCRC_COLORS.DARK_BLUE,
          marginBottom: '0.5rem'
        }}>
          {decodeURIComponent(cbsa || '')} - Counties
        </h1>
      </div>

      {/* Year Filter */}
      <div style={{ 
        marginBottom: '1.5rem',
        display: 'flex',
        gap: '0.5rem',
        alignItems: 'center'
      }}>
        <span style={{ fontWeight: 600, color: NCRC_COLORS.DARK_BLUE }}>Year:</span>
        <button
          onClick={() => setSelectedYear('all')}
          style={{
            padding: '0.5rem 1rem',
            background: selectedYear === 'all' ? NCRC_COLORS.SKY_BLUE : 'white',
            color: selectedYear === 'all' ? 'white' : NCRC_COLORS.DARK_BLUE,
            border: `1px solid ${NCRC_COLORS.SKY_BLUE}`,
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          All Years
        </button>
        {[2022, 2023, 2024].map(year => (
          <button
            key={year}
            onClick={() => setSelectedYear(year)}
            style={{
              padding: '0.5rem 1rem',
              background: selectedYear === year ? NCRC_COLORS.SKY_BLUE : 'white',
              color: selectedYear === year ? 'white' : NCRC_COLORS.DARK_BLUE,
              border: `1px solid ${NCRC_COLORS.SKY_BLUE}`,
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            {year}
          </button>
        ))}
      </div>

      <div style={{ 
        background: 'white', 
        borderRadius: '8px', 
        padding: '1.5rem',
        boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)'
      }}>
        <h2 style={{ 
          fontSize: '1.5rem', 
          color: NCRC_COLORS.DARK_BLUE,
          marginTop: 0,
          marginBottom: '1rem'
        }}>
          County-Level Details
        </h2>
        <RatioTable data={filteredData} />
      </div>
    </div>
  );
};

