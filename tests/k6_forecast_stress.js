// K6 Stress Test for /forecast API
// ENGLISH / ESPAÑOL / ESPERANTO
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '30s', target: 500 }, // Ramp up to 500 users
    { duration: '1m', target: 500 },   // Stay at 500 users
    { duration: '30s', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<800'], // 95% of requests < 800ms
  },
  ext: {
    loadimpact: {
      distribution: {
        'asia': { loadZone: 'amazon:ap-southeast-1', percent: 40 },
        'us': { loadZone: 'amazon:us-east-1', percent: 30 },
        'eu': { loadZone: 'amazon:eu-west-1', percent: 30 },
      }
    }
  }
};

export default function () {
  let res = http.get('https://api.dmglobaltur.com/api/v1/forecast/itinerary?region=Sevilla&category=Luxury');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'body is not empty': (r) => r.body.length > 0,
  });
  sleep(1);
}
