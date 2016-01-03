from ui.models import *
from analysis.parsing import WorkoutLogParser

def make_workouts():
	workout_ids = {}
	for post in Posts.objects.all():
		w = Workout(workout_text=post.post_content, date=post.post_date.date())
		w.save()
		workout_ids[w.id] = post
	return workout_ids

def parse_sets():
	workout_to_sets = {}
	for w in Workout.objects.all():
		parser = WorkoutLogParser(w)
		try:
			sets = parser.parse()
		except Exception as e:
			print("couldn't parse log " + str(w.id))
			print(e)
		workout_to_sets[w.id] = sets	
	return workout_to_sets
			

def delete_all_sets():
	ExerciseSet.objects.all().delete()

def delete_all_workouts():
	Workout.objects.all().delete()
