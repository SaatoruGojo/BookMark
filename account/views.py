from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.http import HttpResponse,JsonResponse
from .forms import (LoginForm,UserRegistrationForm,UserEditForm,ProfileEditForm)
from django.contrib.auth.decorators import login_required
from actions.utils import create_action
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['username'],password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponse('Authenticated Successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

from actions.models import Action

@login_required
def dashboard(request):
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)
    if following_ids:
        actions = actions.filter(user_id__in=following_ids)
        
    actions = actions.select_related('user','user__profile').prefetch_related('target')[:10]
            
    return render(request,'account/dashboard.html',{'section':'dashboard','actions':actions})
    

from .models import Profile,Contact


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            # Save the User object
            new_user.save()
            
            Profile.objects.create(user = new_user)
            create_action(new_user,'has created an account')
            
            return render(
               request,
               'account/register_done.html',
               {'new_user': new_user}
           )
    else:
        user_form = UserRegistrationForm()
    return render(
        request,
        'account/register.html',
        {'user_form': user_form}
    )
# Create your views here.

from django.contrib import messages

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST,files = request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Please correct the error below.')
            
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        
    return render(request, 'account/edit.html',{'user_form':user_form,'profile_form':profile_form})
    
        
        
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
User = get_user_model()
@login_required
def user_list(request):
    users= User.objects.filter(is_active=True)
    return render(request,'account/user/list.html',{'section':'people','users':users})

@login_required
def user_detail(request,username):
    user = get_object_or_404(User,username=username)
    return render(request,'account/user/detail.html',{'section':'people','user':user})




#Adding user follow/unfollow actions with JavaScript
from django.views.decorators.http import require_POST
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user
                )
                create_action(request.user,'is following',user)
                
            else:
                Contact.objects.filter(
                    user_from=request.user,
                    user_to=user
                ).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'error'})
    return JsonResponse({'status':'error'})
            
                
                

