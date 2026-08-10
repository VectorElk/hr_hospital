from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestBlock3DoctorHistory(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Category = cls.env['hr.hospital.doctor.category']
        cls.Doctor = cls.env['hr.hospital.doctor']
        cls.Patient = cls.env['hr.hospital.patient']
        cls.History = cls.env['hr.hospital.doctor.history']

    def test_display_name_and_onchange(self):
        category = self.Category.create({'name': 'Specialist', 'sequence': 10})
        doctor = self.Doctor.create({
            'name': 'House',
            'position': 'Doctor',
            'res_doctor_category_id': category.id,
        })
        patient = self.Patient.create({'name': 'John Smith'})
        history = self.History.create({
            'res_patient_id': patient.id,
            'res_doctor_id': doctor.id,
            'start_date': '2026-01-10',
            'end_date': '2026-01-20',
        })

        history._compute_display_name()
        self.assertEqual(history.display_name, 'John Smith - House (Specialist) 2026-01-10')

        history.end_date = '2026-01-01'
        warning = history._onchange_dates()
        self.assertFalse(history.end_date)
        self.assertEqual(warning['warning']['title'], 'Warning')
        self.assertEqual(
            warning['warning']['message'],
            'Doctor change date cannot be earlier than assignment date.',
        )
