from fastapi import FastAPI, Form
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from baysian_abtest import run_baysian_abtest, save_result_image

app = FastAPI()
templates = Jinja2Templates(directory="templates")
jinja_env = templates.env 

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse('index.html',{'request': request})

# Post
@app.post("/")
async def abtest_result_res(request: Request, segA_n:int = Form(), segA_cv:int = Form(), segB_n:int = Form(), segB_cv:int = Form(...)):
    winner, win_prob, beta_A, beta_B, beta_diff, bins = run_baysian_abtest(segA_n, segA_cv, segB_n, segB_cv)
    base64_img_res, base64_img_diff = save_result_image(beta_A, beta_B, beta_diff, bins)
    return templates.TemplateResponse(
        'index.html', 
        {
            'request': request,
            'segA_n': segA_n,
            'segA_cv': segA_cv,
            'segB_n': segB_n,
            'segB_cv': segB_cv,
            'winner': winner, 
            'win_prob': win_prob,
            'img_res': base64_img_res,
            'img_diff': base64_img_diff
        }
    )    