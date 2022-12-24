import random

from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned

from datacenter.models import Schoolkid
from datacenter.models import Mark
from datacenter.models import Chastisement
from datacenter.models import Lesson
from datacenter.models import Commendation
from datacenter.models import Subject


def get_schoolkid(child_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__icontains=child_name)
        return schoolkid
    except ObjectDoesNotExist:
        print('ОШИБКА: Такого ученика не существует. Проверьте вводимые данные')
    except MultipleObjectsReturned:
        print('ОШИБКА: Найдено более одного ученика - уточните данные.')


def fix_marks(child_name):
    schoolkid = get_schoolkid(child_name)
    marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    marks.update(points=5)


def remove_chastisements(child_name):
    schoolkid = get_schoolkid(child_name)
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()


def create_commendation(child_name, subject):
    try:
        schoolkid = get_schoolkid(child_name)
        subject = Subject.objects.get(
            title=subject,
            year_of_study=schoolkid.year_of_study
        )
        lesson = Lesson.objects.filter(
            year_of_study=schoolkid.year_of_study,
            group_letter=schoolkid.group_letter,
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
            schoolkid=schoolkid,
            subject=lesson.subject,
            teacher=lesson.teacher
        )
    except ObjectDoesNotExist:
        print('ОШИБКА: Такого ученика или предмета не существует. Проверьте вводимые данные')
    except MultipleObjectsReturned:
        print('ОШИБКА: Найдено более одного ученика - уточните данные.')
