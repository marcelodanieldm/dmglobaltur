import React, { useState } from 'react';

const luxuryArchetypes = [
  'Old Money', 'New Rich', 'Digital Nomad', 'Family Luxury', 'Wellness', 'Adventure', 'Cultural', 'Eco-Luxury'
];

export default function Step1Destino({ onNext, formData }) {
  const [city, setCity] = useState(formData.city || '');
  const [archetypes, setArchetypes] = useState(formData.archetypes || []);

  const handleArchetypeChange = (archetype) => {
    setArchetypes(
      archetypes.includes(archetype)
        ? archetypes.filter(a => a !== archetype)
        : [...archetypes, archetype]
    );
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (city && archetypes.length) onNext({ city, archetypes });
  };

  return (
    <form className="step1-destino" onSubmit={handleSubmit}>
      <h2>¿A qué ciudad te enfocas?</h2>
      <input
        type="text"
        placeholder="Ciudad destino (autocompletar)"
        value={city}
        onChange={e => setCity(e.target.value)}
        required
        autoComplete="off"
        list="city-list"
      />
      <datalist id="city-list">
        {/* Ejemplo de ciudades, reemplazar por API real si se desea */}
        <option value="Shanghai" />
        <option value="Beijing" />
        <option value="Hong Kong" />
        <option value="Macau" />
        <option value="Shenzhen" />
      </datalist>
      <h3>Selecciona arquetipos de lujo</h3>
      <div className="archetype-list">
        {luxuryArchetypes.map(a => (
          <label key={a}>
            <input
              type="checkbox"
              checked={archetypes.includes(a)}
              onChange={() => handleArchetypeChange(a)}
            />
            {a}
          </label>
        ))}
      </div>
      <button type="submit" disabled={!city || !archetypes.length}>Siguiente</button>
    </form>
  );
}
