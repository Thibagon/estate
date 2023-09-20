from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate_property_type"
    _description = "Type of property e.g: flat, house, office..."
    _order = "sequence, name"

    name = fields.Char("Type",required=True)
    property_ids = fields.One2many("estate_property", inverse_name="property_type_id", string="Properties")
    sequence = fields.Integer(default="1")
    offer_ids = fields.One2many("estate_property_offer", inverse_name="property_type_id")
    offer_count = fields.Integer(string="Number of offer", compute="_compute_count_offers")

    _sql_constraints = [
        ('unique_name','UNIQUE(name)','Property type name must be unique')
    ]

    def _compute_count_offers(self):
        for record in self:
            record.offer_count = len([o.id for o in record.offer_ids if o.property_type_id.id == record.id])

    def action_view_offers(self):
        res = self.env.ref("training_odoo.property_offer_action_view").read()[0]
        res["domain"] = [('id', 'in', self.offer_ids.ids)]
        return res
