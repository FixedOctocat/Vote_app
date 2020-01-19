from django import forms

from .models import Poll, Choice

class PollForm(forms.ModelForm):
	choice1 = forms.CharField(label='First choice', max_length=150, min_length=1, widget=forms.TextInput(attrs={'class':'form-control'}))
	choice2 = forms.CharField(label='Second choice', max_length=150, min_length=1, widget=forms.TextInput(attrs={'class':'form-control'}))

	class Meta:
		model = Poll
		fields = ['text', 'choice1', 'choice2']
		widgets = {
			'text': forms.Textarea(attrs={'class':"form-control", 'rows':5, 'cols':15})
		}

class EditPollForm(forms.ModelForm):
	class Meta:
		model = Poll
		fields = ['text']
		widgets = {
			'text': forms.Textarea(attrs={'class':"form-control", 'rows':5, 'cols':15})
		}

class ChoiceForm(forms.ModelForm):

    class Meta:
        model = Choice
        fields = ['choice_text']