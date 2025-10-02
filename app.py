import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# --- Database Configuration ---
# Railway provides the database URL as an environment variable.
# If it's not found, we fall back to a local SQLite database for testing.
db_url = os.environ.get("DATABASE_URL", "sqlite:///notes.db")

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Database Model ---
# This class defines the table and its columns.
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Note {self.id}>'

# --- Application Routes ---
@app.route('/', methods=['GET', 'POST'])
def index():
    # If the form is submitted (POST request)
    if request.method == 'POST':
        note_content = request.form['content']
        if note_content: # Ensure content is not empty
            new_note = Note(content=note_content)
            db.session.add(new_note)
            db.session.commit()
        return redirect(url_for('index'))

    # If the page is loaded (GET request)
    else:
        all_notes = Note.query.order_by(Note.id.desc()).all()
        return render_template('index.html', notes=all_notes)

# --- Main Entry Point ---
# This block ensures the database table is created before the first request.
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # The host must be '0.0.0.0' to be accessible within Railway's container
    # The port is provided by the 'PORT' environment variable
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
