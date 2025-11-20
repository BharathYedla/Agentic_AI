# System Architecture Diagram

```
┌────────────────────────────────────────────────────────────────────────────┐
│                  Job Application Email Tracker System                      │
│                         Multi-Agent Architecture                            │
└────────────────────────────────────────────────────────────────────────────┘

                              ┌─────────────────┐
                              │  Email Server   │
                              │  (Gmail/IMAP)   │
                              └────────┬────────┘
                                       │
                                       │ IMAP/SSL
                                       │
                                       ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                         ORCHESTRATOR AGENT                                │
│                    (Coordinates entire workflow)                          │
└──────────────────────────────────────────────────────────────────────────┘
                                       │
                    ┌──────────────────┼──────────────────┐
                    │                  │                  │
                    ▼                  ▼                  ▼
        ┌───────────────────┐  ┌──────────────┐  ┌──────────────┐
        │ EMAIL MONITOR     │  │   OPENAI     │  │  DATABASE    │
        │     AGENT         │  │   GPT API    │  │   MANAGER    │
        │                   │  │              │  │    AGENT     │
        │ • Fetch emails    │  └──────┬───────┘  │              │
        │ • Search inbox    │         │          │ • Save data  │
        │ • Filter dates    │         │          │ • Update     │
        └─────────┬─────────┘         │          │ • Query      │
                  │                   │          └──────┬───────┘
                  │                   │                 │
                  ▼                   │                 │
        ┌───────────────────┐         │                 │
        │ EMAIL CLASSIFIER  │◄────────┘                 │
        │     AGENT         │                           │
        │                   │                           │
        │ • Classify type   │                           │
        │ • Job-related?    │                           │
        │ • Confidence      │                           │
        └─────────┬─────────┘                           │
                  │                                     │
                  ▼                                     │
        ┌───────────────────┐                           │
        │ DATA EXTRACTOR    │                           │
        │     AGENT         │                           │
        │                   │                           │
        │ • Extract company │                           │
        │ • Extract role    │                           │
        │ • Extract status  │                           │
        │ • Extract dates   │                           │
        └─────────┬─────────┘                           │
                  │                                     │
                  └─────────────────────────────────────┘
                                       │
                                       ▼
                            ┌──────────────────┐
                            │  SQLite Database │
                            │                  │
                            │ • JobApplication │
                            │ • EmailLog       │
                            └────────┬─────────┘
                                     │
                                     │
                                     ▼
                            ┌──────────────────┐
                            │    Streamlit     │
                            │    Dashboard     │
                            │                  │
                            │ • Overview       │
                            │ • Applications   │
                            │ • Analytics      │
                            │ • Export         │
                            └──────────────────┘
```

## Data Flow

```
1. Email Fetching
   ┌─────────────┐
   │ Email Server│
   └──────┬──────┘
          │
          ▼
   ┌─────────────┐
   │ Raw Emails  │
   └──────┬──────┘

2. Classification
          │
          ▼
   ┌─────────────┐      ┌──────────┐
   │ Classifier  │◄─────┤ OpenAI   │
   │   Agent     │      │   API    │
   └──────┬──────┘      └──────────┘
          │
          ▼
   ┌─────────────┐
   │ Job-Related │
   │   Emails    │
   └──────┬──────┘

3. Data Extraction
          │
          ▼
   ┌─────────────┐      ┌──────────┐
   │ Extractor   │◄─────┤ OpenAI   │
   │   Agent     │      │   API    │
   └──────┬──────┘      └──────────┘
          │
          ▼
   ┌─────────────┐
   │ Structured  │
   │    Data     │
   └──────┬──────┘

4. Storage
          │
          ▼
   ┌─────────────┐
   │  Database   │
   │   Manager   │
   └──────┬──────┘
          │
          ▼
   ┌─────────────┐
   │   SQLite    │
   │  Database   │
   └─────────────┘
```

## Agent Communication

```
Orchestrator
    │
    ├──► Email Monitor ──► Returns: List[Email]
    │
    ├──► Email Classifier ──► Returns: List[Classification]
    │        ↑
    │        └── Uses: OpenAI API
    │
    ├──► Data Extractor ──► Returns: List[ExtractedData]
    │        ↑
    │        └── Uses: OpenAI API
    │
    └──► Database Manager ──► Returns: List[ApplicationID]
             ↓
          SQLite DB
```

## Monitoring Modes

```
┌─────────────────────────────────────────────────────────────┐
│                      MONITORING MODES                        │
└─────────────────────────────────────────────────────────────┘

1. ONE-TIME SCAN
   ┌─────┐
   │ Run │ ──► Process ──► Done
   └─────┘

2. CONTINUOUS MONITORING
   ┌─────┐     ┌─────┐     ┌─────┐
   │ Run │ ──► │Wait │ ──► │ Run │ ──► ...
   └─────┘     └─────┘     └─────┘
                  ↑           │
                  └───────────┘

3. SCHEDULED MONITORING
   ┌─────────┐     ┌─────────┐     ┌─────────┐
   │Schedule │ ──► │  Wait   │ ──► │  Run    │ ──► ...
   └─────────┘     └─────────┘     └─────────┘
                        ↑               │
                        └───────────────┘
```

## Database Schema

```
┌────────────────────────────────────────────────────────────┐
│                    JobApplication                           │
├────────────────────────────────────────────────────────────┤
│ id (PK)                    INTEGER                          │
│ company_name               VARCHAR(255)                     │
│ role_title                 VARCHAR(255)                     │
│ status                     VARCHAR(50)                      │
│ application_date           DATETIME                         │
│ last_updated               DATETIME                         │
│ email_subject              VARCHAR(500)                     │
│ email_body                 TEXT                             │
│ email_from                 VARCHAR(255)                     │
│ email_date                 DATETIME                         │
│ email_message_id (UNIQUE)  VARCHAR(255)                     │
│ location                   VARCHAR(255)                     │
│ salary_range               VARCHAR(100)                     │
│ application_url            VARCHAR(500)                     │
│ metadata                   JSON                             │
│ notes                      TEXT                             │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│                       EmailLog                              │
├────────────────────────────────────────────────────────────┤
│ id (PK)                    INTEGER                          │
│ message_id (UNIQUE)        VARCHAR(255)                     │
│ subject                    VARCHAR(500)                     │
│ from_address               VARCHAR(255)                     │
│ date                       DATETIME                         │
│ is_job_related             INTEGER (0/1)                    │
│ classification             VARCHAR(50)                      │
│ processed_date             DATETIME                         │
└────────────────────────────────────────────────────────────┘
```

## Technology Stack

```
┌─────────────────────────────────────────────────────────────┐
│                    TECHNOLOGY LAYERS                         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  PRESENTATION LAYER                                          │
│  • Streamlit Dashboard                                       │
│  • Plotly Charts                                             │
│  • Pandas DataFrames                                         │
└─────────────────────────────────────────────────────────────┘
                          ▲
                          │
┌─────────────────────────────────────────────────────────────┐
│  APPLICATION LAYER                                           │
│  • Agno Multi-Agent Framework                                │
│  • Python 3.8+                                               │
│  • CLI Interface (argparse)                                  │
└─────────────────────────────────────────────────────────────┘
                          ▲
                          │
┌─────────────────────────────────────────────────────────────┐
│  BUSINESS LOGIC LAYER                                        │
│  • Email Monitor Agent                                       │
│  • Email Classifier Agent                                    │
│  • Data Extractor Agent                                      │
│  • Database Manager Agent                                    │
│  • Orchestrator Agent                                        │
└─────────────────────────────────────────────────────────────┘
                          ▲
                          │
┌─────────────────────────────────────────────────────────────┐
│  INTEGRATION LAYER                                           │
│  • OpenAI API (GPT-4o-mini)                                  │
│  • IMAP Email Client (imap-tools)                            │
│  • SQLAlchemy ORM                                            │
└─────────────────────────────────────────────────────────────┘
                          ▲
                          │
┌─────────────────────────────────────────────────────────────┐
│  DATA LAYER                                                  │
│  • SQLite Database                                           │
│  • Environment Variables (.env)                              │
└─────────────────────────────────────────────────────────────┘
```
