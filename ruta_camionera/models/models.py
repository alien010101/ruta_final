# -*- coding: utf-8 -*-

from odoo import models, fields, api

# modelo de camiones
class Camion(models.Model):
    _name = 'ruta_camionera.camion'
    _description = 'modelo para crear unidades para las rutas'
    _rec_name = 'numero_economico'

    numero_economico = fields.Char('Número Económico',size=6)
    matricula = fields.Char('Matrícula', size=7)

# modelo ruta
class RutaCamionera(models.Model):
    _name = 'ruta_camionera.ruta_camionera'
    _description = 'Ruta camionera'

    trabajo = fields.Boolean(string='Trabajó')
    unidad = fields.Many2one('ruta_camionera.camion','numero_economico')
    conductor = fields.Many2one('hr.employee','name')
    fecha = fields.Date(string="Fecha")
    
    # vueltas
    sm_civil = fields.Integer(string="SM-Civil")
    cut_voca = fields.Integer(string="CUT-Voca")

    # boletos
    boletos_normal = fields.Integer(string="Normal")
    boletos_trasvale = fields.Integer(string="Trasvale")
    boletos_ninio = fields.Integer(string="Infantil")

    balas = fields.Float(string="Balas")

    #configuracion provisional
    precio_normal = fields.Float(string="Costo boleto normal", default="7.0")
    precio_boletos_trasvale = fields.Float(string="Costo boleto trasvale", default="3.5")
    precio_boletos_ninio = fields.Float(string="Costo boleto niño", default="3.5")

    septimo_dia = fields.Float(string="Séptimo día", default="70")

    operador = fields.Float(string="Operador", default="119")
    subrogado = fields.Float(string="Subrogado", default="562.5")

    mecanicos = fields.Float(string="Mecánicos", default="104.5454")
    mutualidad_operador = fields.Float(string="Mutualidad Operador", default="70.0")
    administracion = fields.Float(string="Administración", default="595.00")
    mutualidad_subrogado = fields.Float(string="Mutualidad Subrogado", default="35")


    

    