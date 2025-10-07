from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_required, current_user
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import json

from config import Config
from models import db, User, Comparacao
from auth import auth_bp
from csv_comparator import CSVComparator

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializa extensões
    db.init_app(app)
    
    # Configuração do Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Registra blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # Cria diretório de uploads se não existir
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Função para verificar extensão do arquivo
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'csv'
    
    @app.route('/')
    @login_required
    def index():
        # Para usuários teste, mostrar apenas estatísticas básicas sem histórico
        if current_user.nivel == 'usuario':
            return render_template('index.html', show_history=False)
        # Para admins, mostrar últimas comparações de TODOS os usuários
        else:
            recent_comparisons = Comparacao.query.order_by(Comparacao.data.desc()).limit(5).all()
            return render_template('index.html', show_history=True, recent_comparisons=recent_comparisons)
    
    @app.route('/compare', methods=['GET', 'POST'])
    @login_required
    def compare():
        if request.method == 'POST':
            # Verifica se os arquivos foram enviados
            if 'file1' not in request.files or 'file2' not in request.files:
                flash('Por favor, selecione ambos os arquivos CSV.', 'error')
                return redirect(url_for('compare'))
            
            file1 = request.files['file1']
            file2 = request.files['file2']
            
            # Verifica se os arquivos têm nomes
            if file1.filename == '' or file2.filename == '':
                flash('Por favor, selecione ambos os arquivos CSV.', 'error')
                return redirect(url_for('compare'))
            
            # Verifica se são arquivos CSV
            if not (allowed_file(file1.filename) and allowed_file(file2.filename)):
                flash('Por favor, envie apenas arquivos CSV.', 'error')
                return redirect(url_for('compare'))
            
            try:
                # Salva os arquivos
                filename1 = secure_filename(file1.filename)
                filename2 = secure_filename(file2.filename)
                
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename1 = f"{current_user.id}_{timestamp}_1_{filename1}"
                filename2 = f"{current_user.id}_{timestamp}_2_{filename2}"
                
                filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
                filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
                
                file1.save(filepath1)
                file2.save(filepath2)
                
                # Compara os arquivos
                key_column = request.form.get('key_column') or None
                comparator = CSVComparator(key_column)
                
                result = comparator.compare_csvs(filepath1, filepath2)
                formatted_result = comparator.format_results_for_display(result)
                
                # SEMPRE salva no banco de dados (tanto para teste quanto para admin)
                resumo_texto = comparator.generate_summary_text(result)
                
                comparacao = Comparacao(
                    id_usuario=current_user.id,
                    arquivo1=file1.filename,
                    arquivo2=file2.filename,
                    resumo=resumo_texto,
                    linhas_novas=result['summary']['new_rows'],
                    linhas_removidas=result['summary']['removed_rows'],
                    linhas_alteradas=result['summary']['modified_rows']
                )
                
                db.session.add(comparacao)
                db.session.commit()
                comparison_id = comparacao.id
                
                # Remove arquivos temporários
                os.remove(filepath1)
                os.remove(filepath2)
                
                return render_template('compare.html', 
                                     result=formatted_result, 
                                     comparison_id=comparison_id,
                                     is_admin=current_user.nivel == 'admin')
                
            except Exception as e:
                flash(f'Erro ao processar arquivos: {str(e)}', 'error')
                # Remove arquivos se houver erro
                try:
                    if 'filepath1' in locals():
                        os.remove(filepath1)
                    if 'filepath2' in locals():
                        os.remove(filepath2)
                except:
                    pass
                return redirect(url_for('compare'))
        
        return render_template('compare.html')
    
    @app.route('/history')
    @login_required
    def history():
        # Apenas admins podem acessar o histórico
        if current_user.nivel != 'admin':
            flash('Acesso negado. Apenas administradores podem visualizar o histórico.', 'error')
            return redirect(url_for('index'))
        
        page = request.args.get('page', 1, type=int)
        # Admin vê TODAS as comparações de TODOS os usuários (teste e admin)
        comparacoes = Comparacao.query.order_by(Comparacao.data.desc())\
                                    .paginate(page=page, per_page=10, error_out=False)
        
        return render_template('history.html', comparacoes=comparacoes)
    
    @app.route('/comparison/<int:comparison_id>')
    @login_required
    def view_comparison(comparison_id):
        # Apenas admins podem ver detalhes de comparações
        if current_user.nivel != 'admin':
            flash('Acesso negado. Apenas administradores podem visualizar detalhes de comparações.', 'error')
            return redirect(url_for('index'))
        
        comparacao = Comparacao.query.get_or_404(comparison_id)
        return render_template('comparison_detail.html', comparacao=comparacao)
    
    return app

def init_db():
    """Inicializa o banco de dados"""
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Banco de dados inicializado com sucesso!")

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)