import pandas as pd
from scarcity_opportunity_detector import detect_opportunities

# Simulación de inventario local y demanda China
local_inventory = pd.DataFrame({
    'sku': ['A1', 'A2', 'A3'],
    'stock': [10, 0, 5]
})
china_demand = pd.DataFrame({
    'sku': ['A1', 'A2', 'A3'],
    'demanda': [8, 20, 2]
})

result = detect_opportunities(local_inventory, china_demand)
print('Resultado de análisis de oportunidades:')
print(result)
