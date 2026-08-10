from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HrHospitalVisitReportWizard(models.TransientModel):
    """Wizard to filter and report hospital visits by doctor, condition, and date range.

    Provides multi-select filters for doctors and conditions with optional date constraints.
    Pre-populates selected doctors from context if called from doctor views.
    """
    _name = 'hr.hospital.visit.report.wizard'
    _description = _('Visit Report Wizard')

    doctor_ids = fields.Many2many(
        comodel_name='hr.hospital.doctor',
        string=_('Doctors'),
    )
    res_condition_ids = fields.Many2many(
        comodel_name='hr.hospital.condition',
        string=_('Conditions'),
    )
    date_start = fields.Date(string=_('Date From'))
    date_end = fields.Date(string=_('Date To'))

    @api.constrains('date_start', 'date_end')
    def _check_date_range(self):
        """Validate date range constraint.

        Raises:
            ValidationError: If start date is after end date.
        """
        for record in self:
            if record.date_start and record.date_end:
                date_start = record.date_start
                date_end = record.date_end
                if date_start > date_end:
                    raise ValidationError(_('Date Start must be earlier than or equal to Date End.'))

    def default_get(self, fields_list):
        """Pre-populate doctor_ids from context if wizard called from doctor view.

        Args:
            fields_list (list): Fields to retrieve defaults for.

        Returns:
            dict: Default values for wizard fields.
        """
        active_model = self.env.context.get('active_model')
        active_ids = self.env.context.get('active_ids') or []
        if not active_ids and self.env.context.get('active_id'):
            active_ids = [self.env.context['active_id']]
        result = super().default_get(fields_list)

        if not isinstance(active_model, str) or not active_ids:
            return result

        active_records = self.env[active_model].browse(active_ids)

        if active_model == 'hr.hospital.doctor' and 'doctor_ids' in fields_list:
            result['doctor_ids'] = [(6, 0, active_records.ids)]
        return result

    def action_open_report(self):
        """Open visit list window with applied filters.

        Builds domain from selected doctors, conditions, and date range.
        Groups results by condition for easier analysis.

        Returns:
            dict: Action window with filtered visits grouped by condition.
        """

        domain = []
        if self.doctor_ids:
            domain.append(('res_doctor_id', 'in', self.doctor_ids.ids))
        if self.date_start:
            domain.append(('date', '>=', self.date_start))
        if self.date_end:
            domain.append(('date', '<=', self.date_end))
        if self.res_condition_ids:
            domain.append(('res_condition_id', 'in', self.res_condition_ids.ids))

        return {
            'type': 'ir.actions.act_window',
            'name': _('Visit Report'),
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,form',
            'target': 'current',
            'domain': domain,
            'context': {
                **self.env.context,
                'group_by': 'res_condition_id',
            },
        }
