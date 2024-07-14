from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify # type: ignore
import firebase_admin # type: ignore
from firebase_admin import credentials, auth # type: ignore
from functools import wraps

app = Flask(__name__, static_folder='static')
app.secret_key = 'rahasia_kunci_yang_sangat_aman'  # Ganti dengan kunci yang benar-benar aman

# Inisialisasi Firebase Admin SDK
cred = credentials.Certificate("path/to/your/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Fungsi login_required (seperti sebelumnya)
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Silakan login terlebih dahulu.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        id_token = request.form.get('idToken')
        try:
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            session['user'] = {'uid': uid}
            return jsonify({"success": True})
        except:
            return jsonify({"success": False, "error": "Invalid token"})
    return render_template('login.html')

# Tambahkan rute signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        id_token = request.form.get('idToken')
        try:
            # Verifikasi token
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            
            # Di sini Anda bisa menambahkan logika tambahan,
            # seperti menyimpan informasi pengguna ke database Anda

            return jsonify({"success": True, "message": "Signup berhasil!"})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})
    return render_template('signup.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('user', None)
    flash('Anda telah berhasil logout.', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)