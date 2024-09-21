from functools import wraps
from graphql import GraphQLError

def ip_from_info(info):
    ip = info.context.META['HTTP_ORIGIN'].strip("http://")
    ip = ip[:ip.index(":")]
    return ip

def ip_is_home(ip):
    return ip == "127.0.0.1"

def user_from_info(info, do_prime=False):
    if do_prime and ip_is_home(ip_from_info(info)):
        return 1
    else:
        return info.context.user.pk

def extract_user_ip(**kwargs):
    if "ip_address" or "user" not in kwargs:
        raise GraphQLError("Session info not available!")

    return (kwargs['ip_address'], kwargs['user'])

def inject_session_data(do_prime=False):
    def curry_inner(func):
        @wraps(func)
        def wrapper(self, info, *args, **kwargs):
            # Access the request object via info.context
            request = info.context
            
            # Get the user's IP address
            ip_address = request.META.get('REMOTE_ADDR')
            
            # Get the authenticated user (None if not authenticated)
            user = request.user
            
            # Inject the ip_address and user into the mutation function
            kwargs['ip_address'] = ip_address
            kwargs['user'] = user

            # Call the original mutate function with the extra data
            return func(self, info, *args, **kwargs)
        return wrapper
    return curry_inner