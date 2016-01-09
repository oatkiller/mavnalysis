from ui.models import ExerciseSet

LBS_TO_KG_CONVERSION = float(0.453592)

def get_highest_pr(queryset):
	lbs_pr = queryset.filter(isLbs=True).first()
	kgs_pr = queryset.filter(isLbs=False).first()
	if lbs_pr is None:
		return kgs_pr
	elif kgs_pr is None:
		return lbs_pr
	
	lbs_pr_in_kg = float(lbs_pr.weight) * LBS_TO_KG_CONVERSION 
	if lbs_pr_in_kg > kgs_pr.weight:
		return lbs_pr
	else:
		return kgs_pr

def generate_pr_entry (exerciseName, reps, user):
	queryset = (ExerciseSet.objects.
		filter(user=user).
		filter(exerciseName=exerciseName).
		filter(reps__gte=reps).
		order_by('-weight')
	)

	pr = get_highest_pr(queryset)	
	if pr != None:
		pr_weight = float(pr.weight) * (LBS_TO_KG_CONVERSION if pr.isLbs else float(1))
		pr_weight_string = "%.2f" % pr_weight

		return {
			'weight' : pr_weight_string,
			'date'   : pr.date
		}
	else:
		return {
			'weight' : None,
			'date'   : None
		}

def generate_pr_entries (exerciseNames, reps, user):
	result = []
	for exerciseName in exerciseNames:
		pr = {
			'name' : exerciseName,
			'prs' : [generate_pr_entry(exerciseName, rep, user) for rep in reps]
		}
		result.append(pr)
	return result

def get_prs(request=None, reps=range(1,6)):
	if request is None:
		return []
	
	exerciseNames = [
		"Back Squat",
		"Front Squat",
		"Clean and Jerk",
		"Snatch",
		"Flat Bench",
		"Overhead Press"
	]

	return generate_pr_entries(exerciseNames, reps, request.user)
