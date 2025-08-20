from odoo import api, fields, models
from asyncio.log import logger

class ReportBorrow(models.AbstractModel):
    _name = 'report.simple_library.minjam_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    
    def generate_xlsx_report(self, workbook, data, objs):

        sheet = workbook.add_worksheet('Peminjaman')
        text_style = workbook.add_format({'font_name': 'Times', 'left': 1, 'bottom':1, 'right':1, 'top':1, 'align': 'left'})
        title_style = workbook.add_format({'font_name': 'Times', 'font_size': 14, 'bold': True, 'valign': 'vcenter', 'align': 'center'})
        header_style = workbook.add_format({'font_name': 'Times', 'bold': True, 'left': 1, 'bottom':1, 'right':1, 'top':1, 'valign': 'vcenter', 'align': 'center', 'bg_color': '#5DB8E5'})
        
        # Atur lebar kolom
        sheet.set_column('A:A', 5)   # No
        sheet.set_column('B:B', 20)  # Kode Peminjaman
        sheet.set_column('C:C', 15)  # No Member
        sheet.set_column('D:D', 25)  # Nama Member
        sheet.set_column('E:E', 30)  # Judul Buku
        sheet.set_column('F:F', 15)  # Tanggal Pinjam
        sheet.set_column('G:G', 20)  # Tanggal Kembali

        # Header judul laporan
        sheet.merge_range('A1:G1', 'LAPORAN PEMINJAMAN BUKU', title_style)
        sheet.merge_range('A2:G2', 'Perpustakaan Simple Library', title_style)
            
        # Header
        headers = [
            "No", "Kode Peminjaman", "Nama Member", "ID Member",
            "Judul Buku", "Tanggal Pinjam", "Batas Pengembalian"
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
            domain.append(('tanggal_pinjam', '>=', date_start))
        if date_end:
            domain.append(('tanggal_pinjam', '<=', date_end))

        peminjaman_records = self.env['borrow.peminjaman'].search(domain, order="tanggal_pinjam desc")
        
        for rec in peminjaman_records:
            for buku in rec.buku_ids:
                sheet.write(row, 0, no, text_style)
                sheet.write(row, 1, rec.name or '', text_style)
                sheet.write(row, 2, rec.no_member or '', text_style)
                sheet.write(row, 3, rec.member_id.name or '', text_style)
                sheet.write(row, 4, rec.buku_ids.name or '', text_style)
                sheet.write(row, 5, rec.tanggal_pinjam or '', date_style)
                sheet.write(row, 6, rec.tanggal_kembali or '', date_style)
                row += 1
                no += 1
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
   