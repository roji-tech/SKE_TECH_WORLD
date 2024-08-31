from django.db import models
from main.models.models import School, Student, Subject, Term

# Create your models here.
# class ContinuousAssessment(models.Model):
#     subject = models.ForeignKey(
#         Subject, on_delete=models.CASCADE, related_name='continuous_assessments')
#     file = models.FileField(
#         upload_to='assessment/%Y/%m/%d/', null=True, blank=True)
#     student = models.ForeignKey(
#         Student, on_delete=models.CASCADE, related_name='continuous_assessments')
#     name = models.CharField(max_length=20)
#     score = models.DecimalField(
#         max_digits=5, decimal_places=2)

#     class Meta:
#         unique_together = ('subject', 'student', 'name')

#     def __str__(self):
#         return f"{self.name} - {self.subject.name} - {self.student.user.get_full_name()}"


class Examination(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name='examinations')
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='examinations')
    term = models.ForeignKey(
        Term, on_delete=models.CASCADE, related_name='examinations')
    date = models.DateField()
    # score = models.DecimalField(
    #     max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.subject.name} Exam - {self.term.name}"

    class Meta:
        unique_together = ('subject', 'term')


class Score(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    examination = models.ForeignKey(Examination, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f'{self.student.name} - {self.examination.subject.name}'


class Result(models.Model):
    examination = models.ForeignKey(
        Examination, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='results')
    # Score from the main exam
    score = models.DecimalField(max_digits=5, decimal_places=2)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('examination', 'student')

    def __str__(self):
        return f"Result for {self.student.user.get_full_name()} - {self.examination.subject.name}"

    def total_score_with_ca(self):
        # Calculate the total score by adding exam score and all CA scores
        ca_score = sum(ca.score for ca in self.student.continuous_assessments.filter(
            subject=self.examination.subject))
        return self.score + ca_score
