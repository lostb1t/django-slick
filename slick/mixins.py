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
    '''
    list_display = ["__unicode__"]
    list_display_links = []
    list_detail_link = ""
    field_sources = []

    def get_list_display(self):
        return getattr(self, "list_display")

    def prepare_list_display(self):
        retval = []
        for field in self.get_list_display():
            print field
            for source in self.field_sources:
                column = source(self, field)
                if column.valid():
                    retval.append(column)
                    break

        return retval

    def get_items(self, object_list, list_display):
        for obj in object_list:
            yield obj, self.get_item(obj, list_display)

    def get_item(self, obj, list_display):
        list_display_links = self.get_list_display_links()
        for name, item in self.get_fields(obj, list_display):
            if item == '':
                # if the the list_display_link is an empty string and it's the only one...
                # it makes it impossible for a user to select fixing here by adding text.
                item = 'None'

            if name in list_display_links:
                item = u"<a href='{}'>{}</a>".format(self.get_detail_link(obj), escape(item))
                yield mark_safe(item)
            else:
                yield item

    def get_fields(self, obj, list_display):
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

            yield field.original, retval

    def get_context_data(self, **kwargs):
        list_display = getattr(self, "_list_display", None) or \
            self.prepare_list_display()

        context = super(ListMixin, self).get_context_data(**kwargs)
        object_list = context.get("object_list")

        context.update(
            items=self.get_items(object_list, list_display)
        )

        return context
        '''