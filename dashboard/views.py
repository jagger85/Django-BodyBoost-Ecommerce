from django.shortcuts import render
from accounts.forms import AddressForm
from accounts.models import Address
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

@login_required(login_url='auth:login')
def address_manager(request):

    user_adrresses = Address.objects.filter(user=request.user)
    context = {
        'addresses' : user_adrresses
    }
    return render(request, 'dashboard/address_manager.html',context)

def settings(request):
    return render(request, 'dashboard/settings.html')


def address_form(request):
    form = AddressForm()
    context = {
        'form': form
    }
    return render(request, 'dashboard/add_address.html', context)


def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = Address.objects.create(
                name=form.cleaned_data['name'],
                street=form.cleaned_data['street'],
                post_code=form.cleaned_data['post_code'],
                city=form.cleaned_data['city'],
                province=form.cleaned_data['province'],
                country=form.cleaned_data['country'],
                order_note=form.cleaned_data['order_note'],
                user=request.user
            )
            address.save()
        else :
            messages.error(request,'the address is invalid')
    user_addresses = Address.objects.filter(user=request.user)
    context = {
        'addresses': user_addresses
    }
    return render(request, 'dashboard/address_manager.html', context)


@login_required(login_url='auth:login')
def delete_address(request, address_id):
    address = Address.objects.get(pk=address_id, user=request.user)
    address.delete()
    messages.success(request, 'Address deleted successfully')

    user_addresses = Address.objects.filter(user=request.user)
    context = {
        'addresses': user_addresses
    }
    return render(request, 'dashboard/address_manager.html', context)



