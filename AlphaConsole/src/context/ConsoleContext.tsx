'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';

interface ConsoleContextType {
  demoMode: boolean;
  toggleDemoMode: () => void;
}

const ConsoleContext = createContext<ConsoleContextType | undefined>(undefined);

export const ConsoleProvider = ({ children }: { children: React.ReactNode }) => {
  const [demoMode, setDemoMode] = useState<boolean>(true); // Default to true as per spec

  useEffect(() => {
    const savedMode = localStorage.getItem('alpha_demo_mode');
    if (savedMode !== null) {
      setDemoMode(savedMode === 'true');
    }
  }, []);

  const toggleDemoMode = () => {
    const newMode = !demoMode;
    setDemoMode(newMode);
    localStorage.setItem('alpha_demo_mode', String(newMode));
  };

  return (
    <ConsoleContext.Provider value={{ demoMode, toggleDemoMode }}>
      {children}
    </ConsoleContext.Provider>
  );
};

export const useConsole = () => {
  const context = useContext(ConsoleContext);
  if (context === undefined) {
    throw new Error('useConsole must be used within a ConsoleProvider');
  }
  return context;
};
