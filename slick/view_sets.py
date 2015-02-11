from django.utils.datastructures import SortedDict

from viewsets import ViewSet as VS, ViewSetListView, ViewSetCreateView, ViewSetDetailView, ViewSetUpdateView, ViewSetDeleteView
from viewsets.mixins.manager import ViewSetMixin as VSM
from viewsets.mixins.actions import ActionMixin
from viewsets.mixins.filter import FilterMixin
from viewsets.mixins.search import SearchMixin
from viewsets.views import ActionListView

from guardian.shortcuts import get_objects_for_user

from .mixins import ListMixin


class AdminListView(FilterMixin, SearchMixin, ListMixin, ActionListView):
    paginate_by = 25


class ViewSetMixin(VSM):
    list_detail_link = "slick:detail"


class ViewSetListView(ViewSetMixin, AdminListView):
    paginate_by = 25


class ViewSet(VS):
    default_app = "slick"
    mixin = ViewSetMixin
    queryset = None


    '''
    def get_urls(self):
        bla = super(ViewSet, self).get_urls()
        print self.links
        #print self.request
        #for link, view in self.links.items():
            #print view[0].request
        #self.links = []
        return bla
    #guardian_view_permission = ''
    
    def get_view_permission_name(self, view):
        name = view.name
        if name == 'detail':
            name = 'view'
        if name == 'update':
            name = 'change'

        return '%s_%s' % (name, self.model._meta.verbose_name.lower())

    def get_queryset(self, view, request, **kwargs):
        #print view.name
        if self.queryset:
            return self.queryset
        else:
            #print self.get_view_permission_name(view)
            #print request.user.has_perm("view_%s" % self.name, obj)
            return get_objects_for_user(request.user, self.get_view_permission_name(view), self.model)

    def has_add_permission(self, request):
        pass

    def has_view_permission(self, request, obj=None):
        if obj:
            return request.user.has_perm("view_%s" % self.name, obj)

        return False

    def has_change_permission(self, request, obj=None):
        pass
    '''