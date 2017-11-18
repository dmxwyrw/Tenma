from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView

from .models import (Series, Issue, Character, Arc,
                     Team, Publisher, Creator, Settings,
                     Roles)
from .tasks import import_comic_files_task, reprocess_issue_task


class SeriesList(ListView):
    model = Series
    context_object_name = 'all_series'


class SeriesDetail(DetailView):
    model = Series


class IssueDetail(DetailView):
    model = Issue

    def get_context_data(self, **kwargs):
        context = super(IssueDetail, self).get_context_data(**kwargs)
        issue = self.get_object()
        context['roles_list'] = Roles.objects.filter(issue=issue)
        return context


class CharacterDetail(DetailView):
    model = Character

    def get_context_data(self, **kwargs):
        context = super(CharacterDetail, self).get_context_data(**kwargs)
        character = self.get_object()
        context['issue_list'] = character.issue_set.all(
        ).order_by('series__name', 'number')
        return context


class ArcDetail(DetailView):
    model = Arc

    def get_context_data(self, **kwargs):
        context = super(ArcDetail, self).get_context_data(**kwargs)
        arc = self.get_object()
        context['issue_list'] = arc.issue_set.all(
        ).order_by('series__name', 'number')
        return context


class TeamDetail(DetailView):
    model = Team

    def get_context_data(self, **kwargs):
        context = super(TeamDetail, self).get_context_data(**kwargs)
        team = self.get_object()
        context['issue_list'] = team.issue_set.all(
        ).order_by('series__name', 'number')
        return context


class PublisherDetail(DetailView):
    model = Publisher


class CreatorDetail(DetailView):
    model = Creator

    def get_context_data(self, **kwargs):
        context = super(CreatorDetail, self).get_context_data(**kwargs)
        creator = self.get_object()
        roles = Roles.objects.filter(creator=creator)
        context['issue_list'] = Issue.objects.filter(
            id__in=roles.values('issue_id'))
        return context


class ServerSettingsView(UpdateView):
    model = Settings
    fields = '__all__'
    template_name = 'comics/server_settings.html'

    def get_object(self, *args, **kwargs):
        return Settings.get_solo()

    def form_valid(self, form):
        self.object = form.save()
        return render(self.request, 'comics/server-settings-success.html', {'server-settings': self.object})


class IssueUpdateView(UpdateView):
    model = Issue
    fields = ['cvid']
    template_name = 'comics/issue_update.html'

    def form_valid(self, form):
        self.object = form.save()
        return render(self.request, 'comics/issue_update_success.html', {'issue-update': self.object})


class IssueDeleteView(DeleteView):
    model = Issue
    success_url = '/'


def read(request, slug):
    issue = get_object_or_404(Issue, slug=slug)
    return render(request, 'comics/read.html', {'issue': issue})


def importer(request):
    import_comic_files_task.delay()
    return HttpResponseRedirect('/')


def reprocess(request, slug):
    reprocess_issue_task.delay(slug)
    return HttpResponseRedirect('/issue/' + slug)


def update_issue_status(request, slug):
    issue = Issue.objects.get(slug=slug)

    if request.GET.get('complete', '') == '1':
        issue.leaf = 1
        issue.status = 2
        issue.save()
    else:
        issue.leaf = int(request.GET.get('leaf', ''))
        issue.status = 1
        issue.save()

    data = {'saved': 1}

    return JsonResponse(data)
