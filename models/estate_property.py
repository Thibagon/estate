from odoo import models,fields
from datetime import date
from dateutil.relativedelta import relativedelta

# Chapter 4
class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Evaluate the real estate value"

    name = fields.Char("Title",required=True)
    description = fields.Text("Description")
    property_type = fields.Char("Property type", required=True)
    postcode = fields.Integer("Postcode", default=31000)
    expected_price = fields.Float("Expected price", required=True)
    living_area_surface= fields.Float("Living area (sqm)",default=1.0)
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection(
        [
            ('N', 'North'),
            ('S', 'South'),
            ('E', 'Est'),
            ('W', 'West')
        ],
        default="S"
    )

    # Chapter 6 (modification and addition to chapter 4 model)
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

    _sql_constraints = [
        ('check_bedrooms',"CHECK(bedrooms > 0)",'You must have bedrooms')
    ]