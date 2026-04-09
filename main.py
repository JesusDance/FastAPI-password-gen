"""
FastAPI password generator

Description:

- This is a simple FastAPI password generator
- Input "admin" into username and password

Features:

- using BaseModel as registration and login only for "admin"
- using random module for generating sixteen symbols password
- managing styles with Bootstrap
- Jinja2 templates
- simple Dockerfile

Routes:

-'/': -main page
-'/gen/': - route for generating password
"""

import random
from typing import Any, Annotated

import uvicorn
from fastapi import FastAPI, status, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


class FormData(BaseModel):
    username: str
    password: str


def password_gen():
    symbols = "`~!@#$%^&*()_+-=/*|[]:;'<>,.?"
    letters_lower_case = "qwertyuiopasdfghjklzxcvbnm"
    letters_upper_case = "QWERTYUIOPASDFGHJKLZXCVBNM"
    numbers = "0123456789"

    random_symbols = random.sample(symbols, k=4)
    random_letters_lower_case = random.sample(letters_lower_case, k=4)
    random_letters_upper_case = random.sample(letters_upper_case, k=4)
    random_numbers = random.sample(numbers, k=4)

    password = (
        random_symbols
        + random_letters_lower_case
        + random_letters_upper_case
        + random_numbers
    )

    random.shuffle(password)
    return "".join(password)


@app.get("/", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
def index(request: Request) -> Any:
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/gen", response_class=HTMLResponse, status_code=status.HTTP_201_CREATED)
def gen_pass(request: Request, data: Annotated[FormData, Form()]) -> Any:
    username = data.username
    password = data.password

    if username == "admin" and password == "admin":
        my_password = password_gen()
        return templates.TemplateResponse(
            request=request, name="index.html", context={"my_password": my_password}
        )
    else:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"error": "Invalid username or password"},
        )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
