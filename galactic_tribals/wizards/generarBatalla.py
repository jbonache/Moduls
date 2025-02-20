# -*- coding: utf-8 -*-

from odoo import models, fields, api

class WizardGenerarBatalla(models.TransientModel):
    _name = 'galactic_tribals.wizard_generar_batalla'
    _description = 'Wizard para generar batallas'

    name = fields.Char(string='Nom', required=True)
    atacant_id = fields.Many2one('galactic_tribals.tribu', string='Atacant', required=True)
    defensor_id = fields.Many2one('galactic_tribals.tribu', string='Defensor', required=True)
    date = fields.Date(string='Data', default=fields.Date.today, required=True)

    def generar_batalla(self):
        if self.atacant_id == self.defensor_id:
            raise models.ValidationError('El atacant i el defensor no poden ser la mateixa tribu.')

        batalla = self.env['galactic_tribals.batalla'].create({
            'name': self.name,
            'date': self.date,
            'atacant': self.atacant_id.id,
            'defensor': self.defensor_id.id,
        })
        return {'type': 'ir.actions.act_window_close'}