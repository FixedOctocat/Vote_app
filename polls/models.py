from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Poll(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
	text = models.CharField(max_length=300)
	pub_date = models.DateField()

	def __str__(self):
		return self.text

	def user_vote(self, user):
		user_votes = user.vote_set.all()
		qs = user_votes.filter(poll=self)
		if qs.exists():
			return False
		return True

	def num_votes(self):
		return self.vote_set.count()

class Choice(models.Model):
	poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=120)

	def __str__(self):
		return "{}".self.choice_text[:20]

	def num_votes(self):
		return self.vote_set.count()	

class Vote(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
	choice = models.ForeignKey(Choice, on_delete=models.CASCADE)