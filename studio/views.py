from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Room, DesignProposal, DesignStyle, Material, Designer, Request
from .forms import RoomForm, DesignProposalForm, CustomUserCreationForm, RequestForm


def index(request):
    num_rooms = Room.objects.count()
    num_designers = Designer.objects.count()
    num_materials = Material.objects.count()

    recent_rooms = Room.objects.all()[:2]
    designers = Designer.objects.all()[:2]
    recent_materials = Material.objects.all()[:2]

    context = {
        'num_rooms': num_rooms,
        'num_designers': num_designers,
        'num_materials': num_materials,
        'recent_rooms': recent_rooms,
        'designers': designers,
        'recent_materials': recent_materials,
    }
    return render(request, 'index.html', context)


class RoomListView(LoginRequiredMixin, generic.ListView):
    model = Room
    template_name = 'studio/room_list.html'
    paginate_by = 2

    def get_queryset(self):
        return Room.objects.filter(user=self.request.user)


class RoomDetailView(LoginRequiredMixin, generic.DetailView):
    model = Room
    template_name = 'studio/room_detail.html'
    context_object_name = 'room'


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
    context_object_name = 'proposal_list'
    paginate_by = 3


class ProposalDetailView(generic.DetailView):
    model = DesignProposal
    template_name = 'studio/proposal_detail.html'
    context_object_name = 'proposal'


class ProposalCreate(PermissionRequiredMixin, CreateView):
    model = DesignProposal
    form_class = DesignProposalForm
    template_name = 'studio/proposal_form.html'
    permission_required = 'studio.can_make_proposal'
    success_url = reverse_lazy('proposals')

    def form_valid(self, form):
        messages.success(self.request, 'Вариант оформления создан!')
        return super().form_valid(form)


class ProposalUpdate(PermissionRequiredMixin, UpdateView):
    model = DesignProposal
    form_class = DesignProposalForm
    template_name = 'studio/proposal_form.html'
    permission_required = 'studio.can_make_proposal'
    success_url = reverse_lazy('proposals')


class ProposalDelete(PermissionRequiredMixin, DeleteView):
    model = DesignProposal
    template_name = 'studio/proposal_confirm_delete.html'
    success_url = reverse_lazy('proposals')
    permission_required = 'studio.can_make_proposal'


class AllRoomsListView(PermissionRequiredMixin, generic.ListView):
    model = Room
    template_name = 'studio/all_rooms_list.html'
    permission_required = 'studio.can_make_proposal'
    paginate_by = 2


class MaterialListView(generic.ListView):
    model = Material
    template_name = 'studio/material_list.html'
    paginate_by = 2


class MaterialCreate(PermissionRequiredMixin, CreateView):
    model = Material
    fields = ['name']
    template_name = 'studio/material_form.html'
    permission_required = 'studio.can_make_proposal'
    success_url = reverse_lazy('materials')


class MaterialUpdate(PermissionRequiredMixin, UpdateView):
    model = Material
    fields = ['name']
    template_name = 'studio/material_form.html'
    permission_required = 'studio.can_make_proposal'
    success_url = reverse_lazy('materials')


class MaterialDelete(PermissionRequiredMixin, DeleteView):
    model = Material
    template_name = 'studio/material_confirm_delete.html'
    permission_required = 'studio.can_make_proposal'
    success_url = reverse_lazy('materials')



class DesignerListView(generic.ListView):
    model = Designer
    template_name = 'studio/designer_list.html'
    context_object_name = 'designer_list'
    paginate_by = 2


class DesignerDetailView(generic.DetailView):
    model = Designer
    template_name = 'studio/designer_detail.html'
    context_object_name = 'designer'


class DesignerCreate(PermissionRequiredMixin, CreateView):
    model = Designer
    fields = ['first_name', 'last_name', 'experience_years', 'phone', 'photo', 'bio']
    template_name = 'studio/designer_form.html'
    permission_required = 'studio.can_make_proposal'
    success_url = reverse_lazy('designers')


class DesignerUpdate(PermissionRequiredMixin, UpdateView):
    model = Designer
    fields = ['first_name', 'last_name', 'experience_years', 'phone', 'photo', 'bio']
    template_name = 'studio/designer_form.html'
    permission_required = 'studio.can_make_proposal'
    success_url = reverse_lazy('designers')


class DesignerDelete(PermissionRequiredMixin, DeleteView):
    model = Designer
    template_name = 'studio/designer_confirm_delete.html'
    permission_required = 'studio.can_make_proposal'
    success_url = reverse_lazy('designers')



class RequestCreate(LoginRequiredMixin, CreateView):
    model = Request
    form_class = RequestForm
    template_name = 'studio/request_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Заявка успешно отправлена!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('my-requests')


class RequestListView(LoginRequiredMixin, generic.ListView):
    model = Request
    template_name = 'studio/request_list.html'
    context_object_name = 'request_list'
    paginate_by = 2

    def get_queryset(self):
        return Request.objects.filter(user=self.request.user)


class RequestDetailView(LoginRequiredMixin, generic.DetailView):
    model = Request
    template_name = 'studio/request_detail.html'
    context_object_name = 'request'

    def get_queryset(self):
        return Request.objects.filter(user=self.request.user)


class RequestDelete(LoginRequiredMixin, DeleteView):
    model = Request
    template_name = 'studio/request_confirm_delete.html'
    success_url = reverse_lazy('my-requests')

    def get_queryset(self):
        return Request.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Заявка удалена.')
        return super().delete(request, *args, **kwargs)


class AllRequestsListView(PermissionRequiredMixin, generic.ListView):
    model = Request
    template_name = 'studio/all_requests_list.html'
    context_object_name = 'request_list'
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
    return render(request, 'registration/register.html', {'form': form})