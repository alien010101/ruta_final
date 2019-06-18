# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


# wizard para el form view de elección de días
class RutaDetails(models.TransientModel):
    _name = 'ruta.reporte.duenio.wizard'

    date_start = fields.Date(string="Fecha inicial", required=True, default=fields.Date.today)
    date_end = fields.Date(string="Fecha final", required=True, default=fields.Date.today)

    @api.multi
    def get_report(self):
        pass
        # """Call when button 'Get Report' clicked.
        # """
        # data = {
        #     'ids': self.ids,
        #     'model': self._name,
        #     'form': {
        #         'date_start': self.date_start,
        #         'date_end': self.date_end,
        #     },
        # }

        # # use `module_name.report_id` as reference.
        # # `report_action()` will call `_get_report_values()` and pass `data` automatically.
        # return self.env.ref('ruta_camionera.recap_report').report_action(self, data=data)