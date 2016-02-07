from models import Servidor, Inventor
try:
    from functools import wraps
except:
    from django.utils.functional import wraps
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def has_permission(permissions=[], home_url=None):
    def decorator(func):
        def inner_decorator(request, *args, **kwargs):
            u = request.user
            if not u.is_superuser:
                try:
                    pessoa = Inventor.objects.get(nome=u.username)
                except Inventor.DoesNotExist:
                    try:
                        pessoa = Servidor.objects.get(nome=u.username)
                    except Servidor.DoesNotExist:
                        try:
                            pessoa = Pesquisador.objects.get(nome=u.username)
                        except Pesquisador.DoesNotExist:
                            return HttpResponseRedirect(reverse(home_url))
                for desc in permissions:
                    print desc
                    perm = pessoa.grupo.permissoes.filter(descricao=desc)
                    if not perm.exists():
                        return HttpResponseRedirect(reverse(home_url))
            return func(request, *args, **kwargs)
        return wraps(func)(inner_decorator)

    if home_url is None:
        home_url = 'index'
    return decorator


