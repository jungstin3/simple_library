from odoo import api, fields, models
from datetime import datetime, time

class GivebackReportWizard(models.TransientModel):
    _name = 'giveback.report.wizard'
    _description = 'Pengembalian Report Wizard'
    
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
        giveback_pengembalian = self.env['giveback.pengembalian'].search(domain)
        
        giveback_report = [{
        'name': rec.member_id.name,  
        'no_member': rec.no_member,
        'pengembalian_buku_ids': ", ".join(rec.pengembalian_buku_ids.mapped('buku_ids.name')),
        'tanggal_pinjam': rec.tanggal_pinjam,
        'tanggal_kembali': rec.tanggal_kembali,
        'tanggal_kembali_sekarang': rec.tanggal_kembali_sekarang
    } for rec in giveback_pengembalian]
        
        data = {
            'giveback_report': giveback_report,
            'form_data': {
                'date_start': self.date_start,
                'date_end': self.date_end,
                'member_ids': self.member_ids.ids
            }
        }
        return self.env.ref('simple_library.balikin_report_xlsx').report_action(self, data=data)
    

            # name = fields.Char(string="No. Pengembalian", required=True, readonly=True, default='New')
    # hitung_buku_ids = fields.Many2many('logbooks.bukulog', string='Buku Dikembalikan')
    # tanggal_kembali_sekarang = fields.Date(string='Tanggal Pengembalian', default=fields.Date.context_today)
    # peminjaman_id = fields.Many2one('borrow.peminjaman', string='Peminjaman', required=True)
    # pengembalian_buku_ids = fields.Many2many('borrow.peminjaman', string='Buku Dikembalikan')
    # tanggal_pinjam = fields.Date(related='peminjaman_id.tanggal_pinjam', store=True)
    # tanggal_kembali = fields.Date(related='peminjaman_id.tanggal_kembali', store=True)
    # member_id = fields.Many2one(related='peminjaman_id.member_id', store=True)
    # no_member = fields.Char(related='peminjaman_id.no_member', store=True)
    # denda = fields.Integer(string='Total Denda', compute='_compute_denda', store=True)
    