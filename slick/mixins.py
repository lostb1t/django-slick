from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.utils.html import escapejs, escape
from django.utils.safestring import mark_safe

from viewsets.mixins.sort import TableMixin


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


class ListMixin(TableMixin):
    def get_row(self, obj, list_display):
        list_display_links = self.get_list_display_links()
        cells = []
        for name, cell in self.get_cells(obj, list_display):
            if cell == '':
                # if the the list_display_link is an empty string and it's the only one...
                # it makes it impossible for a user to select fixing here by adding text.
                cell = 'None'

            if name in list_display_links:
                cell = u"<a href='{}'>{}</a>".format(self.get_detail_link(obj), escape(cell))
                cells.append(mark_safe(cell))
            else:
                cells.append(cell)
        return cells
