# Compass - Mental Health Companion

Compass is an AI-powered mental health companion that provides empathetic responses and personalized advice based on professional therapeutic conversations. It uses a hybrid search approach combining semantic and keyword matching to find relevant responses from a curated dataset of therapeutic conversations.

## Features

- 💬 Real-time chat interface with streaming responses
- 🔍 Hybrid search combining semantic and keyword matching
- 🤖 AI-powered personalized advice generation
- 🚨 Crisis detection and hotline information
- 📱 Responsive, modern UI design
- 🔒 Privacy-focused with no conversation storage

## Tech Stack

### Backend
- FastAPI
- ChromaDB for vector search
- Sentence Transformers for embeddings
- Claude 3.5 for advice generation
- Python 3.12+

### Frontend
- Next.js 15
- React 19
- TypeScript
- Tailwind CSS
- Modern UI components

## Prerequisites

- Python 3.12 or higher
- Node.js 18 or higher
- Anthropic API key (for Claude)

## Local Development Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd compass
```

2. Backend setup:
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env
```

3. Frontend setup:
```bash
cd frontend
npm install
```

4. Build the search index:
```bash
python scripts/build_index.py
```

5. Start the development servers:

Backend:
```bash
uvicorn backend.main:app --reload
```

Frontend (in a new terminal):
```bash
cd frontend
npm run dev
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## Deployment

### Backend (Render)

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - Environment Variables:
     - `ANTHROPIC_API_KEY`
     - `CORS_ORIGINS` (add your frontend URL)

### Frontend (Vercel/Render)

1. Connect your GitHub repository
2. Configure build settings:
   - Framework Preset: Next.js
   - Build Command: `npm run build`
   - Environment Variables:
     - `NEXT_PUBLIC_API_URL` (your backend URL)

## Project Structure

```
compass/
├── backend/
│   ├── main.py           # FastAPI application
│   ├── search_engine.py  # Vector search implementation
│   └── settings.py       # Configuration
├── frontend/
│   ├── src/
│   │   ├── app/         # Next.js pages
│   │   └── components/  # React components
│   └── package.json
├── scripts/
│   └── build_index.py   # Index builder
├── data/                # Generated search index
├── dataset/            # Source Q&A dataset
└── requirements.txt
```

## Essential Files for Deployment

1. Backend:
   - `backend/` directory
   - `requirements.txt`
   - `data/` directory (generated index)
   - `.env` (for local development)

2. Frontend:
   - `frontend/` directory
   - `.env.local` (for local development)

## Environment Variables

### Backend (.env)
```
ANTHROPIC_API_KEY=your_api_key
CORS_ORIGINS=["http://localhost:3000","https://your-frontend-url"]
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - feel free to use this project for any purpose.

## Security

- TLS encryption in production
- No storage of user conversations
- Environment variables for sensitive data
- Input validation and sanitization
- Rate limiting on API endpoints

## Performance Considerations

- Optimized vector search
- Response streaming
- Static page generation
- Responsive image loading
- Efficient state management

## Support

For issues and feature requests, please use the GitHub issue tracker. 