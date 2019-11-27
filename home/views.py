from django.shortcuts import render
from .models import Provider, Visit
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.shortcuts import redirect
from .forms import NewProvider


# Create your views here.
def homeView(request):
	providersList = Provider.objects.all()

	data = []
	
	for prov in providersList:
		line={}
		visits = Visit.objects.filter(provider=prov).order_by('-dateOfVisit')
		print(prov.logo)
		line = {
				'name': prov.name,
				'shortcut': prov.shortcut,
				'logo': prov.logo,
				'visits': [],
				'last_visit': visits[0],
				'visits': visits[1:10]}
		data.append(line)	
		#print(line['last_visit'].dateOfVisit)
	return render(request, 'home.html', {'providers': data})
	

def login_form(request):
	return render(request, 'login_form.html', {})

def login_view(request):
	username = request.POST.get('username', None)
	password = request.POST.get('password', None)
	auth = authenticate(request, username=username, password=password)
	print(auth)
	if auth is not None:
		login(request, auth)
		logged_in_text = 'Zalogowano'
		return redirect('/')
	else:
		print('Nie zalogowany')
		logged_in_text = 'Nie zalogowano'
		return redirect('/login/') #render(request, 'logged_in.html', {'text':logged_in_text})
	
	
@login_required
def logout_view(request):
	if request.user.is_authenticated:
		logout(request)
		return render(request, 'logged_in.html', {'text':'Wylogowano'})
	else:
		return render(request, 'login_form.html', {})
		
		

@login_required
def report_visit(request):
	visit = request.POST.get('provider', None)
	floor = request.POST.get('floor', 13)
	formSent = request.POST.get('form_sent', False)

	providersList = Provider.objects.all()

	shortcuts=[]
	
	for provider in providersList:
		shortcuts.append(provider.shortcut)
		
	prov_fail = False
	print(datetime.today())
	if visit is not None:		
		new = Visit(
					provider = Provider.objects.get(shortcut = visit),
					dateOfVisit = datetime.today(),
					user = request.user,
					floor = floor)
		new.save()
	else:
		if formSent:
			prov_fail=True
	
	
	return render(request, 'report_visit.html', {'providers': providersList, 'prov_fail': prov_fail})


@login_required
def new_provider(request):
	name = request.POST.get('name', None)
	shortcut = request.POST.get('shortcut', None)
	logo = request.POST.get('logo', None)
	if name is not None:
		print('method ok')
		form = NewProvider(request.POST)
		if form.is_valid():
			print('form is valid')
			new = Provider(
							name = name,
							shortcut = shortcut,
							logo = logo)
			new.save()
			return redirect('/', None)
	else:
		form = NewProvider()
	
	return render(request, 'create_provider.html', {'form': form})