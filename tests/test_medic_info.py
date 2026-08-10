from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestBlock3MedicInfo(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.MedicInfo = cls.env['hr.hospital.medic.info']

    def test_age_compute(self):
        record = self.MedicInfo.new({'birth_date': '2000-08-10'})
        record._compute_age()
        self.assertGreaterEqual(record.age, 0)

        empty = self.MedicInfo.new({})
        empty._compute_age()
        self.assertEqual(empty.age, 0)
