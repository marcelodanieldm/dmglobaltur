import React, { useState } from 'react';

export default function Step2Inventario({ onNext, onBack, formData }) {
  const [file, setFile] = useState(null);
  const [filename, setFilename] = useState(formData.inventoryFileName || '');

  const handleFileChange = (e) => {
    const f = e.target.files[0];
    setFile(f);
    setFilename(f ? f.name : '');
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (file) {
      // Aquí se podría subir el archivo a backend
      onNext({ inventoryFile: file, inventoryFileName: filename });
    }
  };

  return (
    <form className="step2-inventario" onSubmit={handleSubmit}>
      <h2>Sube tu inventario</h2>
      <div className="dropzone">
        <input type="file" accept=".csv" onChange={handleFileChange} />
        {filename && <div className="filename">{filename}</div>}
      </div>
      <div className="coming-soon">
        <h4>Integraciones directas (próximamente):</h4>
        <ul>
          <li>Shopify</li>
          <li>Opera PMS</li>
          <li>Cloudbeds</li>
          <li>Prestashop</li>
        </ul>
      </div>
      <div className="wizard-nav">
        <button type="button" onClick={onBack}>Atrás</button>
        <button type="submit" disabled={!file}>Siguiente</button>
      </div>
    </form>
  );
}
