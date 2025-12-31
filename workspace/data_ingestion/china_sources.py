# XHS_Scraper mock implementation
import random
import time
class XHS_Scraper:
    def fetch(self, *args, **kwargs):
        # Simula un 40% de fallo por bloqueo
        if random.random() < 0.4:
            raise Exception("Blocked by XHS")
        return {"source": "XHS_Scraper", "data": "Datos de Xiaohongshu"}

# Ctrip_API mock implementation
class Ctrip_API:
    def fetch(self, *args, **kwargs):
        # Simula un 10% de fallo
        if random.random() < 0.1:
            raise Exception("Ctrip API error")
        return {"source": "Ctrip_API", "data": "Datos de Ctrip"}

# Baidu_Mirror mock implementation
class Baidu_Mirror:
    def fetch(self, *args, **kwargs):
        # Simula un 5% de fallo
        if random.random() < 0.05:
            raise Exception("Baidu Mirror error")
        return {"source": "Baidu_Mirror", "data": "Datos de Baidu"}
