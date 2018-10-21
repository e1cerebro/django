from django import forms
from django.core import validators
from django.contrib.auth.models import User
from first_app.models import Topic, UserProfileInfo


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site', 'profile_pics')

'''
Creating a model form
'''


class NewTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = "__all__"


"""
This function is for creating ur custom validators that will be used by the validators
Django class. It has to be created outside the class and must be have a value params
"""


def check_for_z(value):
    if value[0].lower() != 'z':
        raise forms.ValidationError('Name must start with a z')


class TopicForm(forms.Form):
    name = forms.CharField(max_length=200, validators=[check_for_z])
    email = forms.EmailField()
    verifyemail = forms.EmailField(label='Verify Email')
    message = forms.CharField(widget=forms.Textarea)
    botcatcher = forms.CharField(required=True, widget=forms.HiddenInput,
                                 validators = [validators.MaxLengthValidator(0)]
                                 )

    """
        This is the way a validation function is created. 
        the syntax is clean_fieldElementName
    """
    # def clean_botcatcher(self):
    #     botcatcher = self.cleaned_data['botcatcher']
    #
    #     if len(botcatcher) > 0:
    #         raise forms.ValidationError("THAT FIELD IS HIDDEN AND NOT MEANT TO BE FILLED.")
    #     return botcatcher

    '''
        This is used to clean all the forms at once 
    '''
    def clean(self):
        all_clean_data = super().clean()
        email = all_clean_data['email']
        vmail = all_clean_data['verifyemail']

        if email != vmail:
            raise forms.ValidationError('Emails do not match')


