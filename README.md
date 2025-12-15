# Blog Uygulaması
 
 Bu proje, blog yazılarının kategorilere göre listelendiği, kullanıcıların yorum yapabildiği ve yazıları beğenebildiği web tabanlı bir blog uygulamasıdır. Django kullanılarak klasik template + view yapısında geliştirilmiştir.
 
 ## Özellikler
 
 ### 1. Kategori Yönetimi
 - Kategori listeleme
 - Kategorilere göre blog filtreleme
 - Yönetici (staff) için kategori ekleme/düzenleme/silme
 
 ### 2. Blog Yönetimi
 - Blog listeleme ve detay sayfası
 - Yönetici (staff) için blog oluşturma
 - Blog güncelleme/silme (yazar veya staff)
 - Taslak/Yayınlandı durumları
   - Taslak bloglar sadece yazar veya staff tarafından görüntülenebilir
 
 ### 3. Yorum Sistemi
 - Kullanıcılar bloglara yorum ekleyebilir
 - Kullanıcılar kendi yorumlarını düzenleyebilir
 - Yorum silme
   - Yorum sahibi silebilir
   - Staff tüm yorumları silebilir
 
 ### 4. Beğeni Sistemi
 - Blog beğenme / beğenmekten vazgeçme (toggle)
 - Beğeni sayısı sadece aktif beğenileri (likes=True) sayar
 
 ### 5. Görüntüleme Takibi
 - Blog detayına giren giriş yapmış kullanıcılar için görüntüleme kaydı oluşturma
 
 ### 6. Kullanıcı İşlemleri
 - Giriş / çıkış
 - Kayıt olma (register) sayfası
 
 ### 7. Arayüz / UI
 - Bootstrap 5 tabanlı modern ve responsive arayüz
 - Mobil/Tablet için offcanvas menü, Desktop için sabit sidebar
 
 ## Kullanılan Teknolojiler
 
 - **Backend:** Django 5.2.8
 - **Veritabanı:** SQLite
 - **Frontend:** HTML5, CSS3, Bootstrap 5, Bootstrap Icons
 - **Dil:** Python 3.8+
 
 ## Demo Yönetici Bilgileri
 
 - **Kullanıcı Adı:** admin
 - **Şifre:** admin123
