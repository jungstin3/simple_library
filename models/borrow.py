from odoo import models, fields, api

class Peminjaman(models.Model):
    _name = 'borrow.peminjaman'
    _description = 'Data Peminjaman'

    name = fields.Char(string='No. Peminjaman', required=True, readonly=True, default='New')
    tanggal_pinjam = fields.Date(string='Tanggal Pinjam', default=fields.Date.today)
    tanggal_kembali = fields.Date(string='Tanggal Kembali')
    member_id = fields.Many2one('people.member', string='Member', required=True)
    no_member = fields.Char(string='No Member', related='member_id.partner_id.name', store=True)
    buku_ids = fields.Many2many('books.buku', string='Buku Dipinjam')
    pengembalian_line = fields.One2many('giveback.pengembalian', 'peminjaman_id', string='Pengembalian')
    state = fields.Selection([
        ("draft", "Draft"),
        ("dipinjam", "Dipinjam"),
        ("dikembalikan", "Dikembalikan"),
    ], string="Status", default="draft", required=True)
    
    def action_pinjam(self):
        for record in self:
            for buku in record.buku_ids:
                # Kurangi stok
                if buku.jumlah > 0:
                    buku.jumlah -= 1

                # Tambah ke log
                self.env['logbooks.bukulog'].create({
                    'buku_id': buku.id,
                    'member_id': record.member_id.id,
                    'peminjaman_id': record.id,
                })

    
    def action_pinjam(self):
        for record in self.buku_ids:
            if record.jumlah <= 0:
                raise ValueError("Buku tidak tersedia")
            else:
                record.jumlah -= 1
        self.state = 'dipinjam'
        
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('borrow.peminjaman') or 'New'

        return super(Peminjaman, self).create(vals)
    
    # def action_print_report(self):
    #     peminjaman_data = []
    #     for record in self:
    #         buku_titles = [{'name': buku.name} for buku in record.buku_ids]
    #         peminjaman_data.append({
    #             'name': record.name,
    #             'no_member': record.no_member,
    #             'member_id': record.member_id.name,
    #             'buku_ids': buku_titles,
    #             'tanggal_pinjam': record.tanggal_pinjam.strftime('%Y-%m-%d'),
    #             'tanggal_kembali': record.tanggal_kembali.strftime('%Y-%m-%d'),
    #         })

    #     data = {'peminjaman_line': peminjaman_data}
    #     return self.env.ref('simple_library.peminjaman_report_xlsx').report_action(self, data=data)

