import React, { createContext, useContext, useState, ReactNode } from 'react';

export type Lender = 'frost' | 'webster' | 'both' | null;

interface LenderContextType {
  selectedLender: Lender;
  setSelectedLender: (lender: Lender) => void;
  lenderInfo: {
    frost: { name: string; lei: string; headquarters: string; assets: string; branches: number; states: string[] };
    webster: { name: string; lei: string; headquarters: string; assets: string; branches: number; states: string[] };
  };
}

const LenderContext = createContext<LenderContextType | undefined>(undefined);

export const lenderInfo = {
  frost: {
    name: 'Frost Bank',
    lei: 'G5AHTAP80NWA3Q8RDC78',
    headquarters: 'San Antonio, TX',
    assets: '$51.5 billion',
    branches: 214,
    states: ['TX']
  },
  webster: {
    name: 'Webster Bank',
    lei: 'WV0OVGBTLUP1XIUJE722',
    headquarters: 'Stamford, CT',
    assets: '$81.8 billion',
    branches: 196,
    states: ['CT', 'MA', 'NY', 'RI']
  }
};

export function LenderProvider({ children }: { children: ReactNode }) {
  const [selectedLender, setSelectedLender] = useState<Lender>(null);

  return (
    <LenderContext.Provider value={{ selectedLender, setSelectedLender, lenderInfo }}>
      {children}
    </LenderContext.Provider>
  );
}

export function useLender() {
  const context = useContext(LenderContext);
  if (context === undefined) {
    throw new Error('useLender must be used within a LenderProvider');
  }
  return context;
}

