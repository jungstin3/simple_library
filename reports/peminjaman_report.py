from odoo import api, fields, models
from datetime import datetime
from asyncio.log import logger

class ReportPeminjaman(models.AbstractModel):
    _name = 'report.simple_library.peminjaman_report_xlsx'
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
        
        # # Ambil nilai tanggal dari wizard
        # date_start = data['form_data']['date_start']
        # date_end = data['form_data']['date_end']

        # # Buat domain filter
        # domain = []
        # if date_start:
        #     domain.append(('tanggal_pinjam', '>=', date_start))
        # if date_end:
        #     domain.append(('tanggal_pinjam', '<=', date_end))

        # # Cari data sesuai domain
        # peminjaman_records = self.env['borrow.peminjaman'].search(domain, order="tanggal_pinjam desc")
        peminjaman_records = self.env['borrow.peminjaman'].search([], order="tanggal_pinjam desc")
        
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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # def generate_xlsx_report(self, workbook, data, peminjaman_report):
    #     # create some style to set up the font type, the font size, the border, and the aligment
    #     title_style = workbook.add_format({'font_name': 'Times', 'font_size': 14, 'bold': True, 'valign': 'vcenter', 'align': 'center'})
    #     header_style = workbook.add_format({'font_name': 'Times', 'bold': True, 'left': 1, 'bottom':1, 'right':1, 'top':1, 'valign': 'vcenter', 'align': 'center', 'bg_color': '#5DB8E5'})
    #     text_style = workbook.add_format({'font_name': 'Times', 'left': 1, 'bottom':1, 'right':1, 'top':1, 'align': 'left'})
    #     # result_style = workbook.add_format({'font_name': 'Times', 'bold': True, 'left': 1, 'bottom':1, 'right':1, 'top':1, 'align': 'center', 'bg_color': '#5DB8E5'})
    #     sheet = workbook.add_worksheet('peminjaman_report')
        
    #     # merge cell
    #     sheet.merge_range('A2:F2', 'DAFTAR CUSTOMER YANG DIKELOLA')
    #     sheet.merge_range('A4:A5', 'NO', header_style)
    #     sheet.merge_range('B4:B5', 'NAMA MEMBER', header_style)
    #     sheet.merge_range('C4:C5', 'ID MEMBER', header_style)
    #     sheet.merge_range('D4:D5', 'JUDUL BUKU', header_style)
    #     sheet.merge_range('E4:E5', 'TANGGAL PEMINJAMAN', header_style)
    #     sheet.merge_range('F4:F5', 'BATAS PENGEMBALIAN', header_style)

    #     # set up the column width
    #     sheet.set_column('A:A',3)
    #     sheet.set_column('B:B',30)
    #     sheet.set_column('C:C',30)
    #     sheet.set_column('D:D',20)
    #     sheet.set_column('E:E',20)
    #     sheet.set_column('F:F',20)

    #     peminjaman_data = data.get('peminjaman_report')
    #     if not peminjaman_data:
    #         raise ValueError("Missing 'peminjaman_report' in report data. Received keys: %s" % list(data.keys()))
    
    #     logger.info(data)
    #     # loop for writing data to worksheet
    #     row = 6
    #     for i, report in enumerate(data['peminjaman_data']):
    #         for line in report['peminjaman_line']:
    #             sheet.write(row, 0, i+1, text_style)
    #             sheet.write(row, 1, report['name'], text_style)
    #             sheet.write(row, 2, report['no_member'], text_style)
    #             sheet.write(row, 3, report['member_id'], text_style)
    #             sheet.write(row, 4, report['buku_ids'], text_style)
    #             sheet.write(row, 5, report['tanggal_pinjam'], text_style)
    #             sheet.write(row, 6, report['tanggal_kembali'], text_style)
    #             row += 1
        
        # calculate budget and customer
        # total_budget = sum([suv['budget'] for suv in data['penanggungjwb_report']])
        # total_customer = len(data['penanggungjwb_report'])

        # table title
        # sheet.merge_range('A{}:D{}'.format(row+1, row+1), 'Total Budget', header_style)
        # sheet.merge_range('E{}:H{}'.format(row+1, row+1), total_budget, result_style)
        # sheet.merge_range('A{}:D{}'.format(row+2, row+2), 'Total Customer', header_style)
        # sheet.merge_range('E{}:H{}'.format(row+2, row+2), total_customer, result_style)