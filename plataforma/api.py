from ninja import NinjaAPI, Schema
from weasyprint import HTML, CSS
from django.conf import settings
import os

api = NinjaAPI()

class ContentSchema(Schema):
    html: str
    name: str

@api.post('/api/plano_alimentar')
def gerar_pdf(request, content: ContentSchema):
    bootstrap_css = os.path.join(settings.BASE_DIR, 'templates/static/plataforma/css/bootstrap.css')
    plano_alimentar = os.path.join(settings.BASE_DIR, 'templates/static/plataforma/css/plano_alimentar.css')
    style = os.path.join(settings.BASE_DIR, 'templates/static/plataforma/css/style.css')
    pdf_path = os.path.join(settings.BASE_DIR, 'media/plano_alimentar')

    html = HTML(string=content.html)
    css1 = CSS(bootstrap_css)
    css2 = CSS(plano_alimentar)
    css3 = CSS(style)

    try:
        html.write_pdf(f'{pdf_path}/{content.name}.pdf', stylesheets=[css1, css2, css3])

        return {"success": True,
                "body": f"/media/plano_alimentar/{content.name}.pdf"}

    except:
        return {"success": False,
                "body": ""}