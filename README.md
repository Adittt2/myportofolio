Nama : Aditya Hamka Pratama
NPM : 2506552752
Kelas : PBP F

### Tugas 1

Dalam proses pembuatan tugas 1 ini, saya menggunakan bantuan dari beberapa generative AI seperti gemini untuk membantu saya menjelaskan instruksi dari tugas yang sulit saya pahami, serta claude yang membantu saya dalam proses konversi desain figma menjadi code.

1. Elemen-elemen semantik HTML5 tersebut membuat struktur kode menjadi lebih rapi serta memudahkan pada proses styling dengan menggunakan CSS. Sehingga lebih efisien daripada menggunakan <div> yang sifatnya lebih generik.
2. Tantangan utama tentunya adalah bagaimana cara saya mengkonversi tampilan desktop yang lebar ke dalam sebuah tampilan mobile yang tentunya harus efisien tempat. Prioritas utama tentunya adalah yang berkaitan dengan hal-hal penting yang menggambarkan identitas saya seperti nama dan foto. Untuk pilihan menu awal dapat diringkas ke dalam sebuah menu garis tiga sehingga hemat tempat dan terlihat bagus.
3. Saya tidak dapat update mengenai aktivitas pribadi saya secara langsung (kecuali codenya dibongkar lagi) sehingga yang ingin ditambahkan selanjutnya itu mungkin fitur yang bisa update aktivitas secara real-time tanpa harus bongkar code.

### Tugas 2

Dalam proses pembuatan tugas 2 kali ini, saya menggunakan bantuan dari generative AI yaitu Gemini dan Claude dalam menjelaskan rangkaian alur pekerjaan yang harus saya lakukan serta membantu saya dalam menata tempat dan warna dari web portofolio saya.

1. Saat saya membuka web portofolio dan memencet experience atau certification, browser akan mengirim request kepada server yang kemudian akan ditangkap oleh urls.py project saya yang kemudian akan kembali dikirimkan ke urls.py aplikasi berdasarkan path yang terdapat dalam URL. urls.py aplikasi kemudian akan menentukan view yang sesuai dengan path,  kemudian view mengambil data lewat query dan mengirimnya ke template yang kemudian dirender menjadi hmtl lalu dikirim balik ke browser sebagai response.
2. Data sudah seharusnya di model agar memastikan data dapat di-update dan disesuaikan secara real-time tanpa harus mengubah atau edit code yang kemudian di-deploy kembali karena bersifat statis. Sehingga proses maintenance menjadi lebih efisien.
3. makemigrations hanya bertugas dalam membuat file migrasi tanpa mengubah database, sedangkan migrate bertugas untuk menjalankan migrasi file ke database.

### Tugas 4
Dalam proses pembuuatan tugas 4, saya menggunakan bantuan dari generative AI, yaitu Claude, dalam membantu saya memahami alur dan menyusun code yaitu pada code html dan css.

### Tugas 5
1.Debouncing yaitu menunda terjadinya eksekusi fungsi sampai user berhenti memicunya. Hal tersebut penting karena input pencarian AJAX terpicu setiap karakter ditekan sehingga kalau tanpa debouncing maka inputnya sangat banyak yang dapat membebani server dan database serta tampilan yang akan tidak stabil karena di-render setiap kali mengetik
2.fetch() asinkron dan langsung mengembalikan Promise. Await menjeda fungsi async hingga Promise selesai dan memberikan nilai aslinya tanpa membekukan halaman. Sehingga jika tidak ada await, maka variabel hanya menyimpan Promise yang belum selesai dan bukan nilai aslinya.
3.XSS merupakan serangan saat penyerang menyisipkan JavaScript ke halaman melalui input yang kemudian akan dijalankan di browser victim untuk bertindak atas nama mereja. Data AJAX lebih rentan karena tidak meng-escape {{}} secara otomatis seperti django, 

 