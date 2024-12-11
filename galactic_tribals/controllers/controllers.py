# -*- coding: utf-8 -*-
# from odoo import http


# class GalacticTribals(http.Controller):
#     @http.route('/galactic_tribals/galactic_tribals', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/galactic_tribals/galactic_tribals/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('galactic_tribals.listing', {
#             'root': '/galactic_tribals/galactic_tribals',
#             'objects': http.request.env['galactic_tribals.galactic_tribals'].search([]),
#         })

#     @http.route('/galactic_tribals/galactic_tribals/objects/<model("galactic_tribals.galactic_tribals"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('galactic_tribals.object', {
#             'object': obj
#         })

