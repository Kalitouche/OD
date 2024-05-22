from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import date, timedelta


class TestPropertyOffer(TransactionCase):

    def setUp(self):
        super(TestPropertyOffer, self).setUp()
        # Create a partner
        self.partner = self.env["res.partner"].create(
            {
                "name": "Test Partner",
                "email": "test@example.com",
            }
        )

        # Create a property
        self.property = self.env["estate.property"].create(
            {
                "name": "Test Property",
                "description": "Test Property Description",
            }
        )

    def test_create_offer(self):
        offer = self.env["estate.property.offer"].create(
            {
                "property_id": self.property.id,
                "partner_id": self.partner.id,
                "price": 150000.0,
                "validity": 7,
            }
        )
        self.assertEqual(offer.status, False, "Initial offer status should be empty")

    def test_compute_deadline(self):
        offer = self.env["estate.property.offer"].create(
            {
                "property_id": self.property.id,
                "partner_id": self.partner.id,
                "price": 150000.0,
                "validity": 7,
            }
        )
        expected_deadline = date.today() + timedelta(days=7)
        self.assertEqual(
            offer.deadline, expected_deadline, "Deadline computation is incorrect"
        )

    def test_accept_offer(self):
        offer = self.env["estate.property.offer"].create(
            {
                "property_id": self.property.id,
                "partner_id": self.partner.id,
                "price": 150000.0,
                "validity": 7,
            }
        )
        offer.action_accept_offer()
        self.assertEqual(offer.status, "accepted", "Offer should be accepted")
        self.assertEqual(
            offer.property_id.selling_price,
            offer.price,
            "Property selling price should be updated",
        )

    def test_decline_offer(self):
        offer = self.env["estate.property.offer"].create(
            {
                "property_id": self.property.id,
                "partner_id": self.partner.id,
                "price": 150000.0,
                "validity": 7,
            }
        )
        offer.action_decline_offer()
        self.assertEqual(offer.status, "refused", "Offer should be refused")
        self.assertEqual(
            offer.property_id.selling_price, 0, "Property selling price should be reset"
        )

    def test_validity_constraint(self):
        with self.assertRaises(ValidationError):
            self.env["estate.property.offer"].create(
                {
                    "property_id": self.property.id,
                    "partner_id": self.partner.id,
                    "price": 150000.0,
                    "validity": -1,  # Invalid validity
                }
            )

    def test_unique_accepted_offer(self):
        offer1 = self.env["estate.property.offer"].create(
            {
                "property_id": self.property.id,
                "partner_id": self.partner.id,
                "price": 150000.0,
                "validity": 7,
            }
        )
        offer1.action_accept_offer()

        with self.assertRaises(ValidationError):
            offer2 = self.env["estate.property.offer"].create(
                {
                    "property_id": self.property.id,
                    "partner_id": self.partner.id,
                    "price": 160000.0,
                    "validity": 7,
                }
            )
            offer2.action_accept_offer()


if __name__ == "__main__":
    unittest.main()
