from odoo import api, fields, models
from datetime import datetime, time

class BorrowReportWizard(models.TransientModel):
    _name = 'borrow.report.wizard'
    _description = 'Peminjaman Report Wizard'
    
    date_start = fields.Date(string='Tanggal Mulai')
    date_end = fields.Date(string='Tanggal Akhir')
    
    member_ids = fields.Many2many(
        comodel_name='people.member',
        string='Member',
    )
    
    def print_report_wizard(self):
        domain = []
        member_ids = self.member_ids
        if member_ids:
            domain += [('id', 'in', member_ids.ids)]
        if self.date_start:
            date_start_dt = datetime.combine(self.date_start, time.min)
            domain.append(('tanggal_pinjam', '>=', date_start_dt))
        if self.date_end:
            date_end_dt = datetime.combine(self.date_end, time.max)
            domain.append(('tanggal_pinjam', '<=', date_end_dt))  
        borrow_peminjaman = self.env['borrow.peminjaman'].search(domain)
        
        borrow_report = [{
        'name': rec.member_id.name,  
        'no_member': rec.no_member,
        'buku_ids': ", ".join(rec.buku_ids.mapped('name')),
        'tanggal_pinjam': rec.tanggal_pinjam,
        'tanggal_kembali': rec.tanggal_kembali
    } for rec in borrow_peminjaman]
        
        data = {
            'borrow_report': borrow_report,
            'form_data': {
                'date_start': self.date_start,
                'date_end': self.date_end,
                'member_ids': self.member_ids.ids
            }
        }
        return self.env.ref('simple_library.minjam_report_xlsx').report_action(self, data=data)
    
    
    
    # borrow_report = [{
    #         'name': member_id.name,
    #         'no_member': member_id.no_member,
    #         'member_id': member_id.name,
    #         'buku_ids': member_id.buku_ids.mapped('name'),
    #         'tanggal_pinjam': member_id.tanggal_pinjam,
    #         'tanggal_kembali': member_id.tanggal_kembali
    #     }
    #     for member_id in borrow_peminjaman]
        