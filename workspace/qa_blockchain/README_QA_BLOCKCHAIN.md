
# QA Automation for Blockchain Layer (EN/ES/EO)

---

## English

### Purpose
Automated security audit and transaction stress testing for the DMTrust.soroban smart contract. Ensures zero-failure in commission distributions and protects user funds.

### Test Coverage
- **Functional Test:** Simulates sales and verifies that the contract distributes the exact percentage to each wallet.
- **Boundary Testing:** Validates contract behavior for very small (0.01 USD) and very large (1,000,000 USD) sales, including gas and overflow protections.
- **Recovery Test:** Simulates node failure during payout and verifies system recovery.
- **Integration Test:** Asserts that the CEO Dashboard reflects blockchain balance within <5s after contract event.

### Usage
1. Install dependencies: `npm install` (for JS tests), `pip install -r requirements.txt` (for Python integration test)
2. Run tests: `npx hardhat test` or `pytest test/integration_ceo_dashboard_sync.py`

---

## Español

### Propósito
Auditoría de seguridad automatizada y pruebas de estrés transaccional para el contrato inteligente DMTrust.soroban. Garantiza cero fallos en la distribución de comisiones y protege los fondos de los usuarios.

### Cobertura de Pruebas
- **Prueba Funcional:** Simula ventas y verifica que el contrato distribuye el porcentaje exacto a cada cartera.
- **Pruebas de Límite:** Valida el comportamiento del contrato para ventas muy pequeñas (0.01 USD) y muy grandes (1,000,000 USD), incluyendo protección de gas y desbordamientos.
- **Prueba de Recuperación:** Simula la caída de un nodo durante el pago y verifica la recuperación del sistema.
- **Prueba de Integración:** Verifica que el CEO Dashboard refleje el saldo blockchain en menos de 5 segundos tras el evento del contrato.

### Uso
1. Instala dependencias: `npm install` (para pruebas JS), `pip install -r requirements.txt` (para la prueba de integración en Python)
2. Ejecuta pruebas: `npx hardhat test` o `pytest test/integration_ceo_dashboard_sync.py`

---

## Esperanto

### Celo
Aŭtomata sekureca aŭdito kaj transakcia streĉtestado por la inteligenta kontrakto DMTrust.soroban. Certigas nulajn fiaskojn en komisionaj distribuoj kaj protektas uzantajn financojn.

### Testa Kovrado
- **Funkcia Testo:** Simulas vendojn kaj kontrolas, ke la kontrakto distribuas la ĝustan procenton al ĉiu monujo.
- **Lima Testado:** Validigas la konduton de la kontrakto por tre malgrandaj (0.01 USD) kaj tre grandaj (1,000,000 USD) vendoj, inkluzive de gaso kaj troflua protekto.
- **Reakira Testo:** Simulas nodan fiaskon dum pago kaj kontrolas la reakiradon de la sistemo.
- **Integra Testo:** Asercias, ke la CEO Dashboard reflektas la blokĉenan saldon ene de malpli ol 5 sekundoj post kontrakta evento.

### Uzado
1. Instalu dependecojn: `npm install` (por JS-testoj), `pip install -r requirements.txt` (por la integra testo en Python)
2. Lanĉu testojn: `npx hardhat test` aŭ `pytest test/integration_ceo_dashboard_sync.py`
