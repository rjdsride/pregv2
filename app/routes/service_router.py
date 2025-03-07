from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.utils.tasks import tarefas_por_tipo

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/atendimento", response_class=HTMLResponse)
async def mostrar_formulario_atendimento(request: Request):
    context = {
        "request": request,
        "tipos": list(tarefas_por_tipo.keys()),
        "tarefas_selecionadas": request.session.get("tarefas_selecionadas", []),
        "resultado": request.session.get("resultado", "")
    }
    return templates.TemplateResponse("atendimento.html", context)

@router.post("/atendimento")
async def processar_atendimento(request: Request):
    form_data = await request.form()
    tipo_selecionado = form_data.get("tipo_atendimento")
    tarefas_marcadas = form_data.getlist("tarefas")
    
    dados = tarefas_por_tipo[tipo_selecionado]
    texto_final = []
    
    if tarefas_marcadas:
        texto_final.append(dados['cabecalho'])
        texto_final.append("\nTarefas de conferência:")
        texto_final.extend([f"[X] {tarefa}" for tarefa in tarefas_marcadas])
        
        if dados['notas']:
            texto_final.append("\n" + "\n".join(dados['notas']))
        
        request.session["resultado"] = "\n".join(texto_final)
    else:
        request.session["resultado"] = "⚠️ Selecione pelo menos uma tarefa para gerar o padrão!"
    
    request.session["tipo_selecionado"] = tipo_selecionado
    request.session["tarefas_selecionadas"] = tarefas_marcadas
    
    return RedirectResponse(url="/atendimento", status_code=303)