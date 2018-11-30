# -*- coding: utf-8 -*-
from odoo import http

# class Traningdemo(http.Controller):
#     @http.route('/traningdemo/traningdemo/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/traningdemo/traningdemo/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('traningdemo.listing', {
#             'root': '/traningdemo/traningdemo',
#             'objects': http.request.env['traningdemo.traningdemo'].search([]),
#         })

#     @http.route('/traningdemo/traningdemo/objects/<model("traningdemo.traningdemo"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('traningdemo.object', {
#             'object': obj
#         })