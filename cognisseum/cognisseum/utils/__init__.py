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
