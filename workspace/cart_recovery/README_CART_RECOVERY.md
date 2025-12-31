# Abandoned Cart Recovery Flow

---

## English

### Purpose
Recovers up to 20% of lost sales by detecting abandoned checkouts, sending reminders, and offering incentives. Reports recovered revenue to CEO Dashboard.

### Business Logic
1. Event: User reaches checkout, but no 'success' event in 30 minutes.
2. Action 1 (Email): Send a friendly reminder. If user is from China (by IP), subject is: "Su acceso a los datos de lujo de Madrid está esperando (Alipay disponible)".
3. Action 2 (Incentive): If unpaid after 24h, generate a unique 10% off coupon for the first month using Stripe Coupons API.
4. Tracking: Report to CEO Dashboard how much revenue was recovered by this flow.

---

## Español

### Propósito
Recupera hasta el 20% de ventas perdidas detectando carritos abandonados, enviando recordatorios y ofreciendo incentivos. Reporta ingresos recuperados al CEO Dashboard.

### Lógica de Negocio
1. Evento: El usuario llega al checkout, pero no hay evento de 'success' en 30 minutos.
2. Acción 1 (Email): Enviar recordatorio amable. Si el usuario es de China (por IP), el asunto es: "Su acceso a los datos de lujo de Madrid está esperando (Alipay disponible)".
3. Acción 2 (Incentivo): Si no paga en 24h, generar cupón único del 10% de descuento solo para el primer mes usando la API de Stripe Coupons.
4. Tracking: Reportar al CEO Dashboard cuántos ingresos fueron recuperados por este flujo.

---

## Esperanto

### Celo
Rekuperas ĝis 20% de perditaj vendoj detektante forlasitajn ĉaretojn, sendante rememorigojn kaj ofertante instigojn. Raportas rekuperitajn enspezojn al CEO Dashboard.

### Komerca Logiko
1. Evento: Uzanto atingas la pagon, sed neniu 'success' evento en 30 minutoj.
2. Ago 1 (Retpoŝto): Sendu afablan rememorigon. Se la uzanto estas el Ĉinio (laŭ IP), la temo estas: "Su acceso a los datos de lujo de Madrid está esperando (Alipay disponible)".
3. Ago 2 (Instigo): Se ne pagite post 24h, generu unikan 10%-rabatan kuponon nur por la unua monato per Stripe Coupons API.
4. Spurado: Raportu al CEO Dashboard kiom da enspezoj estis rekuperitaj per ĉi tiu fluo.
