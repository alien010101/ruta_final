# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


# wizard para el form view de elección de días
class RutaDetails(models.TransientModel):
    _name = 'ruta.reporte.wizard'

    date_start = fields.Date(string="Fecha inicial", required=True, default=fields.Date.today)
    date_end = fields.Date(string="Fecha final", required=True, default=fields.Date.today)

    @api.multi
    def get_report(self):
        """Call when button 'Get Report' clicked.
        """
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_start': self.date_start,
                'date_end': self.date_end,
            },
        }

        # use `module_name.report_id` as reference.
        # `report_action()` will call `_get_report_values()` and pass `data` automatically.
        return self.env.ref('ruta_camionera.recap_report').report_action(self, data=data)

class ReportDetallesRuta(models.AbstractModel):
    _name = 'report.ruta_camionera.ruta_report_view'

    @api.model
    def _get_report_values(self, docids, data=None):
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        date_start_obj = datetime.strptime(date_start, DATE_FORMAT)
        date_end_obj = datetime.strptime(date_end, DATE_FORMAT)
        date_diff = (date_end_obj - date_start_obj).days + 1

        #pie del reporte
        total_a_repartir_excedente = 0
        sumatoria_excedente = 0
        operadors_veinte_porciento = 0
        sumatoria_boletos_totales = 0
        ganancia_operador = ''

        #operadores individual
        docs = []
        conductores = []
        cantidad_registros = camiones = self.env['ruta_camionera.ruta_camionera'].search_count([('fecha','>=',date_start),('fecha', '<=', date_end )])
        camiones = self.env['ruta_camionera.ruta_camionera'].search([('fecha','>=',date_start),('fecha', '<=', date_end )], order='unidad asc')
        for camion in camiones:
            # asignacion de variables extra
            vueltas_totales = 0
            boletos_totales = 0
            suma_boletos = 0
            ingreso_valor = 0
            gastos_operativos = 0
            excedente = 0
            aportacion_operador = 0
            aportacion_subrogado = 0
                # boletaje medio
            boletos_x_vuelta = 0
            deficit = 0
            menos = 0
            mas = 0

                #total operador
            total_operador = 0
            costo_de_balas = 0
            operador_sin_deducciones_excedente = 0

            #constantes
            OCHO_PORCIEN = 0.8
            DIECIOCHO_PORCIEN = 0.18
            VEINTE_PORCIEN = 0.2
            COSTO_BOL_NOR = 7
            COSTO_BOL_TRAS = 3.5
            COSTO_BOL_NIN = 3.5
            CERO = 0
            DIA_SIETE = 70

            # Operaciones de los campos del reporte

                # oficina
            vueltas_totales = camion.sm_civil+(OCHO_PORCIEN*camion.cut_voca)
            ingreso_valor = (camion.boletos_normal * COSTO_BOL_NOR) + (camion.boletos_trasvale * COSTO_BOL_TRAS) + (camion.boletos_ninio * COSTO_BOL_NIN)
            gastos_operativos = 681.75*vueltas_totales
            excedente = ingreso_valor - gastos_operativos

                # boletos total
            suma_boletos = camion.boletos_normal+camion.boletos_trasvale+camion.boletos_ninio

                # total operador
            camiones_to = self.env['ruta_camionera.ruta_camionera'].search([('fecha','>=',date_start),('fecha', '<=', date_end )], order='unidad asc')
            suma_suma_operador = 0
            suma_excedente = 0
            suma_boletos_x_vuelta = 0
            suma_vueltas_totales = 0
            dieciocho_porciento = 0

            costo_balas_totales=0
            
            for camion_to in camiones_to:
                # variables de promedio por vuelta
                # boletos_totales_to = camion_to.boletos_normal+((camion_to.boletos_trasvale+camion_to.boletos_ninio)/2)
                boletos_totales_to = (camion_to.boletos_normal+camion_to.boletos_trasvale + camion_to.boletos_ninio)/(camion_to.sm_civil+(camion_to.cut_voca*OCHO_PORCIEN))
                suma_boletos_x_vuelta += boletos_totales_to
                # variables de sumatoria de registros por vueltas totales
                vueltas_totales_to = camion_to.sm_civil+(OCHO_PORCIEN*camion_to.cut_voca)
                suma_vueltas_totales += vueltas_totales_to
                # sumatoria registros excedente
                ingreso_valor_to = (camion_to.boletos_normal * COSTO_BOL_NOR) + (camion_to.boletos_trasvale * COSTO_BOL_TRAS) + (camion_to.boletos_ninio * COSTO_BOL_NIN)
                gastos_operativos_to = 681.75*vueltas_totales_to
                excedente_to = ingreso_valor_to - gastos_operativos_to
                if excedente_to > 0:
                    suma_excedente += excedente_to
                #suamatoria suma operador
                if camion_to.balas > CERO and camion_to.conductor != camion.conductor:
                    costo_de_balas_por_conductor = camion_to.balas * COSTO_BOL_NOR
                    costo_balas_totales += costo_de_balas_por_conductor
                    dieciocho_porciento = (costo_balas_totales * DIECIOCHO_PORCIEN)/cantidad_registros
                        
            promedio_boletos_x_vuelta = suma_boletos_x_vuelta/cantidad_registros ##quitar registros de los que no trabajaron

            if promedio_boletos_x_vuelta >= 158.75:
                incremento_porcentual = suma_excedente * VEINTE_PORCIEN
            elif promedio_boletos_x_vuelta <= 158.75:
                incremento_porcentual = suma_excedente * DIECIOCHO_PORCIEN

            operador_x_vuelta = incremento_porcentual / suma_vueltas_totales

            operador_sin_deducciones_excedente = vueltas_totales * operador_x_vuelta

            balas_negativas = 0
            if camion.balas < 0:
                balas_negativas = camion.balas * -1

            tengo_que_cambiar_el_nombre_a_esta_variable = operador_sin_deducciones_excedente - (camion.balas * 7) + balas_negativas

            costo_de_balas = tengo_que_cambiar_el_nombre_a_esta_variable + dieciocho_porciento

            total_operador = costo_de_balas + DIA_SIETE

            docs.append({
                
                'unidad': camion.unidad.numero_economico,
                'conductor': camion.conductor.name,
                'vueltas-totales': vueltas_totales,
                'b-normal': camion.boletos_normal,
                'b-trasvale': camion.boletos_trasvale,
                'b-ninio': camion.boletos_ninio,
                'boletos-total': suma_boletos,
                'oficina': excedente,
                'balas': camion.balas,
                'total-operador': total_operador,
            })

            #sumatorias pie reporte
            sumatoria_excedente += excedente
            sumatoria_boletos_totales += suma_boletos
        
        #operaciones pie de reporte

        pie = []
        if promedio_boletos_x_vuelta >= 158.75:
            total_a_repartir_excedente = sumatoria_excedente*VEINTE_PORCIEN
            ganancia_operador = '20%'
        elif promedio_boletos_x_vuelta < 158.75:
            total_a_repartir_excedente = sumatoria_excedente*DIECIOCHO_PORCIEN
            ganancia_operador = '18%'

        pendiente = 'pendiente' 

        pie = {
            'total-repartir-excedente': total_a_repartir_excedente,
            'operadores': cantidad_registros,
            'operador-x-vuelta': operador_x_vuelta,
            'septimo-dia': DIA_SIETE,
            'vueltas-totales': suma_vueltas_totales,
            'total-boletos-vendidos': sumatoria_boletos_totales,
            'boletos-promedio-x-vuelta': promedio_boletos_x_vuelta,
            'ganancia-operador': ganancia_operador,
        }

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_start': date_start,
            'date_end': date_end,
            'docs': docs,
            'pie': pie,
        }
    