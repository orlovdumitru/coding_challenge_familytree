import datetime
from .models import *
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

def home(request):
    return render(request, 'home.html')
    


def get_all(request):
    everyone = Person.objects.values()
    return JsonResponse(list(everyone), status=200, safe=False)


def person(request, person_id=None):
    if request.method == "POST":
        date = request.POST.get('birth_date').split(' ')
        bd = datetime.datetime.strptime(request.POST.get('birth_date'), '%b %d %Y')
        person, created = Person.objects.get_or_create(
            pk=person_id, 
            defaults={
                'first_name' : request.POST.get('first_name'),
                'last_name' : request.POST.get('last_name'),
                'phone_number' : request.POST.get('phone_number'),
                'email' : request.POST.get('email'),
                'address' : request.POST.get('address'),
                'birth_date' : bd,
                'created_by' : "Dima",
                'updated_by' : "Dima"
                })
        if not created:
            person.first_name = request.POST.get('first_name')
            person.last_name = request.POST.get('last_name')
            person.phone_number = request.POST.get('phone_number')
            person.email = request.POST.get('email')
            person.address = request.POST.get('address')
            person.birth_date = bd
            person.updated_by = "Dima"
            person.save()
        return redirect('home', permanent=True)
    else:
        if person_id:
            person = Person.objects.get(pk=person_id)
            all_persons = Person.objects.values()
            relations = RelationType.objects.values()

            # everyone = Person.objects.first()
            related_person = Relation.objects.values(
                'relative__first_name',
                'relative__last_name',
                # 'relative__phone_number',
                # 'relative__email',
                # 'relative__address',
                # 'relative__birth_date',
                'relation__type',
                'relation__id'
            ).filter(main_person=person)

            return render(request, 'person.html', {'person':person, 'all_persons': all_persons, 'relations': relations, 'related_person': related_person})
        return render(request, 'person.html')


def create_relation(request, person_id):
    if request.method == "POST":
        related_person = request.POST['relation-person']
        relation = request.POST['relation-type']
        existing_relation = Relation.objects.filter(main_person=person_id, relative=related_person, relation_id=relation)
        if existing_relation.count() >= 1:
            return JsonResponse({'message': 'Relation already exists'}, status=400, safe=False)
        else:
            person_relation = Relation.objects.create(main_person = person_id, relative = related_person, relation = relation)
        return JsonResponse(person_relation, status=200, safe=False)