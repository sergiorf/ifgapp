import os
import errno
import uuid
import settings
from unicodedata import normalize


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


def gen_protocol():
    d = uuid.uuid4()
    res = d.hex
    return 'BR' + res[0:6]


def to_ascii(txt, codif='utf-8'):
    if not isinstance(txt, basestring):
        txt = unicode(txt)
    if isinstance(txt, unicode):
        txt = txt.encode('utf-8')
    return normalize('NFKD', txt.decode(codif)).encode('ASCII', 'ignore')


def doc_location(instance, filename):
    root_path = os.path.join(settings.MODEL_DOC_ROOT, type(instance).__name__, instance.nome)
    full_path = settings.MEDIA_ROOT + os.path.join('/', root_path)

    if not os.path.exists(full_path):
        os.makedirs(full_path)

    return os.path.join(root_path, filename).replace('\\', '/')

