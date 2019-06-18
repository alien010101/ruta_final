# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import date

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


# wizard para el form view de elección de días
class EnrutamientoDetails(models.TransientModel):
    _name = 'enrutamiento.reporte.wizard'
    
    semana_actual = fields.Integer(string="Semana actual", required=True)
    semana_inicial = fields.Many2one('ruta_camionera.semana_inicial', 'Semana inicial', required=True)
    unidad = fields.Many2one('ruta_camionera.camion', 'Unidad', required=True)
    variante_ruta = fields.Many2one('ruta_camionera.variante_ruta', 'Variante Ruta', required=True)

    @api.multi
    def get_report(self):
        # pass
        """Call when button 'Get Report' clicked.
        """
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'semana_actual': self.semana_actual,
                'semana_inicial': self.semana_inicial.semana_inicial,
                'unidad': self.unidad.numero_economico,
                'variante_ruta': self.variante_ruta.nombre,
            },
        }

        # use `module_name.report_id` as reference.
        # `report_action()` will call `_get_report_values()` and pass `data` automatically.
        return self.env.ref('ruta_camionera.enrutamiento_report').report_action(self, data=data)

class ReportDetallesEnrutamiento(models.AbstractModel):
    _name = 'report.ruta_camionera.enrutamiento_report_view'

    @api.model
    def _get_report_values(self, docids, data=None):
        semana_actual = data['form']['semana_actual']
        semana_inicial = data['form']['semana_inicial']
        unidad_form = data['form']['unidad']
        variante_ruta = data['form']['variante_ruta']

        if semana_actual < semana_inicial:
            semana_actual = semana_inicial

        diferencia = semana_actual - semana_inicial
        diferencia = int(diferencia)

        ##acomodo de cronograma segun semana
        cantidad_registros = self.env['ruta_camionera.cronograma_semanal'].search_count([('variante_ruta', '=', variante_ruta )])
        enrutamientos = camiones = self.env['ruta_camionera.cronograma_semanal'].search([('variante_ruta', '=', variante_ruta )], order='id asc')
        cantidad_registros = cantidad_registros
        vueltas = []
        unidades = []

        for enrutamiento in enrutamientos:
            vueltas.append(
                enrutamiento.vuelta.nombre,
            )

        if diferencia>cantidad_registros:
            diferencia= diferencia%cantidad_registros

        if diferencia < 0:
            diferencia = 0

        i = diferencia
        unidades = []

        for enrutamiento in enrutamientos:
            if i == cantidad_registros:
                i = 0
            unidades.append({
                'vuelta': vueltas[i],
                'unidad': enrutamiento.unidad.numero_economico,
            })
            i += 1
        ##tomamos el nombre de la vuelta correspondiente a la unidad

        vuelta_seleccionada = ""
        for unidad in unidades:
            if unidad_form == unidad['unidad']:
                vuelta_seleccionada = unidad['vuelta']
        ##sacamos el recordset de enrutamiento
            # variables

        matutinos = []
        post_matutinos = []
        post_post_matutinos = []
        vespertinos = []
        post_vespertinos = []
        tiene_post_matu = True
        tiene_post_post_matu = True
        tiene_post_vesp = True
        vueltas_datos = camiones = self.env['ruta_camionera.vuelta'].search([('nombre', '=', vuelta_seleccionada )], order='id asc')
        
        
        rinde = vueltas_datos[0].rinde

        matutino_inicio = vueltas_datos[0].matutino_inicio
        matutino_retorno = vueltas_datos[0].matutino_retorno
        matutino_fin = vueltas_datos[0].matutino_fin

        post_matutino_inicio = vueltas_datos[0].post_matutino_inicio
        post_matutino_retorno = vueltas_datos[0].post_matutino_retorno
        post_matutino_fin = vueltas_datos[0].post_matutino_fin

        post_post_matutino_inicio = vueltas_datos[0].post_post_matutino_inicio
        post_post_matutino_retorno = vueltas_datos[0].post_post_matutino_retorno
        post_post_matutino_fin = vueltas_datos[0].post_post_matutino_fin

        vespertino_inicio = vueltas_datos[0].vespertino_inicio
        vespertino_retorno = vueltas_datos[0].vespertino_retorno
        vespertino_fin = vueltas_datos[0].vespertino_fin

        post_vespertino_inicio = vueltas_datos[0].post_vespertino_inicio
        post_vespertino_retorno = vueltas_datos[0].post_vespertino_retorno
        post_vespertino_fin = vueltas_datos[0].post_vespertino_fin

        puntos_vuelta = vueltas_datos[0].matutino
        puntos_vuelta_post_mt = vueltas_datos[0].post_matutino
        puntos_vuelta_vesp = vueltas_datos[0].vespertino
        

        if (not post_matutino_inicio.nombre and not post_matutino_retorno.nombre and not post_matutino_fin.nombre ):
            tiene_post_matu = False

        if (not post_post_matutino_inicio.nombre and not post_post_matutino_retorno.nombre and not post_post_matutino_fin.nombre ):
            tiene_post_post_matu = False
        
        if (not post_vespertino_inicio.nombre and not post_vespertino_retorno.nombre and not post_vespertino_fin.nombre ):
            tiene_post_vesp = False


        for punto in puntos_vuelta:
            indice = 0
            
            matutinos.append({
                'salida_inicio': punto[indice].salida_inicio,
                'salida_media': punto[indice].salida_media,
                'llegada_inicio': punto[indice].llegada_inicio,
            })

        for punto in puntos_vuelta_vesp:
            indice = 0
            
            vespertinos.append({
                'salida_inicio': punto[indice].salida_inicio,
                'salida_media': punto[indice].salida_media,
                'llegada_inicio': punto[indice].llegada_inicio,
            })

        if tiene_post_matu:
            puntos_vuelta_pm = vueltas_datos[0].post_matutino

            for punto in puntos_vuelta_pm:
                indice = 0
                
                post_matutinos.append({
                    'salida_inicio': punto[indice].salida_inicio,
                    'salida_media': punto[indice].salida_media,
                    'llegada_inicio': punto[indice].llegada_inicio,
                })

                indice += 1

        if tiene_post_post_matu:
            puntos_vuelta_post_pm = vueltas_datos[0].post_post_matutino

            for punto in puntos_vuelta_post_pm:
                indice = 0
                
                post_post_matutinos.append({
                    'salida_inicio': punto[indice].salida_inicio,
                    'salida_media': punto[indice].salida_media,
                    'llegada_inicio': punto[indice].llegada_inicio,
                })

                indice += 1
        
        if tiene_post_vesp:
            puntos_vuelta_pv = vueltas_datos[0].post_vespertino

            for punto_vp in puntos_vuelta_pv:
                indice = 0
                
                post_vespertinos.append({
                    'salida_inicio': punto_vp[indice].salida_inicio,
                    'salida_media': punto_vp[indice].salida_media,
                    'llegada_inicio': punto_vp[indice].llegada_inicio,
                })

                indice += 1

        
        
        fecha = date.today()
            
            
        vueltas_salida = {
            'rinde': rinde.nombre,
            'matutino_inicio': matutino_inicio.nombre,
            'matutino_retorno': matutino_retorno.nombre,
            'matutino_fin': matutino_fin.nombre,
            'post_matutino_inicio': post_matutino_inicio.nombre,
            'post_matutino_retorno': post_matutino_retorno.nombre,
            'post_matutino_fin': post_matutino_fin.nombre,
            'tiene_post_matu': tiene_post_matu,
            'vespertino_inicio': vespertino_inicio.nombre,
            'vespertino_retorno': vespertino_retorno.nombre,
            'vespertino_fin': vespertino_fin.nombre,
            'post_vespertino_inicio': post_vespertino_inicio.nombre,
            'post_vespertino_retorno': post_vespertino_retorno.nombre,
            'post_vespertino_fin': post_vespertino_fin.nombre,
            'tiene_post_vesp': tiene_post_vesp,
            'post_post_matutino_inicio': post_post_matutino_inicio.nombre,
            'post_post_matutino_retorno': post_post_matutino_retorno.nombre,
            'post_post_matutino_fin': post_post_matutino_fin.nombre,
            'tiene_post_post_matu': tiene_post_post_matu,
        }

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'semana_actual': semana_actual,
            'semana_inicial': semana_inicial,
            'diferencia': diferencia,
            'cantidad_registros': cantidad_registros,
            'vueltas': vueltas,
            'unidades': unidades,
            'unidad_captura': unidad_form,
            'vuelta_seleccionada': vuelta_seleccionada,
            'vueltas_salida': vueltas_salida,
            'matutinos': matutinos,
            'post_matutinos': post_matutinos,
            'post_post_matutinos': post_post_matutinos,
            'vespertinos': vespertinos,
            'post_vespertinos': post_vespertinos,
            'fecha': fecha.strftime("%d/%m/%Y"),
        }