from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class JduUser(models.Model):
    class ExamStatusChoices(models.TextChoices):
        CONTRACT = 'cont', 'Shartnoma asosida'
        GRANT = 'grnt', 'Budjet asosida'
        FAILED = 'faiL', 'Qabul qilinmadingiz'

    jdu_id = models.PositiveBigIntegerField(primary_key=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)
    phone_num = PhoneNumberField()
    exam_score = models.FloatField()
    parents_phone_num = PhoneNumberField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    quote = models.CharField(max_length=4, choices=ExamStatusChoices, default=ExamStatusChoices.CONTRACT)

    def __str__(self):
        return str(self.jdu_id)
