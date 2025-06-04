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
