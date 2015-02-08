from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied


class UserCheckMixin(object):
    def check_user(self, user):
        return True

    def user_check_failed(self, request, *args, **kwargs):
        raise PermissionDenied

    def dispatch(self, request, *args, **kwargs):
        if not self.check_user(request.user):
            return self.user_check_failed(request, *args, **kwargs)
  
        return super(UserCheckMixin, self).dispatch(request, *args, **kwargs)


class PermissionRequiredMixin(UserCheckMixin):
    permission_required = None

    def check_user(self, user):
        return user.has_perm(self.permission_required)


