# -*- coding: utf-8 -*-
from odoo import http

# class Gc-tjara(http.Controller):
#     @http.route('/gc-tjara/gc-tjara/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gc-tjara/gc-tjara/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gc-tjara.listing', {
#             'root': '/gc-tjara/gc-tjara',
#             'objects': http.request.env['gc-tjara.gc-tjara'].search([]),
#         })

#     @http.route('/gc-tjara/gc-tjara/objects/<model("gc-tjara.gc-tjara"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gc-tjara.object', {
#             'object': obj
#         })