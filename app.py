from flask import Flask, render_template, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = 'super-secret-key'
API_BASE_URL = 'http://localhost:9128'

@app.route('/')
def index():
    if 'token' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        response = requests.post(
            f'{API_BASE_URL}/login',
            json={
                'username': request.form['username'],
                'password': request.form['password']
            }
        )
        if response.status_code == 200:
            session['token'] = response.json().get('access_token')
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Неверные данные')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        response = requests.post(
            f'{API_BASE_URL}/register',
            json={
                'username': request.form['username'],
                'password': request.form['password'],
                'email': request.form['email'],
                'name': request.form['name'],
                'lastname': request.form['lastname']
            }
        )
        if response.status_code == 200:
            return redirect(url_for('login'))
        return render_template('register.html', error=response.text)
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'token' not in session:
        return redirect(url_for('login'))
    
    headers = {'Authorization': f'Bearer {session["token"]}'}
    
    habits = requests.get(f'{API_BASE_URL}/tasks', headers=headers).json()
    leaderboard = requests.get(f'{API_BASE_URL}/leaderboard', headers=headers).json()
    
    return render_template('dashboard.html', 
                         habits=habits,
                         leaderboard=leaderboard)

@app.route('/groups', methods=['GET', 'POST'])
def groups():
    if 'token' not in session:
        return redirect(url_for('login'))
    
    headers = {'Authorization': f'Bearer {session["token"]}'}
    
    if request.method == 'POST':
        requests.post(
            f'{API_BASE_URL}/create_group',
            json={'name': request.form['group_name']},
            headers=headers
        )
        return redirect(url_for('groups'))
    
    groups = requests.get(f'{API_BASE_URL}/groups', headers=headers).json()
    return render_template('groups.html', groups=groups)


@app.route('/logout')
def logout():
    session.pop('token', None)
    return redirect(url_for('login'))


@app.route('/add_task', methods=['POST'])
def add_habit():
    if 'token' not in session:
        return redirect(url_for('login'))
    
    headers = {'Authorization': f'Bearer {session["token"]}'}
    
    try:
        response = requests.post(
            f'{API_BASE_URL}/add_task',
            json={
                'name': request.form['name'],
                'score_amount': request.form['score_amount'],
                'group_id': request.form['group_id']
            },
            headers=headers
        )
        
        if response.status_code != 200:
            return render_template('error.html', error='Ошибка при создании привычки')
            
    except requests.exceptions.RequestException as e:
        return render_template('error.html', error=str(e))
    
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(port=5000, debug=True)