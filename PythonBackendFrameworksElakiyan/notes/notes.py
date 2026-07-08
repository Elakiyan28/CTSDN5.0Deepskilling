'''Journey of GET /api/courses/

Browser → URL Router → View → Model (DB query) → Response.

Middleware sits between request & response.

Middleware Examples

AuthenticationMiddleware → associates users with requests.

CsrfViewMiddleware → protects against CSRF attacks.

WSGI vs ASGI

WSGI → synchronous, default in Django.

ASGI → asynchronous, needed for websockets/async tasks.

MVC vs MVT

MVC: Model–View–Controller.

Django MVT:

Model = Database layer.

View = Controller logic.

Template = Presentation layer.'''