# Backend API & Middleware (Node.js)

- Middleware de permisos y suscripciones (Supabase, Redis, Stripe upgrade_url).
- Endpoints protegidos para insights y features premium.
- Integración lista para consumir desde el ServiceControlPanel frontend.

## Uso

1. Instala dependencias:
   ```bash
   npm install express cors @supabase/supabase-js ioredis
   ```
2. Configura variables de entorno:
   - SUPABASE_URL, SUPABASE_KEY
   - REDIS_URL
   - STRIPE_UPGRADE_URL
3. Ejecuta el servidor:
   ```bash
   node server.js
   ```
4. El frontend debe enviar el header `x-user-id` en cada request.
