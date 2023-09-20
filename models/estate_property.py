from odoo import models,fields,api
from odoo.exceptions import ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta


# Chapter 4
class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Evaluate the real estate value"

    name = fields.Char("Title",required=True)
    description = fields.Text("Description")
    property_type_id = fields.Many2one("estate_property_type", string="Type")
    postcode = fields.Integer("Postcode", default=31000)
    expected_price = fields.Float("Expected price", required=True)
    living_area_surface= fields.Float("Living area (sqm)",default=1.0)
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Float("Garden Area")
    garden_orientation = fields.Selection(
        [
            ('N', 'North'),
            ('S', 'South'),
            ('E', 'Est'),
            ('W', 'West')
        ],
        default="S"
    )
    selling_price = fields.Float("Selling price",readonly=True,copy=False)
    date_availability = fields.Date("Date available",default=date.today()+relativedelta(months=3),copy=False)
    bedrooms = fields.Integer("Bedrooms",default=2)
    active = fields.Boolean("Active",default=True)
    state = fields.Selection(
        [
            ("new","New"),
            ("offer_received","Offer Received"),
            ("offer_accepted","Offer Accepted"),
            ("sold","Sold"),
            ("canceled","Canceled")
        ],
        default="new"
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesman_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    tags_ids = fields.Many2many("estate_tags",string="Tags")
    offer_ids = fields.One2many("estate_property_offer",inverse_name="property_id",string="Offers")
    total_area = fields.Float(readonly=True, compute="_compute_total_area")
    best_offer = fields.Float(compute="_compute_best_offer")

    _sql_constraints = [
        ('check_bedrooms',"CHECK(bedrooms > 0)",'You must have bedrooms')
    ]

    @api.depends("living_area_surface", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area_surface + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            if len(record.offer_ids.ids) > 0:
                record.best_offer = max([p.price for p in record.offer_ids])
            else:
                record.best_offer = 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "N"
        else:
            self.garden_area = None
            self.garden_orientation = None

    def set_state_canceled(self):
        for record in self:
            if record.state != "sold":
                record.state = "canceled"
            else:
                raise ValidationError("You can't sold a canceled property")
        return True

    def set_state_sold(self):
        for record in self:
            if record.state != "canceled":
                record.state = "sold"
            else:
                raise ValidationError("You can't cancel an already sold property")
        return True
