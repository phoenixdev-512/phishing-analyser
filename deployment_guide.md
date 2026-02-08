# Deployment Guide

This guide provides step-by-step instructions for deploying the Phishing URL Analyzer to various environments.

## 1. Local Deployment (Development)

### Backend
1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
2.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Set up environment variables in `.env`:
    ```env
    GROQ_API_KEY=your_key_here
    FRONTEND_URL=http://localhost:5173
    ```
5.  Run the server:
    ```bash
    uvicorn app.main:app --reload
    ```

### Frontend
1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Set up environment variables in `.env`:
    ```env
    VITE_API_BASE_URL=http://127.0.0.1:8000
    ```
4.  Run the development server:
    ```bash
    npm run dev
    ```

---

## 2. Vercel Deployment (Recommended)

This project is configured for easy deployment on [Vercel](https://vercel.com/).

### Prerequisites
-   Vercel CLI installed (`npm i -g vercel`) or a Vercel account.
-   GitHub repository connected to Vercel.

### Configuration
The project includes a `vercel.json` file in the root directory that configures the rewrites for the backend API.

```json
{
    "rewrites": [
        {
            "source": "/api/(.*)",
            "destination": "/backend/index.py"
        }
    ]
}
```

### Steps
1.  **Push to GitHub**: Ensure your latest code is pushed to your repository.
2.  **Import to Vercel**:
    -   Go to the Vercel Dashboard and click "Add New...".
    -   Select your repository.
3.  **Configure Project**:
    -   **Framework Preset**: Vite (Frontend).
    -   **Root Directory**: `./` (Root).
    -   **Environment Variables**:
        -   `GROQ_API_KEY`: Your Groq API Key.
        -   `VITE_API_BASE_URL`: Leave empty or set to `/` if deploying as a monorepo (Vercel handles the API routing via `vercel.json`).
4.  **Deploy**: Click "Deploy".

Vercel will automatically detect the Python backend based on `requirements.txt` and `api/index.py` (or configured destination) and deploy it as a Serverless Function.

### Troubleshooting Vercel Issues
-   **Missing Dependencies**: Ensure `backend/requirements.txt` is present and up-to-date.
-   **Path Errors**: Vercel runs from the root. Ensure python imports in `backend` are relative or correctly structured. The `backend/index.py` entry point helps bridge this.

---

## 3. Docker Deployment (Containerized)

*(Optional: For container-based hosting like Fly.io or DigitalOcean App Platform)*

### Dockerfile (Backend)
Create a `Dockerfile` in the `backend` directory:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Dockerfile (Frontend)
Create a `Dockerfile` in the `frontend` directory:
```dockerfile
FROM node:18-alpine as build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```
