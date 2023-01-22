from fastapi import FastAPI
from starlette.requests import Request
from starlette.templating import Jinja2Templates

import baysian_abtest

app = FastAPI()

@app.get("/tools/baysian_abtest/")
async def read_abtest_result(segA_n: int = 0, segA_cv: int = 0, segB_n: int = 0, segB_cv: int = 0):
    winner, win_prob = baysian_abtest.run_baysian_abtest(segA_n=segA_n, segA_cv=segA_cv, segB_n=segB_n, segB_cv=segB_cv)
    return {"winner": winner, "win_prob": win_prob}

# http://127.0.0.1:8000/tools/baysian_abtest/?segA_n=1000&segA_cv=100&segB_n=1000&segB_cv=105 でサンプル作成できる。

templates = Jinja2Templates(directory="templates")
jinja_env = templates.env 

def index(request: Request):
    return templates.TemplateResponse('index.html',{'request': request})