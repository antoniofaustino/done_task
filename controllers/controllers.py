# -*- coding: utf-8 -*-
from odoo import http

# class CustomSample(http.Controller):
#     @http.route('/custom_sample/custom_sample/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_sample/custom_sample/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_sample.listing', {
#             'root': '/custom_sample/custom_sample',
#             'objects': http.request.env['custom_sample.custom_sample'].search([]),
#         })

#     @http.route('/custom_sample/custom_sample/objects/<model("custom_sample.custom_sample"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_sample.object', {
#             'object': obj
#         })