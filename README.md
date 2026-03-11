# CodexWebTest

Base inicial do projeto **Portal Imobiliário** com Python, Django e MySQL.

## Estrutura criada (Fase 1)

- `config/`: configurações principais do Django.
- `core/`: app inicial com homepage, URLs, testes e estrutura de templates/estáticos.
- `.env.example`: variáveis de ambiente para configuração local.
- `docs/fase-1-setup.md`: guia didático para a turma configurar o projeto passo a passo.

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

Abrir `http://127.0.0.1:8000/`.

## Verificações recomendadas

```bash
python manage.py test
python manage.py check
```
