from slick.utils import resolve_to_view


ARCTIC_MENU = (
    ('Leads', 'lead:list', 'fa-user-circle-o'),
    ('Posts', 'lead:post-list', 'fa-instagram'),
    ('Users', 'users:list', 'fa-user')
)

SIDEBAR = {
    'ITEMS': [
        {
            'label': 'leads',
            'url': 'lead:list',
            'icon': 'fa-user-circle-o',  # Optional
            'permissions': ['model_admin'],  # Optional:
            'permissions': {
                'all': ['model_admin'],  # Optional:
                'any': ['model_admin']  # Optional:
            }
        }
    ]
}

class SideBar(object):
    def __init__(self, config=None):
        self.config = SIDEBAR

    def get_perms(self, item):
        if 'permissions' in item:
            return item['permissions']

    def schema(self):
        return self.config

    def items(self):
        pass


def has_permission(permissions):
    pass

