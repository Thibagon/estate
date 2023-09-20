from odoo import fields, models


class EstateTags(models.Model):
    _name = 'estate_tags'
    _description = 'Tags that can be set on estates'

    name = fields.Char("Name", required=True)

    _sql_constraints = [
        ('unique_name','UNIQUE(name)','Tag name must be unique')
    ]
