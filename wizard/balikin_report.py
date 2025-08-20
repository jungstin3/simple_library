from odoo import api, fields, models
from asyncio.log import logger

class ReportGiveback(models.AbstractModel):
    _name = 'report.simple_library.balikin_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    
    def generate_xlsx_report(self, workbook, data, objs):

        sheet = workbook.add_worksheet('Pengembalian')
        text_style = workbook.add_format({'font_name': 'Times', 'left': 1, 'bottom':1, 'right':1, 'top':1, 'align': 'left'})
        title_style = workbook.add_format({'font_name': 'Times', 'font_size': 14, 'bold': True, 'valign': 'vcenter', 'align': 'center'})
        header_style = workbook.add_format({'font_name': 'Times', 'bold': True, 'left': 1, 'bottom':1, 'right':1, 'top':1, 'valign': 'vcenter', 'align': 'center', 'bg_color': '#5DB8E5'})
        
        # Atur lebar kolom
        sheet.set_column('A:A', 5)   # No
        sheet.set_column('B:B', 20)  # Kode Pengembalian
        sheet.set_column('C:C', 20)  # Kode Peminjaman
        sheet.set_column('D:D', 20)  # ID Member
        sheet.set_column('E:E', 25)  # Nama Member
        sheet.set_column('F:F', 30)  # Judul Buku
        sheet.set_column('G:G', 15)  # Tanggal Pinjam
        sheet.set_column('H:H', 20)  # Tanggal Kembali
        sheet.set_column('I:I', 20)  # Tanggal Pengembalian
        sheet.set_column('J:J', 10)  # Denda

        # Header judul laporan
        sheet.merge_range('A1:J1', 'LAPORAN PENGEMBALIAN BUKU', title_style)
        sheet.merge_range('A2:J2', 'Perpustakaan Simple Library', title_style)
            
        # Header
        headers = [
            "No", "Kode Pengembalian", "Kode Peminjaman", "ID Member", "Nama Member",
            "Judul Buku", "Tanggal Pinjam", "Batas Pengembalian", "Tanggal Pengembalian", "Denda"
        ]
        
        date_style = workbook.add_format({
            'num_format': 'dd/mm/yyyy',  
            'align': 'left',
            'valign': 'vcenter',
            'left': 1, 'bottom': 1, 'right': 1, 'top': 1,
        })
        
        for col, header in enumerate(headers):
            sheet.write(3, col, header, header_style)

        row = 4
        no = 1

        member_ids = data['form_data']['member_ids']
        date_start = data['form_data']['date_start']
        date_end = data['form_data']['date_end']

        domain = []
        if member_ids:
            domain.append(('member_id', 'in', member_ids))
        if date_start:
            domain.append(('tanggal_kembali_sekarang', '>=', date_start))
        if date_end:
            domain.append(('tanggal_kembali_sekarang', '<=', date_end))

        pengembalian_records = self.env['giveback.pengembalian'].search(domain, order="tanggal_kembali_sekarang desc")

        for rec in pengembalian_records:
            for buku in rec.pengembalian_buku_ids:
                sheet.write(row, 0, no, text_style) # No
                sheet.write(row, 1, rec.name or '', text_style) # Kode Pengembalian
                sheet.write(row, 2, rec.peminjaman_id.name or '', text_style) # Kode Peminjaman
                sheet.write(row, 3, rec.member_id.name or '', text_style) # ID Member
                sheet.write(row, 4, rec.no_member or '', text_style) # Nama Member
                sheet.write(row, 5, ", ".join(buku.buku_ids.mapped("name")), text_style) # Judul Buku
                sheet.write(row, 6, rec.tanggal_pinjam or '', date_style) # Tanggal Pinjam
                sheet.write(row, 7, rec.tanggal_kembali or '', date_style) # Tanggal Kembali
                sheet.write(row, 8, rec.tanggal_kembali_sekarang or '', date_style) # Tanggal Pengembalian
                sheet.write(row, 9, rec.denda or 0, text_style) # Denda
                row += 1
                no += 1
     
        # calculate budget and customer
        total_denda = sum(rec.denda for rec in pengembalian_records)
        total_customer = len(set(pengembalian_records.mapped('member_id.name')))

        # table title
        sheet.merge_range('A{}:F{}'.format(row+1, row+1), 'Total Denda', header_style)
        sheet.merge_range('G{}:J{}'.format(row+1, row+1), total_denda, text_style)
        sheet.merge_range('A{}:F{}'.format(row+2, row+2), 'Total Customer', header_style)
        sheet.merge_range('G{}:J{}'.format(row+2, row+2), total_customer, text_style)
        

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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
   