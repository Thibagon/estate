from odoo import fields, models


class EstateSalesman(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate_property", inverse_name="salesman_id")

