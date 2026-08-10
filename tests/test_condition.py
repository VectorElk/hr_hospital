from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestBlock3Condition(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Condition = cls.env['hr.hospital.condition']

    def test_display_name_and_loop_constraint(self):
        parent = self.Condition.create({
            'name': 'Autoimmune',
            'description': 'Root condition',
        })
        child = self.Condition.create({
            'name': 'Lupus',
            'description': 'Child condition',
            'parent_id': parent.id,
        })

        child._compute_display_name()
        self.assertEqual(child.display_name, 'Autoimmune/Lupus')

        with self.assertRaises(ValidationError):
            parent.write({'parent_id': child.id})
