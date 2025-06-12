from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from .forms import NoteForm
from .models import Marker
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def save_map_state(request):
  request.session['map_center'] = (
    request.POST.get('map_center_lat'),
    request.POST.get('map_center_lon')
  )
  request.session['map_zoom'] = request.POST.get('map_zoom')


class GetNotes:
  def get_notes_data(self, request):
    markers = Marker.objects.filter(user=request.user)
    markers_data = [
      {
        'latitude': m.latitude,
        'longitude': m.longitude,
        'title': m.title,
        'description': m.description,
        'id': m.id,
        'created_at': m.created_at.strftime('%Y-%m-%d %H:%M'),
        'slug': m.slug,
        'image': m.image.url if m.image else '',
        'public_id': str(m.public_id),
      }
        for m in markers
    ]
    return markers_data


class MainView(LoginRequiredMixin, View, GetNotes):
  def post(self, request):

    save_map_state(request)

    form = NoteForm(request.POST)
    if form.is_valid():
      note = form.save(commit=False)
      note.user = request.user
      if 'image' in request.FILES:
        note.image = request.FILES['image']
      try:
          note.save()
          return redirect('map:index')
      except IntegrityError:
          messages.error(request, 'У вас уже есть заметка с таким заголовком.')
      return redirect('map:index')
    return render(request, 'map/main.html', context={'form': form, 'notes': self.get_notes_data(request), 'edit_mode': False})
    
  def get(self, request):
    return render(request, 'map/main.html', context={'form': NoteForm(), 'notes': self.get_notes_data(request), 'edit_mode': False})


class EditView(LoginRequiredMixin, View, GetNotes):
  def post(self, request, slug):

    save_map_state(request)

    mark = get_object_or_404(Marker, slug=slug, user=request.user)
    form = NoteForm(request.POST, instance=mark)
    if form.is_valid():
      if 'image' in request.FILES:
        mark.image = request.FILES['image']
      form.save()
      return redirect('map:index')
    return render(request, 'map/main.html', context={'form': form, 'notes': self.get_notes_data(request), 'edit_mode': True})
    
    
  def get(self, request, slug):
    mark = get_object_or_404(Marker, slug=slug, user=request.user)
    form = NoteForm(instance=mark)
    return render(request, 'map/main.html', context={'form': form, 'notes': self.get_notes_data(request), 'edit_mode': True})


class DeleteView(LoginRequiredMixin, View, GetNotes):
  def post(self, request, slug):

    save_map_state(request)
    
    note = get_object_or_404(Marker, slug=slug, user=request.user)
    note.delete()
    return redirect('map:index')
  
  def get(self, request):
    return redirect('map:index')


@login_required
def share_marker(request, public_id):
    original = get_object_or_404(Marker, public_id=public_id)

    if original.user == request.user:
      messages.error(request, 'Это уже ваша метка ;(')
      return redirect('map:index')
    
    if Marker.objects.filter(user=request.user, longitude=original.longitude, latitude=original.latitude).exists():
      messages.error(request, 'Это место занято ;(')
      return redirect('map:index')
    
    new_title = original.title
    if Marker.objects.filter(user=request.user, title=new_title).exists():
      new_title = original.title + '(копия)'

    new_marker = Marker(
      user=request.user,
      latitude=original.latitude,
      longitude=original.longitude,
      title=new_title,
      description=original.description,
      image=original.image
    )

    try:
      new_marker.save()
      messages.success(request, 'Метка успешно добавлена ;)')
    except Exception as e:
      messages.error(request, f'Ошибка при копировании: {e}')

    return redirect('map:index')