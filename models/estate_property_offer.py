from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate_property_offer'
    _description = 'Offers made for a given property'

    price = fields.Float("Price",required=True)
    status = fields.Selection(
        [
            ('accepted','Accepted'),
            ('refused','Refused'),
            ('eval','In evaluation')
        ],
        copy=False,
        default='eval'
    )
    partner_id = fields.Many2one("res.partner",string="Partner",required=True)
    property_id = fields.Many2one("estate_property",string="Property",required=True)
