import React from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useLender } from '../context/LenderContext';
import { LendingRecord, filterData, getUniqueValues } from '../utils/dataProcessor';
import { RatioTable } from './RatioTable';
import { NCRC_COLORS } from '../utils/ncrcColors';

interface CBSAViewProps {
  data: LendingRecord[];
}

export const CBSAView: React.FC<CBSAViewProps> = ({ data }) => {
  const navigate = useNavigate();
  const { lender, state } = useParams<{ lender: string; state: string }>();
  const { lenderInfo } = useLender();

  // Filter data
  let filteredData = data;
  if (lender && lender !== 'both') {
    filteredData = filterData(data, { bank: lenderInfo[lender as 'frost' | 'webster'].name });
  }
  if (state) {
    filteredData = filterData(filteredData, { state });
  }

  // Get unique CBSAs
  const cbsas = getUniqueValues(filteredData, 'cbsa') as string[];

  const handleCBSAClick = (cbsa: string) => {
    if (lender && state) {
      navigate(`/county/${lender}/${state}/${encodeURIComponent(cbsa)}`);
    }
  };

  const handleRowClick = (record: LendingRecord) => {
    handleCBSAClick(record.cbsa);
  };

  return (
    <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '2rem' }}>
      <div style={{ marginBottom: '2rem' }}>
        <button
          onClick={() => navigate(`/state/${lender || 'both'}`)}
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
          ← Back to States
        </button>
        <h1 style={{ 
          fontSize: '2rem', 
          color: NCRC_COLORS.DARK_BLUE,
          marginBottom: '0.5rem'
        }}>
          {state} - CBSAs
        </h1>
        <p style={{ color: NCRC_COLORS.GRAY }}>
          Click on a CBSA or table row to view county-level details
        </p>
      </div>

      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))', 
        gap: '1rem',
        marginBottom: '2rem'
      }}>
        {cbsas.map(cbsa => {
          const cbsaData = filterData(filteredData, { cbsa });
          return (
            <div
              key={cbsa}
              onClick={() => handleCBSAClick(cbsa)}
              style={{
                background: 'white',
                border: `1px solid ${NCRC_COLORS.GRAY}`,
                borderRadius: '6px',
                padding: '1rem',
                cursor: 'pointer',
                transition: 'all 0.2s ease'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.borderColor = NCRC_COLORS.SKY_BLUE;
                e.currentTarget.style.backgroundColor = '#F9FAFB';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.borderColor = NCRC_COLORS.GRAY;
                e.currentTarget.style.backgroundColor = 'white';
              }}
            >
              <div style={{ fontWeight: 600, color: NCRC_COLORS.DARK_BLUE }}>
                {cbsa}
              </div>
              <div style={{ fontSize: '0.875rem', color: NCRC_COLORS.GRAY, marginTop: '0.25rem' }}>
                {cbsaData.length} records
              </div>
            </div>
          );
        })}
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
          Ratio Table (All CBSAs)
        </h2>
        <RatioTable data={filteredData} onRowClick={handleRowClick} />
      </div>
    </div>
  );
};

