from django.db import models
from django.core.validators import MinValueValidator


class CovidData(models.Model):
    s_no = models.IntegerField(primary_key=True)
    observation_date = models.DateField(null=False)
    state = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=False)
    last_update = models.DateTimeField()
    confirmed = models.IntegerField(validators=[MinValueValidator(0)])
    deaths = models.IntegerField(validators=[MinValueValidator(0)])
    recovered = models.IntegerField(validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.observation_date}_{self.country}_{self.state}"
