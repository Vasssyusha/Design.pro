from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Room, DesignProposal
from .forms import RoomForm, DesignProposalForm, CustomUserCreationForm


def index(request):
    num_rooms = Room.objects.count()
    num_proposals = DesignProposal.objects.count()
    num_designers = User.objects.filter(groups__name='designers').count()
    recent_rooms = Room.objects.all()[:5]

    context = {
        'num_rooms': num_rooms,
        'num_proposals': num_proposals,
        'num_designers': num_designers,
        'recent_rooms': recent_rooms,
    }
    return render(request, 'index.html', context)


class RoomListView(LoginRequiredMixin, generic.ListView):
    model = Room
    template_name = 'studio/room_list.html'
    paginate_by = 5

    def get_queryset(self):
        return Room.objects.filter(user=self.request.user)


class RoomDetailView(LoginRequiredMixin, generic.DetailView):
    model = Room
    template_name = 'studio/room_detail.html'


class RoomCreate(LoginRequiredMixin, CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'studio/room_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Помещение успешно добавлено!')
        return super().form_valid(form)


class RoomUpdate(LoginRequiredMixin, UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'studio/room_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Помещение обновлено!')
        return super().form_valid(form)


class RoomDelete(LoginRequiredMixin, DeleteView):
    model = Room
    template_name = 'studio/room_confirm_delete.html'
    success_url = reverse_lazy('rooms')


class ProposalListView(generic.ListView):
    model = DesignProposal
    template_name = 'studio/proposal_list.html'
    paginate_by = 5


class ProposalDetailView(generic.DetailView):
    model = DesignProposal
    template_name = 'studio/proposal_detail.html'


class ProposalCreate(PermissionRequiredMixin, CreateView):
    model = DesignProposal
    form_class = DesignProposalForm
    template_name = 'studio/proposal_form.html'
    permission_required = 'studio.can_make_proposal'

    def form_valid(self, form):
        form.instance.designer = self.request.user
        messages.success(self.request, 'Предложение создано!')
        return super().form_valid(form)


class ProposalUpdate(PermissionRequiredMixin, UpdateView):
    model = DesignProposal
    form_class = DesignProposalForm
    template_name = 'studio/proposal_form.html'
    permission_required = 'studio.can_make_proposal'


class ProposalDelete(PermissionRequiredMixin, DeleteView):
    model = DesignProposal
    template_name = 'studio/proposal_confirm_delete.html'
    success_url = reverse_lazy('proposals')
    permission_required = 'studio.can_make_proposal'


class AllRoomsListView(PermissionRequiredMixin, generic.ListView):
    model = Room
    template_name = 'studio/all_rooms_list.html'
    permission_required = 'studio.can_make_proposal'
    paginate_by = 5


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return HttpResponseRedirect(reverse('index'))
    else:
        form = CustomUserCreationForm()
    return render(request, 'studio/register.html', {'form': form})