# Personal Productivity Intelligence System
*Analisi comportamentale e consigli personalizzati per migliorare produttività e benessere.*

## Panoramica del Progetto

Il **Personal Productivity Intelligence System** è una piattaforma pensata per aiutare professionisti, freelance e team a capire *come lavorano davvero*, attraverso un approccio completamente **privacy-first**.
Il sistema non raccoglie contenuti sensibili, ma solo dati contestuali (applicazione, finestra attiva, durata), trasformandoli in insight utili e consigli pratici generati da un'IA connessa ai tuoi dati reali.

Il progetto si compone di tre macro-componenti:

1. **Activity Tracker** – Registra le attività svolte sul dispositivo in modo leggero e non invasivo.
2. **Backend Intelligence Layer** – Classifica, aggrega e analizza i dati.
3. **Dashboard + AI Coach** – Visualizza i pattern lavorativi e genera insight personalizzati tramite un LLM integrato via MCP.

---

## Obiettivi

- Rendere visibili i pattern reali di lavoro.
- Identificare focus, distrazioni, interruzioni e trend.
- Generare consigli pratici e personalizzati tramite IA.
- Migliorare produttività e benessere senza ricorrere a strumenti invasivi.
- Dare pieno controllo dei dati all’utente.

---

## Destinatari

### 1. **Knowledge workers**
Sviluppatori, designer, product manager, marketer e chiunque lavori molte ore al computer.

### 2. **Freelance e lavoratori autonomi**
Per ottimizzare gestione del tempo e capire i propri ritmi naturali.

### 3. **Team remoti o ibridi**
Insight aggregati, totalmente etici e non invasivi.

### 4. **Manager e team leader**
Per comprendere carichi di lavoro e prevenire burn-out.

### 5. **Appassionati di self-improvement**
Per sviluppare consapevolezza e migliorare la qualità della propria giornata.

---

## Come funziona

### 1. Activity Tracking
Il tracker registra:
- processo attivo
- titolo finestra / dominio browser
- timestamp inizio/fine
- eventi di pausa/resume
- device ID

**Nessun contenuto sensibile. Nessun keylogging. Nessuno screenshot.**

---

### 2. Motore di Classificazione
Gli eventi vengono assegnati a categorie significative per il lavoro digitale, tra cui:

- **CODING**
- **DEVOPS_GIT**
- **DB_TECH**
- **MEETINGS_CALLS**
- **DOC_RESEARCH_WORK_WEB**
- **SOCIAL_ENTERTAINMENT**
- **BREAK_IDLE**
- **OTHER_WEB**
- **MISC**

La classificazione è **rule-based, trasparente, configurabile ed estendibile**.

---

### 3. Motore di Aggregazione
Il backend calcola:
- durata totale per categoria
- percentuali sul totale
- breakdown per applicazione / finestra
- trend giornalieri
- finestre di deep work e di distrazione
- pattern ricorrenti

Risultato: una vera mappa comportamentale del proprio lavoro.

---

### 4. AI Insights tramite MCP
L’LLM accede ai dati tramite **MCP tools** che wrappano le API del backend.

Questo permette di chiedere all’assistente, ad esempio:

- “Perché ieri ho perso concentrazione?”
- “Come posso ridurre le interruzioni?”
- “Qual è il mio pattern di produttività settimanale?”

L’IA elabora **sui dati reali dell’utente**, generando consigli personalizzati, contestuali e utili.

---

### 5. Dashboard
La dashboard mostra:
- timeline delle attività
- grafico categorie
- analisi per giorno
- breakdown applicazioni / finestre
- insight generati dall’IA
- pulsanti “Chiedi un consiglio” su ogni grafico

---

## Stack Tecnologico

### Backend
- Python 3.13
- FastAPI
- MongoDB + Beanie
- Repository pattern
- MCP Tools (FastMCP)
- Datapizza AI Agent
- OpenAI / Claude LLM

### Frontend
- React
- Chart.js
- TailwindCSS
- Chat/Insight Panel

### Architettura
Eventi → DB → Classificazione → Aggregazione → API → MCP → LLM → Insight

---

## Privacy First

- Nessun contenuto sensibile raccolto
- I dati rimangono locali o sotto pieno controllo dell’utente
- L’IA accede ai dati solo tramite tool esplicitamente autorizzati

---

## Cosa permette di fare

- Capire come lavori davvero
- Scoprire pattern invisibili
- Identificare finestre di deep work
- Ridurre distrazioni e switching
- Migliorare focus e benessere
- Adottare abitudini sostenibili e consapevoli

---

## Roadmap

- Insight settimanali automatici
- Rilevamento anomalie (fatica, overload)
- Obiettivi e tracking
- Classificatore ibrido rule-based + ML
- Insight aggregati per team (privacy-preserving)

---

## Conclusione

Il Personal Productivity Intelligence System non è un semplice tracker, né una dashboard:
È un **coach digitale**, progettato per aiutarti a lavorare meglio, vivere meglio e prendere decisioni basate su consapevolezza e dati reali.
