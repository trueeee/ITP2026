# Definition of Done (DoD) – Hållbarhetskollen

En user story eller uppgift anses vara **klar** först när följande kriterier är uppfyllda:

## 1. Funktionalitet & Acceptans
- [ ] Alla acceptanskriterier för uppgiften är uppfyllda och verifierade.
- [ ] Funktionaliteten är testad manuellt och går att demonstrera (demo-ready).
- [ ] Rimlig felhantering och inputvalidering finns (t.ex. inga negativa utsläppsmängder eller tomma fält).

## 2. Kodkvalitet & Process
- [ ] Koden är skriven på en separat branch och hanterad via en Pull Request (PR).
- [ ] Koden har granskats och godkänts av minst en (1) annan teammedlem (Code Review).
- [ ] Inga hemligheter (API-nycklar, lösenord) finns med i repot.

## 3. Testning & CI (Continuous Integration)
- [ ] Relevanta automatiska tester har lagts till (enhetstester för beräkningslogik, integrationstester för API).
- [ ] CI-pipelinen (tester via `pytest` + kodformatering/linting) är grön innan merge.

## 4. Dokumentation
- [ ] Uppdateringar som påverkar systemet återspeglas i `README.md` (eller via autogenererad Swagger-dokumentation i FastAPI).
- [ ] Koden följer projektets namnstandard och är organiserad enligt den bestämda arkitekturen (API/DB/UI separerat).
