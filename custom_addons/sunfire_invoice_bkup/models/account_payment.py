from odoo import api, fields, models


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    tds=fields.Monetary('TDS')

    @api.one
    @api.depends('invoice_ids', 'amount', 'payment_date', 'currency_id','tds')
    def _compute_payment_difference(self):
        if len(self.invoice_ids) == 0:
            return
        if self.invoice_ids[0].type in ['in_invoice', 'out_refund']:
            self.payment_difference = self.amount - self._compute_total_invoices_amount()
            #print("debug3===============>",self.payment_difference,self.amount)
        else:
            self.payment_difference = self._compute_total_invoices_amount() - self.amount-self.tds
            #print("debug4@@@@@@@@@@",self.payment_difference,self.amount)

    def _get_shared_move_line_vals(self, debit, credit, amount_currency, move_id, invoice_id=False):
        """ Returns values common to both move lines (except for debit, credit and amount_currency which are reversed)
        """
        #print("_get_shared_move_line_vals=======>tds,debit,credit",self.tds,debit,credit)
        return {
            'partner_id': self.payment_type in ('inbound', 'outbound') and self.env['res.partner']._find_accounting_partner(self.partner_id).id or False,
            'invoice_id': invoice_id and invoice_id.id or False,
            'move_id': move_id,
            'debit': debit,
            'credit': credit,
            'amount_currency': amount_currency or False,
            'payment_id': self.id,
            'tds':self.tds
        }
    
class account_abstract_payment(models.AbstractModel):
    _inherit = "account.abstract.payment" 

    @api.model
    def _compute_total_invoices_amount(self):
        """ Compute the sum of the residual of invoices, expressed in the payment currency """
        payment_currency = self.currency_id or self.journal_id.currency_id or self.journal_id.company_id.currency_id or self.env.user.company_id.currency_id

        total = 0
        for inv in self.invoice_ids:
            if inv.currency_id == payment_currency:
                total += inv.residual_signed
                #print("Debug1@@@@@@@@@",total,inv.residual_signed)
            else:
                total += inv.company_currency_id.with_context(date=self.payment_date).compute(
                    inv.residual_company_signed, payment_currency)
                #print("Debug2=============>",total,inv.residual_signed)
        return abs(total)
   