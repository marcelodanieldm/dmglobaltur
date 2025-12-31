# Zero-Knowledge Proof (ZKP) & Tourist Data Encryption Integration

---

## English

### Purpose
This document describes the integration plan for Zero-Knowledge Proofs (ZKP) and encryption of tourist data in the DM Global Tur backend and smart contract layer, to fully comply with Sprint 6 business rules.

### Implementation Plan
- **Tourist Data Encryption:**
  - All personally identifiable tourist data is encrypted at rest and in transit using AES-256 or similar.
  - Only authorized parties (store, tourist, DM Global Tur) can decrypt with their private keys.
- **Zero-Knowledge Proofs (ZKP):**
  - When a sale is validated, the contract emits a ZKP attesting that the sale is real and the commission is correct, without revealing tourist identity.
  - DMCs and auditors can verify the ZKP on-chain or via API.
- **Smart Contract:**
  - Add a function to accept and store ZKP hashes for each sale.
  - Add a public view to verify ZKP validity for any transaction.

### Next Steps
1. Update backend API to encrypt tourist data before storing or sending to blockchain.
2. Integrate a ZKP library (e.g., snarkjs, circom, or zk-SNARKs for Soroban if available).
3. Update smart contract to store and verify ZKP hashes.
4. Document endpoints and contract methods for external verification.

---

## Español

### Propósito
Este documento describe el plan de integración de Zero-Knowledge Proofs (ZKP) y cifrado de datos de turistas en el backend y contrato inteligente de DM Global Tur, para cumplir totalmente con las reglas de negocio del Sprint 6.

### Plan de Implementación
- **Cifrado de Datos de Turistas:**
  - Todos los datos personales de turistas se cifran en reposo y en tránsito (AES-256 o similar).
  - Solo las partes autorizadas (tienda, turista, DM Global Tur) pueden descifrar con sus claves privadas.
- **Zero-Knowledge Proofs (ZKP):**
  - Al validar una venta, el contrato emite una ZKP que certifica la venta y la comisión, sin revelar la identidad del turista.
  - DMCs y auditores pueden verificar la ZKP en la blockchain o vía API.
- **Contrato Inteligente:**
  - Añadir función para aceptar y almacenar hashes de ZKP por venta.
  - Añadir vista pública para verificar la validez de la ZKP de cualquier transacción.

### Próximos Pasos
1. Actualizar el backend para cifrar datos de turistas antes de almacenarlos o enviarlos a blockchain.
2. Integrar una librería de ZKP (snarkjs, circom, o zk-SNARKs para Soroban si está disponible).
3. Actualizar el contrato inteligente para almacenar y verificar hashes de ZKP.
4. Documentar endpoints y métodos de contrato para verificación externa.

---

## Esperanto

### Celo
Ĉi tiu dokumento priskribas la integriĝan planon por Zero-Knowledge Proofs (ZKP) kaj ĉifrado de turistaj datumoj en la backend kaj inteligenta kontrakto de DM Global Tur, por plene plenumi la Sprint 6 regulojn.

### Plenuma Plano
- **Ĉifrado de Turistaj Datumoj:**
  - Ĉiuj persone identigeblaj turistaj datumoj estas ĉifritaj ĉe ripozo kaj dum transdono (AES-256 aŭ simila).
  - Nur rajtigitaj partioj (vendejo, turisto, DM Global Tur) povas malĉifri per siaj privataj ŝlosiloj.
- **Zero-Knowledge Proofs (ZKP):**
  - Kiam vendo estas validumita, la kontrakto eldonas ZKP atestilon pri la vendo kaj komisiono, sen malkaŝi la identecon de la turisto.
  - DMC-oj kaj reviziantoj povas kontroli la ZKP surĉene aŭ per API.
- **Inteligenta Kontrakto:**
  - Aldonu funkcion por akcepti kaj konservi ZKP-hashojn por ĉiu vendo.
  - Aldonu publikan vidon por kontroli la validecon de ZKP por ajna transakcio.

### Sekvaj Paŝoj
1. Ĝisdatigi la backend por ĉifri turistajn datumojn antaŭ konservado aŭ sendado al blokĉeno.
2. Integru ZKP-bibliotekon (snarkjs, circom, aŭ zk-SNARKs por Soroban se disponebla).
3. Ĝisdatigi la inteligentan kontrakton por konservi kaj kontroli ZKP-hashojn.
4. Dokumenti API-finojn kaj kontraktajn metodojn por ekstera kontrolo.
