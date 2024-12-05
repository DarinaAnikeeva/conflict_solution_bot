from django.db import models
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'conflict_solution.settings'

class Situation(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name='Краткое название'
    )
    situation = models.TextField(
        verbose_name="Ситуация"
    )

    rivalry = models.CharField(
        max_length=50,
        verbose_name="Соперничество"
    )
    rivalry_answer = models.TextField(
        verbose_name="Ответ на соперничество",
        blank=True
    )

    device = models.CharField(
        max_length=50,
        verbose_name="Приспособление"
    )
    device_answer = models.TextField(
        verbose_name="Ответ на приспособление",
        blank=True
    )

    avoidance = models.CharField(
        max_length=50,
        verbose_name="Избегание"
    )
    avoidance_answer = models.TextField(
        verbose_name="Ответ на избегание",
        blank=True
    )

    compromise = models.CharField(
        max_length=50,
        verbose_name="Компромисс"
    )
    compromise_answer = models.TextField(
        verbose_name="Ответ на компромисс",
        blank=True
    )

    cooperation = models.CharField(
        max_length=50,
        verbose_name="Сотрудничество"
    )
    cooperation_answer = models.TextField(
        verbose_name="Ответ на сотрудничество",
        blank=True
    )

    class Meta:
        verbose_name = 'ситуация'

        verbose_name_plural = 'ситуации'

    def __str__(self):
        return f'{self.name}'



class Advice(models.Model):
    advice = models.TextField(
        verbose_name='совет'
    )

    class Meta:
        verbose_name_plural = 'советы'



class Feedback(models.Model):
    feedback = models.TextField(
        verbose_name='Обратная связь'
    )

    class Meta:
        verbose_name_plural = 'обратная связь'