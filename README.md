# Daily Diet API

API RESTful para controle de refeições diárias, implementada com Flask, SQLAlchemy e autenticação de sessão via Flask-Login.

## Visão Geral

Este projeto fornece uma API para:
- cadastro de usuários
- login/logout de sessão
- cadastro, consulta, atualização e remoção de refeições
- controle de acesso baseado em usuário e administrador

## Tecnologias

- Python 3.x
- Flask 2.3.3
- Flask-SQLAlchemy 3.0.5
- Flask-Login 0.6.3
- bcrypt 4.0.1
- PyMySQL 1.1.0
- MySQL 5.7 (compatível)

## Estrutura do Projeto

- `app.py` - entrada principal da aplicação
- `database.py` - configuração do SQLAlchemy
- `models/` - definições de `User` e `Meal`
- `routes/` - endpoints da API
- `requirements.txt` - dependências do Python
- `docker-compose.yml` - serviço MySQL para desenvolvimento

## Pré-requisitos

1. Python 3.x instalado
2. MySQL acessível ou container via Docker
3. `pip` instalado

## Instalação e execução

1. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure a conexão com o banco de dados em `app.py`:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@localhost/daily_diet_db'
   ```
   Altere também `app.config['SECRET_KEY']` para uma chave segura em produção.
4. Execute a aplicação:
   ```bash
   python app.py
   ```

## Uso com Docker Compose

O `docker-compose.yml` já define um serviço MySQL:

- usuário: `admin`
- senha: `admin123`
- banco: `daily_diet_db`

Para iniciar o banco de dados:
```bash
docker-compose up -d
```

## Endpoints da API

### Usuário

- `POST /create_user`
  - Corpo JSON: `{"username": "nome", "password": "senha"}`
  - Cria um usuário com a role padrão `user`.

- `POST /login`
  - Corpo JSON: `{"username": "nome", "password": "senha"}`
  - Autentica e inicia sessão.

- `GET /logout`
  - Encerra a sessão do usuário autenticado.

- `PUT /user/<user_id>`
  - Atualiza a senha do usuário.
  - Apenas o próprio usuário ou administradores podem atualizar.
  - Corpo JSON: `{"password": "nova_senha"}`

- `DELETE /user/<user_id>`
  - Remove um usuário.
  - Apenas administradores podem excluir usuários.

### Refeições

- `POST /meals`
  - Cria uma nova refeição para o usuário autenticado.
  - Corpo JSON exemplo:
    ```json
    {
      "name": "Almoço",
      "description": "Frango grelhado com salada",
      "date": "2026-05-02T12:30:00",
      "good_for_diet": true
    }
    ```

- `GET /meals`
  - Lista todas as refeições do usuário atual.
  - Administradores recebem todas as refeições.

- `GET /meal/<meal_id>`
  - Retorna os detalhes de uma refeição específica.

- `PUT /meal/<meal_id>`
  - Atualiza os dados de uma refeição existente.

- `DELETE /meal/<meal_id>`
  - Exclui uma refeição.

> Observação: todas as rotas de refeição exigem usuário autenticado.

## Observações importantes

- A senha de usuário é armazenada como hash usando `bcrypt`.
- As roles estão definidas em `models/user.py`; o valor padrão é `user`.
- Em produção, remova segredos e use variáveis de ambiente para banco de dados e chave secreta.

## Melhoria sugerida

- adicionar variáveis de ambiente para conexão com o banco
- criar endpoints de listagem de usuários e roles
- implementar testes automatizados
