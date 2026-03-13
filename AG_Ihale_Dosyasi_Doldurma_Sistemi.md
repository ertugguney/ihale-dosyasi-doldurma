# İhale Dosyası Doldurma Sistemi Güncelleme Serüveni (Faz 1, Faz 2 & Faz 3)

Kullanıcı tarafından yönlendirilen toplam 40 adet değişiklik talebi alınmış ve tam kapsamlı şablon motoru güncellemeleri başarıyla uygulanmıştır.

**Talepler:**
İlk faz 13 madde, ikinci faz talimat/kelime boşlukları (14-22) maddelerinden oluşmaktaydı. Geri kalan yeni faz (23-40) kapsamı:
23. Sözleşme başlığında İhale Türü'nün büyük harfle ve bold olarak yazdırılması.
24. Ön Ödeme kısmındaki kompleks yapının UI ile entegre bir şekilde, "Yapılmayacaktır" ise oranın gizlenip cümlenin sadece "yapılmayacaktır" yapılması; "Yapılacaktır" ise girilen oranın eklenerek cümlenin oluşturulması.
25. Kesin Teminat "İSTENMEMEKTEDİR" seçilirse ikinci oransal cümle talimatının silinmesi, İSTENMEKTEDİR ise girilen değerle ikinci cümlenin oluşturulması.
26. Proje adında "Projesi" kelimesi varsa tekrarın önlenmesi.
27. "İsteklinin adı : … … … … … … … … …" boşluğunun proje adıyla eşleşmesinin iptal edilmesi.
28. "dava_gecmisi_yili" alanı için UI etiketinin "Kaç yıl geriye doğru Adli Sicil Kaydı İstenecek" olarak güncellenmesi.
30. Yayın referansı `<Örnek: TR21-23-İKT-XX/01>` ve `<ÖRNEK:...>` ibarelerinin tamamen silinmesi.
34. `< Proje adı >Projesi için <Mal Alımı...>` yapılarının boşluk kurallarına göre (`> Projesi`) birleştirilmesi.
35. Tablolardaki `<Lot Numarası>` alanının çıktıdan silinmesi.
38. `< Lot No, ihale lotlara bölünmüş ise>` yapısının korunduğundan emin olunması.
39. `<hizmetleri sağlamayı / malları tedarik etmeyi / yapım işini üstlenmeyi>` ifadesinin seçilen İhale Türü'ne göre uygun eş metinle değiştirilmesi.

**Çözüm Yaklaşımı:**
1. `field_config.py` alan eşleştirmelerindeki iptal edilecek kısımlar map'ten çıkarılıp `INSTRUCTION_FIELDS`'a (silinecekler) eklendi.
2. `doc_generator.py` motorunda özel regex `re.sub(r'(?i)\s+projesi$', '', str(value))` kurgulanarak Proje adındaki mükerrer hatalar giderildi. 
3. Ön Ödeme ve Kesin Teminat için "Yapılmayacaktır/İSTENMEMEKTEDİR" gibi negative varyantlarda `para.text` veya koşullu paragraf silme uygulandı. UI tarafında `app.py` üzerinde de `st.selectbox` koşullu gösterime bağlandı.

**Geliştirici Komutu:**
Uygulamayı çalıştırarak güncel kodlar test edilebilir.
```powershell
cd c:\Users\eguney\Desktop\ihale ; $start_time = Get-Date ; streamlit run app.py ; $end_time = Get-Date ; Write-Host "Toplam Yürütme Süresi: $(($end_time - $start_time).TotalSeconds) saniye" 
```
