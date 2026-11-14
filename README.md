# M M Jagannath — Personal Portfolio

A modern, responsive student portfolio for **M M Jagannath**, a second-year B.Tech Computer Science and Engineering (Artificial Intelligence and Machine Learning) student at Jain University, Bengaluru.

**Live website:** [https://mm-jagannath-portfolio.vercel.app/](https://mm-jagannath-portfolio.vercel.app/)

## Main features

- Responsive one-page portfolio for desktop, tablet and mobile
- Accessible navigation, keyboard focus states and reduced-motion support
- Original animations and interactive section highlighting
- CareerCompass project links
- Chess rating cards with the official FIDE profile link
- Contact form connected to a real Flask JSON API
- Server-side validation with accurate success and error responses
- SQLite storage for local development
- Neon PostgreSQL storage through `DATABASE_URL` in production
- Automated tests for page rendering, health checks, validation and database storage

## Technologies

- **Frontend:** HTML5, CSS3 and JavaScript
- **Backend:** Python and Flask
- **Local database:** SQLite
- **Production database:** Neon PostgreSQL
- **Deployment:** Vercel Python Functions

Python, Flask, PostgreSQL and the deployment platform are implementation technologies; they are not presented as personal skills on the portfolio.

## Run locally

### Easiest Windows method

Double-click `RUN_PORTFOLIO.bat`. It checks Python and Flask, starts the real
Flask backend, waits for the server, and opens the portfolio in your browser.
Keep the minimized **Portfolio Flask Server** window open while testing.

### Manual method

1. Open PowerShell in the project folder.
2. Create a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```powershell
   pip install -r requirements-dev.txt
   ```

4. Start the application:

   ```powershell
   python app.py
   ```

5. Open `http://127.0.0.1:5000`.

Submitted contact messages are stored locally in `instance/portfolio_messages.db`.

## Run automated tests

```powershell
python -m unittest discover -s tests -v
```

## API endpoints

### `GET /api/health`

Returns the backend status and active storage adapter.

### `POST /api/contact`

Accepts JSON:

```json
{
  "name": "Visitor Name",
  "email": "visitor@example.com",
  "message": "A message containing at least ten characters."
}
```

Successful messages receive HTTP `201`; invalid data receives HTTP `400` with field-specific errors.

## Production-ready storage configuration

The app uses SQLite by default during local development. In production, configure a managed PostgreSQL connection string as the secure `DATABASE_URL` environment variable in the hosting dashboard. Never commit the real value to source control.

When `DATABASE_URL` is present, Flask connects through `psycopg` and automatically creates the `contact_messages` table if required. Valid form submissions are inserted into PostgreSQL and receive HTTP `201`. If the variable is absent, the application falls back to the local SQLite database.

## Deployment

The repository contains `vercel.json` for the preferred function region. Vercel automatically detects the top-level Flask `app` object in `app.py` and installs the packages declared in `requirements.txt`.

Production secrets and database credentials must be configured in Vercel project settings and are deliberately excluded from this repository.

## Project structure

```text
.
├── app.py                     Flask application and API routes
├── static/
│   ├── css/styles.css         Responsive design system
│   ├── js/app.js              Navigation, animations and form integration
│   └── favicon.svg
├── templates/index.html       Portfolio page
├── tests/test_app.py          Backend and database tests
├── requirements.txt           Production dependencies
├── requirements-dev.txt       Local/test dependencies
├── RUN_PORTFOLIO.bat          Windows development launcher
└── vercel.json                Deployment configuration
```

## Security and privacy

- Environment files, local databases and Vercel project metadata are ignored by Git.
- No database credentials, API keys or visitor messages are stored in this repository.
- Contact input is validated on the server before database insertion.
- The application limits request and message sizes and returns accurate error responses.
