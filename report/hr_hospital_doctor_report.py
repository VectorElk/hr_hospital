import base64
from pathlib import Path

from odoo import fields, models


class ReportHrHospitalDoctor(models.AbstractModel):
    _name = 'report.hr_hospital.hr_hospital_doctor_report_document'
    _description = 'Doctor Report'

    def _get_logo_data_uri(self):
        logo_path = Path(__file__).resolve().parents[1] / 'static' / 'description' / 'icon.png'
        if not logo_path.exists():
            return False
        return 'data:image/png;base64,%s' % base64.b64encode(logo_path.read_bytes()).decode()

    def _get_report_values(self, docids, data=None):
        doctors = self.env['hr.hospital.doctor'].browse(docids)
        company = self.env.company
        visit_lines_by_doctor = {}
        patient_lines_by_doctor = {}
        visit_model = self.env['hr.hospital.visit']
        patient_model = self.env['hr.hospital.patient']

        for doctor in doctors:
            visit_lines_by_doctor[doctor.id] = visit_model.search(
                [('res_doctor_id', '=', doctor.id)],
                order='planned_date desc, id desc',
            )
            patient_lines_by_doctor[doctor.id] = patient_model.search(
                [('family_doctor_id', '=', doctor.id)],
                order='name asc, id asc',
            )

        return {
            'doc_ids': docids,
            'doc_model': 'hr.hospital.doctor',
            'docs': doctors,
            'company': company,
            'logo_data_uri': self._get_logo_data_uri(),
            'generated_on': fields.Datetime.now(),
            'visit_lines_by_doctor': visit_lines_by_doctor,
            'patient_lines_by_doctor': patient_lines_by_doctor,
        }
