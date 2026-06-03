# Product Backlog – Hållbarhetskollen

## US-01: Användarhantering
**Som** administratör  
**vill jag** skapa, lista och ta bort profiler  
**så att** utsläpp kan loggas per individ.

### Acceptanskriterier
- [ ] Formulär skapar användare (autogenererat ID).
- [ ] Lista över alla användare visas.
- [ ] Går att ta bort användare (med UI-meddelanden).

### Noteringar
- Datamodell: Tabell `User`.
- API-endpoints: GET/POST/DELETE under `/ui/users`.
- Testidéer: Skicka tomt namn.
- Risker/antaganden: MVP kräver endast namn.

---

## US-02: Logga aktivitet
**Som** användare  
**vill jag** logga aktiviteter (t.ex. resor, mat)  
**så att** jag spårar mina CO₂e-utsläpp.

### Acceptanskriterier
- [ ] Formulär på `/ui/activities`.
- [ ] Dynamiska listor (dropdowns) för kategori/nyckel.
- [ ] Mängden måste vara > 0.

### Noteringar
- Datamodell: Tabell `Activity`.
- API-endpoints: GET/POST `/ui/activities`.
- Testidéer: Negativ mängd ska ge fel (422).
- Risker/antaganden: Emissionsfaktorer är förinlästa.

---

## US-03: Aktivitetshistorik
**Som** användare  
**vill jag** se tidigare registrerade händelser  
**så att** jag får en detaljerad utsläppsvy.

### Acceptanskriterier
- [ ] Loggade händelser visas i en HTML-tabell.
- [ ] Det går att filtrera på en specifik användare.
- [ ] CO₂e-värdet räknas ut och visas per rad.

### Noteringar
- Datamodell: Samkör `Activity` med `EmissionFactor`.
- API-endpoints: Visas via `/ui/activities`.
- Testidéer: Kontrollera att beräkningen stämmer överens med faktorn.
- Risker/antaganden: UI avrundar snyggt.

---

## US-04: Veckorapport
**Som** användare  
**vill jag** summera utsläppen för en angiven vecka  
**så att** jag kan följa min utveckling över tid.

### Acceptanskriterier
- [ ] Inputfält för användare och måndagsdatum.
- [ ] Totalt CO₂e för 7 dagar summeras och visas.
- [ ] Json-data finns att hämta via rent API.

### Noteringar
- Datamodell: Aggregering av data i `Activity`.
- API-endpoints: GET `/ui/reports/weekly` och API `/reports/weekly`.
- Testidéer: Testa att skicka en vecka utan data (ska visa 0).
- Risker/antaganden: Användaren måste själva välja en måndag.

---

## US-05: Enhetlig layout
**Som** användare  
**vill jag** ha en konsekvent webbdesign  
**så att** tjänsten är logisk att navigera i.

### Acceptanskriterier
- [ ] Samma navigationsmeny (topbar) på alla sidor.
- [ ] Layout bygger på en gemensam `base.html`.
- [ ] Designen styrs helt av `static/styles.css`.

### Noteringar
- Datamodell: N/A.
- API-endpoints: Mount på `/static`.
- Testidéer: Visuell granskning.
- Risker/antaganden: Kräver inga avancerade animationer för en MVP.

---

## Backlog
| ID | Story | Prioritet | Estimat | Status | Länk issue |
|---:|------|-----------|---------|--------|-----------|
| US-01 | Användarhantering | Hög | S | Klar | #1 |
| US-02 | Logga aktivitet | Hög | M | Klar | #2 |
| US-03 | Aktivitetshistorik | Hög | M | Klar | #3 |
| US-04 | Veckorapport | Hög | M | Klar | #4 |
| US-05 | Enhetlig layout | Mellan | S | Klar | #5 |
