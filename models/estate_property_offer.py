from odoo import fields, models, api
from datetime import date
from dateutil.relativedelta import relativedelta

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
    validity = fields.Integer("Validity in days",default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            date_of_creation = date.today() if not record.create_date else record.create_date.date()
            record.date_deadline = date_of_creation+relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            date_of_creation = date.today() if not record.create_date else record.create_date.date()
            delta = relativedelta(record.date_deadline, date_of_creation)
            record.validity = delta.days + delta.months * 30 + delta.years * 12
