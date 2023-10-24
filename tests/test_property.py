import datetime
import unittest
from odoo import fields
from odoo.tests import common, users, tagged, Form
from odoo.exceptions import ValidationError


@tagged("post_install", "-at_install", "estate")
class PropertyTestCase(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(PropertyTestCase, cls).setUpClass()
        cls.buyer = cls.env["res.partner"].create({"name": "Patrice"})
        cls.properties = cls.env["estate_property"].create(
            [
                {
                    "name": "T2 - test_Argoulet",
                    "expected_price": 1234.00,
                }
            ]
        )
        cls.offers = cls.env["estate_property_offer"].create(
            [
                {
                    "price": 15000,
                    "status": "eval",
                    "partner_id": cls.buyer.id,
                    "property_id": cls.properties[0].id,
                }
            ]
        )

    def test_set_state_sold(self):
        # Test it's impossible to sell property without accepted offer
        with self.assertRaises(ValidationError):
            self.properties.set_state_sold()

        # Accept the offer
        self.offers.accept_offer()

        # It now should sell
        self.properties.set_state_sold()
        self.assertRecordValues(self.properties, [{"state": "sold"}])

        with self.assertRaises(ValidationError):
            self.offers = self.env["estate_property_offer"].create(
                [
                    {
                        "price": 9846851,
                        "status": "eval",
                        "partner_id": self.buyer.id,
                        "property_id": self.properties[0].id,
                    }
                ]
            )

    def test_garden_reset(self):
        with Form(self.properties[0]) as prop:
            self.assertFalse(prop.garden)
            self.assertEqual(prop.garden_area, 0)
            self.assertFalse(prop.garden_orientation)
            prop.garden = True

            self.assertEqual(prop.garden_area, 10)
            self.assertEqual(prop.garden_orientation, "N")
            prop.garden = False

            self.assertEqual(prop.garden_area, 0)
            self.assertFalse(prop.garden_orientation)
