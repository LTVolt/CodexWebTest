# Fase 1 — Setup base do Portal Imobiliário (Django + MySQL)

Este guia documenta a base do projeto para a turma seguir e compreender cada passo.

## 1) Criar ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 2) Instalar dependências

```bash
pip install -r requirements.txt
```

Dependências usadas nesta fase:
- `Django`: framework web principal.
- `PyMySQL`: driver para Django comunicar com MySQL.

## 3) Configurar variáveis de ambiente

Copiar ficheiro de exemplo:

```bash
cp .env.example .env
```

Editar `.env` com as credenciais locais de MySQL.

## 4) Criar base de dados no MySQL

Exemplo via terminal mysql:

```sql
CREATE DATABASE realestate_portal CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'portal_user'@'localhost' IDENTIFIED BY 'change-me';
GRANT ALL PRIVILEGES ON realestate_portal.* TO 'portal_user'@'localhost';
FLUSH PRIVILEGES;
```

## 5) Aplicar migrações e correr o projeto

```bash
python manage.py migrate
python manage.py runserver
```

Aceder a: `http://127.0.0.1:8000/`

## 6) Documentação oficial (obrigatória para estudo)

- Django tutorial: https://docs.djangoproject.com/en/stable/intro/tutorial01/
- Django databases: https://docs.djangoproject.com/en/stable/ref/databases/
- Django models: https://docs.djangoproject.com/en/stable/topics/db/models/
- MySQL manual: https://dev.mysql.com/doc/

## 7) Checklist de aprendizagem da turma

- [ ] Explicar a função de `INSTALLED_APPS`, `MIDDLEWARE` e `TEMPLATES`
- [ ] Compreender por que usamos `.env` para segredos
- [ ] Saber criar e aplicar migrações
- [ ] Validar ligação Django ↔ MySQL
- [ ] Confirmar que ficheiros estáticos carregam na página inicial
