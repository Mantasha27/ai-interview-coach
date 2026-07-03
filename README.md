# AI Interview Coach

A web app where you can practice interviews with AI evaluation. Answer questions by speaking or typing, get instant feedback, and track your progress over time.

## What It Does

- Practice Interviews - Choose from HR, General, Data Science, or Web Development
- Speak or Type - Answer questions using your microphone or keyboard  
- AI Feedback - Get instant scoring and suggestions for improvement
- Track Progress - See your performance across multiple interviews
- Download Results - Export your scores as CSV

## Quick Start

### Setup
```bash
# Clone repo
git clone https://github.com/Mantasha27/ai-interview-coach.git
cd ai-interview-coach

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

App opens at `http://localhost:8501`

## Project Structure

```
ai-interview-coach/
├── app.py              # Main app logic
├── auth.py             # Login/Register
├── database.py         # SQLite setup
├── nlp_engine.py       # Answer evaluation (TF-IDF + Cosine Similarity)
├── admin.py            # Admin dashboard
├── utils.py            # Speech recognition & text-to-speech
├── requirements.txt    # Dependencies
└── data/               # CSV question files
    ├── hr_q.csv & hr_a.csv
    ├── ds_q.csv & ds_a.csv
    ├── g_q.csv & g_a.csv
    └── wd_q.csv & wd_a.csv
```

## How It Works

1. Login/Register - Create account with username & password (SHA256 hashed)
2. Choose Domain - Pick an interview type (HR, Data Science, etc)
3. Answer Questions - Get 5 random questions, answer by speaking or typing
4. Get Feedback - App compares your answer to expected answer and gives score
5. View Results - See detailed feedback, graphs, and download CSV

## How Evaluation Works

- Converts both answers to vectors using TF-IDF
- Calculates similarity (0-10 scale)
- Finds missing keywords you didn't mention
- Gives confidence score based on answer quality
- Personalized feedback: "Excellent", "Good", "Needs improvement", etc

## Tech Stack

- Frontend - Streamlit (web UI)
- Backend - Python
- Database - SQLite
- NLP - scikit-learn (TF-IDF, Cosine Similarity)
- Speech - Google Speech Recognition + gTTS
- Graphs - Matplotlib

## Security

- Passwords hashed with SHA256 (one-way)
- .env file ignored (never uploaded)
- Database file ignored (no passwords leaked)
- Use .env.example as template

## Features

- 4 interview domains (200 questions total)  
- Speech-to-text & text-to-speech  
- Real-time scoring & feedback  
- Performance tracking over time  
- Download results as CSV  
- Admin dashboard with statistics  
- Secure login system  

## What Gets Scored

- Score (0-10) - How well your answer matches
- Percentage (0-100%) - Overall performance
- Confidence (0-100%) - How detailed your answer is
- Missing Keywords - Important concepts you forgot to mention

## Troubleshooting

**Streamlit not found?**
```bash
pip install -r requirements.txt
```

**Microphone not working?**
- Check microphone is connected
- Grant permission if asked
- Try restarting the app

**CSV files missing?**
- Make sure all CSV files are in same folder as app.py
- Check filenames: hr_q.csv, hr_a.csv, etc.

**Database error?**
```bash
rm database.db
streamlit run app.py
```

## Want to Contribute?

1. Fork repo
2. Create branch: `git checkout -b feature/your-feature`
3. Make changes and test
4. Commit: `git commit -m "Add feature"`
5. Push: `git push origin feature/your-feature`
6. Open Pull Request

## License

MIT License - feel free to use this however you want

## Made By

Mantasha Shaikh  
GitHub: [@Mantasha27](https://github.com/Mantasha27)  
Email: shaikhmantasha41990@gmail.com

## If You Like It

Drop a star on the repo! Means a lot.
