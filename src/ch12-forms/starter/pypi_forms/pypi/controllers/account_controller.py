from pyramid.request import Request
from pyramid.view import view_config
import pyramid.httpexceptions as x

# ################### INDEX #################################
from pypi.infrastructure import cookie_auth
from pypi.services import user_service


@view_config(route_name='account_home',
             renderer='pypi:templates/account/index.pt')
def index(request):
    user_id = cookie_auth.get_user_id_via_auth_cookie(request)
    user = user_service.find_user_by_id(user_id)
    if not user:
        x.HTTPFound('/account/login')

    return {
        'user': user
    }


# ################### REGISTRATION ############################

@view_config(route_name='register',
             renderer='pypi:templates/account/register.pt',
             request_method='GET')
def register_get(_):
    return {
        'email': None,
        'name': None,
        'password': None,
        'error': None
    }


@view_config(route_name='register',
             renderer='pypi:templates/account/register.pt',
             request_method='POST')
def register_post(request: Request):
    email = request.POST.get('email')
    name = request.POST.get('name')
    password = request.POST.get('password')

    if not email or not name or not password:
        return {
            'email': email,
            'name': name,
            'password': password,
            'error': 'Some required fields are missing'}

    # create user
    user = user_service.create_user(email, name, password)
    cookie_auth.set_auth(request, user.id)

    return x.HTTPFound('/account')


# ################### REGISTRATION ############################

@view_config(route_name='login',
             renderer='pypi:templates/account/login.pt',
             request_method='GET')
def login_get(_):
    return {
        'email': None,
        'password': None,
        'error': None
    }


@view_config(route_name='login',
             renderer='pypi:templates/account/login.pt',
             request_method='POST')
def login_post(request: Request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    user = user_service.login_user(email, password)

    if not user:
        return {
            'email': email,
            'password': password,
            'error': 'The user could not be found or the password is incorrect'}

    cookie_auth.set_auth(request, user.id)
    return x.HTTPFound('/account')


# ################### LOGOUT ############################

@view_config(route_name='logout')
def logout(request):
    return {}
