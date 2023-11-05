API

---

Получение пользователей  
GET: api/v1/users/  
Регистрация пользователя, поля: first_name, last_name, email, password, confirm_password, accept_policy  
POST: api/v1/users/  
При переходе по ссылке из письма редирект на страницу /confirm-email-success/?auth=<token>  
Авторизация, поля: email, password  
POST: api/v1/login/
Добавление клиента, поля: first_name, last_name, email, doctor_id(id пользователя, который добавляет клиента)  
POST: api/v1/users/add/  
Стандартная схема подтверждения по email  
Получение клиентов(user - ссылка на самого пользователя, doctor - ссылка на пользователя, являющегося доктором)  
GET: api/v1/users/  
Создание задачи, поля: title, text, assignment_type, status, tags  