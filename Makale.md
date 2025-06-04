<h1> Gerçek Zamanlı Sözdizimi Vurgulayıcı Tasarımı ve Uygulaması </h1>

<h2> Özet </h2>

Bu makale, Python programlama dili kullanılarak geliştirilen, gramer tabanlı bir gerçek zamanlı sözdizimi vurgulayıcının (syntax highlighter) tasarımını, 
geliştirilme sürecini ve uygulamasını ayrıntılı bir şekilde ele almaktadır. Sistem, sıfırdan yazılmış bir sözcüksel çözümleyici (lexer), 
bir sözdizimsel çözümleyici (parser) ve Tkinter kütüphanesiyle oluşturulmuş bir grafik kullanıcı arayüzü (GUI) içermektedir. Belirlenmiş bir gramer yapısını destekleyen bu sistem, 
anahtar kelimeler, operatörler, semboller, sayılar, tanımlayıcılar, karakter sabitleri ve yorumlar gibi çeşitli token türlerini gerçek zamanlı olarak renklendirir ve sözdizimsel hataları anında tespit eder.
Harici vurgulama kütüphanelerine bağımlı olmadan geliştirilen proje, kullanıcı dostu bir arayüzle kod görselleştirme ve hata analizi sunar. lexer_test.py ve parser_test.py dosyalarıyla yapılan kapsamlı birim testler, 
sistemin doğruluğunu ve güvenilirliğini doğrulamıştır. Bu makale, sistemin mimarisini, gramer tanımını, modüllerin işleyişini, test süreçlerini, performans optimizasyonlarını ve gelecekteki geliştirme olanaklarını derinlemesine incelemektedir.

<h2> 1. Giriş </h2>

Sözdizimi vurgulama, modern programlama ortamlarının vazgeçilmez bir özelliğidir. Kodun okunabilirliğini artırarak geliştiricilere, kod yapısını hızlıca anlamaları ve sözdizimsel hataları kolayca tespit etmeleri için görsel bir rehber sağlar. Bu proje, belirli bir gramer yapısına uygun, gerçek zamanlı bir sözdizimi vurgulayıcı geliştirmeyi hedeflemiştir. Sistem, Python ile tamamen sıfırdan yazılmış üç temel bileşenden oluşur: sözcüksel çözümleyici (lexer.py), sözdizimsel çözümleyici (parser.py) ve grafik kullanıcı arayüzü (highlighter_gui.py). Ayrıca, sistemin doğruluğunu test etmek için lexer_test.py ve parser_test.py dosyalarıyla kapsamlı birim testler uygulanmıştır. Projenin amacı, derleyici tasarımı ilkelerini pratikte uygulayarak, kullanıcı dostu bir arayüzle gerçek zamanlı kod analizi ve görselleştirme sunmaktır. Bu makale, sistemin tasarım felsefesini, teknik detaylarını, test süreçlerini ve potansiyel iyileştirme alanlarını ayrıntılı bir şekilde ele alacaktır.


<h2>2. Sistem Mimarisi</h2>

Sözdizimi vurgulayıcı, üç ana modülden oluşan modüler bir yapıya sahiptir:
Sözcüksel Çözümleyici (Lexer): Giriş kodunu karakter karakter tarar ve token’lara ayırır.
Sözdizimsel Çözümleyici (Parser): Token akışını Backus-Naur Form (BNF) gramerine göre analiz eder ve sözdizimsel doğruluğu kontrol eder.
Grafik Kullanıcı Arayüzü (GUI): Tkinter ile geliştirilen arayüz, token’ları renk kodlarıyla görselleştirir ve hata mesajlarını gerçek zamanlı olarak kullanıcıya sunar.
Sistem, aşağıdaki token türlerini destekler:<br>
Anahtar Kelimeler: <p font-color = "red">if , else , print , int , char , elif </p> <br>
Operatörler: + , - , * , / , = , == , != , > , <<br>
Semboller: &nbsp;&nbsp;( &nbsp;&nbsp; , &nbsp;&nbsp;  )&nbsp;&nbsp;, &nbsp;&nbsp;:  <br>
Sayılar: Tam sayı değerler (örn. 5, 123)<br>
Tanımlayıcılar: Kullanıcı tanımlı değişken isimleri (INT_VAR, CHAR_VAR)<br>
Karakter Sabitleri: Tek tırnak içindeki karakterler (örn. 'a', 'x')<br>
Yorumlar: # ile başlayan satır içi açıklamalar<br>

Sistem, kullanıcı girdisini anlık olarak işler, token’lara ayırır, gramer kurallarına göre doğrular ve GUI’de renklendirilmiş token’larla birlikte hata mesajlarını gösterir. Bu modüler yapı, sistemin hem bakımını hem de gelecekteki geliştirmelerini kolaylaştırır.


<h2>3. Sözcüksel Çözümleyici (Lexical Analyzer)</h2>

Sözcüksel çözümleyici, lexer.py dosyasındaki tokenize fonksiyonu ile uygulanmıştır. Bu fonksiyon, giriş kodunu karakter karakter tarayarak token’lara ayırır ve her token’ı uygun bir kategoriyle etiketler. Sözcüksel analiz, durum diyagramı (state diagram) yaklaşımına dayanır ve düzenli ifadeler yerine programlama tabanlı bir yöntem kullanır. Bu yaklaşım, sistemin taşınabilirliğini ve anlaşılırlığını artırır.

<h3>3.1 Token Sınıflandırma </h3>

classify fonksiyonu, kelimeleri aşağıdaki kurallara göre sınıflandırır:

Anahtar Kelimeler: if, else, print, int, char, elif için KEYWORD etiketi.

Sayılar: Sayısal değerler için NUMBER etiketi (örn. 123).

Değişken Tanımlayıcıları: int veya char anahtar kelimelerinden sonra gelen tanımlayıcılar için sırasıyla INT_VAR veya CHAR_VAR etiketi.

Genel Tanımlayıcılar: Daha önce tanımlanmamış değişken isimleri için ID etiketi.

Karakter Sabitleri: Tek tırnak içindeki karakterler için CHAR_LITERAL etiketi (örn. 'a').

Yorumlar: # ile başlayan satırlar için COMMENT etiketi.
