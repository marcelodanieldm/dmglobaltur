# ServiceControlPanel (Next.js/React)

- Dashboard con Action Cards para Vibe-Matching, Scarcity y Reputation Risk.
- Drawer lateral con detalles técnicos.
- Estados visuales: Loading, Active, Alert (según Sentiment Score).
- Mobile-First, colores: fondo #1A1A1A, acentos #D4AF37.
- Consume insights desde `/api/v1/forecast/insights` (protegido por middleware de permisos).

## Uso

1. Instala dependencias y ejecuta el backend (Express):
   ```bash
   cd ../../backend
   npm install
   node server.js
   ```
2. Integra el componente en tu app Next.js o React:
   ```jsx
   import ServiceControlPanel from './ServiceControlPanel';
   <ServiceControlPanel />
   ```
3. Asegúrate de enviar el header `x-user-id` en las peticiones para simular el usuario.
