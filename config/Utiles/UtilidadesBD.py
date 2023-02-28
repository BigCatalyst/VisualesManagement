

def setID_Siguiente(a):
    if a.id is None:
        l=getattr(a.__class__, 'objects').order_by('id')
        cantidad=len(l)
        if cantidad>0:
            a.id=l[cantidad-1].id+1
        else:
            a.id=1

