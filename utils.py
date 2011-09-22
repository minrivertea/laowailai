


def set_message(request, msg):
    assert type(msg) in (unicode, str)
    request.user.message_set.create(message=msg)