from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator


class Profile(models.Model):
    first_name = models.CharField(_("first_name"), max_length=255)
    last_name = models.CharField(_("last_name"), max_length=255)
    picture = models.ImageField(_("picture"), upload_to='profile', blank=True)
    intro_line = models.CharField(_("introduction line"), max_length=255, blank=True)
    jobs = models.ManyToManyField('my_profile.Job', blank=True)
    projects = models.ManyToManyField('my_profile.Project', blank=True)
    resume = models.FileField(_("resume"), blank=True)
    dob = models.DateField(_("date of birth"), blank=True, null=True)
    nationality = models.CharField(_("nationality"), max_length=255, blank=True)
    freelance = models.BooleanField(_("freelance"), default=True)
    phone_number = models.CharField(_("phone_number"), max_length=255, blank=True)
    address = models.CharField(_("address"), max_length=255, blank=True)
    languages = models.ManyToManyField('my_profile.Language', blank=True)
    email = models.EmailField(_("email"), blank=True, null=True)
    blurb = models.TextField(_("blurb"), blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def all_jobs(self):
        return self.jobs.all()

    @property
    def len_all_jobs(self):
        return len(self.all_jobs)

    @property
    def all_projects(self):
        return self.projects.all()

    @property
    def len_all_projects(self):
        return len(self.all_projects)

    @property
    def all_languages(self):
        return self.languages.all()

    @property
    def len_all_languages(self):
        return len(self.all_languages)

    @property
    def all_social_media_links(self):
        return self.social_media_links.all()

    @property
    def len_all_social_media_links(self):
        return len(self.all_social_media_links)

    @property
    def all_experience(self):
        return self.experience.all()

    @property
    def len_all_experience(self):
        return len(self.all_experience)

    @property
    def all_education(self):
        return self.education.all()

    @property
    def len_all_education(self):
        return len(self.all_education)

    @property
    def all_skills(self):
        return self.skills.order_by('technology__name')

    @property
    def len_all_skills(self):
        return len(self.all_skills)


class Job(models.Model):
    name = models.CharField(_("name"), max_length=255)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(_("name"), max_length=255)
    client = models.ForeignKey('my_profile.Client', on_delete=models.PROTECT, related_name='projects',
                               verbose_name='client', blank=True, null=True)
    desc = models.TextField(_("description"), blank=True)
    start_date = models.DateField(_("start date"), blank=True, null=True)
    end_date = models.DateField(_("end date"), blank=True, null=True)
    link = models.URLField(_("link"), blank=True)
    technologies = models.ManyToManyField('my_profile.Technology', blank=True)
    image = models.ImageField(_("image"), upload_to='projects', blank=True)

    def __str__(self):
        return self.name


class Technology(models.Model):
    name = models.CharField(_("name"), max_length=255)

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(_("name"), max_length=255)

    def __str__(self):
        return self.name


class About(models.Model):
    pass


class Language(models.Model):
    name = models.CharField(_("name"), max_length=255)

    BASIC = 'Basic'
    INTERMEDIATE = 'Intermediate'
    ADVANCED = 'Advanced'
    FLUENT = 'Fluent'
    NATIVE = 'Native'

    LEVEL_CHOICES = (
        (BASIC, 'Basic'),
        (INTERMEDIATE, 'Intermediate'),
        (ADVANCED, 'Advanced'),
        (FLUENT, 'Fluent'),
        (NATIVE, 'Native'),
    )
    level = models.CharField(_("level"), max_length=20, choices=LEVEL_CHOICES, default=BASIC)

    def __str__(self):
        return f"{self.name}({self.level})"


class SocialMedia(models.Model):
    name = models.CharField(_("name"), max_length=255)
    website = models.URLField(_("website"), blank=True)
    html_icon_class = models.CharField(_("html icon"), max_length=255)

    def __str__(self):
        return self.name


class SocialMediaLink(models.Model):
    profile = models.ForeignKey('my_profile.Profile', on_delete=models.CASCADE, related_name='social_media_links')
    social_media = models.ForeignKey('my_profile.SocialMedia', on_delete=models.CASCADE, related_name='links')
    link = models.URLField(_("link"))

    def __str__(self):
        return f"{self.profile.name} - {self.social_media.name}"


class Contact(models.Model):
    name = models.CharField(_("name"), max_length=255)
    email = models.EmailField(_("email"))
    comment = models.TextField(_("content"), blank=True)
    created = models.DateField(_("created"), auto_created=True, auto_now_add=True, editable=False)


class Experience(models.Model):
    profile = models.ForeignKey('my_profile.Profile', on_delete=models.CASCADE, related_name='experience')
    position = models.CharField(_("position"), max_length=255)
    company = models.CharField(_("company"), max_length=255)
    start_date = models.DateField(_("start date"), blank=True, null=True)
    end_date = models.DateField(_("end date"), blank=True, null=True)
    desc = models.TextField(_("description"), blank=True)

    def __str__(self):
        return f"{self.profile.name} - {self.position} - {self.company} - {self.start_date} to {self.end_date}"


class Education(models.Model):
    profile = models.ForeignKey('my_profile.Profile', on_delete=models.CASCADE, related_name='education')
    qualification = models.CharField(_("qualification"), max_length=255)
    school = models.CharField(_("school"), max_length=255)
    start_date = models.DateField(_("start date"), blank=True, null=True)
    end_date = models.DateField(_("end date"), blank=True, null=True)
    desc = models.TextField(_("description"), blank=True)

    def __str__(self):
        return f"{self.profile.name} - {self.qualification} - {self.school} - {self.start_date} to {self.end_date}"


class Skill(models.Model):
    profile = models.ForeignKey('my_profile.Profile', on_delete=models.CASCADE, related_name='skills')
    technology = models.ForeignKey('my_profile.Technology', on_delete=models.CASCADE, related_name='skills')
    rating = models.FloatField(_("rating"), default=1, validators=[MinValueValidator(0), MaxValueValidator(5)],)

    def __str__(self):
        return f"{self.profile.name} - {self.technology.name} - {self.rating}"
