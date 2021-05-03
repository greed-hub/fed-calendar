from django.db import models

class Season(models.Model):
    name = models.CharField(max_length = 300, blank = True, null = True)
    title = models.CharField(max_length = 300, blank=True, null=True)
    endingText = models.CharField(max_length = 300, blank=True, null=True)
    date_start = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)
    totalexp = models.IntegerField(blank=True, null=True)
    expression = models.CharField(max_length = 300, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.CharField(max_length = 150, blank=True, null=True)
    image_modal = models.CharField(max_length = 150, blank=True, null=True)
    external_link = models.CharField(max_length=300, blank=True, null=True)

class EventStyle(models.Model):
    name = models.CharField(max_length = 50, blank=True, null=True)
    border_color = models.CharField(max_length = 50, blank=True, null=True)
    rowA_color = models.CharField(max_length = 50, blank=True, null=True)
    rowB_color = models.CharField(max_length = 50, blank=True, null=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    event_type = ((0, "official"),
                  (1, "double"),)
    name = models.CharField(max_length = 300, blank = True, null = True)
    event_type = models.IntegerField(choices = event_type, blank=True, null=True)
    image_modal = models.CharField(max_length=300, blank=True, null=True)
    image = models.CharField(max_length=300, blank=True, null=True)
    date_start = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)
    external_link = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    html_content = models.CharField(max_length=600, blank=True, null=True)
    event_style = models.ForeignKey(EventStyle, on_delete=models.CASCADE, null=True, blank=True)

class CommunityEvent(models.Model):
    event_platform = ((0, "common"),
                      (1, "pc"),
                      (2, "ps"),
                      (3, "xbox"),)

    timezone = ((0, "GMT-11"), (1, "GMT-10"), (2, "GMT-9"), (3, "GMT-8"), (4, "GMT-7"), (5, "GMT-6"), (6, "GMT-5"), (7, "GMT-4"),
                (8, "GMT-3"), (9, "GMT-2"), (10, "GMT-1"), (11, "GMT+0"), (12, "GMT+1"), (13, "GMT+2"), (14, "GMT+3"), (15, "GMT+4"), (16, "GMT+5"),
                (17, "GMT+6"), (18, "GMT+7"), (19, "GMT+8"), (20, "GMT+9"), (21, "GMT+10"), (22, "GMT+11"), (23, "GMT+12"),)

    name = models.CharField(max_length = 300, blank = True, null = True)
    event_platform = models.IntegerField(choices = event_platform, blank=True, null=True)
    image_modal = models.CharField(max_length=300, blank=True, null=True)
    image = models.CharField(max_length=300, blank=True, null=True)
    date_start = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)
    time_start = models.DateTimeField(blank=True, null=True)
    timezone = models.IntegerField(choices = timezone, blank=True, null=True)
    external_link = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    html_content = models.CharField(max_length=600, blank=True, null=True)
    event_style = models.ForeignKey(EventStyle, on_delete=models.CASCADE, null=True, blank=True)


class Weekly(models.Model):
    active = models.BooleanField(blank=True, null=True)
    name = models.CharField(max_length = 300, blank = True, null = True)
    title_en = models.CharField(max_length = 300, blank=True, null=True)
    title_pl = models.CharField(max_length = 300, blank=True, null=True)
    description_en = models.TextField(blank=True, null=True)
    description_pl = models.TextField(blank=True, null=True)
    short_description_en = models.CharField(max_length = 300, blank=True, null=True)
    short_description_pl = models.CharField(max_length = 300, blank=True, null=True)
    image_en = models.CharField(max_length = 150, blank=True, null=True)
    image_pl = models.CharField(max_length = 150, blank=True, null=True)

class Daily(models.Model):
    name = models.CharField(max_length = 300, blank = True, null = True)
    title_en = models.CharField(max_length = 300, blank=True, null=True)
    title_pl = models.CharField(max_length = 300, blank=True, null=True)
    description_en = models.TextField(blank=True, null=True)
    description_pl = models.TextField(blank=True, null=True)
    short_description_en = models.CharField(max_length = 300, blank=True, null=True)
    short_description_pl = models.CharField(max_length = 300, blank=True, null=True)
    image_en = models.CharField(max_length = 150, blank=True, null=True)
    image_pl = models.CharField(max_length = 150, blank=True, null=True)
