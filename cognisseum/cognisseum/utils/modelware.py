def make_model(model, acc, ip, **kwargs):
    return model(user_created=acc, user_last_updated=acc, ip_created=ip, ip_last_updated=ip, **kwargs)


def curry_model(acc, ip):
    def inner(model, **kwargs):
        try:
            model = model.objects.get(**kwargs)
        except Exception:
            model = make_model(model, acc, ip, **kwargs)
            model.save()
        return model
    return inner