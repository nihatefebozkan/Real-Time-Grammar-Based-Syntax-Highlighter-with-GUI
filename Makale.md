# Gerçek Zamanlı Sözdizimi Vurgulayıcı: Tasarım ve Uygulama


## Özet

Bu makale, Python programlama dili kullanılarak geliştirilen, gramer tabanlı bir gerçek zamanlı sözdizimi vurgulayıcının (syntax highlighter) tasarımını, geliştirilme sürecini ve uygulamasını ayrıntılı bir şekilde ele almaktadır. Sistem, sıfırdan yazılmış bir sözcüksel çözümleyici (`lexer.py`), bir sözdizimsel çözümleyici (`parser.py`) ve Tkinter kütüphanesiyle oluşturulmuş bir grafik kullanıcı arayüzü (`highlighter_gui.py`) içermektedir. Belirlenmiş bir gramer yapısını destekleyen bu sistem, anahtar kelimeler, operatörler, semboller, sayılar, tanımlayıcılar, karakter sabitleri ve yorumlar gibi çeşitli token türlerini gerçek zamanlı olarak renklendirir ve sözdizimsel hataları anında tespit eder. Harici vurgulama kütüphanelerine bağımlı olmadan geliştirilen proje, kullanıcı dostu bir arayüzle kod görselleştirme ve hata analizi sunar. `lexer_test.py` ve `parser_test.py` dosyalarıyla yapılan kapsamlı birim testler, sistemin doğruluğunu ve güvenilirliğini doğrulamıştır. Bu makale, sistemin mimarisini, gramer tanımını, modüllerin işleyişini, test süreçlerini, performans optimizasyonlarını, kullanıcı deneyimini ve gelecekteki geliştirme olanaklarını derinlemesine incelemektedir.

## 1. Giriş

Sözdizimi vurgulama, modern programlama ortamlarının vazgeçilmez bir özelliğidir. Kodun okunabilirliğini artırarak geliştiricilere, kod yapısını hızlıca anlamaları ve sözdizimsel hataları kolayca tespit etmeleri için görsel bir rehber sağlar. Bu proje, belirli bir gramer yapısına uygun, gerçek zamanlı bir sözdizimi vurgulayıcı geliştirmeyi hedeflemiştir. Sistem, Python ile tamamen sıfırdan yazılmış üç temel bileşenden oluşur:

- **Sözcüksel Çözümleyici** (`lexer.py`): Giriş kodunu token’lara ayırır.
- **Sözdizimsel Çözümleyici** (`parser.py`): Token akışını Backus-Naur Form (BNF) gramerine göre analiz eder.
- **Grafik Kullanıcı Arayüzü** (`highlighter_gui.py`): Tkinter ile kodun gerçek zamanlı renklendirilmesini sağlar.

Ayrıca, sistemin doğruluğunu test etmek için `lexer_test.py` ve `parser_test.py` dosyalarıyla kapsamlı birim testler uygulanmıştır. Projenin amacı, derleyici tasarımı ilkelerini pratikte uygulayarak, kullanıcı dostu bir arayüzle gerçek zamanlı kod analizi ve görselleştirme sunmaktır. Bu makale, sistemin tasarım felsefesini, teknik detaylarını, test süreçlerini, performans analizini, kullanıcı deneyimini ve potansiyel iyileştirme alanlarını ayrıntılı bir şekilde ele alacaktır.

## 2. Sistem Mimarisi

Sözdizimi vurgulayıcı, modüler bir yapıya sahip olup üç ana bileşenden oluşur:

- **Sözcüksel Çözümleyici (Lexer):** Giriş kodunu karakter karakter tarar ve token’lara ayırır. Her token, belirli bir kategoriye (anahtar kelime, operatör, vb.) atanır.
- **Sözdizimsel Çözümleyici (Parser):** Token akışını BNF gramerine göre analiz eder ve sözdizimsel doğruluğu kontrol eder. Hatalı yapılar için hata mesajları üretir.
- **Grafik Kullanıcı Arayüzü (GUI):** Tkinter ile geliştirilen arayüz, token’ları renk kodlarıyla görselleştirir ve hata mesajlarını gerçek zamanlı olarak kullanıcıya sunar.

Sistem, aşağıdaki token türlerini destekler:

- **Anahtar Kelimeler**: `if`, `else`, `print`, `int`, `char`, `elif`
- **Operatörler**: `+, -, *, /, =, ==, !=, >, <`
- **Semboller**: `(, ), :`
- **Sayılar**: Tam sayı değerler (örn. `5`, `123`)
- **Tanımlayıcılar**: Kullanıcı tanımlı değişken isimleri (`INT_VAR` için `int` değişkenleri, `CHAR_VAR` için `char` değişkenleri)
- **Karakter Sabitleri**: Tek tırnak içindeki karakterler (örn. `'a'`, `'x'`)
- **Yorumlar**: `#` ile başlayan satır içi açıklamalar

Bu modüler yapı, sistemin bakımını kolaylaştırır ve gelecekteki geliştirmeler için esneklik sağlar. Kullanıcı girdisi, anlık olarak işlenir, token’lara ayrılır, gramer kurallarına göre doğrulanır ve GUI’de renklendirilmiş token’larla birlikte hata mesajları gösterilir.

## 3. Sözcüksel Çözümleyici (Lexical Analyzer)

Sözcüksel çözümleyici, `lexer.py` dosyasındaki `tokenize` fonksiyonu ile uygulanmıştır. Bu fonksiyon, giriş kodunu karakter karakter tarayarak token’lara ayırır ve her token’ı uygun bir kategoriyle etiketler. Sözcüksel analiz, durum diyagramı (state diagram) yaklaşımına dayanır ve düzenli ifadeler yerine programlama tabanlı bir yöntem kullanır. Bu yaklaşım, sistemin taşınabilirliğini ve anlaşılırlığını artırır.

### 3.1 Token Sınıflandırma

`classify` fonksiyonu, kelimeleri aşağıdaki kurallara göre sınıflandırır:

- **Anahtar Kelimeler**: `if`, `else`, `print`, `int`, `char`, `elif` için `KEYWORD` etiketi.
- **Sayılar**: Sayısal değerler için `NUMBER` etiketi (örn. `123`).
- **Değişken Tanımlayıcıları**: `int` veya `char` anahtar kelimelerinden sonra gelen tanımlayıcılar için sırasıyla `INT_VAR` veya `CHAR_VAR` etiketi.
- **Genel Tanımlayıcılar**: Daha önce tanımlanmamış değişken isimleri için `ID` etiketi.
- **Karakter Sabitleri**: Tek tırnak içindeki karakterler için `CHAR_LITERAL` etiketi (örn. `'a'`).
- **Yorumlar**: `#` ile başlayan satırlar için `COMMENT` etiketi.

Aşağıdaki kod parçası, `classify` fonksiyonunun temel yapısını gösterir:
```python
def classify(word, prev_keyword=None, typed_ids=None):
    keywords = ["if", "print", "else", "elif", "int", "char"]
    if word in keywords:
        return ("KEYWORD", word)
    elif is_number(word):
        return ("NUMBER", word)
    elif prev_keyword == "int":
        typed_ids[word] = "INT_VAR"
        return ("INT_VAR", word)
    elif prev_keyword == "char":
        typed_ids[word] = "CHAR_VAR"
        return ("CHAR_VAR", word)
    else:
        return (typed_ids.get(word, "ID"), word)
```
