import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-key-for-local')

# --- DB接続設定 ---
DB_USER = os.getenv('MYSQL_USER')
DB_PASS = os.getenv('MYSQL_PASSWORD')
DB_HOST = os.getenv('MYSQL_HOST', 'db-flask')
DB_NAME = os.getenv('MYSQL_DATABASE')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # ログインしていない時に飛ばされる関数名

# --- モデル定義 ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime)
    is_completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    # ユーザーと紐付けたい場合はここに user_id を追加しますが、
    # 今回は「自分一人専用」であれば、まずはアクセス制限だけで十分です。

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_request
def create_tables():
    db.create_all()
    # 環境変数からユーザー名とパスワードを取得
    admin_user = os.getenv('TODO_ADMIN_USER', 'hisao5232')
    admin_pass = os.getenv('TODO_ADMIN_PASS', 'your_default_password')

    # ユーザーがいない場合のみ作成
    if not User.query.filter_by(username=admin_user).first():
        hashed_password = generate_password_hash(admin_pass, method='pbkdf2:sha256')
        new_user = User(username=admin_user, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

# --- 認証ルート ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- メインルート（@login_required を追加） ---
@app.route('/')
@login_required
def index():
    todos = Todo.query.order_by(Todo.created_at.desc()).all()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form.get('title')
    description = request.form.get('description')
    due_date_str = request.form.get('due_date')
    
    due_date = datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else None
    
    if title:
        new_task = Todo(title=title, description=description, due_date=due_date)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
@login_required
def update(id):
    todo = Todo.query.get_or_404(id)
    todo.title = request.form.get('title')
    todo.description = request.form.get('description')
    todo.is_completed = 'is_completed' in request.form
    
    due_date_str = request.form.get('due_date')
    if due_date_str:
        todo.due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
        
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    