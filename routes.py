@route('/whereis/<id>')
def whgusr(id):
    out = whereis_getuser(id)
    return out

@route('/whereis/everybody')
def whgusrall():
    out = whereis_getall()
    return out

@route('/whereis/me', method='POST')
@auth_basic(whereis_check)
def whme():
    out = whereis_me()
    return out
