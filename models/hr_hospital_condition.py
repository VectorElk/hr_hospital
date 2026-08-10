from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HrHospitalCondition(models.Model):
    """Hospital medical conditions/diseases with hierarchical classification.

    Supports parent-child condition relationships to model disease hierarchies.
    Prevents circular hierarchies through cycle detection.
    """
    _name = 'hr.hospital.condition'
    _description = 'Hospital Condition'

    name = fields.Char(required=True)
    description = fields.Char(required=True)

    res_visit_ids = fields.One2many('hr.hospital.visit', 'condition_id')

    parent_id = fields.Many2one('hr.hospital.condition', string='Parent Condition', ondelete='restrict')

    @api.depends('parent_id', 'name')
    def _compute_display_name(self):
        """Compute hierarchical display name from condition path.

        Builds full path from root to current condition, e.g. 'Autoimmune/Lupus'.
        Handles cycle detection to prevent infinite loops.
        """
        for record in self:
            path = []
            current = record
            visited = set()

            while current:
                current_data = current.read(['id', 'parent_id', 'name'])[0]
                if current_data['id'] in visited:
                    break
                visited.add(current_data['id'])
                path.append(current_data['name'])
                parent_value = current_data['parent_id']
                current = self.browse(parent_value[0]) if parent_value else False

            record.display_name = '/'.join(reversed(path)) if path else 'N/A'

    @api.constrains('parent_id')
    def _check_no_hierarchy_loop(self):
        """Prevent circular hierarchies in condition classification.

        Raises:
            ValidationError: If condition would create a circular parent-child chain.
        """
        for record in self:
            current = record.parent_id
            visited = {record.id}

            while current:
                current_data = current.read(['id', 'parent_id'])[0]
                if current_data['id'] in visited:
                    raise ValidationError('Circular hierarchy detected: condition cannot be its own ancestor.')
                visited.add(current_data['id'])
                parent_value = current_data['parent_id']
                current = self.browse(parent_value[0]) if parent_value else False
