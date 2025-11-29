import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useLender } from '../context/LenderContext';
import { LendingRecord, filterData, getUniqueValues, calculateSummaryStats } from '../utils/dataProcessor';
import { NCRC_COLORS } from '../utils/ncrcColors';

interface StateViewProps {
  data: LendingRecord[];
}

export const StateView: React.FC<StateViewProps> = ({ data }) => {
  const navigate = useNavigate();
  const { selectedLender, lenderInfo } = useLender();

  // Filter data by selected lender
  const filteredData = selectedLender && selectedLender !== 'both'
    ? filterData(data, { bank: lenderInfo[selectedLender].name })
    : data;

  // Get unique states
  const states = getUniqueValues(filteredData, 'state') as string[];

  const handleStateClick = (state: string) => {
    if (selectedLender) {
      navigate(`/cbsa/${selectedLender}/${state}`);
    }
  };

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '2rem' }}>
      <div style={{ marginBottom: '2rem' }}>
        <h1 style={{ 
          fontSize: '2rem', 
          color: NCRC_COLORS.DARK_BLUE,
          marginBottom: '0.5rem'
        }}>
          {selectedLender && selectedLender !== 'both' 
            ? `${lenderInfo[selectedLender].name} - States` 
            : 'All States'}
        </h1>
        <p style={{ color: NCRC_COLORS.GRAY }}>
          Select a state to view CBSA-level analysis
        </p>
      </div>

      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', 
        gap: '1.5rem' 
      }}>
        {states.map(state => {
          const stateData = filterData(filteredData, { state });
          const stats = calculateSummaryStats(stateData);

          return (
            <div
              key={state}
              onClick={() => handleStateClick(state)}
              style={{
                background: 'white',
                border: `2px solid ${NCRC_COLORS.GRAY}`,
                borderRadius: '8px',
                padding: '1.5rem',
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.borderColor = NCRC_COLORS.SKY_BLUE;
                e.currentTarget.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
                e.currentTarget.style.transform = 'translateY(-2px)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.borderColor = NCRC_COLORS.GRAY;
                e.currentTarget.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.1)';
                e.currentTarget.style.transform = 'translateY(0)';
              }}
            >
              <h2 style={{ 
                fontSize: '1.5rem', 
                color: NCRC_COLORS.DARK_BLUE,
                marginTop: 0,
                marginBottom: '1rem'
              }}>
                {state}
              </h2>
              
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: NCRC_COLORS.GRAY }}>Total Loans (2024):</span>
                  <span style={{ fontWeight: 600 }}>{stats.totalLoans.toLocaleString()}</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: NCRC_COLORS.GRAY }}>Avg Ratio:</span>
                  <span style={{ fontWeight: 600 }}>
                    {stats.avgRatio > 0 ? stats.avgRatio.toFixed(2) : 'N/A'}
                  </span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: NCRC_COLORS.GRAY }}>Underperforming Areas:</span>
                  <span style={{ 
                    fontWeight: 600,
                    color: stats.underperformingAreas > 0 ? NCRC_COLORS.RED : NCRC_COLORS.GRAY
                  }}>
                    {stats.underperformingAreas}
                  </span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: NCRC_COLORS.GRAY }}>CBSAs:</span>
                  <span style={{ fontWeight: 600 }}>
                    {getUniqueValues(stateData, 'cbsa').length}
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

