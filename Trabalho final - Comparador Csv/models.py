from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    nivel = db.Column(db.String(20), default='usuario')
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com comparações
    comparacoes = db.relationship('Comparacao', backref='usuario', lazy=True)
    
    def set_password(self, password):
        self.senha_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.senha_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'

class Comparacao(db.Model):
    __tablename__ = 'comparacoes'
    
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    arquivo1 = db.Column(db.String(255), nullable=False)
    arquivo2 = db.Column(db.String(255), nullable=False)
    resumo = db.Column(db.Text)
    linhas_novas = db.Column(db.Integer, default=0)
    linhas_removidas = db.Column(db.Integer, default=0)
    linhas_alteradas = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<Comparacao {self.id} - {self.data}>'