from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uuid

app = FastAPI()
templates = Jinja2Templates(directory="templates")

pastes = {}

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/paste", response_class=HTMLResponse)
def create_paste(request: Request, title: str = Form(...), content: str = Form(...)):
    paste_id = str(uuid.uuid4())[:8]
    pastes[paste_id] = {"title": title, "content": content}
    return templates.TemplateResponse("index.html", {
        "request": request, "paste_id": paste_id, "title": title, "content": content
    })

@app.get("/paste/{paste_id}", response_class=HTMLResponse)
def view_paste(request: Request, paste_id: str):
    paste = pastes.get(paste_id)
    if not paste:
        return HTMLResponse("Paste not found", status_code=404)
    return templates.TemplateResponse("index.html", {
        "request": request, "paste_id": paste_id, "title": paste["title"], "content": paste["content"]
    })
