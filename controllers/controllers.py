# -*- coding: utf-8 -*-
# from odoo import http


# class SimpleLibrary(http.Controller):
#     @http.route('/simple_library/simple_library', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/simple_library/simple_library/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('simple_library.listing', {
#             'root': '/simple_library/simple_library',
#             'objects': http.request.env['simple_library.simple_library'].search([]),
#         })

#     @http.route('/simple_library/simple_library/objects/<model("simple_library.simple_library"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('simple_library.object', {
#             'object': obj
#         })

