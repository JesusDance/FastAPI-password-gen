import random
import uvicorn
from typing import Any, Annotated
from pydantic import BaseModel

from fastapi import FastAPI, HTTPException, status, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


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

    password = (random_symbols + random_letters_lower_case +
                       random_letters_upper_case + random_numbers)

    random.shuffle(password)
    my_password = "".join(password)
    return my_password


@app.get("/", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
def index(request: Request):
    return templates.TemplateResponse(request=request,
                                      name="index.html")


@app.post("/gen", response_class=HTMLResponse, status_code=status.HTTP_201_CREATED)
def gen_pass(request: Request, data: Annotated[FormData, Form()]):
    my_password = password_gen()

    return templates.TemplateResponse(request=request,
                                      name="index.html",
                                      context={"my_password": my_password})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
