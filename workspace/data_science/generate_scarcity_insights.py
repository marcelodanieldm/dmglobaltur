"""
Script para cruzar market_trends y client_inventory y generar insights de Scarcity
- Si hashtag_or_keyword coincide con product_name y hay stock, crea un insight en client_insights
"""
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
supabase: Client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

# 1. Obtener tendencias de China
trends = supabase.table('market_trends').select('*').execute().data

# 2. Para cada usuario, cruzar con su inventario
users = supabase.table('users').select('id').execute().data
for user in users:
    user_id = user['id']
    inventory = supabase.table('client_inventory').select('*').eq('user_id', user_id).execute().data
    for trend in trends:
        for item in inventory:
            if trend['hashtag_or_keyword'].lower() in item['product_name'].lower() and item['current_stock'] > 0:
                # Generar insight
                insight = {
                    'user_id': user_id,
                    'service_type': 'Scarcity',
                    'insight_title': f"Oportunidad: {item['product_name']} en tendencia en China",
                    'insight_body': {
                        'trend': trend['hashtag_or_keyword'],
                        'stock': item['current_stock'],
                        'region': trend['target_region'],
                        'sentiment_score': trend['sentiment_score'],
                        'virality_velocity': trend['virality_velocity']
                    },
                    'opportunity_score': int(min(100, (trend['virality_velocity'] or 0) * 10)),
                    'is_critical': trend['sentiment_score'] > 0.7 and trend['virality_velocity'] > 1.0,
                    'was_opened': False
                }
                supabase.table('client_insights').insert(insight).execute()
                print(f"Insight generado para usuario {user_id}: {insight['insight_title']}")
