import os
import errno
import uuid


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