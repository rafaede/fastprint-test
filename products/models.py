from django.db import models

class Kategori(models.Model):
    id_kategori = models.AutoField(primary_key=True)
    nama_kategori = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nama_kategori
    
    class Meta:
        db_table = 'kategori'

class Status(models.Model):
    id_status = models.AutoField(primary_key=True)
    nama_status = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nama_status
    
    class Meta:
        db_table = 'status'

class Produk(models.Model):
    id_produk = models.AutoField(primary_key=True)
    nama_produk = models.CharField(max_length=200)
    harga = models.DecimalField(max_digits=15, decimal_places=2)
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE, db_column='kategori_id')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, db_column='status_id')
    
    def __str__(self):
        return self.nama_produk
    
    class Meta:
        db_table = 'produk'