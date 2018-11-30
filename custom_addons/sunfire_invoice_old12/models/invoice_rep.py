from odoo import tools
from num2words import num2words
from odoo import api, fields, models
class account_invoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def get_num(self,x):
        return str(x[10:14])
        # return float(''.join(ele for ele in x if ele.isdigit()))
    def get_num_igst(self,x):
        return str(x[4:8])
    @api.multi
    def set_amt_in_worlds(self,amount):
        return num2words(amount,lang='en_IN').replace(',', ' ').title()
    @api.multi
    def my_func(self):
        sale_order_obj=self.env["sale.order"]
        se_id=sale_order_obj.search([('name','=',self.origin)])
        return se_id.opf_name
