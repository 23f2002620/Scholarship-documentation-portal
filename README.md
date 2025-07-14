# Scholarship Documentation Portal

## Overview

The Scholarship Documentation Portal is a web application built with Flask and SQLite to streamline the scholarship application and documentation process for students. It provides a secure, user-friendly interface for uploading required documents, tracking application status, and managing the overall workflow related to scholarship schemes.

---

## Features

- **User Authentication:** Secure login for students to access their personalized dashboard.
- **Document Upload:** Upload required documents (marksheets, certificates, Aadhar, etc.) in various formats (PDF, DOC, DOCX).
- **Application Tracking:** Visual tracker showing progress—from document upload to digital verification and payment.
- **Persistent Storage:** Uses SQLite for storing user credentials and document/application status.
- **Responsive UI:** Modern, clean interface with responsive design for ease of use.

---

## Prerequisites

- Python 3.x
- Flask
- SQLite3

---

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/23f2002620/Scholarship-documentation-portal
   cd Scholarship-documentation-portal
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the Database**
   The database is initialized automatically when you first run the app (see `init_db()` in `app.py`).

4. **Run the Application**
   ```bash
   python app.py
   ```

5. **Access the Portal**
   Open your browser and go to `http://127.0.0.1:5000`

---

## Usage

- **Login:** Use the default credentials or register (if registration is implemented).
- **Upload Documents:** Navigate to the upload page after login and submit the required documents.
- **Track Application:** Go to the tracking page to see your application’s progress.
- **Logout:** Use the logout link to end your session.

---

## File Structure

```
Scholarship-documentation-portal/
├── app.py
├── requirements.txt
├── scholarship.db
├── templates/
│   ├── login.html
│   ├── upload.html
│   └── track.html
├── static/
│   └── aicte_logo.png
└── uploads/
```

---

## Contributing

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/YourFeature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/YourFeature`
5. Open a pull request.

---

## License

This project is licensed under the MIT License.

---

## Acknowledgments

- Inspired by the need to simplify scholarship applications for students.
- Thanks to all contributors and users for their feedback and support.

**Contact:**  
For support or questions, email: saravanank171205@gmail.com
