# -*- coding: utf-8 -*-
from tokenize import String

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError
import random
import re
from odoo.modules.module import get_module_resource
import base64

class Player(models.Model):
    _name = 'galactic_tribals.player'
    _description = 'Player Model for Galactic Tribals'

    @api.model
    def _get_default_image(self):
        # Obtener la ruta del archivo utilizando get_module_resource
        image_path = get_module_resource('galactic_tribals', 'static/src/img/avatar_default.png')
        try:
            with open(image_path, 'rb') as image_file:
                return base64.b64encode(image_file.read())
        except FileNotFoundError:
            # Retorna False si no se encuentra el archivo
            return False

    #def _get_default_image_notrun(self):
    #    return self.env.ref('galactic_tribals.avatar_default_1').avatar

    name = fields.Char(string='Nom', required=True)
    email = fields.Char(string='Correu electrònic', required=True)
    register_date = fields.Datetime(string='Data de registre', required=True, default = lambda self: fields.Datetime.now())
    level = fields.Integer(string='Nivell', compute='_get_level')
    battle_points = fields.Integer(string='Punts')
    isActive = fields.Boolean(default=True)
    avatar = fields.Image(default=lambda self: self._get_default_image(), max_width=100, max_height=100)
    #avatar = fields.Image(max_width=100, max_height=100)
    #avatar=fields.Image(default=_get_default_image, max_width=100, max_height=100)

    # Fields per a les Relacions
    tribu = fields.Many2one('galactic_tribals.tribu', ondelete='set null', help='La tribu a la que pertany')
    edificacions = fields.One2many(string='Els meus edificis', comodel_name='galactic_tribals.construccio', inverse_name='player')
    naus = fields.One2many('galactic_tribals.nau', 'player')

    # Fields relationals
    batalles = fields.Many2many('galactic_tribals.batalla', related='tribu.batalles', readonly=True)
    aliances = fields.Many2many('galactic_tribals.alianza', related='tribu.aliances', readonly=True)

    player_progress = fields.One2many('galactic_tribals.player_progress', 'player' )
    # Funcions compute
    @api.depends('battle_points')
    def _get_level(self):
        date = fields.datetime.now()
        for player in self:
            player.level = 1 + (player.battle_points // 100)
            #registre en el model de player_progress
            self.env['galactic_tribals.player_progress'].create({'name':player.level, 'player': player.id, 'date': date})

    # Constrains
    @api.constrains('email')
    def _check_mail(self):
        regex = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'
        for p in self:
            if p.email and not re.match(regex, p.email):
                raise ValidationError('El correu electrónic no es vàlid.')

    _sql_constraints = [('nom_unic','unique(name)','Ja existeix un jugador amb eixe mateix nom.')]

    # onchange handler
    @api.onchange('register_date')
    def _onchange_dreg(self):
        now = fields.Datetime.now()
        if self.register_date > now:
            return {
                'warning': {
                    'title': "Bad Register data",
                    'message': "La fecha de registre no pot ser posterior a l'actual",
                    'type' : 'notification'
                }
            }

    @api.model
    def record_player_levels(self):
        """
        Registra los level actuales de todos los jugadores. Se ejecutará por un cron cada minuto
        """
        players = self.search([])
        for player in players:
            self.env['galactic_tribals.player_progress'].create({
                'name': f"Progrés de {player.name}",
                'player': player.id,
                'date': fields.Date.today(),
            })

class Tribu(models.Model):
    _name = 'galactic_tribals.tribu'
    _description = 'Tribu Model for Galactic Tribals'

    name = fields.Char(string='Nom', required=True)
    home_planet = fields.Char(string='Planeta d\'orige', required=True)
    ability = fields.Char(string='Habilitat', required=True)
    lider = fields.Char(string='Líder' , compute='_get_lider')

    # Fields per a les Relacions
    players = fields.One2many(string='Els meus jugadors',comodel_name='galactic_tribals.player', inverse_name='tribu', readonly=True)
    batalles = fields.Many2many(comodel_name='galactic_tribals.batalla',
                                relation='tribus_batalles',
                                column1='tribu_id',
                                column2='batalla_id',
                                readonly=True )
    aliances = fields.Many2many(comodel_name='galactic_tribals.alianza',
                                relation='tribus_aliances',
                                column1='tribu_id',
                                column2='alianza_id',
                                readonly=True)

    def _get_lider(self):
        for tribe in self:
            tribe.lider = " "
            fechahora_lider = datetime.now()
            for p in tribe.players:
                if p.register_date <= fechahora_lider:
                    fechahora_lider = p.register_date
                    tribe.lider = p.name

    # Constrains
    _sql_constraints = [('nom_unic', 'unique(name)', 'Ja existeix una tribu amb eixe mateix nom.')]

class Planeta(models.Model):
    _name = 'galactic_tribals.planeta'
    _description = 'Planeta Model for Galactic Tribals'

    name = fields.Char(string='Nom', required=True)
    environment = fields.Char(string='Entorn', required=True)
    status = fields.Char(string='Estat', required=True)

    # Fields per a les Relacions
    construccions = fields.One2many('galactic_tribals.construccio', 'planeta', readonly=True)
    #recursos = fields.One2many(string='Els meus recursos',comodel_name='galactic_tribals.recurs', inverse_name='planeta', readonly=True )
    recursos = fields.Many2many(comodel_name='galactic_tribals.recurs',
                                relation='recursos_planetas',
                                column1='planeta_id',
                                column2='recurs_id')
    # Constrains
    _sql_constraints = [('nom_unic', 'unique(name)', 'Ja existeix un planeta amb eixe mateix nom.')]

class Recurs(models.Model):
    _name = 'galactic_tribals.recurs'
    _description = 'Recurs Model for Galactic Tribals'

    name = fields.Char(string='Nom', required=True)
    type = fields.Char(string='Tipo', required=True)
    quantity = fields.Char(string='Quantitat disponible', required=True, default = lambda q: random.randint(100, 500) )

    # Fields per a les Relacions
    #planeta = fields.Many2one('galactic_tribals.planeta', ondelete='set null', help='El planeta on es troba')
    planetas = fields.Many2many(comodel_name='galactic_tribals.planeta',
                                relation='recursos_planetas',
                                column2='planeta_id',
                                column1='recurs_id')

    # Constrains
    _sql_constraints = [('nom_unic', 'unique(name)', 'Ja existeix un recurs amb eixe mateix nom.')]

class Construccio(models.Model):
    _name = 'galactic_tribals.construccio'
    _description = 'Construccio Model for Galactic Tribals'

    name = fields.Char(string='Nom', required=True)
    type = fields.Char(string='Tipo', required=True)
    status = fields.Char(string='Estat', required=True)

    # Fields per a les Relacions
    planeta = fields.Many2one('galactic_tribals.planeta', ondelete='set null', help='El planeta on s"ha construit')
    player = fields.Many2one('galactic_tribals.player', ondelete='set null', help='El jugador que l"ha construit', string='Builded by')

    # Constrains
    _sql_constraints = [('nom_unic', 'unique(name)', 'Ja existeix una construccio amb eixe mateix nom.')]

class Nau(models.Model):
    _name = 'galactic_tribals.nau'
    _description = 'Nau Model for Galactic Tribals'

    name = fields.Char(string='Nom', required=True)
    type = fields.Char(string='Tipo', required=True)
    firepower = fields.Integer(string='Firepower', required=True)

    # Fields per a les Relacions
    player = fields.Many2one('galactic_tribals.player', ondelete='set null', help='El jugador que la pilota', string='Driver')

    # Constrains
    _sql_constraints = [('nom_unic', 'unique(name)', 'Ja existeix una nau amb eixe mateix nom.')]

class Batalla(models.Model):
    _name = 'galactic_tribals.batalla'
    _description = 'Batalla Model for Galactic Tribals'

    name = fields.Char(string='Nom', required=True)
    date = fields.Date(string='Data', required=True)
    progress = fields.Integer(string='Progres de la lluita', default=0)
    #guanyador = fields.Char(string='Guanyador', required=True)

    # Fields per a les Relacions
    tribus = fields.Many2many(comodel_name='galactic_tribals.tribu',
                              relation='tribus_batalles',
                              column2='tribu_id',
                              column1='batalla_id')

    players = fields.Many2many(comodel_name='galactic_tribals.player',
                               relation='players_batalles',
                               column1='batalla_id',
                               column2='player_id')

    # Fields relationals
    #guanyador = fields.Many2one('galactic_tribals.tribu', ondelete='set null', help='El guanyador de la batalla', readonly=True,
    #                            compute='_get_resultat', store=True)

    guanyador = fields.Many2one('galactic_tribals.tribu', ondelete='set null', help='El guanyador de la batalla', readonly=True)

    # Constrains
    _sql_constraints = [('nom_unic', 'unique(name)', 'Ja existeix una batalla amb eixe mateix nom.')]

    @api.depends('name')
    def _get_resultat(self):
        for b in self:
            numero = random.randint(0, 1)
            bat = [b.tribus[0], b.tribus[1]]
            b.guanyador = bat[numero]

    def update_progress(self):
        """
        Incrementa el progrés de la batalla de 0 a 100.
        Quan arriba al 100, determina el guanyador.
        Finalment es desvinculen els jugadors de la relació en la batalla sense eliminar-los de players, clar.
        """
        for batalla in self:
            if batalla.progress < 100:
                batalla.progress += 10  # Incrementa el progrés en 10

            if batalla.progress >= 100:
                batalla.progress = 100

                if len(batalla.tribus) >= 2:
                    # Determina aleatòriament el guanyador entre les tribus participants.
                    batalla.guanyador = random.choice(batalla.tribus.ids)
                else:
                    batalla.guanyador = False  # No hi ha prou tribus per determinar un guanyador.

                # Desvincula els jugadors de la batalla
                batalla.players.write({'batalles': [(3, batalla.id)]})

    # Creará una nueva batalla entre 2 tribus aleatorias y invocará a la funcion que simula el progreso de la
    # batalla y determina un ganador

    def create_random_battle(self):
        # Seleccionar dos tribus aleatorias
        tribus = self.env['galactic_tribals.tribu'].search([])
        if len(tribus) < 2:
            raise ValidationError("No hay suficientes tribus para generar una batalla.")

        tribu1, tribu2 = random.sample(tribus, 2)

        # Crear el registro de batalla
        nueva_batalla = self.create({
            'name': f'Batalla entre {tribu1.name} y {tribu2.name}',
            'date': fields.Date.today(),
            'tribus': [(6, 0, [tribu1.id, tribu2.id])],
        })

        # Simular la batalla
        self.simulate_battle(nueva_batalla.id)

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
    #falla
    @api.model
    def create_random_battle_KK(self):
        # Seleccionar dos tribus aleatorias
        tribus = self.env['galactic_tribals.tribu'].search([])
        if len(tribus) < 2:
            raise ValidationError("No hay suficientes tribus para generar una batalla.")

        tribu1, tribu2 = random.sample(tribus, 2)

        # Crear el registro de batalla
        nueva_batalla = self.create({
            'name': f'Batalla entre {tribu1.name} y {tribu2.name}',
            'date': fields.Date.today(),
            'tribus': [(6, 0, [tribu1.id, tribu2.id])],
        })

        # Simular la batalla
        self.simulate_battle(nueva_batalla.id)
        return True
        #return nueva_batalla

    @api.model
    def simulate_battle(self, batalla_id):
        batalla = self.browse(batalla_id)
        while batalla.progress < 100:
            batalla.update_progress()

        return {
            'name': batalla.name,
            'winner': batalla.guanyador.name if batalla.guanyador else 'No hi ha guanyador',
        }

class Alianza(models.Model):
    _name = 'galactic_tribals.alianza'
    _description = 'Alianza Model for Galactic Tribals'

    name = fields.Char(string='Nom', required=True)
    date = fields.Date(string='Data', required=True)
    status = fields.Char(string='Estat', required=True)

    # Fields per a les Relacions
    tribus = fields.Many2many(comodel_name='galactic_tribals.tribu',
                                relation='tribus_aliances',
                                column2='tribu_id',
                                column1='alianza_id')

    # Constrains
    _sql_constraints = [('nom_unic', 'unique(name)', 'Ja existeix una aliança amb eixe mateix nom.')]

class Player_progress(models.Model):
    _name = 'galactic_tribals.player_progress'
    _description = 'Player Progress Model'

    name = fields.Char(string='Nom', required=True)
    date = fields.Char(string='Data', default= lambda d : fields.datetime.now())

    player = fields.Many2one(
        comodel_name='galactic_tribals.player',
        string='Player',
        ondelete='cascade',
        required=True
    )