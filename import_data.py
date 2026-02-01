import os
import django
import requests
from hashlib import md5

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Kategori, Status, Produk

url = "https://recruitment.fastprint.co.id/tes/api_tes_programmer"

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}

# Coba berbagai username
usernames_to_try = [
    "tesprogrammer010226C14",
    "tesprogrammer010226C15",
    "tesprogrammer010226C16",
    "tesprogrammer010226C17",
    "tesprogrammer010226C18",
]

# Password yang sudah terbukti berhasil
raw_password = "bisacoding-01-02-26"
password = md5(raw_password.encode()).hexdigest()

print("🔄 Mencari username yang valid...\n")

session = requests.Session()
success = False
valid_username = None

for username in usernames_to_try:
    print(f"Testing: {username}... ", end="")
    
    response = session.post(url, 
        data={
            'username': username,
            'password': password
        },
        headers=headers
    )
    
    if response.status_code == 200:
        try:
            data = response.json()
            if 'data' in data and data.get('error') != 1:
                print("✅ VALID!")
                valid_username = username
                success = True
                break
            else:
                print(f"❌ {data.get('ket', 'Invalid')}")
        except:
            print("❌ Error parsing")
    else:
        print(f"❌ HTTP {response.status_code}")

if not success:
    print("\n❌ Tidak ada username yang valid. Username mungkin berubah lagi.")
    print("Coba cek halaman test untuk hint username terbaru.")
    exit()

print(f"\n✅ Username valid: {valid_username}")
print("🔄 Mengambil data dari API...\n")

# Ambil data lagi dengan username yang valid
response = session.post(url, 
    data={
        'username': valid_username,
        'password': password
    },
    headers=headers
)

if response.status_code == 200:
    data = response.json()
    
    print(f"✅ Data berhasil diambil!")
    print(f"📊 Total data: {len(data['data'])} produk\n")
    
    # Clear existing data
    print("🗑️ Menghapus data lama...")
    Produk.objects.all().delete()
    Kategori.objects.all().delete()
    Status.objects.all().delete()
    
    # Collect unique kategori dan status
    kategori_set = set()
    status_set = set()
    
    for item in data['data']:
        kategori_set.add(item['kategori'])
        status_set.add(item['status'])
    
    print(f"\n📋 Membuat {len(kategori_set)} kategori...")
    kategori_dict = {}
    for idx, nama in enumerate(sorted(kategori_set), 1):
        kategori = Kategori.objects.create(
            id_kategori=idx,
            nama_kategori=nama
        )
        kategori_dict[nama] = kategori
        print(f"  ✓ {nama}")
    
    print(f"\n📋 Membuat {len(status_set)} status...")
    status_dict = {}
    for idx, nama in enumerate(sorted(status_set), 1):
        status_obj = Status.objects.create(
            id_status=idx,
            nama_status=nama
        )
        status_dict[nama] = status_obj
        print(f"  ✓ {nama}")
    
    print(f"\n📦 Mengimpor {len(data['data'])} produk...")
    count = 0
    for item in data['data']:
        Produk.objects.create(
            id_produk=item['id_produk'],
            nama_produk=item['nama_produk'],
            harga=item['harga'],
            kategori=kategori_dict[item['kategori']],
            status=status_dict[item['status']]
        )
        count += 1
        if count % 10 == 0:
            print(f"  → {count} produk...")
    
    print(f"\n🎉 IMPORT SELESAI!")
    print(f"✅ {Kategori.objects.count()} kategori")
    print(f"✅ {Status.objects.count()} status")  
    print(f"✅ {Produk.objects.count()} produk")
    
else:
    print(f"❌ Error: {response.status_code}")