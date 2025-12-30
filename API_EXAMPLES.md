# API Usage Examples / Ejemplos de Uso de la API / API-Uzaj Ekzemploj

---

## ENGLISH

### Ingest Data (POST)
```
curl -X POST "http://localhost:8000/api/v1/ingest/xiaohongshu" \
     -H "Content-Type: application/json" \
     -d @xiaohongshu_trends.json
```

### Get Latest Trends (GET, API Key required)
```
curl -X GET "http://localhost:8000/api/v1/trends/xiaohongshu" \
     -H "X-API-Key: changeme"
```

---

## ESPAÑOL

### Ingestar datos (POST)
```
curl -X POST "http://localhost:8000/api/v1/ingest/xiaohongshu" \
     -H "Content-Type: application/json" \
     -d @xiaohongshu_trends.json
```

### Consultar tendencias (GET, requiere API Key)
```
curl -X GET "http://localhost:8000/api/v1/trends/xiaohongshu" \
     -H "X-API-Key: changeme"
```

---

## ESPERANTO

### Enigi datumojn (POST)
```
curl -X POST "http://localhost:8000/api/v1/ingest/xiaohongshu" \
     -H "Content-Type: application/json" \
     -d @xiaohongshu_trends.json
```

### Ricevi tendencojn (GET, postulas API-ŝlosilon)
```
curl -X GET "http://localhost:8000/api/v1/trends/xiaohongshu" \
     -H "X-API-Key: changeme"
```
