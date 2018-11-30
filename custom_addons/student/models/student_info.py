from odoo import api, fields, models,_
from odoo.exceptions import UserError


class StudentInfo(models.Model):
    _name = 'student.info'
    _description = 'Student INformation Form'

    fname = fields.Char(string='First Name',required=True)
    lname = fields.Char(string='Last Name')
    age = fields.Integer(string='Age')
    address=fields.Char(string="Address")
    roll_no=fields.Integer(string="Roll No.")
    partner_id=fields.Many2one('res.partner',string="Parent")
    parent_id=fields.Many2one('parent.info')
    stud_line=fields.One2many('student.subject','stud_id')
    fullname=fields.Char(string="Full name")
    
    # @api.onchange('age')
    # def validation_age(self):
    #     print("self===========>>>>>",self,self.age)
    #     if self.age:
    #         if self.age>20:
    #             raise UserError(_('Age Not Valid'))

    # @api.depends('lname','fname')
    # def compute_fullname(self):
    #     if self.lname and self.fname:
    #         self.fullname=self.fname+' '+self.lname

    # @api.multi
    # def compute_fullname(self):
    #     #if self.lname and self.fname:
    #     self.fullname=self.fname+' '+self.lname 

    def validation_age(self,vals):
        print("vals===========>>>>>",vals)
        if 'age' in vals:
            if vals['age']>20:
                raise UserError(_('Age Not Valid'))

    @api.model
    def create(self,vals):
        self.validation_age(vals)    
        new_id = super(StudentInfo,self).create(vals)
        return new_id



    @api.multi
    def write(self,vals):
        self.validation_age(vals)
        new_id = super(StudentInfo,self).write(vals)
        return new_id
class ResPartner(models.Model):
    _inherit='res.partner'
    addhar_no=fields.Char(string='Adhar No.')
class ParentInfo(models.Model):
    _name='parent.info'
    name=fields.Char('Parent Name')

class subjects_info(models.Model):
    _name="subject.info"
    _rec_name="name"
    name=fields.Char(string="Subject Name")

class student_subject(models.Model):
    _name="student.subject"

    stud_id=fields.Many2one('student.info')
    subject=fields.Many2one("subject.info",string="Subject")
    #subject=fields.Char(string="Subject")

