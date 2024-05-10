# Приложение голосования, которое нужно запустить
import uvicorn

if __name__ == '__main__':
    # Как тут правильно задать config?
    config = uvicorn.Config("app:app/app", port=8080, reload=True)
    server = uvicorn.Server(config)
    server.run()

# Команда для создания БД через Терминал (VS Code)
'''
docker run --name vote_db -p 5432:5432 -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=password -e POSTGRES_DB=vote_db -d postgres:16.2

docker pull postgres

docker run -d --name postgresCont -p 5432:5432 -e POSTGRES_PASSWORD=pass123 postgres
'''
# После этого подключаюсь к БД через расширение VS Code
# Введя аналогичные данные.

# Затем запускаю Fast Api через uvicorn
'''
Т.е. ввожу в терминале 

uvicorn app:app
'''
