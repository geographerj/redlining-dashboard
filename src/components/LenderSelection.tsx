import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useLender, lenderInfo } from '../context/LenderContext';
import { NCRC_COLORS } from '../utils/ncrcColors';

export const LenderSelection: React.FC = () => {
  const navigate = useNavigate();
  const { setSelectedLender } = useLender();

  const handleLenderSelect = (lenderKey: 'frost' | 'webster') => {
    setSelectedLender(lenderKey);
    navigate(`/state/${lenderKey}`);
  };

  const handleCompareBoth = () => {
    setSelectedLender('both');
    navigate('/compare/both');
  };

  const frost = lenderInfo.frost;
  const webster = lenderInfo.webster;

  return (
    <div style={{ 
      maxWidth: '1200px', 
      margin: '0 auto', 
      padding: '2rem',
      fontFamily: 'Calibri, Arial, sans-serif'
    }}>
      <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
        <h1 style={{ 
          fontSize: '2.5rem', 
          color: NCRC_COLORS.DARK_BLUE, 
          marginBottom: '0.5rem' 
        }}>
          Redlining Analysis Dashboard
        </h1>
        <p style={{ fontSize: '1.2rem', color: NCRC_COLORS.GRAY }}>
          Select a lender to begin analysis
        </p>
      </div>

      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', 
        gap: '2rem',
        marginBottom: '3rem'
      }}>
        {/* Frost Bank Card */}
        <div 
          onClick={() => handleLenderSelect('frost')}
          style={{
            background: 'white',
            border: `2px solid ${NCRC_COLORS.GRAY}`,
            borderRadius: '12px',
            padding: '2rem',
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
          <div style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center',
            marginBottom: '1.5rem',
            paddingBottom: '1rem',
            borderBottom: `2px solid ${NCRC_COLORS.GRAY}`
          }}>
            <h2 style={{ fontSize: '1.8rem', color: NCRC_COLORS.DARK_BLUE, margin: 0 }}>
              {frost.name}
            </h2>
            <span style={{
              padding: '0.25rem 0.75rem',
              borderRadius: '20px',
              backgroundColor: NCRC_COLORS.SKY_BLUE,
              color: 'white',
              fontSize: '0.875rem',
              fontWeight: 600
            }}>
              TX
            </span>
          </div>
          
          <div style={{ marginBottom: '1.5rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.75rem 0', borderBottom: `1px solid #F3F4F6` }}>
              <span style={{ fontWeight: 500, color: NCRC_COLORS.GRAY }}>Headquarters:</span>
              <span style={{ fontWeight: 600, color: NCRC_COLORS.BLACK }}>{frost.headquarters}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.75rem 0', borderBottom: `1px solid #F3F4F6` }}>
              <span style={{ fontWeight: 500, color: NCRC_COLORS.GRAY }}>Assets:</span>
              <span style={{ fontWeight: 600, color: NCRC_COLORS.BLACK }}>{frost.assets}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.75rem 0', borderBottom: `1px solid #F3F4F6` }}>
              <span style={{ fontWeight: 500, color: NCRC_COLORS.GRAY }}>Branches:</span>
              <span style={{ fontWeight: 600, color: NCRC_COLORS.BLACK }}>{frost.branches}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.75rem 0', borderBottom: `1px solid #F3F4F6` }}>
              <span style={{ fontWeight: 500, color: NCRC_COLORS.GRAY }}>States:</span>
              <span style={{ fontWeight: 600, color: NCRC_COLORS.BLACK }}>{frost.states.join(', ')}</span>
            </div>
            <div style={{ 
              display: 'flex', 
              justifyContent: 'space-between', 
              padding: '1rem',
              borderRadius: '6px',
              marginTop: '0.5rem',
              backgroundColor: '#FEF3C7',
              borderBottom: 'none'
            }}>
              <span style={{ fontWeight: 500, color: NCRC_COLORS.GRAY }}>LEI:</span>
              <span style={{ fontWeight: 600, color: NCRC_COLORS.BLACK, fontFamily: 'monospace' }}>{frost.lei}</span>
            </div>
          </div>

          <button style={{
            width: '100%',
            padding: '1rem',
            background: NCRC_COLORS.SKY_BLUE,
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            fontSize: '1.1rem',
            fontWeight: 600,
            cursor: 'pointer',
            transition: 'background 0.2s'
          }}
          onMouseEnter={(e) => e.currentTarget.style.background = NCRC_COLORS.DARK_BLUE}
          onMouseLeave={(e) => e.currentTarget.style.background = NCRC_COLORS.SKY_BLUE}
          >
            Analyze {frost.name}
          </button>
        </div>

        {/* Webster Bank Card */}
        <div 
          onClick={() => handleLenderSelect('webster')}
          style={{
            background: 'white',
            border: `2px solid ${NCRC_COLORS.GRAY}`,
            borderRadius: '12px',
            padding: '2rem',
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
          <div style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center',
            marginBottom: '1.5rem',
            paddingBottom: '1rem',
            borderBottom: `2px solid ${NCRC_COLORS.GRAY}`
          }}>
            <h2 style={{ fontSize: '1.8rem', color: NCRC_COLORS.DARK_BLUE, margin: 0 }}>
              {webster.name}
            </h2>
            <span style={{
              padding: '0.25rem 0.75rem',
              borderRadius: '20px',
              backgroundColor: NCRC_COLORS.PURPLE,
              color: 'white',
              fontSize: '0.875rem',
              fontWeight: 600
            }}>
              Multi-State
            </span>
          </div>
          
          <div style={{ marginBottom: '1.5rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.75rem 0', borderBottom: `1px solid #F3F4F6` }}>
              <span style={{ fontWeight: 500, color: NCRC_COLORS.GRAY }}>Headquarters:</span>
              <span style={{ fontWeight: 600, color: NCRC_COLORS.BLACK }}>{webster.headquarters}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.75rem 0', borderBottom: `1px solid #F3F4F6` }}>
              <span style={{ fontWeight: 500, color: NCRC_COLORS.GRAY }}>Assets:</span>
              <span style={{ fontWeight: 600, color: NCRC_COLORS.BLACK }}>{webster.assets}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.75rem 0', borderBottom: `1px solid #F3F4F6` }}>
              <span style={{ fontWeight: 500, color: NCRC_COLORS.GRAY }}>Branches:</span>
              <span style={{ fontWeight: 600, color: NCRC_COLORS.BLACK }}>{webster.branches}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.75rem 0', borderBottom: `1px solid #F3F4F6` }}>
              <span style={{ fontWeight: 500, color: NCRC_COLORS.GRAY }}>States:</span>
              <span style={{ fontWeight: 600, color: NCRC_COLORS.BLACK }}>{webster.states.join(', ')}</span>
            </div>
            <div style={{ 
              display: 'flex', 
              justifyContent: 'space-between', 
              padding: '1rem',
              borderRadius: '6px',
              marginTop: '0.5rem',
              backgroundColor: '#FEF3C7',
              borderBottom: 'none'
            }}>
              <span style={{ fontWeight: 500, color: NCRC_COLORS.GRAY }}>LEI:</span>
              <span style={{ fontWeight: 600, color: NCRC_COLORS.BLACK, fontFamily: 'monospace' }}>{webster.lei}</span>
            </div>
          </div>

          <button style={{
            width: '100%',
            padding: '1rem',
            background: NCRC_COLORS.SKY_BLUE,
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            fontSize: '1.1rem',
            fontWeight: 600,
            cursor: 'pointer',
            transition: 'background 0.2s'
          }}
          onMouseEnter={(e) => e.currentTarget.style.background = NCRC_COLORS.DARK_BLUE}
          onMouseLeave={(e) => e.currentTarget.style.background = NCRC_COLORS.SKY_BLUE}
          >
            Analyze {webster.name}
          </button>
        </div>
      </div>

      {/* Compare Both Option */}
      <div style={{ 
        textAlign: 'center', 
        padding: '2rem',
        background: '#F9FAFB',
        borderRadius: '12px',
        border: `2px dashed ${NCRC_COLORS.GRAY}`
      }}>
        <button 
          onClick={handleCompareBoth}
          style={{
            padding: '1rem 2rem',
            background: 'white',
            border: `2px solid ${NCRC_COLORS.SKY_BLUE}`,
            borderRadius: '8px',
            fontSize: '1.1rem',
            fontWeight: 600,
            color: NCRC_COLORS.SKY_BLUE,
            cursor: 'pointer',
            transition: 'all 0.2s',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = NCRC_COLORS.SKY_BLUE;
            e.currentTarget.style.color = 'white';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = 'white';
            e.currentTarget.style.color = NCRC_COLORS.SKY_BLUE;
          }}
        >
          <span style={{ fontSize: '1.5rem' }}>⚖️</span>
          Compare Both Banks
        </button>
        <p style={{ marginTop: '0.5rem', color: NCRC_COLORS.GRAY, fontSize: '0.9rem' }}>
          View side-by-side comparison of both lenders across all states
        </p>
      </div>
    </div>
  );
};

