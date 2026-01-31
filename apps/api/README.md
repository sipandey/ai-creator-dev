# Creator AI API

A FastAPI-based backend service for the Creator AI platform, providing AI-powered content creation tools for short-form video creators.

## Overview

This API serves as the backend for Creator AI, an agentic AI platform that helps content creators generate personalized scripts, strategies, and personas for Instagram Reels, TikTok, and YouTube Shorts.

### Key Features

- **User Authentication**: JWT-based auth with secure password hashing
- **Persona Management**: AI-powered creator persona analysis and refinement
- **Content Strategy**: Weekly content planning with personalized recommendations
- **Script Generation**: AI-generated video scripts tailored to creator style
- **Feedback Loop**: Learning system that improves recommendations over time
- **Multi-modal Analysis**: Support for text, audio, and video content analysis

## Prerequisites

- Python 3.9+
- PostgreSQL database (Neon recommended)
- OpenAI API key
- FFmpeg (for media processing)

## Quick Start

### 1. Environment Setup

```bash
cd apps/api

# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Variables

Copy and configure your `.env` file:

```bash
# Database
DATABASE_URL=postgresql://username:password@host:port/database

# OpenAI
OPENAI_API_KEY=your_openai_api_key

# CORS (for frontend connection)
ALLOWED_ORIGINS=http://localhost:3000

# Optional: Third-party APIs
GOOGLE_APPLICATION_CREDENTIALS=/path/to/google/credentials.json
AZURE_SPEECH_KEY=your_azure_key
RAPIDAPI_KEY=your_rapidapi_key
```

### 3. Database Setup

```bash
# Run database migrations
python -m alembic upgrade head

# Verify connection
python test_connection_variations.py
```

### 4. Start the API Server

```bash
# Development mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:

- **Interactive API Docs**: `http://localhost:8000/docs` (Swagger UI)
- **Alternative Docs**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`

## API Endpoints

### Authentication

- `POST /auth/signup` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user info

### Persona Management

- `GET /persona` - Get user persona
- `POST /persona` - Create/update persona
- `POST /persona/builder` - Build persona from content samples
- `POST /persona/enhanced` - Enhanced multi-modal persona analysis

### Content Creation

- `POST /strategy` - Generate weekly content strategy
- `POST /script` - Generate video script
- `GET /preferences` - Get user preferences
- `POST /preferences` - Update preferences

### Learning & Feedback

- `POST /feedback` - Submit feedback on generated content
- `POST /persona/refine` - Refine persona based on feedback

## Project Structure

```
apps/api/
├── app/
│   ├── main.py              # FastAPI application & routes
│   ├── core/
│   │   ├── config.py        # Configuration & settings
│   │   ├── database.py      # Database connection
│   │   ├── security.py      # Password hashing & JWT
│   │   └── deps.py          # Dependencies
│   ├── models/              # SQLAlchemy models
│   ├── routes/              # API route handlers
│   ├── services/            # Business logic
│   ├── agents/              # AI agent implementations
│   ├── llm/                 # LLM client & prompts
│   └── schemas/             # Pydantic schemas
├── alembic/                 # Database migrations
├── requirements.txt         # Python dependencies
├── Dockerfile              # Container configuration
├── .env                    # Environment variables
└── test_connection_variations.py  # DB connection testing
```

## Development

### Running Tests

```bash
# Add tests when available
pytest
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "migration message"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Code Style

- Follow PEP 8
- Use type hints
- Keep agent logic isolated from HTTP/DB layers

## Deployment

### Docker

```bash
# Build image
docker build -t creator-ai-api .

# Run container
docker run -p 8000:8000 --env-file .env creator-ai-api
```

### Environment Variables for Production

```bash
DATABASE_URL=your_production_db_url
OPENAI_API_KEY=your_production_key
ENVIRONMENT=production
ALLOWED_ORIGINS=https://yourdomain.com
```

## Troubleshooting

### Common Issues

1. **Module Import Errors**

   ```bash
   # Ensure you're in the correct directory
   cd apps/api
   PYTHONPATH=/Users/youruser/path/to/apps/api python -m uvicorn app.main:app
   ```

2. **Database Connection Issues**

   ```bash
   # Test connection
   python test_connection_variations.py
   # Check DATABASE_URL in .env
   ```

3. **OpenAI API Errors**
   - Verify `OPENAI_API_KEY` in `.env`
   - Check API quota and billing

4. **CORS Issues**
   - Update `ALLOWED_ORIGINS` in `.env`
   - Restart the server

### Logs

The API uses Python logging. Check console output for errors:

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
uvicorn app.main:app --log-level debug
```

### Health Checks

```bash
curl http://localhost:8000/health
# Should return: {"status": "healthy", "version": "2.0.0"}
```

## Contributing

1. Follow the existing code patterns
2. Keep agents stateless and JSON-in/JSON-out
3. Add proper error handling
4. Update this README for any new features

## License

[Add license information here]
