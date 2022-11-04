from django.shortcuts import get_object_or_404
from django.utils.translation import  ugettext_lazy as _
from django.http import JsonResponse

def toggle_status(request, pk, model, key, model_serializer, active, format=None):
	if (active):
		obj = model.objects.inactive_rows()
	else:
		obj = model.objects.active_rows()
	instance = get_object_or_404(obj, pk=pk)
	request.data["is_active"] = active
	serializer = model_serializer(instance, data=request.data, partial=True)
	if serializer.is_valid():
		serializer.save(key=instance)
		return JsonResponse(serializer.data, status=200)
	return JsonResponse(serializer.errors, status=400)
