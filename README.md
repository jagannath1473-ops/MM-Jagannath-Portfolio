# M M Jagannath - Personal Portfolio

A modern, responsive personal portfolio for **M M Jagannath**, a second-year B.Tech student at Jain University, Bengaluru. The site presents my education, technical skills, CareerCompass project, competitive chess ratings, and a functional contact form backed by Python Flask and persistent production storage.

**Live website:** [https://mm-jagannath-portfolio.vercel.app/](https://mm-jagannath-portfolio.vercel.app/)

## About Me

I am a second-year B.Tech student pursuing Computer Science and Engineering with a specialization in Artificial Intelligence and Machine Learning at Jain University, Bengaluru (2025-Present). I am interested in computer science, programming, technology, AI/ML, experimentation, practical projects, problem-solving, and competitive chess. I value curiosity, persistence, adaptability, and continuous learning.

## My Technical Skills

### Programming and Technical Skills

- Java
- SQL
- HTML
- C++
- C

### Core Concepts

- Object-Oriented Programming (OOP)
- AI & ML Fundamentals

## Portfolio Website Features

- Premium responsive layout for desktop, tablet, and mobile
- Smooth navigation, scroll-triggered reveals, subtle parallax, and interactive card effects
- Accessible keyboard focus states and reduced-motion support
- Education and seven-skill presentation
- CareerCompass featured-project card with working live and GitHub links
- Competitive chess rating cards with the official FIDE profile link
- Contact form connected to a real Flask JSON API
- Server-side validation with accurate success and error responses
- SQLite storage for local development and Neon PostgreSQL for production
- Automated tests for page rendering, health checks, validation, and database storage

## Featured Project - CareerCompass

**CareerCompass** is a career-guidance web application developed as a team project to help students explore career paths, educational opportunities, and future academic choices.

Key features include career exploration, aptitude and interest-based guidance, career categories, college and course recommendations, and interactive educational guidance. My involvement included AI-assisted development coordination, requirements refinement, troubleshooting, testing, and GitHub publication.

- [CareerCompass live website](https://careercompass-mmjagannath.vercel.app/)
- [CareerCompass GitHub repository](https://github.com/jagannath1473-ops/CareerCompass)

## Chess Achievements and Ratings

### FIDE

- FIDE ID: 583023305
- Rapid rating: 1462 (August 2026)
- [Official FIDE profile](https://ratings.fide.com/profile/583023305)

### Lichess Personal Best

- Rapid: 1631
- Blitz: 1711
- Bullet: 1616

### Chess.com Personal Best

- Rapid: 1454

These ratings are presented as recorded personal-best or dated values; they are not described as current ratings.

## Technologies Used in This Project

- HTML5
- CSS3
- JavaScript
- Python
- Flask
- SQLite for local development
- Neon PostgreSQL for production storage
- Vercel for deployment

These are technologies used to build and operate this portfolio. They are separate from, and do not expand, the personal technical skills listed above.

## Python Flask Backend

JavaScript submits the contact form to `POST /api/contact`. Flask validates the visitor's name, email address, and message on the server before storing valid submissions. Successful requests receive HTTP `201`; invalid requests receive HTTP `400` with field-specific errors. `GET /api/health` reports the backend status and active storage adapter.

## Database Storage

The application uses SQLite by default during local development. Local contact messages are stored in `instance/portfolio_messages.db`, which is excluded from Git.

In production, the application reads a managed Neon PostgreSQL connection string from the secure `DATABASE_URL` environment variable configured in Vercel. The credential is never committed to this repository. When configured, Flask creates the `contact_messages` table if necessary and inserts validated form submissions into PostgreSQL.

## Run Locally

### Windows launcher

1. Download or clone the repository.
2. Double-click `RUN_PORTFOLIO.bat`.
3. Keep the **Portfolio Flask Server** window open.
4. The portfolio opens at `http://127.0.0.1:5000`.

### Manual setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
python app.py
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000).

Run the automated backend tests with:

```powershell
python -m unittest discover -s tests -v
```

## Project Structure

```text
.
��� app.py
��� static/
�   ��� css/styles.css
�   ��� js/app.js
�   ��� favicon.svg
��� templates/index.html
��� tests/test_app.py
��� requirements.txt
��� requirements-dev.txt
��� RUN_PORTFOLIO.bat
��� vercel.json
��� .gitignore
```

## Security and Privacy

- `.env` files, local databases, Python caches, Vercel metadata, and temporary outputs are ignored.
- No database credentials, API keys, visitor messages, or other secrets are included.
- Contact input is validated on the server before database insertion.
- Production credentials must be configured only through secure hosting environment variables.

## Credits and Acknowledgments

Developed by **M M Jagannath** as a college portfolio project. CareerCompass is acknowledged as a team project; the contribution described above reflects my actual involvement. Thanks to Jain University, Bengaluru, for the academic context and learning environment supporting this work.

## License

This repository is provided for educational and portfolio purposes.

