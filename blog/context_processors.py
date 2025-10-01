from .models import Notificacion

def notificaciones_context(request):
    if request.user.is_authenticated:
        return {
            "notificaciones_no_leidas": request.user.notificaciones.filter(leido=False).count()
        }
    return {"notificaciones_no_leidas": 0}
