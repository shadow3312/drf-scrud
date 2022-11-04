"""
Utils module to be completed
Contains all useful fonctions for the ScrudViewset
"""

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _

def toggle_status(request, pk, model, key, model_serializer, active, format=None):
	"""
	Toggle on or off status of an instance
	of a model containing is_active field
	"""
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
