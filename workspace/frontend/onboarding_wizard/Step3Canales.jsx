import React, { useState } from 'react';

export default function Step3Canales({ onNext, onBack, formData }) {
  const [channels, setChannels] = useState(formData.channels || { whatsapp: false, email: true });

  const handleChange = (e) => {
    setChannels({ ...channels, [e.target.name]: e.target.checked });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onNext({ channels });
  };

  return (
    <form className="step3-canales" onSubmit={handleSubmit}>
      <h2>¿Cómo quieres recibir notificaciones?</h2>
      <label>
        <input
          type="checkbox"
          name="whatsapp"
          checked={channels.whatsapp}
          onChange={handleChange}
        />
        WhatsApp
      </label>
      <label>
        <input
          type="checkbox"
          name="email"
          checked={channels.email}
          onChange={handleChange}
        />
        Email
      </label>
      <div className="wizard-nav">
        <button type="button" onClick={onBack}>Atrás</button>
        <button type="submit">Finalizar</button>
      </div>
    </form>
  );
}
