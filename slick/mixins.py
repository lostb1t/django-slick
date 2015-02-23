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
    def prepare_list_display(self):
        retval = []
        for field in self.get_list_display():
            label = None
            if isinstance(field, tuple):
                label = field[1]
                field = field[0]
            
            for source in self.field_sources:
                column = source(self, field)
                if column.valid():
                    column.label = label
                    retval.append(column)
                    break

        return retval

    def get_cells(self, obj, list_display):
        for field in list_display:
            try:
                retval = field.value(obj)
            except Exception as ex:
                print (type(ex), ex)
                retval = mark_safe(u"<i style='color:darkred;' " + \
                    u"class='glyphicon glyphicon-exclamation-sign' " + \
                    u"title='{}: {}'></i>".format(type(ex).__name__, escape(str(ex))))

            if retval is None:
                retval = "_"

            label = field.label if field.label is not None else field.header()
            yield field.original, retval, label

    def get_row(self, obj, list_display):
        list_display_links = self.get_list_display_links()
        cells = []
        #print list_display
        for name, cell, label in self.get_cells(obj, list_display):
            #print name
            if cell == '':
                # if the the list_display_link is an empty string and it's the only one...
                # it makes it impossible for a user to select fixing here by adding text.
                cell = 'None'

            if name in list_display_links:
                cell = u"<a href='{}'>{}</a>".format(self.get_detail_link(obj), escape(cell))
                cells.append({'label': label, 'value': mark_safe(cell)})
            else:
                cells.append({'label': label, 'value': cell})
        return cells
