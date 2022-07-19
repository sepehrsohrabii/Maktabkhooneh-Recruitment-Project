from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator



User = get_user_model()


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Teacher(BaseModel):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)


class Course(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=10000, validators=[MinValueValidator(10000)])
    published_at = models.DateTimeField()
    
    @property
    def get_avg_score(self):
        reviews = Review.objects.filter(course=self)
        count = len(reviews)
        sum = 0
        if count == 0:
            return 'No Review Available'
        else:
            for rvw in reviews:
                sum += rvw.score
            return {'Average Score': (sum/count), 'Review Number': count}


class Review(BaseModel):
    SCORE_CHOICES = (
        (5, "5"),
        (4, "4"),
        (3, "3"),
        (2, "2"),
        (1, "1"),
    )

    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    score = models.SmallIntegerField(choices=SCORE_CHOICES)
