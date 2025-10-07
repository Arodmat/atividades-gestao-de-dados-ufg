# Comparador de CSV - Alterações Implementadas

Aplicação web desenvolvida em Flask para comparação de arquivos CSV, com sistema de permissões diferenciado entre usuários teste e administradores.

## Funcionalidades

- **Autenticação de usuários**: Sistema de login e registro com dois níveis de acesso
- **Upload de arquivos CSV**: Interface simples para upload de dois arquivos
- **Comparação inteligente**: Identifica linhas novas, removidas e alteradas
- **Visualização clara**: Resultados organizados em tabelas e abas
- **Sistema de permissões**:
  - **Usuários Teste**: Podem realizar comparações e ver resultados apenas na sessão atual
  - **Usuários Admin**: Têm acesso completo ao histórico de todas as comparações do sistema
- **Banco de dados PostgreSQL**: Armazenamento seguro de dados e histórico (apenas para admins)

## Sistema de Permissões

### Usuário Teste (`nivel = 'usuario'`)
- ✅ Pode fazer login no sistema
- ✅ Pode realizar comparações de CSV ilimitadas
- ✅ Visualiza os resultados completos na tela
- ❌ **NÃO** tem acesso ao menu "Histórico"
- ❌ **NÃO** tem comparações salvas no banco de dados
- ❌ **NÃO** pode ver comparações anteriores

### Usuário Administrador (`nivel = 'admin'`)
- ✅ Pode fazer login no sistema
- ✅ Pode realizar comparações de CSV ilimitadas
- ✅ Visualiza os resultados completos na tela
- ✅ **TEM** acesso ao menu "Histórico" 
- ✅ **TEM** comparações salvas automaticamente no banco
- ✅ **VÊ** todas as comparações realizadas por qualquer admin
- ✅ Pode visualizar detalhes de comparações anteriores

## Alterações Implementadas

### 1. Lógica de Aplicação (`app-updated.py`)
- **Rota `/`**: Diferencia conteúdo baseado no nível do usuário
- **Rota `/compare`**: Salva comparações no banco APENAS para admins
- **Rota `/history`**: Restringe acesso apenas para admins
- **Histórico**: Admins veem TODAS as comparações, não apenas as próprias

### 2. Interface do Usuário

#### Template Base (`base-updated.html`)
- Menu "Histórico" visível apenas para admins
- Badge visual indicando tipo de usuário (Admin/Teste)

#### Página Inicial (`index-updated.html`)
- Conteúdo adaptado ao tipo de usuário
- Usuários teste: Foco em realizar comparações
- Admins: Acesso a estatísticas e histórico recente

#### Página de Comparação (`compare-updated.html`)
- Aviso claro para usuários teste sobre não persistência
- Indicação visual quando comparação é salva (apenas admins)
- Botão histórico disponível apenas para admins

#### Histórico (`history-updated.html`)
- Título indicando "Visualização Administrativa"
- Coluna adicional mostrando qual usuário fez cada comparação
- Estatísticas do sistema completo

## Estrutura do Banco de Dados

As comparações são salvas **APENAS** quando realizadas por usuários administradores:

### Tabela `usuarios`
- Todos os usuários (teste e admin) são armazenados
- Campo `nivel` diferencia os tipos: `'usuario'` ou `'admin'`

### Tabela `comparacoes`
- **Apenas** comparações de usuários admin são salvas
- Campo `id_usuario` referencia qual admin fez a comparação
- Usuários teste não geram registros nesta tabela

## Usuários de Teste Pré-configurados

- **Admin**: `admin@comparador.com` / `admin123`
  - Acesso completo ao sistema e histórico
- **Teste**: `teste@comparador.com` / `teste123`
  - Comparações temporárias, sem persistência

## Instalação e Configuração

### 1. Instale as dependências
```bash
pip install -r requirements.txt
```

### 2. Configure PostgreSQL
```sql
CREATE DATABASE comparador_csv;
CREATE USER seu_usuario WITH PASSWORD 'sua_senha';
GRANT ALL PRIVILEGES ON DATABASE comparador_csv TO seu_usuario;
```

### 3. Configure variáveis de ambiente
```bash
cp .env.example .env
# Edite .env com suas configurações de banco
```

### 4. Inicialize o banco
```bash
python init_db.py
```

### 5. Execute a aplicação
```bash
# Substitua app.py pelo arquivo atualizado
python app-updated.py
```

## Fluxo de Uso

### Para Usuários Teste
1. Login → Página inicial com instruções
2. "Nova Comparação" → Upload dos arquivos
3. Visualização dos resultados (temporária)
4. Nova comparação quando necessário

### Para Usuários Admin
1. Login → Página inicial com estatísticas
2. "Nova Comparação" → Upload dos arquivos
3. Visualização dos resultados (salva automaticamente)
4. Acesso ao "Histórico" para ver todas as comparações
5. Detalhamento de comparações anteriores

## Segurança e Controles

- **Controle de acesso**: Middleware verifica nível do usuário
- **Isolamento de dados**: Usuários teste não deixam rastros no banco
- **Validação de permissões**: Rotas protegidas por decoradores
- **Interface adaptativa**: Menus e opções baseados em permissões

## Principais Benefícios da Alteração

1. **Separação clara de responsabilidades**: Teste vs. Produção
2. **Controle de dados**: Apenas comparações importantes são persistidas
3. **Experiência personalizada**: Interface adapta-se ao tipo de usuário  
4. **Segurança**: Controle granular de acesso a funcionalidades
5. **Escalabilidade**: Fácil adição de novos níveis de usuário

O sistema agora oferece uma experiência diferenciada onde usuários teste podem explorar a funcionalidade livremente, enquanto administradores têm controle total sobre o histórico e dados persistentes do sistema.
