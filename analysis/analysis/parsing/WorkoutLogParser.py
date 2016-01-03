import re
import xml.etree.ElementTree as ET

from HTMLParser import HTMLParser
from ui.models import ExerciseSet, Workout
from django.contrib.auth.models import User


""" TODO:

	1. Post date: 4-6-2014 "warmup: 3x 2 pause sn ext" tries to parse 2 pause sn e as an int
	2. Parsing delimiters ; and '
	3

"""

def remove_tags(text):
	text = re.sub(r'</?p(re)?>',r'\n', text)	
	return re.sub(r'</?[^>]*?>','',text)

def has_failure_text(input_string):
	if 'pin' in input_string.lower():
		return True
	elif 'f' in input_string.lower():
		return True

	return False

def has_Pr_text(input_string):
	if 'pr' in input_string.lower():
		return True
	return False

class WorkoutLogParser:
	exercise_set_regex = re.compile('^.*:.*$')
	extract_multi_set_regex = re.compile('^.*x([^+(]*)x.*')
	extract_multi_rep_regex = re.compile('^.*x\d+x(.*)')
	extract_multi_weight_regex = re.compile('^([^x]+)x\d+x.*')
	extract_single_weight_regex = re.compile('^#?([^x]*)#?k?g?x.*')
	extract_single_rep_regex = re.compile('^[^x]*x(.*|\(.*\))')
	non_digit_regex = re.compile('\D')
	sets = []

	# If one set of this workout is considered lbs, then all should be lbs unless otherwise specified
	isLbs = False

	def __init__(self, workout):
		if not isinstance(workout,Workout):
			raise Exception("Tried to parse a non-workout")

		self.workout = workout
		self.html_parser = HTMLParser()

		""" Remove unnecessary &nbsp; etc """
	def unescape_html(self,text):
		text = remove_tags(text)
		return self.html_parser.unescape(text)

	def split_by_line(self,text):
		return text.replace(r'\r',r'').split(r'\n')

	def determine_if_lbs(self, text):
		if "kg" in text:
			self.isLbs = False
		elif "#" in text or "lbs" in text:
			self.isLbs = True

	def parse_reps(self,input_reps):
		hasFailure = False
		hasPr = False
		extras = ''
		reps = input_reps
		if has_failure_text(input_reps):
			hasFailure = True
		if has_Pr_text(input_reps):
			hasPr = True
		if self.non_digit_regex.search(reps) is not None:
			extras = self.non_digit_regex.split(input_reps, maxsplit=1)[1]
			if self.non_digit_regex.match(reps) is not None:
				reps = 0
			else:
				reps = int(self.non_digit_regex.split(input_reps, maxsplit=1)[0])

		return reps, extras, hasPr, hasFailure

	def get_weight_from_string(self, weight):
		if 'bw' in weight.lower():
			isBodyWeight = True
			return 0
		if 'bar' in weight.lower():
			if self.isLbs:
				return 45
			else:
				return 20
		else:
		 weight = re.sub(r'(kgs?|#|lbs)','',weight)
		 try:
		 	return float(weight)
		 except Exception as e:
		  return 0

	def create_single_set(self,exercise_name,_set):
		self.determine_if_lbs(_set)
		isBodyWeight = False
		if self.extract_single_weight_regex.match(_set) is None:
			reps = 1
			weight = self.get_weight_from_string(_set)
		else:
			weight = self.extract_single_weight_regex.match(_set).group(1)

			reps = self.extract_single_rep_regex.match(_set).group(1)
			weight = self.get_weight_from_string(weight)

		if 'sec' in str(reps) or re.compile('\ds').search(str(reps)) is not None:
			reps = reps.split('s')[0]
			isSeconds = True
		else:
			isSeconds = False

		reps, extras, hasPr, hasFailure = self.parse_reps(str(reps))

		try:
			exset = ExerciseSet(
				exerciseName=exercise_name,
				reps = reps,
				weight = weight,
				isBodyWeight = isBodyWeight,
				isLbs = self.isLbs,
				isSeconds = isSeconds,
				hasFailure = hasFailure,
				workout = self.workout,
				extras = extras,
				date = self.workout.date,
				user = User.objects.get(username='dmav')
				)
			exset.save()	
			self.sets.append(exset)
		except Exception as e:
			print(e)

	def create_sets(self,exercise_name, _set):
		if self.extract_multi_set_regex.match(_set) is None:
			self.create_single_set(exercise_name,_set)
		else:
			num_of_sets = self.extract_multi_set_regex.match(_set).group(1)
			int(num_of_sets)
			for set_number in range(0,int(num_of_sets)):
				reps = self.extract_multi_rep_regex.match(_set).group(1)
				weight = self.extract_multi_weight_regex.match(_set).group(1)
				self.create_single_set(exercise_name, weight + 'x' + reps)

	def parse_line(self,line):
		if line == '':
			return
		elif self.exercise_set_regex.match(line) is not None:
			exercise_name = line.split(':',1)[0]
			sets = line.split(':',1)[1]
			for _set in sets.split(','):
				# sanitize set
				_set = _set.lstrip().rstrip()
				self.create_sets(exercise_name, _set)
		else:
			# ADD TO COMMENTS
			self.workout.comments = self.workout.comments + \
				r'\n' + line.lstrip().rstrip()
			self.workout.save()

	def parse(self):
		unescaped_content = self.unescape_html(self.workout.workout_text)
		for line in self.split_by_line(unescaped_content):
			self.parse_line(line)
		return self.sets
