from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError
from datetime import date
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = "estate_property_offer"
    _description = "Offers made for a given property"
    _order = "price desc"

    price = fields.Float("Price", required=True)
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused"), ("eval", "In evaluation")],
        copy=False,
        default="eval",
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate_property", string="Property", required=True)
    validity = fields.Integer("Validity in days", default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )
    property_type_id = fields.Many2one(
        "estate_property_type", related="property_id.property_type_id"
    )

    _sql_constraints = [
        (
            "strictly_positive_offer_price",
            "CHECK(price>0)",
            "Offer price must be strictly positive",
        )
    ]

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            date_of_creation = (
                date.today() if not record.create_date else record.create_date.date()
            )
            record.date_deadline = date_of_creation + relativedelta(
                days=record.validity
            )

    @api.model
    def create(self, vals):
        prop = self.env["estate_property"].browse(vals["property_id"])
        if prop.state == "sold":
            raise ValidationError(f"You can't create an offer on a sold property")
        best_offer = prop.best_offer
        if vals["price"] >= best_offer:
            return super().create(vals)
        else:
            raise UserError(f"You can't put an offer lower than {best_offer}")

    def _inverse_date_deadline(self):
        for record in self:
            date_of_creation = (
                date.today() if not record.create_date else record.create_date.date()
            )
            delta = relativedelta(record.date_deadline, date_of_creation)
            record.validity = delta.days + delta.months * 30 + delta.years * 12

    def accept_offer(self):
        if not self._has_an_accepted_offer():
            for record in self:
                if (
                    record.status != "refused"
                    and record.property_id.state != "canceled"
                ):
                    record.status = "accepted"
                    record.property_id.selling_price = record.price
                    record.property_id.buyer_id = record.partner_id
                    self._refuse_all_others()
                    record.property_id.state = "offer_accepted"
                else:
                    raise ValidationError("This offer has been refused")
        else:
            raise ValidationError(
                "An offer has already been accepted for this property"
            )

    def refuse_offer(self):
        for offer in self:
            if offer.status != "accepted":
                offer.status = "refused"
            else:
                raise ValidationError("This offer is already accepted")

    def _has_an_accepted_offer(self):
        for property_offer in self.property_id.offer_ids:
            # The first hand of the condition give the possibility to click on the same accepted offer more than once
            if property_offer.id != self.id and property_offer.status == "accepted":
                return True

    def _refuse_all_others(self):
        for property_offer in self.property_id.offer_ids:
            if property_offer.id != self.id:
                property_offer.status = "refused"
