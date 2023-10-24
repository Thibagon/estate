import datetime
import unittest
from odoo import fields
from odoo.tests import common, users
from odoo.exceptions import ValidationError


class PropertyOfferCase(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(PropertyOfferCase, cls).setUpClass()
        cls.admin_user = cls.env.ref("base.user_admin")

        cls.offer1 = cls.env["estate_property_offer"].create(
            {
                "price": float(360.52),
                "status": "accepted",
                "partner_id": (0, 0, {"name": "toto"}),
                "property_id": (0, 0, {"name": "propto"}),
                "validity": 50,
                "date_deadline": datetime.datetime(2023, 5, 23),
                "property_type_id": (0, 0, {"name": "house"}),
            }
        )

    @users("admin_user")
    def test_refuse_offer(self):
        print(f"Hello I am a test")
        offer = self.offer1.with_user(self.env.user)
        self.assertRaises(ValidationError)
