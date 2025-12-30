// DM Global Tur Dashboard JS
// ENGLISH / ESPAÑOL / ESPERANTO

// EN: Fetches Xiaohongshu trends from the backend API and renders them as cards.
// ES: Obtiene tendencias de Xiaohongshu desde la API backend y las muestra como tarjetas.
// EO: Ricevas tendencojn de Xiaohongshu el la backend-API kaj montras ilin kiel kartojn.

document.addEventListener('DOMContentLoaded', async () => {
  const container = document.getElementById('trends-container');
  container.innerHTML = '<p><!-- EN -->Loading... <!-- ES -->Cargando... <!-- EO -->Ŝargante...</p>';
  try {
    // EN: Replace with your deployed backend URL if needed
    // ES: Cambia por la URL de tu backend desplegado si es necesario
    // EO: Anstataŭigu per via backend-URL se necese
    const API_URL = 'http://localhost:8000/api/v1/trends/xiaohongshu';
    const API_KEY = 'changeme'; // EN: Set your API key here
    const resp = await fetch(API_URL, {
      headers: { 'X-API-Key': API_KEY }
    });
    if (!resp.ok) throw new Error('API error: ' + resp.status);
    const data = await resp.json();
    if (!Array.isArray(data) || data.length === 0) {
      container.innerHTML = '<p><!-- EN -->No trends found. <!-- ES -->No se encontraron tendencias. <!-- EO -->Neniu tendenco trovita.</p>';
      return;
    }
    container.innerHTML = '';
    data.forEach(trend => {
      const card = document.createElement('div');
      card.className = 'trend-card';
      card.innerHTML = `
        <h4>${trend.hashtag}</h4>
        <div class="count">
          <!-- EN -->Posts: <!-- ES -->Posts: <!-- EO -->Afiŝoj: ${trend.post_count}
        </div>
        <div class="sentiment">
          <!-- EN -->Avg. Sentiment: <!-- ES -->Sentimiento Promedio: <!-- EO -->Meza Sentimento: ${trend.avg_sentiment}
        </div>
        <ul>
          ${trend.sample_posts.map(url => `<li><a href="${url}" target="_blank">${url}</a></li>`).join('')}
        </ul>
      `;
      container.appendChild(card);
    });
  } catch (err) {
    container.innerHTML = `<p style="color:red;">${err.message}</p>`;
  }
});
