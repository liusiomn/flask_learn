from flask_restful import abort

# format response object

def get_response(code, msg, data=None):
    if code >= 400:
        abort(code, message=msg)
    return {
        'message': msg,
        'data': data
    }, code
