# Infrastructure

## Cloud Stack (LOCKED)

- **Frontend:** Vercel (Free Hobby Tier)
- **Backend:** Render (Free Individual Tier)
- **Database:** Neon (Serverless Postgres Free Tier)

**Principle:** Infrastructure must not slow a solo founder.

## Database

### Technology Stack
- **Database:** Neon (Serverless Postgres)
- **ORM:** SQLAlchemy 2.x
- **Migrations:** Alembic
- **Strategy:** Avoid ENUMs for MVP flexibility

### Connection Management
- Connection pooling handled by Neon
- Environment-based configuration
- Automatic scaling with usage

## Deployment

### Frontend (Vercel)
- Automatic deployments from main branch
- Preview deployments for PRs
- Environment variables managed in Vercel dashboard
- Domain: `creator-ai.in` (configured via Vercel)

### Backend (Render)
- Docker-based deployments
- Environment variables for configuration
- Health checks and monitoring
- Domain: Default Render subdomain (e.g., `onrender.com`)

## Environment Variables

Required environment variables:

    ```bash
    # Database
    DATABASE_URL=postgresql://...
    
    # Authentication
    JWT_SECRET_KEY=...
    JWT_ALGORITHM=HS256
    
    # LLM Provider
    OPENAI_API_KEY=...
    # or
    ANTHROPIC_API_KEY=...
    
    # Environment
    ENVIRONMENT=development|staging|production

    # Deployment
    NEXT_PUBLIC_API_URL=https://... (Frontend)
    ALLOWED_ORIGINS=https://creator-ai.in,... (Backend)
    PORT=8000 (Backend, for Render)
    ```

## Monitoring

- Application logs via platform logging (Vercel/Render)
- Database monitoring via Neon dashboard
- Error tracking (to be implemented)
