import random

from datacenter.models import Schoolkid
from datacenter.models import Mark
from datacenter.models import Chastisement
from datacenter.models import Lesson
from datacenter.models import Commendation


def fix_marks(schoolkid):
    child = Schoolkid.objects.get(full_name__contains=schoolkid)
    marks = Mark.objects.filter(schoolkid=child, points__in=[2, 3])
    marks.update(points=5)


def remove_chastisements(schoolkid):
    child = Schoolkid.objects.get(full_name__contains=schoolkid)
    chastisements = Chastisement.objects.filter(schoolkid=child)
    chastisements.delete()


def create_commendation(schoolkid, subject):
    child = Schoolkid.objects.get(full_name__contains=schoolkid)
    lesson = Lesson.objects.filter(
        year_of_study=child.year_of_study,
        group_letter=child.group_letter,
        subject__title=subject
    ).order_by('-date').first()

    commendations = [
        'Прекрасно!',
        'Ты меня приятно удивил!',
        'Очень хороший ответ!',
        'Так держать!',
        'Ты растешь над собой!',
        'Великолепно!'
    ]
    commendation_text = random.choice(commendations)
    Commendation.objects.create(
        text=commendation_text,
        created=lesson.date,
        schoolkid=child,
        subject=lesson.subject,
        teacher=lesson.teacher
    )
