import React, { useState } from 'react';
import Step1Destino from './Step1Destino';
import Step2Inventario from './Step2Inventario';
import Step3Canales from './Step3Canales';
import OnboardingSuccess from './OnboardingSuccess';

const steps = [
  { label: 'Destino', component: Step1Destino },
  { label: 'Inventario', component: Step2Inventario },
  { label: 'Canales', component: Step3Canales },
];

export default function OnboardingWizard({ onFinish }) {
  const [step, setStep] = useState(0);
  const [formData, setFormData] = useState({});
  const [completed, setCompleted] = useState(false);

  const CurrentStep = steps[step].component;

  const handleNext = (data) => {
    setFormData({ ...formData, ...data });
    if (step < steps.length - 1) {
      setStep(step + 1);
    } else {
      setCompleted(true);
      onFinish && onFinish({ ...formData, ...data });
    }
  };

  const handleBack = () => {
    if (step > 0) setStep(step - 1);
  };

  if (completed) return <OnboardingSuccess />;

  return (
    <div className="onboarding-wizard">
      <div className="wizard-steps">
        {steps.map((s, i) => (
          <div key={s.label} className={`wizard-step${i === step ? ' active' : ''}`}>{s.label}</div>
        ))}
      </div>
      <div className="wizard-content">
        <CurrentStep onNext={handleNext} onBack={handleBack} formData={formData} />
      </div>
    </div>
  );
}
