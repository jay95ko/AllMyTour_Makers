from django.db import models
from core.models import TimeStamp


class Maker(TimeStamp):
    makername = models.CharField(max_length=40)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, null=True, blank=True
    )
    makernickname = models.CharField(max_length=40)
    profile = models.ImageField(null=True, blank=True, upload_to="profile/")
    introduce = models.TextField(null=True, blank=True)
    idcard = models.ImageField(null=True, blank=True, upload_to="idcard/")
    bankbook_image = models.ImageField(null=True, blank=True, upload_to="bankbook/")
    status = models.CharField(max_length=40, null=True, blank=True)
    bank = models.CharField(max_length=45, null=True, blank=True)
    account_number = models.CharField(max_length=45, null=True, blank=True)
    account_holder = models.CharField(max_length=45, null=True, blank=True)
    productform = models.CharField(max_length=45, null=True, blank=True)
    language = models.ManyToManyField("Language", null=True, blank=True)
    region = models.ManyToManyField("Region", null=True, blank=True)
    category = models.ManyToManyField("Category", null=True, blank=True)
    tour = models.ManyToManyField("Tour", through="Maker_tour", null=True, blank=True)

    class Meta:
        db_table = "makers"


class DraftMaker(TimeStamp):
    makername = models.CharField(max_length=40, null=True, blank=True)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, null=True, blank=True
    )
    makernickname = models.CharField(max_length=40, null=True, blank=True)
    profile = models.ImageField(null=True, blank=True, upload_to="profile/")
    introduce = models.TextField(null=True, blank=True)
    idcard = models.ImageField(null=True, blank=True, upload_to="idcard/")
    bankbook_image = models.ImageField(null=True, blank=True, upload_to="bankbook/")
    status = models.CharField(max_length=40, null=True, blank=True)
    bank = models.CharField(max_length=45, null=True, blank=True)
    account_number = models.CharField(max_length=45, null=True, blank=True)
    account_holder = models.CharField(max_length=45, null=True, blank=True)
    productform = models.CharField(max_length=45, null=True, blank=True)
    language = models.ManyToManyField("DraftLanguage", null=True, blank=True)
    region = models.ManyToManyField("DraftRegion", null=True, blank=True)
    category = models.ManyToManyField("DraftCategory", null=True, blank=True)
    tour = models.ManyToManyField(
        "DraftTour", through="DraftMaker_Drafttour", null=True, blank=True
    )

    class Meta:
        db_table = "draft_makers"


class Sns(models.Model):
    kind = models.CharField(max_length=45, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    maker = models.ForeignKey("Maker", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "sns"


class DraftSns(models.Model):
    kind = models.CharField(max_length=45, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    maker = models.ForeignKey(
        "DraftMaker", on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        db_table = "draftsns"


class Evidence(models.Model):
    kind = models.CharField(max_length=45, null=True, blank=True)
    image = models.ImageField(upload_to="evidence/", null=True, blank=True)
    maker = models.ForeignKey("Maker", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "evidences"


class DraftEvidence(models.Model):
    kind = models.CharField(max_length=45, null=True, blank=True)
    image = models.ImageField(upload_to="evidence/", null=True, blank=True)
    maker = models.ForeignKey(
        "DraftMaker", on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        db_table = "draftevidences"


class Language(models.Model):
    Language = models.CharField(max_length=45, null=True, blank=True)

    class Meta:
        db_table = "languages"


class DraftLanguage(models.Model):
    Language = models.CharField(max_length=45, null=True, blank=True)

    class Meta:
        db_table = "draftlanguages"


class Region(models.Model):
    region = models.CharField(max_length=45, null=True, blank=True)

    class Meta:
        db_table = "regions"


class DraftRegion(models.Model):
    region = models.CharField(max_length=45, null=True, blank=True)

    class Meta:
        db_table = "draftregions"


class Category(models.Model):
    name = models.CharField(max_length=45, null=True, blank=True)

    class Meta:
        db_table = "categories"


class DraftCategory(models.Model):
    name = models.CharField(max_length=45, null=True, blank=True)

    class Meta:
        db_table = "draftcategories"


class Tour(models.Model):
    kind = models.CharField(max_length=45, null=True, blank=True)

    class Meta:
        db_table = "tours"


class DraftTour(models.Model):
    kind = models.CharField(max_length=45, null=True, blank=True)

    class Meta:
        db_table = "drafttours"


class Maker_tour(models.Model):
    tour = models.ForeignKey("Tour", on_delete=models.CASCADE, null=True, blank=True)
    maker = models.ForeignKey("Maker", on_delete=models.CASCADE, null=True, blank=True)
    limit_people = models.IntegerField(null=True, blank=True, default=0)
    limit_load = models.IntegerField(null=True, blank=True, default=0)

    class Meta:
        db_table = "maker_tours"


class DraftMaker_Drafttour(models.Model):
    tour = models.ForeignKey(
        "DraftTour", on_delete=models.CASCADE, null=True, blank=True
    )
    draftmaker = models.ForeignKey(
        "DraftMaker", on_delete=models.CASCADE, null=True, blank=True
    )
    limit_people = models.IntegerField(null=True, blank=True, default=0)
    limit_load = models.IntegerField(null=True, blank=True, default=0)

    class Meta:
        db_table = "draftmaker_drafttours"
