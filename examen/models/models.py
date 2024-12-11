# -*- coding: utf-8 -*-
from random import randint

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource
import base64

class Furgoneta(models.Model):
    _name = 'examen.furgoneta'
    _description = 'Les furgonetes'

    @api.model
    def _get_default_image(self):
        # Obtener la ruta del archivo utilizando get_module_resource
        image_path = get_module_resource('examen', 'static/src/img/photo.jpeg')
        try:
            with open(image_path, 'rb') as image_file:
                return base64.b64encode(image_file.read())
        except FileNotFoundError:
            # Retorna False si no se encuentra el archivo
            return False

    name = fields.Char(string="Furgoneta", required=True)
    matricula = fields.Char(string="Matrícula", required=True)
    capacitat = fields.Integer(string="Capacitat (m3)", required=True )
    foto = fields.Image(default=lambda self: self._get_default_image(), max_width=100, max_height=100)
    volum_disponible = fields.Integer(compute='_get_disponible')

    viatges = fields.One2many(string='Els meus viates', comodel_name='examen.viatge', inverse_name='furgoneta', readonly=True)

    # Fields relationals
    paquets = fields.Many2many('examen.paquet', related='viatges.paquets')

    # Funcions compute
    def _get_disponible(self):
        for f in self:
            volum_total = 0
            for p in f.paquets:
                volum_total = volum_total + p.volum
            f.volum_disponible = f.capacitat - volum_total
            #print('Disponibleeeeee', f.volum_disponible)

    @api.constrains('viatges')
    def _check_volum_total(self):
        for f in self:
            print('Disponibleeeeee', f.volum_disponible)
            if f.volum_disponible < 0:
                raise ValidationError("Warning: El paquet no cap en aquesta furgoneta. Supera el seu volum disponible")

class Paquet(models.Model):
    _name = 'examen.paquet'
    _description = 'Els paquets'

    name = fields.Char(string="Identificador", required=True)
    volum = fields.Integer(string="Volum", required=True)

    viatges = fields.Many2many(comodel_name='examen.viatge',
                                relation='viatges_paquets',
                                column1='paquet_id',
                                column2='viatge_id')

class Viatge(models.Model):
    _name = 'examen.viatge'
    _description = 'Els viatges'

    id = fields.Integer(string="Identificador", required=True)
    name = fields.Char(string="Nom del conductor", required=True)

    #paquets = fields.One2many(string='Els cotxes de la escuderia', comodel_name='examen.car', inverse_name='team')
    furgoneta = fields.Many2one(string='La furgoneta utilitzada', comodel_name='examen.furgoneta', ondelete='set null')
    paquets = fields.Many2many(comodel_name='examen.paquet',
                                relation='viatges_paquets',
                                column2='paquet_id',
                                column1='viatge_id',
                                readonly=True)



