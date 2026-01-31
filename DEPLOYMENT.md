# Deployment Guide (Free Tier)

This guide explains how to deploy the Creator AI platform using entirely free resources: **Vercel** for the frontend and **Render** for the backend.

## Prerequisites

- GitHub account with this repository pushed.
- Vercel account (Free Hobby Plan).
- Render account (Free Individual Plan).
- Domain registrar access for `creator-ai.in`.
- Neon database URL (Postgres) - Neon offers a free tier.
- OpenAI API Key.

## 1. Backend Deployment (Render)

Render offers a free tier for Web Services that supports Docker.

1.  **Login to Render**: Go to [render.com](https://render.com/) and log in.
2.  **New Web Service**: Click "New +" -> "Web Service".
3.  **Connect GitHub**: Select "Build and deploy from a Git repository" and connect your GitHub account. Select this repository.
4.  **Configure Service**:
    -   **Name**: Choose a unique name (e.g., `creator-ai-backend`).
    -   **Region**: Choose a region close to your users (e.g., Singapore or Frankfurt).
    -   **Branch**: `main` (or your working branch).
    -   **Root Directory**: `apps/api` (Important: Set this so Render finds the Dockerfile).
    -   **Runtime**: **Docker**.
    -   **Instance Type**: **Free**.
5.  **Environment Variables**:
    -   Scroll down to "Environment Variables" and add:
        -   `DATABASE_URL`: Your Neon Postgres connection string.
        -   `OPENAI_API_KEY`: Your OpenAI API Key.
        -   `JWT_SECRET_KEY`: A secure random string.
        -   `ALLOWED_ORIGINS`: `https://creator-ai.in,https://www.creator-ai.in` (This allows your frontend to talk to this backend).
6.  **Deploy**: Click "Create Web Service".
    -   Render will build the Docker image. This might take a few minutes.
    -   Once deployed, copy the **onrender.com URL** (e.g., `https://creator-ai-backend.onrender.com`). You will need this for the frontend.

**Note on Free Tier**: Render's free tier spins down after 15 minutes of inactivity. The first request after a while may take ~50 seconds to respond. This is expected behavior for the free tier.

## 2. Frontend Deployment (Vercel)

1.  **Login to Vercel**: Go to [vercel.com](https://vercel.com/).
2.  **Add New Project**: Import from GitHub and select this repository.
3.  **Configure Project**:
    -   **Root Directory**: Click "Edit" and select `apps/web`.
    -   **Framework Preset**: Next.js.
4.  **Environment Variables**:
    -   Add:
        -   `NEXT_PUBLIC_API_URL`: Paste the **Render URL** you copied earlier (e.g., `https://creator-ai-backend.onrender.com`). **Do not add a trailing slash.**
5.  **Deploy**: Click "Deploy".
6.  **Domain Setup**:
    -   Go to the project **Settings** -> **Domains**.
    -   Add `creator-ai.in`.
    -   Vercel will provide DNS records (A record @ `76.76.21.21`).
    -   Go to your domain registrar and update the A record for `creator-ai.in` to point to Vercel's IP.

## 3. DNS Configuration Summary

You only need to configure the main domain for the Frontend. The API will use the free Render subdomain.

| Type | Name | Value | Purpose |
| :--- | :--- | :--- | :--- |
| **A** | `@` (root) | `76.76.21.21` (Vercel IP) | Frontend (creator-ai.in) |
| **CNAME** | `www` | `cname.vercel-dns.com` | Frontend (www.creator-ai.in) |

## 4. Troubleshooting

-   **"Server Error" on Frontend**: Check if the backend is awake. On the free tier, the first request wakes it up.
-   **CORS Errors**: Ensure `ALLOWED_ORIGINS` in Render exactly matches `https://creator-ai.in`.
-   **Build Failures**: Check logs in Render/Vercel Dashboard.
