from odoo import models, fields, api

class Member(models.Model):
    _name = 'people.member'
    _inherits = {'res.partner': 'partner_id'}
    _description = 'Data Member Perpustakaan'

    image = fields.Binary(string='Foto')
    partner_id = fields.Many2one('res.partner', string='Nama', required=True, ondelete='restrict')
    name = fields.Char(string='Nomor Anggota', required=True, readonly=True, default='New')
    jenis_kelamin = fields.Selection([('laki_laki', 'Laki-laki'), ('perempuan', 'Perempuan')], string='Jenis Kelamin')
    peminjaman_line = fields.One2many('borrow.peminjaman', 'member_id', string='Daftar Peminjaman')
    peminjaman = fields.Integer(string='Jumlah Peminjaman', compute='_compute_peminjaman', store=True)
    pengembalian_line = fields.One2many('giveback.pengembalian', 'member_id', string='Daftar Pengembalian')
    pengembalian = fields.Integer(string='Jumlah Pengembalian', compute='_compute_pengembalian', store=True)
    
    @api.depends('peminjaman_line.state')
    def _compute_peminjaman(self):
        for record in self:
            aktif = record.peminjaman_line.filtered(lambda r: r.state == 'dipinjam')
            record.peminjaman = len(aktif)
            print("Peminjaman aktif:", aktif) 
    #.filtered(lambda r: not r.xxx_id)
    
    @api.depends('pengembalian_line.state')
    def _compute_pengembalian(self):
        for record in self:
            aktif = record.pengembalian_line.filtered(lambda r: r.state == 'dikembalikan')
            record.pengembalian = len(aktif)
            print("Pengembalian aktif:", aktif)
    
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('people.member') or 'New'
            return super(Member, self).create(vals)
        
    def action_view_peminjaman_smart(self):
        self.ensure_one()
        return{
            'name': 'Peminjaman Member',
            'type': 'ir.actions.act_window',
            'res_model': 'borrow.peminjaman',
            'view_mode': 'list,form',
            'domain': [('member_id', '=', self.id)],
            'context':{'create': False},
            'target': 'current'
        }

    def action_view_pengembalian_smart(self):
        self.ensure_one()
        return{
            'name': 'Pengembalian Member',
            'type': 'ir.actions.act_window',
            'res_model': 'giveback.pengembalian',
            'view_mode': 'list,form',
            'domain': [('member_id', '=', self.id)],
            'context':{'create': False},
            'target': 'current'
        }
    
    def action_print_peminjaman_report(self):
        peminjaman_data = []
        for record in self:
            buku_titles = [{'name': buku.name} for buku in record.buku_ids]
            peminjaman_data.append({
                'name': record.name,
                'no_member': record.no_member,
                'member_id': record.member_id.name,
                'buku_ids': ", ".join([b['name'] for b in buku_titles]),
                'tanggal_pinjam': record.tanggal_pinjam.strftime('%Y-%m-%d'),
                'tanggal_kembali': record.tanggal_kembali.strftime('%Y-%m-%d'),
            })

        data = {'peminjaman_report': peminjaman_data}
        return self.env.ref('simple_library.peminjaman_report_xlsx').report_action(self, data=data)
