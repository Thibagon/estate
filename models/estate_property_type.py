from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate_property_type"
    _description = "Type of property e.g: flat, house, office..."

    name = fields.Char("Type",required=True)