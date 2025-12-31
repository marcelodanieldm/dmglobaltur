# Watchdog de Anomalías - DM Global Tur

## ¿Qué hace este script?
- Monitorea ventas, pagos y consumo de IA en tiempo real.
- Detecta caídas de ventas, fallos de pasarela y anomalías en el costo de Gemini.
- Usa Gemini 1.5 Flash para diagnosticar y explicar anomalías.
- Envía alertas críticas a CEO y QA por Slack y/o email.

## Requisitos previos
- Python 3.9+
- Variables de entorno configuradas en un archivo `.env`:
  - SUPABASE_URL, SUPABASE_KEY
  - STRIPE_API_KEY
  - GEMINI_API_KEY
  - SLACK_WEBHOOK_URL (opcional)
  - RESEND_API_KEY (opcional, para email)
  - CEO_EMAILS (coma-separado)
  - QA_EMAIL (opcional)

## Instalación de dependencias

```bash
pip install supabase-py stripe google-generativeai python-dotenv requests
```

## Ejecución manual

```bash
python ceo_financial_dashboard/watchdog_anomalias.py
```

## Ejecución automática (recomendado)
- **Windows:** Usa el Programador de Tareas para ejecutar el script cada 10 minutos.
- **Linux:** Añade una entrada al crontab:

```
*/10 * * * * /usr/bin/python3 /ruta/absoluta/ceo_financial_dashboard/watchdog_anomalias.py
```

## Notas
- El script es asíncrono y no bloquea otros procesos.
- Las alertas se envían solo si se detecta una anomalía.
- Los diagnósticos de IA se generan solo cuando hay un evento crítico.

## Personalización
- Puedes ajustar los umbrales y la lógica de alerta en el archivo `watchdog_anomalias.py`.
- Para nuevos canales de alerta, añade la integración en la función `send_critical_alert()`.

---

**Soporte:** daniel@dmglobaltur.com
