from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from db import unique_url_check, add_pattern

app = FastAPI()


# Эндпоинт типа POST с полным адресом localhost:80/news_api/parser/add/news - сюда я шлю JSON в примере
@app.post("/api/add_pattern/")
async def root(request: Request):
    if request.method == 'POST':
        r_body = await request.json()
        print(r_body)
        name = r_body['name']
        url = r_body['url']
        user = r_body['username']
        title_path = r_body['schema']['title']['path']
        title_hash = r_body['schema']['title']['hash']
        time_path = r_body['schema']['time']['path']
        time_hash = r_body['schema']['time']['hash']
        short_path = r_body['schema']['shortContent']['path']
        short_hash = r_body['schema']['shortContent']['hash']
        main_path = r_body['schema']['mainArticle']['path']
        main_hash = r_body['schema']['mainArticle']['hash']
        author_path = r_body['schema']['author']['path']
        author_hash = r_body['schema']['author']['hash']
        print(name, "\n", user, "\n", url, "\n", title_path, "\n", title_hash, "\n", time_path, "\n", time_hash, "\n",
              short_path, "\n", short_hash, "\n", main_path, "\n", main_hash, "\n", author_path, "\n", author_hash, "\n")
        add_pattern(name, user, url, title_path, title_hash, time_path, time_hash, author_path,
                    author_hash, short_path, short_hash, main_path, main_hash)
        return JSONResponse({"success": True, "error": None})


# Ожидаю, получить JSON в котором два поля - success (boolean) и error (строка или null)


# Эндпоинт типа POST с полным адресом localhost:80/news_api/parser/unique -
# сюда я шлю JSON в котором всего одно поле строкового типа - url
@app.post("/api/check_pattern/")
async def unique(request: Request):
    if request.method == 'POST':
        r_body = await request.json()
        url = r_body['url']
        result, name = unique_url_check(url)
        if result:
            return JSONResponse({"success": True, "error": None, "unique": False, "name": name})
        elif result is not True:
            return JSONResponse({"success": True, "error": None, "unique": True, "name": name})


# Ожидаю, получить JSON в котором три поля - success (boolean, получилось приконектиться и
# получить данные из бд), error (строка или null) и unique(boolean, уникальный ли url)

