from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class ProjectTask(models.Model):
    _inherit = 'project.task'

    stage_id_name = fields.Char(compute="_compute_stage_id_name")

    def _compute_stage_id_name(self):
        for rec in self:
            rec.stage_id_name = rec.stage_id.name

    def set_subtasks_done(self):
        done_stage = self.env['project.task.type'].search([('name', 'in', ['Done', 'Concluído'])], limit=1).id
        (self | self.child_ids.filtered(lambda task: task.stage_id.name not in ['Done', 'Concluído'])).write(
            {'stage_id': done_stage})
        return {
            'type': 'ir.actions.client',
            'tag': 'reload'
        }

    @api.multi
    def open_confirm_wizard(self):
        new = self.env['confirm.wizard'].create({
            'project_task': self.id,
            'name': self.warning_message_wizard(),
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Confirm',
            'res_model': 'confirm.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': new.id,
            'view_id': self.env.ref('done_task.confirm_wizard_view', False).id,
            'target': 'new',
            'context': {'self': self.id}
        }

    def warning_message_wizard(self):
        warning = _("When you press 'Confirm', the following tasks will be set as 'Done':<br/>")
        tasks_not_in_done = self | self.child_ids.filtered(lambda t: t.stage_id.name not in ['Done', 'Concluído'])
        for task in tasks_not_in_done:
            warning += ' '.join(['-', task.name, '<br/>'])
        return warning


class Project(models.Model):
    _inherit = 'project.project'

    @api.multi
    def refresh_project(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }


class ConfirmWizard(models.TransientModel):
    _name = 'confirm.wizard'
    _description = 'Confirm Wizard'

    project_task = fields.Many2one('project.task')
    name = fields.Html()

    @api.multi
    def confirm_action(self):
        #
        return self.project_task.set_subtasks_done()
