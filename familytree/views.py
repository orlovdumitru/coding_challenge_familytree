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
        date = request.POST.get('birth_date')#.split(' ')
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


def create_relation(request):
    if request.method == "POST":
        related_person = request.POST['relation-person']
        relation = request.POST['relation-type']
        person_id = request.POST['person_id']
        existing_relation = Relation.objects.filter(main_person_id=person_id, relative_id=related_person, relation_id=relation)
        if existing_relation.count() >= 1:
            return JsonResponse({'message': 'Relation already exists'}, status=400, safe=False)
        else:
            person_relation = Relation.objects.create(main_person_id=person_id, relative_id=related_person, relation_id=relation)
            mainRelation = RelationType.objects.get(pk=relation)

            if mainRelation.type == 'siblings' or mainRelation.type == 'cousin':
                Relation.objects.create(main_person_id=related_person, relative_id=person_id, relation_id=relation)
            elif mainRelation.type == 'parent':
                childRelation = RelationType.objects.filter(type='children').first()
                Relation.objects.create(main_person_id=related_person, relative_id=person_id, relation_id=childRelation.id)
            elif mainRelation.type == 'children':
                parentRelation = RelationType.objects.filter(type='parent').first()
                Relation.objects.create(main_person_id=related_person, relative_id=person_id, relation_id=parentRelation.id)
            # elif mainRelation == 'grandparent':
            #     nephewRelation = RelationType.objects.filter(type='nephew')
            #     Relation.objects.create(main_person = related_person, relative = person_id, relation = nephewRelation.id)
        return_data = Relation.objects.values(
                'relative__first_name',
                'relative__last_name',
                # 'relative__phone_number',
                # 'relative__email',
                # 'relative__address',
                # 'relative__birth_date',
                'relation__type',
                'relation__id'
            ).filter(main_person_id=person_id)
        return JsonResponse({"person_relation": return_data}, status=200, safe=False)


#### API IMPLEMENTATION ####
def get_relatives(request):
    relation = request.GET.get('relation', None)
    first_name = request.GET.get('first_name', None)
    last_name = request.GET.get('last_name', None)
    
    return_data = Relation.objects.values(
        'relative__first_name',
        'relative__last_name',
        'relative__phone_number',
        'relative__email',
        'relative__address',
        'relative__birth_date',
        'relation__type',
        'relation__id'
    )
    if relation:
        return_data = return_data.filter(relation__type=relation)
    if first_name:
        return_data = return_data.filter(main_person__first_name=first_name)
    if last_name:
        return_data = return_data.filter(main_person__last_name=last_name)
    if return_data.count() > 0:
        return JsonResponse(list(return_data), safe=False, status=200)
    else:
        return JsonResponse({'error':"No data found"}, status=404)
        
    # localhost:8000/get_relatives?first_name=Fname&last_name=Lname&relation=siblings