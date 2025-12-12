from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView,DeleteView
from django.urls import reverse_lazy
from .models import Customer
from .forms import CustomerForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Customer, Activity
from .forms import ActivityForm
from django.shortcuts import get_object_or_404


@login_required
@require_POST
def ajax_add_activity(request):
    customer_id = request.POST.get('customer_id')
    customer = get_object_or_404(Customer, id= customer_id)

    if customer.user != request.user:
        return JsonResponse({'message': '権限がありません'}, status=403)
    
    form = ActivityForm(request.POST)

    if form.is_valid():
        activity = form.save(commit=False)
        activity.customer = customer
        activity.save()

        response_data= {
            'message' : '成功しました' ,
            'activity_date': activity.activity_date.strftime('%Y-%m-%d'),
            'status' : activity.get_status_display(),
            'note' : activity.note,
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'message' : '入力内容に誤りがあります', 'errors' : form.errors}, status=400)
    


class CustomerListView(LoginRequiredMixin,ListView):
    """
    顧客一覧を表示するビュー
    """

    model = Customer

    template_name = "irodori_app/customer_list.html"

    context_object_name = "customers"

    paginate_by = 10

    #queryset = Customer.objects.all().order_by("company_name")

    def get_queryset(self):
        
        queryset = Customer.objects.filter(user=self.request.user)
        #queryset = super().get_queryset()
        
        query = self.request.GET.get("query")
        if query:
            queryset = queryset.filter(
                Q(company_name__icontains=query) |
                Q(contact_name__icontains=query) |
                Q(email__icontains=query) |
                Q(phone__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()

        return queryset

        #return Customer.objects.filter(user=self.request.user).order_by('company_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query', '')
        return context



class CustomerDetailView(LoginRequiredMixin,DetailView):
    """
    顧客詳細を表示するビュー
    """

    model = Customer

    template_name = "irodori_app/customer_detail.html"

    context_object_name = "customer"

    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)

class CustomerCreateView(LoginRequiredMixin,CreateView):

    model = Customer

    form_class = CustomerForm

    template_name = "irodori_app/customer_form.html"

    success_url = reverse_lazy('customer_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CustomerUpdateView(LoginRequiredMixin,UpdateView):

    model = Customer

    form_class = CustomerForm

    template_name = "irodori_app/customer_form.html"

    success_url = reverse_lazy('customer_list')

    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)


class CustomerDeleteView(LoginRequiredMixin,DeleteView):
    
    model = Customer

    template_name = "irodori_app/customer_confirm_delete.html"

    success_url = reverse_lazy('customer_list')

    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)