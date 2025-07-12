from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import ShortURL
from .forms import ShortURLForm
import random, string
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect



# Redirects anonymous users to login, authenticated users to dashboard
def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

@login_required
def search_results(request):
    query = request.GET.get('query', '').strip()
    results = ShortURL.objects.filter(user=request.user)

    if query:
        results = results.filter(
            Q(title__icontains=query) |
            Q(original_url__icontains=query) |
            Q(short_url__icontains=query)
        )

    return render(request, 'search_results.html', {
        'results': results,
        'query': query
    })


# Home view (Only ONE definition!)
def home(request):
    return render(request, 'home.html')


# User signup view
def signup(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'signup.html', {'form': form})


# User login view
def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        login(request, form.get_user())
        return redirect('dashboard')
    return render(request, 'login.html', {'form': form})


@csrf_protect
def shorten_url_view(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        # your shortening logic here
        return redirect('success_page')  # or render a response
    return render(request, 'shorten_url.html')

# Logout view
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# Generates a random 6-character short URL code (with uniqueness check)
def generate_short_url():
    while True:
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        if not ShortURL.objects.filter(short_url=code).exists():
            return code


# Adds a new URL with a maximum limit of 5 per user
@login_required
def add_url(request):
    url_count = ShortURL.objects.filter(user=request.user).count()

    if url_count >= 5:
        return render(request, 'add_url.html', {
            'error': '❌ You’ve reached the maximum limit of 5 URLs.'
        })

    form = ShortURLForm(request.POST or None)
    if form.is_valid():
        short = form.save(commit=False)
        short.user = request.user
        short.short_url = generate_short_url()
        short.save()
        return redirect('dashboard')

    return render(request, 'add_url.html', {'form': form})


# Displays all URLs with optional search and pagination
@login_required
def url_list(request):
    search_query = request.GET.get('search', '').strip()

    # Get current user's URLs
    urls = ShortURL.objects.filter(user=request.user)

    # Apply search filters
    if search_query:
        urls = urls.filter(
            Q(title__icontains=search_query) |
            Q(original_url__icontains=search_query) |
            Q(short_url__icontains=search_query)
        )

    # Pagination - 3 URLs per page
    paginator = Paginator(urls, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'url_list.html', {
        'page_obj': page_obj,
        'search_query': search_query
    })



# Edits a specific URL
@login_required
def edit_url(request, id):
    short = get_object_or_404(ShortURL, id=id, user=request.user)
    form = ShortURLForm(request.POST or None, instance=short)
    if form.is_valid():
        form.save()
        return redirect('dashboard')
    return render(request, 'edit_url.html', {'form': form})


# Deletes a specific URL
@login_required
def delete_url(request, id):
    short = get_object_or_404(ShortURL, id=id, user=request.user)
    short.delete()
    return redirect('dashboard')


# Redirects from short URL to the original URL
def redirect_url(request, code):
    short = get_object_or_404(ShortURL, short_url=code)
    short.visit_count += 1
    short.visited_at = timezone.now()
    short.save()
    return redirect(short.original_url)
