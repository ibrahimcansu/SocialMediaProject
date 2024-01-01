from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegistrationForm, PostUploadForm, UserProfileForm, UserPersonalProfileForm
from .models import ProfileUser, UserFollowing, PostModel, LikeModel
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from itertools import chain


@login_required(login_url='signin')
def index(request):
    current_user = request.user
    current_profile = ProfileUser.objects.get(user=current_user)
    upload_form = PostUploadForm(request.POST or None, request.FILES)
    followed_people = UserFollowing.objects.filter(user_id=current_user).values('following_user_id')   
    posts = PostModel.objects.filter(post_owner__in=followed_people).annotate(like_count=Count('liked')) 


    follow_suggestion_number=[]
    suggestions = ProfileUser.objects.exclude(user_id__in=followed_people).order_by('?')[:2]

    for suggestion in suggestions:
        current_suggestion = User.objects.get(username=suggestion)
        follow_suggestion_number.append((current_suggestion.followers.all().count())-1)
        

    context = {
        'current_profile': current_profile,
        'upload_form': upload_form,
        'posts': posts, 
        'suggestions': suggestions,
        'follow_suggestion_number':follow_suggestion_number

     }

    if upload_form.is_valid():
        instance = upload_form.save(commit=False)
        instance.post_owner = current_user
        instance.save()
        messages.success(request, 'Your image has been uploaded!')
        return redirect('index')
    
    return render(request,'index.html', context)


def like(request, pk):
    current_user = request.user
    current_post = PostModel.objects.get(id=pk)
    if current_user.liker.filter(liked_post=current_post).exists():
        current_user.liker.filter(liked_post=current_post).delete()
    else:
        LikeModel.objects.create(like_owner=current_user, liked_post=current_post).save()
    return redirect(index)





def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid Credentials')
            return render(request, 'signin.html')
    else:
        return render(request, 'signin.html')
    
    
@login_required(login_url='signin')
def signout(request):
    logout(request)
    return redirect('signin')


def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            current_user = User.objects.get(email=form.cleaned_data['email']) 
            ProfileUser.objects.create(user=current_user, id_user=current_user.id)
            UserFollowing.objects.create(user_id=current_user, following_user_id=current_user)
            messages.success(request, 'Kayıt başarılı')
            return redirect('signin')
        else:
            return render(request, 'signup.html', {'form':form})
    else:
        form =UserRegistrationForm()
        return render(request, 'signup.html', {'form':form})


@login_required(login_url='signin')
def setting(request, pk):
    if request.user.id == pk:
        current_record1 = User.objects.get(id=pk)
        current_record2 = ProfileUser.objects.get(user=current_record1)
        form1 = UserProfileForm(request.POST or None, instance=current_record2)
        form2 = UserPersonalProfileForm(request.POST or None, instance=current_record1)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            if request.FILES.get('image') != None:
                image_record = ProfileUser.objects.get(user=current_record1)
                image = request.FILES.get('image')
                image_record.profileimg = image
                image_record.save()
            messages.success(request, 'Kayıt Başarılı')
            return redirect('index')
        
        return render(request, 'setting.html',{
            'form1':form1,
            'form2':form2,
            'current_record2':current_record2
            })
    else:
        return render(request, 'error.html')


@login_required(login_url='signin')
def profile(request, pk):
    current_user = User.objects.get(username=pk)
    post_number = current_user.poster.all().count()   #poster kullanımı
    current_active_user = request.user
    current_profile = ProfileUser.objects.get(user=current_user)
    following_num = (current_user.following.all().count())-1
    followers_num = (current_user.followers.all().count())-1
    takip = current_active_user.following.filter(following_user_id=current_user).exists()
    post_content = current_user.poster.all()
    context = {
        'current_user': current_user,
        'following_num': following_num,
        'followers_num': followers_num,
        'current_profile': current_profile,
        'takip': takip,
        'post_number': post_number,
        'post_content': post_content
    }

    if request.method == 'POST':
        if takip:
            current_active_user.following.filter(follwing_user_id=current_user).delete()
            context['followers_num'] -= 1
            context['takip'] = False
        else:
            UserFollowing.objects.create(user_id=current_active_user, following_user_id=current_user).save()
            context['followers_num'] += 1
            context['takip'] = True
        return render(request,'profile.html', context)
    return render(request, 'profile.html', context)


@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = ProfileUser.objects.get(user=user_object)


    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)
        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = ProfileUser.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
    else:
        username_profile_list = None

    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})



