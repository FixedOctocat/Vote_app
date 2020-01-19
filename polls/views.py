from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
import datetime

from .models import Poll, Choice, Vote
from .forms import PollForm, EditPollForm, ChoiceForm

# Create your views here.
@login_required
def delete_poll(request, poll_id):
	poll = Poll.objects.get(id=poll_id)

	if request.user != poll.owner:
		return redirect('/')

	poll.delete()
	messages.success(request, 'Poll deleted', extra_tags='alert alert-success alert-dismissible fade show')
	return redirect('polls:list')

@login_required
def delete_choice(request, choice_id):
	choice = Choice.objects.get(id=choice_id)
	poll = Poll.objects.get(id=choice.poll.id)

	if request.user != poll.owner:
		return redirect('/')

	choice.delete()
	messages.success(request, 'Choice deleted', extra_tags='alert alert-success alert-dismissible fade show')
	return redirect('polls:list')

@login_required
def add_choice(request, poll_id):
	poll = Poll.objects.get(id=poll_id)

	if request.user != poll.owner:
		return redirect('/')

	if request.method == "POST":
		form = ChoiceForm(request.POST)
		if form.is_valid():
			new_choice = form.save(commit=False)
			new_choice.poll = poll
			new_choice.save()
			messages.success(request, 'Choice added', extra_tags='alert alert-success alert-dismissible fade show')
			return redirect('polls:list')
	else:
		form = ChoiceForm()
	return render(request, 'polls/add_choice.html', {'form':form})

@login_required
def edit_poll(request, poll_id):
	poll = Poll.objects.get(id=poll_id)
	print(request)
	if request.user != poll.owner:
		return redirect('home')

	if request.method == 'POST':
		form = EditPollForm(request.POST, instance=poll)
		if form.is_valid():
			form.save()
			messages.success(request, 'Poll edited',extra_tags='alert alert-success')
			return redirect('polls:list')
	else:
		form = EditPollForm(instance=poll)

	return render(request, 'polls/poll_edit.html', {'form':form, 'poll':poll})

@login_required
def polls_list(request):
	polls = Poll.objects.all()

	context = {
		'polls':polls
	}

	return render(request, 'polls/polls_list.html', context)

@login_required
def poll_detail(request, poll_id):
	poll = Poll.objects.get(id=poll_id)
	user_voted = poll.user_vote(request.user)
	context = {
		'poll':poll,
		'user_can_vote':user_voted
	}

	return render(request, 'polls/poll_detail.html', context)

@login_required
def poll_vote(request, poll_id):
	poll = Poll.objects.get(id=poll_id)
	choice_id = request.POST.get('choice')

	if not poll.user_vote(request.user):
		messages.error(request, 'You voted earlier!')
		return HttpResponseRedirect(reverse('polls:detail', args=(poll_id,)))

	if choice_id:
		choice = Choice.objects.get(id=choice_id)
		new_vote = Vote(user=request.user, poll=poll, choice=choice)
		new_vote.save()
	else:
		messages.error(request, 'No Choice!')
		return HttpResponseRedirect(reverse('polls:detail', args=(poll_id,)))

	context = {
		'poll':poll
	}

	return render(request, 'polls/poll_results.html', context)

@login_required
def add_poll(request):
	if request.method == 'POST':
		form = PollForm(request.POST)
		if form.is_valid():
			new_poll = form.save(commit=False)
			new_poll.pub_date = datetime.datetime.now()
			new_poll.owner = request.user
			new_poll.save()

			newChoice1 = Choice(poll=new_poll, choice_text=form.cleaned_data['choice1']).save()
			newChoice2 = Choice(poll=new_poll, choice_text=form.cleaned_data['choice2']).save()
			messages.success(request, 'Poll added',extra_tags='alert alert-success')
			return redirect('polls:list')
	else:
		form = PollForm()

	context = {'form': form}
	return render(request, 'polls/poll_add.html', context)