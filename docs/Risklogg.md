# Risklogg – Hållbarhetskollen

## Översikt
Riskloggen är anpassad efter det faktiska genomförandet av projektet och visar de viktigaste riskerna som uppstod och hanterades under utvecklingen.

---

## Risker

| ID | Risk | Sannolikhet | Konsekvens | Åtgärd | Ägare | Status |
|----|------|-------------|------------|--------|--------|--------|
| R1 | Scope blir för stort (för många features) | H | H | MVP-fokus och tydlig prioritering av user stories | PO | Hanterad |
| R2 | Merge-konflikter i Git vid samarbete | M | M | Små commits och tydliga ändringar per fil | SM | Hanterad |
| R3 | Fel i CO₂e-beräkningar | M | H | Testade formler mot exempeldata och justerade vid behov | Dev | Hanterad |
| R4 | Problem med databasrelationer (User–Activity) | M | H | Tydlig datamodell i SQLAlchemy och tidig testning | Dev | Hanterad |
| R5 | Otydlig kravbild i början av projektet | M | M | Förtydligade user stories och backlog tidigt i processen | PO | Hanterad |

---

## Noteringar

### Vad har ändrats sedan senaste uppdateringen?
Riskerna har hanterats under projektets gång och inga kritiska öppna risker kvarstår i slutversionen.

### Topp 3 risker som påverkat projektet mest
1. Scope creep (R1)
2. CO₂e-beräkningar (R3)
3. Databasrelationer (R4)

