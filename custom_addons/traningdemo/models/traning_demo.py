# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError,ValidationError
import re
import datetime
from odoo.addons import decimal_precision as dp
from dateutil.relativedelta import relativedelta
import smtplib

# create_by | create_date | update_by | update_date
# Ajinkya      17/10/2018                
# Info : 


class traningdemo(models.Model):
    _name ="traningdemo.info"
    from_date=fields.Date(string="From Date", help="Enter The Seminar Start Date",required="True")
    to_date=fields.Date(string="To Date", help="Enter the Seminar End Date",required="True")
    traning_title=fields.Char(string="Traning Title", help="Enter The Title Of Seminar Which Are Going To Conduct",required="True")
    duration=fields.Char(string="Duration of Seminar",compute='cal_duration', help="How many Day to compelete the seminar")
    traning_method=fields.Char(string="Traning Method", help="Enter The Type ie Online or Manual")
    learning=fields.Char(string="Learning", help="Learning")
    job_impact=fields.Char(string="Job Impact", help="Job Impact")
    business_impact=fields.Char(string="Business Impact",help="Enter The Venue")
    certification_completed=fields.Char(string="Certification Completed",help="Certification Completed")
    cost_of_traning=fields.Float(string="Cost Of Traning",digits=dp.get_precision('cost_of_traning'), help="Cost Of Traning/Certification")
    #vendor=fields.Many2one("res.partner")
    vendor=fields.Many2one("res.partner")
    traning_by=fields.Char(string="Traning By",help="Enter The Name Of Traniner")
    certification= fields.Selection([('yes','Yes'),('no','No')],'Certification',default='no',required="True")
    date_certificate_tobeuploaded=fields.Date(string="Date By which ceritificate to be uploaded",help="When candidate get certificate of completion ")
    release= fields.Selection([('yes','Yes'),('no','No')],'Release',default='no')
    #traningdemo_line=fields.One2many("traningdemoline.info",'traningdemo_id')
    #_sql_constraints = [('unique_user_id', 'unique(traningdemo_line.user_id,traningdemo_line.traningdemo_id,from_date)', 'Please Enter the Unique Employee')]
    traningdemo_line=fields.One2many("traningdemoline.info",'traningdemo_id',domain=[x for x in [('state','=','tobeapproved')]])
    traningdemo_line_approved=fields.One2many("traningdemoline.info",'traningdemo_id',domain=[x for x in [('state','=','approved')]])
    traningdemo_line_withdraw=fields.One2many("traningdemoline.info",'traningdemo_id',domain=[x for x in [('state','=','withdraw')]])
    traningdemo_line_waiting=fields.One2many("traningdemoline.info",'traningdemo_id',domain=[x for x in [('state','=','waiting')]])


    
    
    
    @api.onchange('traning_title') # to check the title name should start with only A-Z and only character
    def title_validation(self):
        if self.traning_title:
            for order in self.search([]): # to retrive all the data from the database
                if order.traning_title:
                  #  print("@@@@@@@@@@@@@@@@@@@@",order.traning_title)
                    if order.traning_title.lower().strip().replace(" ","") == self.traning_title.lower().strip().replace(" ",""): # this is to convert the string into lower case , remive the white sapce from the database value and also from the user input
                        raise Warning("Traning title already exists")




        
    @api.constrains('traning_title') # same as the above function 
    def validation_title(self):
        #self.title_validation()
        if self.traning_title:
            for order in self.search([]):
                if order.traning_title:
                   # print("===================>",order.traning_title)
                    if order.traning_title.lower().strip().replace(" ","") == self.traning_title.lower().strip().replace(" ","") and self.id!=order.id:
                        raise Warning("Traning title already exists")
            
    @api.onchange('cost_of_traning') # to check whether the cost of traning should not be -ve
    def cost_validation(self):          
        if self.cost_of_traning:
            if self.cost_of_traning < 0: # to check that the user has not enterd the -ve cost
                raise UserError("Invalid Cost")

    
    @api.onchange('from_date')# to check the the start not be less than the current date
    def check_startdate(self):
        if self.from_date:
            print("hello================>>",datetime.date.today())
            print(self.from_date)
            start_date = datetime.datetime.strptime(self.from_date,'%Y-%m-%d').date() # this is for the covertion into  the date
            if start_date < datetime.date.today():
               
                raise Warning("Please Enter a Valid Start Date")

    @api.multi
    @api.onchange('to_date') # to check the the end date should not be less than the current date
    def validate_endate(self):
        if self.from_date and self.to_date:
            if self.to_date < self.from_date: # this is for the to check that the end date is not greater than the start date
                raise ValidationError("Please Enter a Valid End Date ")

    @api.depends('from_date','to_date')# calculation of start date and the end date and give the calculated no day from the strat date and the end date
    def cal_duration(self):
        for order in self:
            if order.from_date and order.to_date:
                start_date = datetime.datetime.strptime(order.from_date,'%Y-%m-%d').date()
                end_date = datetime.datetime.strptime(order.to_date,'%Y-%m-%d').date()
                y_date=datetime.datetime.strptime('2018-10-25','%Y-%m-%d').date() # this is to take the fix date 
                x_date=datetime.datetime.strptime('2018-10-26','%Y-%m-%d').date() # same as above
                z=x_date-y_date  # we have taken the x and y date becoz it will give the 1 no and it is stored in the z variable
                order.k=str(z).split(',')[0] # to split the comma from the date and take only the date not the time  
                d1=end_date-start_date+z
                order.duration=str(d1).split(',')[0]    # this is to covert from the date to string 
 
                print("No of days========>",d1.days)
            


# action after clicking on the self nominate button then then this method is called.
# in this method is we have done that the if a manager or a user logs in then the user or a manager can nominate self that th
    @api.multi
    def get_nomine(self):
        print('login user id',self.env.uid)
        print('self.id=====>',self.id)
        hr_emp_obj=self.env['hr.employee']
        hr_emp_ids=hr_emp_obj.search([('user_id','=',self.env.uid)])
        vals={
             'traningdemo_id':self.id,
             'user_id':hr_emp_ids.id
        }
        tr_id=self.traningdemo_line.create(vals)
        print('tayar id',tr_id.id)

    



    @api.onchange('date_certificate_tobeuploaded') # to check the the end date should not be less than the current date
    def validate_upload_date(self):
            if self.date_certificate_tobeuploaded < self.to_date: # this is for the to check that the end date is not greater than the start date
                raise Warning("Enter valid End date ")

            

    
class traningdemo_line(models.Model): # this is for the add the item dynamically  into the  db 
    _name="traningdemoline.info"
    traningdemo_id=fields.Many2one("traningdemo.info")
    user_id=fields.Many2one("hr.employee",string="Assigned Employee",required=True,help="Select the user for the traning")
    _sql_constraints = [('unique_user_id', 'unique(user_id,traningdemo_id)', 'Please Enter the Unique Employee')]
    state=fields.Selection([('tobeapproved','Tobeapproved'),('approved','Approved'),('withdraw','Withdraw'),('waiting','Waiting'),('reject','Reject')],default="tobeapproved")
    approved_flag=fields.Boolean(string="Approve")
    withdraw_flag=fields.Boolean(string="Withdraw")
    waiting_flag=fields.Boolean(string="Waiting")
    reject_flag=fields.Boolean(string="Reject")

    # this is to change  the state in the state drop down list accordin to the manager.
    @api.onchange('approved_flag','withdraw_flag','waiting_flag','reject_flag')
    def change_stateTobeapproved_approved(self):
        if self.approved_flag == True:
            self.write({'state': 'approved'})
        elif self.withdraw_flag == True:
            self.write({'state': 'withdraw'})
        elif self.waiting_flag == True:
            self.write({'state': 'waiting'})
        elif self.reject_flag == True:
            self.write({'state': 'reject'})
        else:
            self.write({'state': 'tobeapproved'})

    # If Admin assign a user who is already assign to another project for that particular duration 
    @api.onchange('traningdemo_id','user_id') 
    def validate_seminarofusers(self):
        user_obj_id=self.search([('user_id','=',self.user_id.id)])
        for order in user_obj_id:
            from_date_of_order=datetime.datetime.strptime(order.traningdemo_id.from_date,'%Y-%m-%d').date()
            to_date_of_order=datetime.datetime.strptime(order.traningdemo_id.to_date,'%Y-%m-%d').date()
            from_date_of_traningdemo_id=datetime.datetime.strptime(str(self.traningdemo_id.from_date),'%Y-%m-%d').date()
            to_date_of_trainingdemo_id=datetime.datetime.strptime(str(self.traningdemo_id.to_date),'%Y-%m-%d').date()
            if (from_date_of_order < to_date_of_trainingdemo_id)or(from_date_of_order>from_date_of_traningdemo_id):
                raise UserError("{} is already assign to {} from {} date to {} date".format(self.user_id.name,self.traningdemo_id.traning_title,from_date_of_order,to_date_of_order))

    @api.constrains('user_id')
    def validate_blank_user(self):
        if self.user_id:
            if self.user_id==False: 
                print("User is Blank----",self.user_id)
                raise ValidationError('Please select the user')


   




