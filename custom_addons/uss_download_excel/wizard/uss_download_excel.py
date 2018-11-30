# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time
from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
##from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
import xlwt
import datetime
import unicodedata
import base64
##import StringIO
##import csv, cStringIO
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

class UssDownloadExcel(models.TransientModel):
    _name = "uss.download.excel"
    _description = "Download sample Excel Sheet"
    date_from = fields.Date('Date From')

    @api.multi
    def uss_excel_report(self):
        data = {}
        _logger.info("In excel report method ! ")
        workbook = xlwt.Workbook()
        
        #Style for Excel
        style0 = xlwt.easyxf('font: bold True; font :name Arial;align: horiz left;')
        style1 = xlwt.easyxf('font:bold True;  font :name Arial; align: horiz right;')

        style2 = xlwt.easyxf('font :name Arial;align: horiz left;')
        style3 = xlwt.easyxf('font :name Arial; align: horiz right;', num_format_str='#,##0.00')
        style4 = xlwt.easyxf('font: bold True; font :name Arial;align: horiz right;')
        style5 = xlwt.easyxf('font :bold True; font: name Arial; align: horiz right;', num_format_str='#,##0.00')


        #Excel Heading Manipulation        
        sheet = workbook.add_sheet("sample sheet")
        sheet.col(1).width = 256 * 70
        heading1 = ' Sample Excel Sheet : ' 

        sheet.write(1,1,heading1,style0)
          
        sheet.col(0).width = 256 * 10
        sheet.col(1).width = 256 * 50
        sheet.col(2).width = 256 * 20
        sheet.write(5,0,'Sr No', style0)
        sheet.write(5,1,'Description', style0)
        sheet.write(5,2,'Expenditure $', style1)

        # workbook.save('excel_sheet.xls')
        # result_file = open('excel_sheet.xls','rb').read()
        # attach_id = self.env['wizard.excel.report'].create({
        #                                 'name':'excel_sheet.xls',
        #                                 'report':base64.encodestring(result_file)
        #             })

        workbook.save('/tmp/excel_sheet.xls')
        result_file = open('/tmp/excel_sheet.xls','rb').read()
        attach_id = self.env['wizard.excel.report'].create({
                                       'name':'excel_sheet.xls',
                                       'report':base64.encodestring(result_file)
                   })
        return {
            'name': _('Notification'),
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'wizard.excel.report',
            'res_id':attach_id.id,
            'data': None,
            'type': 'ir.actions.act_window',
            'target':'new'
        }
        
class WizardExcelReport(models.TransientModel):
    _name = "wizard.excel.report"
    
    report = fields.Binary('Prepared file',filters='.xls', readonly=True)
    name = fields.Char('File Name', size=32)        
   
