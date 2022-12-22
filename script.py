import random

from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned

from datacenter.models import Schoolkid
from datacenter.models import Mark
from datacenter.models import Chastisement
from datacenter.models import Lesson
from datacenter.models import Commendation
from datacenter.models import Subject


def fix_marks(schoolkid):
    try:
        child = Schoolkid.objects.get(full_name__icontains=schoolkid)
        marks = Mark.objects.filter(schoolkid=child, points__in=[2, 3])
        marks.update(points=5)
    except ObjectDoesNotExist:
        print('ОШИБКА: Такого ученика не существует. Проверьте вводимые данные')
    except MultipleObjectsReturned:
        print('ОШИБКА: Найдено более одного ученика - уточните данные.')


def remove_chastisements(schoolkid):
    try:
        child = Schoolkid.objects.get(full_name__icontains=schoolkid)
        chastisements = Chastisement.objects.filter(schoolkid=child)
        chastisements.delete()
    except ObjectDoesNotExist:
        print('ОШИБКА: Такого ученика не существует. Проверьте вводимые данные')
    except MultipleObjectsReturned:
        print('ОШИБКА: Найдено более одного ученика - уточните данные.')


def create_commendation(schoolkid, subject):
    try:
        child = Schoolkid.objects.get(full_name__icontains=schoolkid)
        subject = Subject.objects.get(
            title=subject,
            year_of_study=child.year_of_study
        )
        lesson = Lesson.objects.filter(
            year_of_study=child.year_of_study,
            group_letter=child.group_letter,
            subject=subject
        ).order_by('-date').first()

        commendations = [
            'Прекрасно!',
            'Ты меня приятно удивил!',
            'Очень хороший ответ!',
            'Так держать!',
            'Ты растешь над собой!',
            'Великолепно!',
            'Молодец!',
            'Гораздо лучше, чем я ожидал!',
            'Ты, как всегда, точен!',
            'Я поражен!',
            'Я вижу, как ты стараешься!',
            'Ты многое сделал, я это вижу!',
            'Замечательно!',
            'Потрясающе!',
            'С каждым разом у тебя получается всё лучше!'
        ]
        commendation_text = random.choice(commendations)
        Commendation.objects.create(
            text=commendation_text,
            created=lesson.date,
            schoolkid=child,
            subject=lesson.subject,
            teacher=lesson.teacher
        )
    except ObjectDoesNotExist:
        print('ОШИБКА: Такого ученика или предмета не существует. Проверьте вводимые данные')
    except MultipleObjectsReturned:
        print('ОШИБКА: Найдено более одного ученика - уточните данные.')
