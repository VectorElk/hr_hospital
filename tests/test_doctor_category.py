from psycopg2.errors import UniqueViolation

from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestBlock3DoctorCategory(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Category = cls.env['hr.hospital.doctor.category']

    def test_unique_name_constraint(self):
        self.Category.create({'name': 'Specialist', 'sequence': 10})

        with self.assertRaises(UniqueViolation):
            self.Category.create({'name': 'Specialist', 'sequence': 20})
