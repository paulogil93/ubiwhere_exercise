# Exercício de Python & Django

## Abstract

O objetivo deste projeto incide na criação de uma REST API que permita a gestão de ocorrências em ambiente urbano.  Para chegar a uma implementação que respeitasse todas as *guidelines* e requisitos, foram usadas várias classes tais como *Serializers*, *Filters*, *ModelViewSets* e *Routers*. A lista de endpoints pode ser encontrada através do Swagger UI, acessível através do endpoint **docs/**.

## Instalação

Para poder correr este exercício é necessário configurar a base de dados, instalar as dependências e configurar grupos e permissões.

### Base de Dados

Como foi sugerido, a base de dados escolhida foi PostgreSQL com PostGIS. Para isso foi usada a imagem Docker mdillon/postgis.

#### Configuração do container

```
docker pull mdillon/postgis
docker run --name postgis -e POSTGRES_DB=ubiwhere -e POSTGRES_USER=ubiwhere -e POSTGRES_PASSWORD=j6PGae%PsQWaPf?SG4tj -d mdillon/postgis
```
####  Configuração no Django

Com o container da base de dados criado, é necessário configurar a BD nas definições do Django:

```python
DATABASES  =  {
	'default':  {
		'ENGINE':  'django.contrib.gis.db.backends.postgis',
		'NAME':  'ubiwhere',
		'USER':  'ubiwhere',
		'PASSWORD':  'j6PGae%PsQWaPf?SG4tj',
		'HOST':  '172.17.0.2',
		'PORT':  '5432',
	}
}
```

### Django

#### Criar Python Virtual Environment

```
python3 -m venv env
source env/bin/activate
```
#### Instalar dependências

Instalar todas as dependências necessárias ao funcionamento da API.

```
pip install -r requirements.txt

```
#### Migrar modelos para a base de dados

```
python exercise/manage.py makemigrations
python exercise/manage.py migrate
```
#### Criar um superuser

```
python exercise/manage.py createsuperuser
```

#### Configurar grupos e permissões

Para lidar com as diferentes permissões, é necessário criar dois grupos distintos e atribuir as permissões a cada um deles. Pode-se usar a shell do Django:

```
python exercise/manage.py shell
```

Importar os módulos correspondentes aos grupos e permissões:
```
from django.contrib.auth.models import Group, Permission
```

Criar os grupos:
```
users = Group.objects.get_or_create(name='Users')
admins = Group.objects.get_or_create(name='Administrators')
users = Group.objects.get(name='Users')
admins = Group.objects.get(name='Administrators')
```

Obter as permissões para o grupo Users:
```
add_incident = Permission.objects.get(codename='add_incident')
view_incident = Permission.objects.get(codename='view_incident')
```

Atribuir as permissões ao grupo Users:
```
users.permissions.add(add_incident)
users.permissions.add(view_incident)
```

Obter as permissões para o grupo Administrators:
```
add_user = Permission.objects.get(codename='add_user')
change_user = Permission.objects.get(codename='change_user')
view_user = Permission.objects.get(codename='view_user')
change_incident = Permission.objects.get(codename='change_incident')
```

Atribuir as permissões  ao grupo Administrators:
```
admins.permissions.add(add_incident)
admins.permissions.add(view_incident)
admins.permissions.add(add_user)
admins.permissions.add(change_user)
admins.permissions.add(view_user)
admins.permissions.add(change_incident)
```

#### Swagger UI
É necessário alterar um parâmetro no layout do rest_framework_swagger para que este funcione na nova versão do Django.
Basta editar o seguinte ficheiro e trocar *load staticfiles* por *load static*.
```
env/lib/python3.7/site-packages/rest_framework_swagger/templates/rest_framework_swagger/index.html
```
