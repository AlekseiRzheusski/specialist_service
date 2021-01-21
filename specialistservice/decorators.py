from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.deconstruct import deconstructible
import os
from uuid import uuid4

def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name

			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('You are not authorized to view this page')
		return wrapper_func
	return decorator

def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('index')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func

@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        if instance.username:
            filename = '{}.{}'.format(instance.username, ext)
        if os.path.exists(os.path.join(self.path, filename)):
            print(os.path.join(self.path, filename))
            os.remove(os.path.join(self.path, filename))
        return os.path.join(self.path, filename)

path_and_rename = PathAndRename("./account_images")