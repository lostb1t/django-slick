

class ModelDict(object):
    @staticmethod
    def to_dict(instance):
        fields =  dict([
            (f.attname, getattr(instance, f.attname))
            for f in instance._meta.local_fields
        ])
        m2m_fields = dict([
            (f.attname, set([
                obj.id for obj in getattr(instance, f.attname).all()
            ]))
            for f in instance._meta.local_many_to_many
        ])
        fields.update(m2m_fields)
        return fields

    @staticmethod
    def compare_dicts(dict1, dict2):
        #old_state, old_m2m_state = self._as_dict(self.instance1)
        #new_state, new_m2m_state = self._as_dict(self.instance2)
        changed_fields = dict([
            (key, value)
            for key, value in dict1.iteritems()
            if value != dict2[key]
        ])
        '''
        changed_m2m_fields = dict([
            (key, value)
            for key, value in old_m2m_state.iteritems()
            if sorted(value) != sorted(new_m2m_state[key])
        ])
        '''
        #print changed_fields
        #changed_fields.update(changed_m2m_fields)
        return changed_fields
