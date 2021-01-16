from inspect import Parameter, Signature

def make_signature(names):
    return Signature([Parameter(name, Parameter.KEYWORD_ONLY) for name in names])


class ComponentMeta(type):

    def __new__(cls, name, bases, clsdict):
        clsobj = super().__new__(cls, name, bases, clsdict)
        sig = make_signature(clsobj.properties)
        setattr(clsobj, '__signature__', sig)
        return clsobj
