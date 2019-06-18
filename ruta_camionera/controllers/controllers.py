# -*- coding: utf-8 -*-
from odoo import http

# class RutaCamionera(http.Controller):
#     @http.route('/ruta_camionera/ruta_camionera/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ruta_camionera/ruta_camionera/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ruta_camionera.listing', {
#             'root': '/ruta_camionera/ruta_camionera',
#             'objects': http.request.env['ruta_camionera.ruta_camionera'].search([]),
#         })

#     @http.route('/ruta_camionera/ruta_camionera/objects/<model("ruta_camionera.ruta_camionera"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ruta_camionera.object', {
#             'object': obj
#         })