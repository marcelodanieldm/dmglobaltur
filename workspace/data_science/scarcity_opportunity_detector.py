"""
Modelo de Detección de Brechas de Stock (Scarcity)
- Cruza inventario local (CSV/API) y demanda en China (Baidu/Tmall)
- Calcula OpportunityIndex y alerta si > 0.8
- Optimizado para 10,000 SKUs en <5s
"""
import pandas as pd
import numpy as np
import requests
import time

FACTOR_DIVISA = 1.0  # Ajustar según tipo de cambio

# Simulación: carga inventario local
local_inventory = pd.read_csv('local_inventory.csv')  # columnas: sku, stock
# Simulación: carga demanda China
china_demand = pd.read_csv('china_demand.csv')  # columnas: sku, demanda

def detect_opportunities(local_inventory, china_demand, factor_divisa=FACTOR_DIVISA):
    merged = pd.merge(local_inventory, china_demand, on='sku', how='inner')
    merged['OpportunityIndex'] = (merged['demanda'] / merged['stock'].replace(0, np.nan)) * factor_divisa
    merged['OpportunityIndex'] = merged['OpportunityIndex'].replace([np.inf, -np.inf], np.nan).fillna(0)
    alerts = merged[merged['OpportunityIndex'] > 0.8]
    # Aquí se dispararía la alerta al microservicio
    for _, row in alerts.iterrows():
        print(f"ALERTA SKU {row['sku']}: OpportunityIndex={row['OpportunityIndex']:.2f}")
    return merged

if __name__ == '__main__':
    t0 = time.time()
    result = detect_opportunities(local_inventory, china_demand)
    print(result.head())
    print(f"Tiempo total: {time.time()-t0:.2f}s")
