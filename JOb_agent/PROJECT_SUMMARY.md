# Job Application Email Tracker - Project Summary

## 🎯 Project Overview

A sophisticated multi-agent AI system that automatically monitors your email inbox, identifies job-related emails, extracts structured information, and maintains a comprehensive database of all your job applications.

## 🏗️ Architecture

### Multi-Agent System Design

The system consists of 5 specialized agents working together:

```
┌─────────────────────────────────────────────────────────────┐
│                    Orchestrator Agent                        │
│         (Coordinates the entire workflow)                    │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│Email Monitor │───▶│Email         │───▶│Data Extractor│
│Agent         │    │Classifier    │    │Agent         │
│              │    │Agent         │    │              │
└──────────────┘    └──────────────┘    └──────────────┘
                                                │
                                                ▼
                                        ┌──────────────┐
                                        │Database      │
                                        │Manager Agent │
                                        └──────────────┘
                                                │
                                                ▼
                                        ┌──────────────┐
                                        │SQLite        │
                                        │Database      │
                                        └──────────────┘
```

### Agent Responsibilities

1. **Email Monitor Agent**
   - Connects to email server via IMAP
   - Fetches emails (recent, unread, or all)
   - Searches for job-related keywords
   - Returns raw email data

2. **Email Classifier Agent**
   - Uses OpenAI GPT to analyze emails
   - Determines if email is job-related
   - Classifies email type:
     - Application confirmation
     - Rejection
     - Interview request
     - Job offer
     - Follow-up
     - General job communication
   - Provides confidence scores

3. **Data Extractor Agent**
   - Extracts structured information using AI
   - Identifies:
     - Company name
     - Job title/role
     - Location
     - Application status
     - Salary range
     - Important dates
     - Contact information
   - Handles unstructured email formats

4. **Database Manager Agent**
   - Manages all database operations
   - Prevents duplicate entries
   - Updates existing applications
   - Tracks status progression
   - Maintains email logs

5. **Orchestrator Agent**
   - Coordinates workflow between agents
   - Manages data flow
   - Handles errors and retries
   - Provides monitoring modes:
     - One-time scan
     - Continuous monitoring
     - Scheduled monitoring

## 📁 Project Structure

```
JOb_agent/
├── agents/
│   ├── __init__.py
│   ├── email_monitor_agent.py       # Email fetching
│   ├── email_classifier_agent.py    # AI classification
│   ├── data_extractor_agent.py      # Data extraction
│   ├── database_manager_agent.py    # Database operations
│   └── orchestrator_agent.py        # Workflow coordination
├── models/
│   ├── __init__.py
│   └── database.py                  # SQLAlchemy models
├── utils/
│   ├── __init__.py
│   ├── config.py                    # Configuration management
│   └── email_client.py              # IMAP email client
├── main.py                          # CLI entry point
├── dashboard.py                     # Streamlit dashboard
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment template
├── .gitignore                       # Git ignore rules
├── README.md                        # Project documentation
├── SETUP.md                         # Setup guide
├── quickstart.sh                    # Quick start script
└── PROJECT_SUMMARY.md              # This file
```

## 🗄️ Database Schema

### JobApplication Table
- **id**: Primary key
- **company_name**: Company name
- **role_title**: Job title
- **status**: Application status
- **application_date**: When applied
- **last_updated**: Last update timestamp
- **email_subject**: Email subject
- **email_body**: Email content
- **email_from**: Sender address
- **email_date**: Email date
- **email_message_id**: Unique email ID
- **location**: Job location
- **salary_range**: Salary information
- **application_url**: Job posting URL
- **metadata**: JSON field for flexible data
- **notes**: Additional notes

### EmailLog Table
- **id**: Primary key
- **message_id**: Unique email identifier
- **subject**: Email subject
- **from_address**: Sender
- **date**: Email date
- **is_job_related**: Boolean flag
- **classification**: Email type
- **processed_date**: When processed

## 🔄 Workflow

1. **Email Fetching**
   - Connect to email server
   - Fetch emails based on mode (recent/unread/all)
   - Return email data

2. **Classification**
   - Analyze each email with AI
   - Determine if job-related
   - Classify email type
   - Calculate confidence score

3. **Data Extraction**
   - Extract structured information
   - Parse company, role, status
   - Identify dates and locations
   - Extract contact details

4. **Database Storage**
   - Check for duplicates
   - Create or update records
   - Track status progression
   - Log processed emails

5. **Reporting**
   - Generate statistics
   - Display results
   - Update dashboard

## 🚀 Features

### Core Features
- ✅ Automatic email monitoring
- ✅ AI-powered classification
- ✅ Intelligent data extraction
- ✅ Duplicate detection
- ✅ Status tracking
- ✅ Real-time updates
- ✅ Scheduled monitoring
- ✅ Web dashboard

### Dashboard Features
- 📊 Overview with key metrics
- 📋 Searchable application list
- 📈 Analytics and charts
- 📥 CSV export
- 🔍 Advanced filtering
- 📅 Timeline visualization

## 🔧 Configuration

### Environment Variables
```env
OPENAI_API_KEY=your_key
EMAIL_ADDRESS=your_email
EMAIL_PASSWORD=your_password
EMAIL_IMAP_SERVER=imap.gmail.com
EMAIL_IMAP_PORT=993
DATABASE_URL=sqlite:///job_tracker.db
CHECK_INTERVAL=3600
LOOKBACK_DAYS=30
AI_MODEL=gpt-4o-mini
TEMPERATURE=0.3
```

## 📊 Usage Examples

### One-Time Scan
```bash
python main.py --mode once --days 7
```

### Continuous Monitoring
```bash
python main.py --mode continuous --interval 3600
```

### Launch Dashboard
```bash
streamlit run dashboard.py
```

### Quick Start
```bash
./quickstart.sh
```

## 🔐 Security Considerations

1. **Email Security**
   - Uses app-specific passwords
   - IMAP over SSL/TLS
   - No password storage in code

2. **API Security**
   - API keys in environment variables
   - Not committed to version control
   - Rate limiting awareness

3. **Data Security**
   - Local SQLite database
   - No external data sharing
   - Sensitive data in .env

## 🎯 Use Cases

1. **Job Search Tracking**
   - Track all applications
   - Monitor response rates
   - Identify patterns

2. **Interview Management**
   - Track interview invitations
   - Schedule management
   - Follow-up reminders

3. **Analytics**
   - Success rate analysis
   - Company insights
   - Timeline tracking

4. **Organization**
   - Centralized data repository
   - Easy search and filter
   - Export capabilities

## 🔮 Future Enhancements

Potential improvements:
- [ ] Email notifications for important updates
- [ ] Integration with job boards
- [ ] Calendar integration for interviews
- [ ] Resume version tracking
- [ ] Cover letter management
- [ ] Networking contact tracking
- [ ] Salary negotiation insights
- [ ] Mobile app
- [ ] Multi-user support
- [ ] Cloud deployment option

## 🛠️ Technology Stack

- **Framework**: Agno (Multi-agent framework)
- **AI/ML**: OpenAI GPT-4o-mini
- **Database**: SQLAlchemy + SQLite
- **Email**: imap-tools
- **Dashboard**: Streamlit
- **Charts**: Plotly
- **Data**: Pandas
- **Environment**: python-dotenv

## 📝 Development Notes

### Design Decisions

1. **SQLite Database**
   - Simple setup, no server required
   - Portable, single file
   - Sufficient for personal use
   - Easy to backup

2. **Agno Framework**
   - Built for multi-agent systems
   - Clean agent abstraction
   - Easy delegation
   - Good for AI workflows

3. **OpenAI GPT**
   - Excellent at text understanding
   - Handles unstructured data well
   - Reliable classification
   - Good extraction accuracy

4. **Streamlit Dashboard**
   - Quick to develop
   - Interactive visualizations
   - Python-native
   - Easy deployment

### Known Limitations

1. **Email Provider Support**
   - Requires IMAP access
   - Some providers may have restrictions
   - Rate limiting possible

2. **AI Accuracy**
   - Depends on email content quality
   - May misclassify ambiguous emails
   - Extraction accuracy varies

3. **Performance**
   - API calls can be slow
   - Large email volumes may take time
   - Rate limits apply

## 📚 Documentation

- **README.md**: Overview and features
- **SETUP.md**: Detailed setup instructions
- **PROJECT_SUMMARY.md**: This file
- **Code Comments**: Inline documentation
- **Docstrings**: Function documentation

## 🤝 Contributing

This is a personal project, but improvements are welcome:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - Feel free to use and modify for your needs.

## 🙏 Acknowledgments

- Agno framework for multi-agent capabilities
- OpenAI for powerful language models
- Streamlit for easy dashboard creation
- The Python community for excellent libraries

---

**Created**: 2024
**Author**: Job Tracker Team
**Version**: 1.0.0
