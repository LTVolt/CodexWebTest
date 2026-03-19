# Fase 2 — Modelação do domínio imobiliário

Nesta fase criamos o **modelo de dados completo** do portal para suportar anúncios, pesquisa, leads e favoritos.

## Modelos criados

- `UserProfile`: extensão do utilizador com papel (`cliente`, `agente`, `admin`) e telefone.
- `Location`: distrito, cidade, bairro e código postal.
- `PropertyType`: tipos de imóvel (apartamento, moradia, terreno...).
- `Amenity`: comodidades (piscina, elevador, garagem...).
- `Property`: entidade principal do imóvel/anúncio.
- `PropertyImage`: imagens de cada imóvel (com ordenação e imagem principal).
- `Lead`: pedidos de contacto/interesse por imóvel.
- `Favorite`: relação utilizador ↔ imóvel guardado.

## Relações importantes

- `Property.agent -> User`
- `Property.location -> Location`
- `Property.property_type -> PropertyType`
- `Property.amenities -> ManyToMany(Amenity)`
- `PropertyImage.property -> Property`
- `Lead.property -> Property`
- `Favorite(user, property)` com constraint única para evitar duplicados

## Regras de negócio já refletidas

- Tipos e estados de anúncio com `TextChoices`.
- Slugs automáticos em `PropertyType` e `Property`.
- Índices no modelo `Property` para filtros comuns (`status`, `listing_type`, `price`).
- `Favorite` sem duplicação por utilizador/imóvel (unique constraint).

## Próximos comandos (no ambiente local da turma)

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

A seguir, validar os modelos em `/admin` criando dados de teste para pesquisa e listagem.

## Documentação para estudo

- Django models: https://docs.djangoproject.com/en/stable/topics/db/models/
- Field types: https://docs.djangoproject.com/en/stable/ref/models/fields/
- Model Meta options: https://docs.djangoproject.com/en/stable/ref/models/options/
- Django admin: https://docs.djangoproject.com/en/stable/ref/contrib/admin/
