import os
import errno
import uuid
import settings
from unicodedata import normalize
import re
from django.db.models import Q


def create_obj2(klass_obj, params):
    return create_obj({}, klass_obj, params)


def create_obj(id, klass_obj, params):
    obj = None
    if id:
        try:
            obj = klass_obj.objects.get(**id)
        except klass_obj.DoesNotExist:
            obj = None
    if obj is not None:
        print "%s (%s) ja existe" % (klass_obj.__name__, obj.id)
    else:
        obj = klass_obj(**params)
        obj.clean()
        obj.save()
        print "%s (%s) criado com sucesso..." % (klass_obj.__name__, obj.id)
    return obj


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def gen_num_pedido():
    d = uuid.uuid4()
    res = d.hex
    return 'BR' + res[0:6]


def gen_num_protocolo():
    d = uuid.uuid4()
    res = d.hex
    return res[0:8]


def gen_random():
    d = uuid.uuid4()
    str = d.hex
    return str[0:16]


def to_ascii(txt, codif='utf-8'):
    if not isinstance(txt, basestring):
        txt = unicode(txt)
    if isinstance(txt, unicode):
        txt = txt.encode('utf-8')
    return normalize('NFKD', txt.decode(codif)).encode('ASCII', 'ignore')


def doc_location(instance, filename):
    id = instance.nome if hasattr(instance, 'nome') else instance.codigo
    root_path = os.path.join(settings.MODEL_DOC_ROOT, type(instance).__name__, id)
    full_path = settings.MEDIA_ROOT + os.path.join('/', root_path)

    if not os.path.exists(full_path):
        os.makedirs(full_path)

    return os.path.join(root_path, filename).replace('\\', '/')


def normalize_query(query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall, normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in individual keywords, getting rid of unnecessary spaces
        and grouping quoted words together.
        Example:
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None  # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None  # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


def merge_dicts(*dict_args):
    '''
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    '''
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result