from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Profile, Contact
from .forms import ContactForm
from math import floor


class ProjectPanel:
    def __init__(self, project, panel_number, tech):
        self.project = project
        self.panel = f"panel-{panel_number}"
        self.tech = tech

    @property
    def tech_len(self):
        return len(self.tech)


class SkillLayout:
    def __init__(self):
        self.row_len = 6
        self.row_1 = []
        self.row_2 = []

    class Skill:
        def __init__(self, skill):
            self.technology = skill.technology
            self.rating = skill.rating
            self.stars = []
            for i in range(floor(skill.rating)):
                self.stars.append('')
            self.half = (skill.rating % 1) != 0

    def add_skill(self, skill):
        if len(self.row_1) < self.row_len:
            self.row_1.append(SkillLayout.Skill(skill))
        elif len(self.row_2) < self.row_len:
            self.row_2.append(SkillLayout.Skill(skill))


def my_profile(request):
    profile = get_object_or_404(Profile, pk=1)
    project_panels = []
    for idx, project in enumerate(profile.projects.order_by('start_date')):
        project_panels.append(ProjectPanel(project, idx+1, project.technologies.all()))
    skill_layout = SkillLayout()
    for skill in profile.all_skills:
        skill_layout.add_skill(skill)
    context = {
        'profile': profile,
        'name': profile.name,
        'intro_line': profile.intro_line,
        'first_job': profile.jobs.all()[0] if len(profile.jobs.all()) > 0 else '',
        'jobs': profile.jobs.all()[1:] if len(profile.jobs.all()) > 1 else [],
        'project_panels': project_panels,
        'main_picture': profile.picture,
        'contact_form': ContactForm(),
        'skill_layout': skill_layout,
    }
    return render(request, 'profile/index.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            contact_data = Contact(
                name=form.cleaned_data.get('name'),
                email=form.cleaned_data.get('email'),
                comment=form.cleaned_data.get('comment'),
            )
            contact_data.save()
        return HttpResponse("success")
