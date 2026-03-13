# Görev 43 (Görev 16): Madde 14 Sözleşme Kodu Otomatik Doldurma

## Amaç
"İSTEKLİLERE TALİMATLAR" bölümünde yer alan "Sözleşme kodu:" satırındaki talimat metninin silinerek, formda girilen gerçek sözleşme kodunun dökümana otomatik olarak ve kalın (bold) formatta eklenmesi.

## Yapılan İşlemler
1. **Tespit ve Temizlik**:
   - `Sözleşme kodu:` ifadesini ve `<Ajans ile Yararlanıcı arasında...>` talimatını içeren paragraflar programatik olarak tespit edildi.
   - Paragrafın içeriği temizlenerek statik prefix ("Sözleşme kodu: ") ve dinamik veri alanı olarak yeniden yapılandırıldı.

2. **Dinamik Veri Aktarımı**:
   - Form verisindeki `sozlesme_kodu` alanı (Alan ID) kullanılarak gerçek kod dökümana işlendi.

3. **Görsel Düzenleme (Format)**:
   - Dökümana eklenen sözleşme kodu metni dikkati artırmak ve resmiyet sağlamak amacıyla **Koyu (Bold)** yazı tipiyle formatlandı.
   - İtalik format temizlendi.

4. **Güvenlik ve Bütünlük**:
   - `continue` komutu ile bu paragrafın genel run işleme döngüsünden kaçınılması sağlandı, böylece mizanpaj ve boldluk ayarlarının bozulması önlendi.

## Sonuç
`test_fix_16.py` scripti ile yapılan testlerde, döküman çıktısında talimatın tamamen kalktığı ve yerine formdan gelen kodun (örn: `TR21-23-IKT-01`) kalın bir şekilde yazıldığı doğrulanmıştır.

---
**Durum:** ✅ Tamamlandı
**Tarih:** 12.03.2026
