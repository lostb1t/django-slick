from django.db.models.signals import post_save

# http://stackoverflow.com/questions/110803/dirty-fields-in-django/11011415#11011415
class DirtyFieldsMixin(object):
    def __init__(self, *args, **kwargs):
        super(DirtyFieldsMixin, self).__init__(*args, **kwargs)
        #post_save.connect(self._reset_state, sender=self.__class__, dispatch_uid='%s._reset_state' % self.__class__.__name__)
        self._reset_state()

    def _as_dict(self):
        fields =  dict([
            (f.attname, getattr(self, f.attname))
            for f in self._meta.local_fields
        ])
        m2m_fields = dict([
            (f.attname, set([
                obj.id for obj in getattr(self, f.attname).all()
            ]))
            for f in self._meta.local_many_to_many
        ])
        return fields, m2m_fields

    def _reset_state(self, *args, **kwargs):
        self._original_state, self._original_m2m_state = self._as_dict()

    def get_dirty_fields(self):
        new_state, new_m2m_state = self._as_dict()
        changed_fields = dict([
            (key, value)
            for key, value in self._original_state.iteritems()
            if value != new_state[key]
        ])
        changed_m2m_fields = dict([
            (key, value)
            for key, value in self._original_m2m_state.iteritems()
            if sorted(value) != sorted(new_m2m_state[key])
        ])
        #print changed_fields
        changed_fields.update(changed_m2m_fields)
        return changed_fields



def send_notifications():
    pass