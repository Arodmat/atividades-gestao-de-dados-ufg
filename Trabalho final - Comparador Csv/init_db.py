from app_final import create_app
from models import db, User

def init_database():
    """Inicializa o banco de dados e cria um usuário admin padrão"""
    app = create_app()
    
    with app.app_context():
        # Remove todas as tabelas e recria
        db.drop_all()
        db.create_all()
        
        # Cria usuário admin padrão
        admin = User(
            nome='Administrador',
            email='admin@comparador.com',
            nivel='admin'
        )
        admin.set_password('admin123')
        
        # Cria usuário de teste
        teste = User(
            nome='Usuário Teste',
            email='teste@comparador.com',
            nivel='usuario'
        )
        teste.set_password('teste123')
        
        db.session.add(admin)
        db.session.add(teste)
        db.session.commit()
        
        print("Banco de dados inicializado com sucesso!")
        print("Usuários criados:")
        print("  Admin - Email: admin@comparador.com, Senha: admin123")
        print("  Teste - Email: teste@comparador.com, Senha: teste123")

if __name__ == '__main__':
    init_database()