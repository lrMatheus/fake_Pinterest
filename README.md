# FakePinterest

![Flask](https://img.shields.io/badge/Flask-Framework-blue)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Cloudinary](https://img.shields.io/badge/Cloudinary-Image%20Hosting-orange)
![MIT License](https://img.shields.io/badge/License-MIT-green)


## Descrição
FakePinterest é uma aplicação web inspirado no Pinterest, permitindo cadastro, login, upload de fotos e visualização de perfis. Utiliza Flask, banco de dados PostgreSQL (Render) e integração com Cloudinary para armazenamento de imagens.

## Instalação
1. Clone o repositório:
   ```powershell
   git clone <url-do-repositorio>
   ```
2. Instale as dependências:
   ```powershell
   pip install -r requirements.txt
   ```
3. Configure as variáveis de ambiente em um arquivo `.env`:
   - `SECRET_KEY`
   - `PG_USER`, `PG_PASSWORD`, `PG_HOST`, `PG_PORT`, `PG_DATABASE`
   - `CLOUDINARY_URL`
4. Execute o projeto:
   ```powershell
   python main.py
   ```



## Rotas
| Rota                | Método | Parâmetros         | Retorno                        | Descrição                                 |
|---------------------|--------|-------------------|--------------------------------|-------------------------------------------|
| `/`                 | GET/POST | email, senha      | Página inicial/login           | Login do usuário                          |
| `/criarconta`       | GET/POST | email, username, senha, confirma_senha | Página de cadastro           | Criação de nova conta                     |
| `/perfil/<id_usuario>` | GET   | id_usuario        | Página de perfil do usuário    | Exibe perfil e fotos do usuário           |
| `/feed`             | GET     | -                 | Página de feed                 | Exibe todas as fotos postadas             |
| `/logout`           | GET     | -                 | Redireciona para login         | Logout do usuário                         |
| `/postar`           | POST    | foto              | Redireciona para perfil        | Upload de nova foto                       |


## Funcionalidades
- Cadastro e login de usuários
- Upload de fotos com Cloudinary
- Visualização de perfis
- Feed com todas as fotos postadas
- Logout


## Tecnologias Utilizadas
- Flask
- Flask-WTF
- Flask-Login
- Flask-Bcrypt
- Flask-SQLAlchemy
- Python
- PostgreSQL
- Cloudinary
- HTML/CSS
- Jinja2
