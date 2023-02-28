from tasks.models import Contact

def context(request):
    context_data = dict()
    context_data['contact'] = Contact.objects.filter(id=1).first()
    return context_data