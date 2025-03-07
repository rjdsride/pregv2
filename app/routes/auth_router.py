from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.services.ad_auth import authenticate_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    if request.session.get("user"):
        return RedirectResponse(url="/")
    return templates.TemplateResponse("login.html", {"request":request})

@router.post("/login")
async def login(request: Request):
    form_data = await request.form()
    username = form_data.get("username")
    password = form_data.get("password")

    auth_result = authenticate_user(username, password)

    if not auth_result.get("authenticated"):
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Credenciais Inválidas"
        })
    
    request.session["user"] = {
        "username": auth_result["username"],
        "email": auth_result["email"],
        "first_name": auth_result["first_name"],
        "last_name": auth_result["last_name"],
        "permissions": auth_result["permissions"],
    }

    return RedirectResponse(url="/", status_code=303)

@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login")