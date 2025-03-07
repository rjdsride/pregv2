from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    user = request.session.get("user")
    
    if not user:
        return RedirectResponse(url="/login")
    
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "user": {
                "username": user["username"],
                "email": user["email"],
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "permissions": user["permissions"]
            }
        }
    )