# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SemanaInicial(models.Model):
    _name = 'ruta_camionera.semana_inicial'
    _rec_name = 'semana_inicial'

    semana_inicial = fields.Integer(string="semana inicial", required=True)

    ##########HOJA HORARIOS

class Punto(models.Model):
    _name = 'ruta_camionera.punto'
    _rec_name = 'nombre'

    nombre = fields.Char('Nombre', size=15, required=True)

    #  modelo para puntos de vuelta
class PuntosVuelta(models.Model):
    _name = 'ruta_camionera.puntos_vuelta'

    salida_inicio = fields.Float('Salida')
    salida_media = fields.Float('Salida Media')
    llegada_inicio = fields.Float('Llegada inicio')


# modelo de vueltas
class Vuelta(models.Model):
    _name = 'ruta_camionera.vuelta'
    _description = 'establece los tiempos de cada vuelta'
    _rec_name = 'nombre'
    

    nombre = fields.Char('Nombre', size=7, required=True)
    rinde = fields.Many2one('ruta_camionera.punto','Rinde')
    # rinde = fields.Char('Rinde', size=10)

    # turno matutino vueltas

    matutino_inicio = fields.Many2one('ruta_camionera.punto','Inicio')
    matutino_retorno = fields.Many2one('ruta_camionera.punto','Retorno')
    matutino_fin = fields.Many2one('ruta_camionera.punto','Fin')

    matutino = fields.Many2many('ruta_camionera.puntos_vuelta', 'matutino_rel', string='Vueltas')

    post_matutino_inicio = fields.Many2one('ruta_camionera.punto','Inicio')
    post_matutino_retorno = fields.Many2one('ruta_camionera.punto','Retorno')
    post_matutino_fin = fields.Many2one('ruta_camionera.punto','Fin')

    post_matutino = fields.Many2many('ruta_camionera.puntos_vuelta', 'post_matutino_rel', string='Vueltas')

    post_post_matutino_inicio = fields.Many2one('ruta_camionera.punto','Inicio')
    post_post_matutino_retorno = fields.Many2one('ruta_camionera.punto','Retorno')
    post_post_matutino_fin = fields.Many2one('ruta_camionera.punto','Fin')

    post_post_matutino = fields.Many2many('ruta_camionera.puntos_vuelta', 'post_post_matutino_rel', string='Vueltas')

    # turno vespertino vueltas

    vespertino_inicio = fields.Many2one('ruta_camionera.punto','Inicio')
    vespertino_retorno = fields.Many2one('ruta_camionera.punto','Retorno')
    vespertino_fin = fields.Many2one('ruta_camionera.punto','Fin')

    vespertino = fields.Many2many('ruta_camionera.puntos_vuelta', 'vespertino_rel', string='Vueltas')

    post_vespertino_inicio = fields.Many2one('ruta_camionera.punto','Inicio')
    post_vespertino_retorno = fields.Many2one('ruta_camionera.punto','Retorno')
    post_vespertino_fin = fields.Many2one('ruta_camionera.punto','Fin')

    post_vespertino = fields.Many2many('ruta_camionera.puntos_vuelta', 'post_vespertino_rel', string='Vueltas')
    
#######HOJA CRONOGRAMA RUTAS
class CronogramaSemanal(models.Model):
    _name = 'ruta_camionera.cronograma_semanal'

    vuelta = fields.Many2one('ruta_camionera.vuelta', 'Vuelta', required=True)
    unidad = fields.Many2one('ruta_camionera.camion', 'Unidad', required=True)

    variante_ruta = fields.Many2one('ruta_camionera.variante_ruta', 'Variante ruta')

class VarianteRuta(models.Model):
    _name = 'ruta_camionera.variante_ruta'
    _rec_name = 'nombre'

    nombre = fields.Char('Variante Ruta',size=15, required=True)