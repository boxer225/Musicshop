from django.contrib.auth import login, logout
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views.generic import ListView, TemplateView
from django.db.models import Q
from .forms import ContactForm, RegisterForm, LoginForm, CommentForm
from cart.forms import CartAddProductForm
from django.contrib import messages
from django.views.decorators.http import require_POST
from cart.cart import Cart

class Home(ListView):
    model = Catalog
    template_name = 'musicshop/index.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_ordering(self):
        ordering = self.request.GET.get('orderby')
        return ordering


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = Catalog.objects.all().count()
        context['order'] = f'{self.request.GET.get("orderby")}&'
        context['ordby'] = self.request.GET.get("orderby")
        return context


class ProductsByCategory(ListView):
    model = Catalog
    template_name = 'musicshop/category.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        ordering = self.request.GET.get('orderby')
        res = Catalog.objects.filter(category__slug=self.kwargs['slug'])
        if ordering:
            res = res.order_by(ordering)
        return res


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        context['count'] = Catalog.objects.filter(category__slug=self.kwargs['slug']).count()
        context['order'] = f'{self.request.GET.get("orderby")}&'
        return context


class Search(ListView):
    template_name = 'musicshop/search.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        ordering = self.request.GET.get('orderby')
        res = Catalog.objects.filter(Q(name__icontains=self.request.GET.get('s')) | Q(category__name__icontains=self.request.GET.get('s')))
        if ordering:
            res = res.order_by(ordering)
        return res

    def get_ordering(self):
        ordering = self.request.GET.get('orderby')
        return ordering


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f's={self.request.GET.get("s")}&'
        context['count'] = Catalog.objects.filter(Q(name__icontains=self.request.GET.get('s')) | Q(category__name__icontains=self.request.GET.get('s'))).count()
        context['order'] = f'{self.request.GET.get("orderby")}&'
        context['ordby'] = self.request.GET.get("orderby")
        return context


def get_message(request):
    form = ContactForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            subject = "Музыкальный магазин"
            body = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'message': form.cleaned_data['content'],
            }
            message = '\n'.join(body.values())
            try:
                send_mail(subject, message, 'admin@example.com', ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Найден некорректный заголовок')
            return redirect('home')
    form = ContactForm()
    return render(request, 'musicshop/contact.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = RegisterForm()

    return render(request, 'musicshop/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'musicshop/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


class Product(TemplateView):
    template_name = 'musicshop/product.html'
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Catalog.objects.get(slug=self.kwargs['slug'])
        context['category'] = Category.objects.get(catalog__slug=self.kwargs['slug'])
        context['count'] = Catalog.objects.get(slug=self.kwargs['slug']).comment.all().count()
        context['comments'] = Catalog.objects.get(slug=self.kwargs['slug']).comment.all()
        context.update({'CommentForm': CommentForm, 'cart_product_form': CartAddProductForm})
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['product'] = Catalog.objects.get(slug=self.kwargs['slug'])
        product_slug = self.kwargs.get('slug', None)
        form = CommentForm(self.request.POST)
        cart_product_form = CartAddProductForm(self.request.POST)
        if form.is_valid():
            form_upd = form.save(commit=False)
            form_upd.save()
            Catalog.objects.get(slug=self.kwargs['slug']).comment.add(form_upd)
            return HttpResponse(reverse_lazy('product', args=(product_slug, )))
        else:
            context['comments'] = Catalog.objects.get(slug=self.kwargs['slug']).comment.all()
            context.update({'CommentForm': form, 'cart_product_form': cart_product_form})
            return self.render_to_response(context)






