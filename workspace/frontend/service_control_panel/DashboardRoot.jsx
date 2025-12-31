import React, { useEffect, useState } from 'react';
import OnboardingWizardContainer from '../onboarding_wizard/OnboardingWizardContainer';
import ServiceControlPanel from './ServiceControlPanel';

export default function DashboardRoot() {
  const [showOnboarding, setShowOnboarding] = useState(false);
  useEffect(() => {
    // Lógica: mostrar onboarding si el usuario es nuevo o no tiene inventario cargado
    // Aquí se simula con localStorage, reemplazar por lógica real si se desea
    const onboardingDone = window.localStorage.getItem('onboarding_done');
    setShowOnboarding(!onboardingDone);
  }, []);

  const handleOnboardingFinish = () => {
    window.localStorage.setItem('onboarding_done', '1');
    setShowOnboarding(false);
  };

  return (
    <div>
      {showOnboarding ? (
        <OnboardingWizardContainer userId={window.localStorage.getItem('user_id') || ''} onFinish={handleOnboardingFinish} />
      ) : (
        <ServiceControlPanel />
      )}
    </div>
  );
}
