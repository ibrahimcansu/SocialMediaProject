from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, EmailInput, Textarea
from .models import ProfileUser, PostModel


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User 
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labeld = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'E-mail',
        }
        widgets = {
            'username':TextInput(attrs={'class':'bg-gray-200 mb-2 shadow-none  dark:bg-gray-800','style':'border: 1px solid #d3d5d8 !important;','placeholder':'Username'}),
            'first_name':TextInput(attrs={'class':'bg-gray-200 mb-2 shadow-none  dark:bg-gray-800','style':'border: 1px solid #d3d5d8 !important;','placeholder':'First Name'}),
            'last_name':TextInput(attrs={'class':'bg-gray-200 mb-2 shadow-none  dark:bg-gray-800','style':'border: 1px solid #d3d5d8 !important;','placeholder':'Last Name'}),
            'email':EmailInput(attrs={'class':'bg-gray-200 mb-2 shadow-none  dark:bg-gray-800','style':'border: 1px solid #d3d5d8 !important;','placeholder':'E-mail'}),

        }
    
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
                
        self.fields['password1'].widget.attrs['class'] = 'bg-gray-200 mb-2 shadow-none  dark:bg-gray-800'
        self.fields['password1'].widget.attrs['style'] = 'border: 1px solid #d3d5d8 !important;'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'bg-gray-200 mb-2 shadow-none  dark:bg-gray-800'
        self.fields['password2'].widget.attrs['style'] = 'border: 1px solid #d3d5d8 !important;'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'


class UserProfileForm(ModelForm):
    
    class Meta:
        model = ProfileUser
        fields = ['bio', 'location', 'working_at', 'profileimg']
        labels = {
            'bio':'About Me',
            'location': 'Location',
            'working_at': 'Working at',
            'profileimg': 'Profile Image',
                  }
        widgets = {
            'bio':Textarea(attrs={'class':'shadow-none bg-gray-100'}),
            'location':TextInput(attrs={'class':'shadow-none bg-gray-100'}),
            'working_at':TextInput(attrs={'class':'shadow-none bg-gray-100'}),
            }

class UserPersonalProfileForm(ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',]
        labels = {
            "username": "Username",
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "E-mail",
            }
        
class PostUploadForm(ModelForm):

    class Meta:
        model = PostModel
        fields = ['post_img','post_caption']
        labels = {'post_caption' : 'Your Comments!'}
        widgets = {                
            'post_caption':Textarea(attrs={'class':'shadow-none bg-gray-100'})
            }    








