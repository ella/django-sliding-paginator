from django.db import models

class Comment(models.Model):
    text = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s written at %s" % (self.text, self.date)