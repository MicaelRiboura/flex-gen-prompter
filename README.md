# FlexGenPropter


## Como começar

### 1. Crie um ambiente venv do python
```
python -m venv env
```

### 2. Inicialize o ambiente venv
```
source ./env/bin/activate
```


### 3. Instale as dependências do projeto
```
pip install -r requirements.txt
```

### 4. Crie as tabelas do banco de dados
```
python manage.py migrate
```

### 5. Execute a aplicação
```
python manage.py runserver
```

### 6. Execute o redis com Docker
```
run -d --name redis -p 6379:6379 redis
```

### 7. Execute o worker do celery
```
celery -A flexgenprompter.celery worker -l info -P gevent
```