# Team Registration Web App

A full-stack web application built with Flask for team registration and payment processing.

## Features

- User registration with team details
- Payment via QR code
- Screenshot upload and UTR validation
- Admin dashboard for viewing submissions
- SQLite database with SQLAlchemy ORM
- Secure file uploads
- Email validation
- Mobile responsive UI with Bootstrap

## Setup Instructions

1. **Create Virtual Environment:**
   ```
   python -m venv venv
   ```

2. **Activate Virtual Environment:**
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

3. **Install Dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Add QR Code Image:**
   - Place your QR code image as `static/qr.png`

5. **Run the Application:**
   ```
   python app.py
   ```

6. **Access the App:**
   - Open http://127.0.0.1:5000/ in your browser
   - Admin login: username `admin`, password `admin`
   - Admin panel: http://127.0.0.1:5000/admin

## File Structure

```
.
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   ├── index.html        # Registration form
│   ├── admin.html        # Admin dashboard
│   └── login.html        # Admin login
└── static/
    ├── styles.css        # Custom styles
    ├── qr.png           # Payment QR code (add manually)
    └── uploads/         # Uploaded screenshots
```

## Security Notes

- Change the SECRET_KEY in app.py for production
- Use proper admin authentication in production
- File uploads are limited to images only
- UTR numbers must be unique