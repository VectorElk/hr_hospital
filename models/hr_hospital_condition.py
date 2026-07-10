from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HrHospitalCondition(models.Model):
    _name = 'hr.hospital.condition'
    _description = 'Hospital Condition'

    name = fields.Char(required=True)
    description = fields.Char(required=True)

    res_visit_ids = fields.Many2many('hr.hospital.visit')

    parent_id = fields.Many2one('hr.hospital.condition', string='Parent Condition', ondelete='cascade')
    display_name = fields.Char(compute='_compute_display_name', store=False)

    @api.depends('parent_id', 'name')
    def _compute_display_name(self):
        for record in self:
            path = []
            current = record
            visited = set()

            while current:
                if current.id in visited:
                    break
                visited.add(current.id)
                path.append(current.name)
                current = current.parent_id

            record.display_name = '/'.join(reversed(path)) if path else 'N/A'

    @api.constrains('parent_id')
    def _check_no_hierarchy_loop(self):
        for record in self:
            if not record.parent_id:
                continue

            visited = set()
            current = record.parent_id

            while current:
                if current.id in visited:
                    raise ValidationError('Circular hierarchy detected: condition cannot be its own ancestor.')
                visited.add(current.id)
                current = current.parent_id
