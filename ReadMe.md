# TestTastSoftSpace

### Этот мини-проект выполнен исходя тестового задания для компании "Soft Space".
### Проект включает в себя одно приложение "users" с классическими crud-операциями

### Использованные технологии
- Django + DRF
- Postgresql
- Docker
- DRF-simplejwt
- drf_yasg



### Что нужно для запуска?
- docker

### Как запускать?
- Клонировать этот репозиторий
- В терминал, открытом в корне проекта ввести ```docker-compose up --build 
  -d```
- Запустить тесты (опционально) ```docker exec -ti web python manage.py test```
- Создать суперюзера (опционально) ```docker exec -ti web python manage.py 
  createsuperuser```
- Перейти на http://0.0.0.0:8080/api/docs/ для просмотра документации

### Как тестировать через Postman?
- [POST] http://0.0.0.0:8080/api/users/ ```body={"username":<username>, 
  "password":<password>}```
- [POST]  http://0.0.0.0:8080/api/token/ ```body={"username":<username>, 
  "password":<password>}``` - получаем access, refresh токены
- [GET][PATCH][DELETE] http://0.0.0.0:8080/api/users/{id} ```headers=
  {"Authectication": Bearer  <access_token>```
- [POST]  http://0.0.0.0:8080/api/token/refresh/ ```body={"refresh": 
  <refresh_token>}``` - чтобы получить новый access-токен



