import sqlite3

def init_db():
    conn = sqlite3.connect('scholarship.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        username TEXT PRIMARY KEY,
                        password TEXT
                    )''')
    
    # Create applications table
    cursor.execute('''CREATE TABLE IF NOT EXISTS applications (
                        username TEXT,
                        document TEXT,
                        status TEXT,
                        PRIMARY KEY (username, document),  -- Make (username, document) unique for conflict handling
                        FOREIGN KEY (username) REFERENCES users(username)
                    )''')
    
    # Insert the first user
    cursor.execute('INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)', ('user1', 'password1'))
    
    conn.commit()
    conn.close()

# Flask app code (unchanged)
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

# Upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('scholarship.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('upload'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    username = session['username']
    conn = sqlite3.connect('scholarship.db')
    cursor = conn.cursor()

    # Fetch already uploaded documents
    cursor.execute('SELECT document, status FROM applications WHERE username = ?', (username,))
    uploaded_docs = cursor.fetchall()
    uploaded_docs_dict = {doc[0]: doc[1] for doc in uploaded_docs}  # Convert to dict for easier lookup

    if request.method == 'POST':
        required_docs = [
            "10th_std_marksheet", "12th_std_marksheet", "diploma_certificate",
            "domicile_certificate", "aadhar_card", "family_income_certificate",
            "sc_st_certificate", "disability_certificate"
        ]

        try:
            for doc in required_docs:
                file = request.files.get(doc)
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    print(f"Uploaded {filename} to {app.config['UPLOAD_FOLDER']}")  # Debugging print statement

                    # Corrected SQL Execution
                    cursor.execute(
                        """
                        INSERT INTO applications (username, document, status) 
                        VALUES (?, ?, ?) 
                        ON CONFLICT(username, document) 
                        DO UPDATE SET status = EXCLUDED.status
                        """, 
                        (username, doc, 'Uploaded')
                    )

                else:
                    # If document is not uploaded, mark it as 'Not Uploaded'
                    cursor.execute(
                        """
                        INSERT INTO applications (username, document, status) 
                        VALUES (?, ?, ?) 
                        ON CONFLICT(username, document) 
                        DO UPDATE SET status = EXCLUDED.status
                        """, 
                        (username, doc, 'Not Uploaded')
                    )

            conn.commit()
            flash('Documents uploaded successfully.')
        except Exception as e:
            conn.rollback()
            flash(f'An error occurred while uploading documents: {e}')
            print(f"Error during file upload: {e}")  # Debugging print statement
        finally:
            conn.close()

        return redirect(url_for('track'))

    conn.close()

    # Render the upload page and show already uploaded documents
    return render_template('upload.html', uploaded_docs=uploaded_docs_dict)

@app.route('/track')
def track():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    username = session['username']
    conn = sqlite3.connect('scholarship.db')
    cursor = conn.cursor()

    # Check document upload status
    cursor.execute('SELECT document, status FROM applications WHERE username = ?', (username,))
    status = cursor.fetchall()
    conn.close()

    # Determine if all documents are uploaded
    documents_uploaded = all(doc[1] == 'Uploaded' for doc in status)
    
    # Steps for the tracker; only "Documents uploaded" should show tick if all documents are uploaded
    steps = {
        'Documents uploaded': documents_uploaded,
        'Digital verification': False,  # Always False unless additional logic is added
        'Payment process': False,       # Always False unless additional logic is added
        'Payment processed to your specified bank account.': False  # Always False
    }

    return render_template('track.html', steps=steps, documents_uploaded=documents_uploaded)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()  # Initialize the database and insert the first user
    app.run(debug=True)
