from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import NeedCreateForm
from .models import NeedRequest, HelpAssignment
from django.views.generic import ListView
from .utils import get_lat_long



class NeedCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = NeedCreateForm()
        return render(request, 'community_service/need_create.html', {'form': form})

    def post(self, request):
        form = NeedCreateForm(request.POST, request.FILES)
        if form.is_valid():
            need = form.save(commit=False)
            need.created_by = request.user

            lat, lon = get_lat_long(need.location)
            if lat is None or lon is None:
                form.add_error("location", "Invalid location. Please enter a valid address.")
                return render(request, 'community_service/need_create.html', {'form': form})

            need.latitude = lat
            need.longitude = lon
            need.save()

            return redirect('need_detail', pk=need.id)

        return render(request, 'community_service/need_create.html', {'form': form})


class NeedDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        need = get_object_or_404(NeedRequest, pk=pk)
        return render(request, "community_service/need_detail.html", {"need": need})


class NeedListView(ListView):
    model = NeedRequest
    template_name = 'community_service/need_list.html'
    context_object_name = 'needs'
    ordering = ['-created_at']   


class AcceptNeedView(LoginRequiredMixin, View):
    def post(self, request, need_id):
        need = get_object_or_404(NeedRequest, id=need_id)

        # If already taken
        if need.status != "Open":
            return redirect("need_detail", pk=need.id)

        # Create assignment
        HelpAssignment.objects.create(
            need=need,
            helper=request.user
        )

        need.status = "In Progress"
        need.save()

        return redirect("need_detail", pk=need.id)


class CancelNeedView(LoginRequiredMixin, View):
    def post(self, request, need_id):
        need = get_object_or_404(NeedRequest, id=need_id)

        # Only helper can cancel
        if not hasattr(need, "assignment"):
            return redirect("need_detail", pk=need.id)

        if need.assignment.helper != request.user:
            return redirect("need_detail", pk=need.id)

        need.assignment.delete()
        need.status = "Open"
        need.save()

        return redirect("need_detail", pk=need.id)



class CompleteNeedView(LoginRequiredMixin, View):
    def post(self, request, need_id):
        need = get_object_or_404(NeedRequest, id=need_id)

        # Only helper can complete
        if not hasattr(need, "assignment"):
            return redirect("need_detail", pk=need.id)

        if need.assignment.helper != request.user:
            return redirect("need_detail", pk=need.id)

        need.status = "Completed"
        need.save()

        return redirect("need_detail", pk=need.id)


