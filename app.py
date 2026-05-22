from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from models import db, User, Post, Reaction

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here' # セッション管理等に必要なキー
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'sns.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    posts = Post.query.filter_by(parent_id=None).order_by(Post.created_at.desc()).all()
    return render_template('index.html', posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            flash('Username already exists.')
            return redirect(url_for('register'))
            
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        return redirect(url_for('index'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
            
        flash('Please check your login details and try again.')
        return redirect(url_for('login'))
        
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/post', methods=['POST'])
@login_required
def create_post():
    content = request.form.get('content')
    if content:
        new_post = Post(user_id=current_user.id, content=content)
        db.session.add(new_post)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/post/<int:post_id>/reply', methods=['POST'])
@login_required
def reply_post(post_id):
    content = request.form.get('content')
    parent_post = Post.query.get_or_404(post_id)
    if content:
        new_reply = Post(user_id=current_user.id, content=content, parent_id=parent_post.id)
        db.session.add(new_reply)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/post/<int:post_id>/react', methods=['POST'])
@login_required
def react_post(post_id):
    reaction_type = request.form.get('reaction_type', 'like')
    post = Post.query.get_or_404(post_id)
    
    existing_reaction = Reaction.query.filter_by(user_id=current_user.id, post_id=post.id, reaction_type=reaction_type).first()
    
    if existing_reaction:
        db.session.delete(existing_reaction)
    else:
        new_reaction = Reaction(user_id=current_user.id, post_id=post.id, reaction_type=reaction_type)
        db.session.add(new_reaction)
        
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
