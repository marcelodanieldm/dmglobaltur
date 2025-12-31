import { useCallback } from 'react';
import OnboardingWizard from './OnboardingWizard';

export default function OnboardingWizardContainer({ userId }) {
  // Simula el endpoint backend para análisis Gemini
  const handleFinish = useCallback(async (formData) => {
    const data = new FormData();
    data.append('city', formData.city);
    data.append('archetypes', JSON.stringify(formData.archetypes));
    data.append('channels', JSON.stringify(formData.channels));
    data.append('user_id', userId);
    if (formData.inventoryFile) {
      data.append('inventory', formData.inventoryFile);
    }
    await fetch('/api/onboarding/analyze', {
      method: 'POST',
      body: data,
    });
  }, [userId]);

  return <OnboardingWizard onFinish={handleFinish} />;
}
