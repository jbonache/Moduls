# -*- coding: utf-8 -*-
from odoo import http


class MyGalacticController(http.Controller):
    @http.route('/galactic_tribals/battles', auth='user', type='json')
    def battle(self):
        return {
            'html': """
                <div id="galactic_tribals_banner" style="background-color: tomato">
                    <link href="/galactic_tribals/static/src/css/banner.css"
                        rel="stylesheet">
                    <h1>Battles</h1>
                    <p>Batalles de Galactic Tribals</p>
                    <!--
                    <a class="boton" type="action" data-reload-on-close="true" role="button" 
                        data-method="generar_batalla" data-model="galactic_tribals.wizard_generar_batalla">
                        Generar Battle
                    </a>
                    -->
                    <a class="boton" type="action" data-reload-on-close="true" role="button"
                        data-action="%(action_wizard_generar_batalla)d">
                            Generar Battle
                    </a>
                </div> """
        }

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
