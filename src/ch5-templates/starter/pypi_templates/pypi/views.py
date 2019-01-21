from pyramid.view import view_config

def get_test_packages():
    return [
        {'name': 'requests', 'version': '1.2.3'},
        {'name': 'sqlalchemy', 'version': '2.0.0'},
        {'name': "pyramid", 'version': '1.9.1'}
    ]

@view_config(route_name='home', renderer='templates/home_index.pt')
def home_index(_):
    return {
        'packages': get_test_packages()
    }

@view_config(route_name='about', renderer='templates/about.pt')
def about(_):
    return {}
