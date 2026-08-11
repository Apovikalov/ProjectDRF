В Django-приложении на DRF создан файл docker-compose.yml, который использует 
сервисы web, db, redis, celery и celery-beat.

Созданы файлы .env и .env.example, в которых указаны параметры DATABASE
(NAME, USER, PASSWORD, HOST, PORT) и POSTGRES (DB, USER, PASSWORD, HOST).

Проект запускается через docker-compose с выполнением команды docker-compose up --build.