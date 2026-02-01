from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Produk, Kategori, Status
from decimal import Decimal

def produk_list(request):
    # Get filter parameter
    filter_status = request.GET.get('status', 'all')
    
    if filter_status == 'bisa_dijual':
        produk_list = Produk.objects.filter(status__nama_status='bisa dijual')
    else:
        produk_list = Produk.objects.all()
    
    # Get all status for filter dropdown
    status_list = Status.objects.all()
    
    context = {
        'produk_list': produk_list,
        'status_list': status_list,
        'current_filter': filter_status,
    }
    return render(request, 'products/produk_list.html', context)

def produk_tambah(request):
    if request.method == 'POST':
        nama_produk = request.POST.get('nama_produk', '').strip()
        harga = request.POST.get('harga', '').strip()
        kategori_id = request.POST.get('kategori_id')
        status_id = request.POST.get('status_id')
        
        # Validasi
        errors = []
        
        if not nama_produk:
            errors.append('Nama produk harus diisi!')
        
        if not harga:
            errors.append('Harga harus diisi!')
        else:
            try:
                harga_decimal = Decimal(harga)
                if harga_decimal <= 0:
                    errors.append('Harga harus berupa angka positif!')
            except:
                errors.append('Harga harus berupa angka!')
        
        if not kategori_id:
            errors.append('Kategori harus dipilih!')
        
        if not status_id:
            errors.append('Status harus dipilih!')
        
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            # Simpan produk
            Produk.objects.create(
                nama_produk=nama_produk,
                harga=harga_decimal,
                kategori_id=kategori_id,
                status_id=status_id
            )
            messages.success(request, 'Produk berhasil ditambahkan!')
            return redirect('produk_list')
    
    kategori_list = Kategori.objects.all()
    status_list = Status.objects.all()
    
    context = {
        'kategori_list': kategori_list,
        'status_list': status_list,
    }
    return render(request, 'products/produk_form.html', context)

def produk_edit(request, pk):
    produk = get_object_or_404(Produk, pk=pk)
    
    if request.method == 'POST':
        nama_produk = request.POST.get('nama_produk', '').strip()
        harga = request.POST.get('harga', '').strip()
        kategori_id = request.POST.get('kategori_id')
        status_id = request.POST.get('status_id')
        
        # Validasi
        errors = []
        
        if not nama_produk:
            errors.append('Nama produk harus diisi!')
        
        if not harga:
            errors.append('Harga harus diisi!')
        else:
            try:
                harga_decimal = Decimal(harga)
                if harga_decimal <= 0:
                    errors.append('Harga harus berupa angka positif!')
            except:
                errors.append('Harga harus berupa angka!')
        
        if not kategori_id:
            errors.append('Kategori harus dipilih!')
        
        if not status_id:
            errors.append('Status harus dipilih!')
        
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            # Update produk
            produk.nama_produk = nama_produk
            produk.harga = harga_decimal
            produk.kategori_id = kategori_id
            produk.status_id = status_id
            produk.save()
            
            messages.success(request, 'Produk berhasil diupdate!')
            return redirect('produk_list')
    
    kategori_list = Kategori.objects.all()
    status_list = Status.objects.all()
    
    context = {
        'produk': produk,
        'kategori_list': kategori_list,
        'status_list': status_list,
    }
    return render(request, 'products/produk_form.html', context)

def produk_hapus(request, pk):
    produk = get_object_or_404(Produk, pk=pk)
    
    if request.method == 'POST':
        nama = produk.nama_produk
        produk.delete()
        messages.success(request, f'Produk "{nama}" berhasil dihapus!')
        return redirect('produk_list')
    
    context = {
        'produk': produk,
    }
    return render(request, 'products/produk_confirm_delete.html', context)