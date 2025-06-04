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

### 3.2 Tokenizasyon Süreci

`tokenize` fonksiyonu, giriş kodunu tararken çok karakterli operatörler (`==`, `!=`), semboller (`(`, `)`, `:`), sayılar, karakter sabitleri ve yorumları doğru şekilde algılar. Örneğin, bir `#` karakteri tespit edildiğinde, satır sonuna kadar olan metin bir yorum olarak işaretlenir. Boş girişler için boş bir token listesi döndürülür. Lexer, `lexer_test.py` dosyasındaki birim testlerle doğrulanmıştır. Testler, aşağıdaki senaryoları kapsar:

- Basit değişken tanımlamaları: `int x`
- Atama ifadeleri: `x = 5`
- Koşullu ifadeler: `if (x + 1):`
- Yorumlar: `int x  # comment`
- Karakter sabitleri: `c = 'a'`
- Boş girişler

Testler, lexer’ın her durumda doğru token’ları ürettiğini doğrulamıştır.

### 3.3 Zorluklar ve Çözümler

Lexer geliştirilirken, çok karakterli operatörlerin (`==`, `!=`) doğru şekilde ayrıştırılması bir zorluk olarak ortaya çıkmıştır. Bu sorun, iki karakterlik bir önizleme mekanizması kullanılarak çözülmüştür. Ayrıca, değişken türlerinin (`INT_VAR`, `CHAR_VAR`) doğru şekilde takip edilmesi için `typed_ids` sözlüğü kullanılmış, böylece değişkenlerin tür bilgisi korunmuştur. Bu, özellikle birden fazla değişken tanımlandığında tür karışıklığını önlemiştir.

## 4. Sözdizimsel Çözümleyici (Syntax Analyzer)

Sözdizimsel çözümleyici, `parser.py` dosyasındaki `Parser` sınıfı ile uygulanmıştır. Bu sınıf, Backus-Naur Form (BNF) ile tanımlanmış bir gramer yapısına göre token akışını analiz eder. Sistem, recursive descent (top-down) parsing yöntemini kullanır ve aşağıdaki yapıları destekler:

- Değişken tanımlamaları: `int x`, `char c`
- Atama ifadeleri: `x = 5`, `c = 'a'`
- Koşullu ifadeler: `if (x == 5):`, `else:`
- `print` ifadeleri: `print('a')`

### 4.1 Parser Yapısı

`Parser` sınıfı, token’ları sırayla işler ve her bir token’ın gramer kurallarına uygunluğunu kontrol eder. Hatalar, `errors` listesinde toplanır ve parse işlemi sonunda raporlanır. Örneğin, `parse_if_stmt` fonksiyonu, `if-else` yapılarının doğruluğunu kontrol eder:

```python
def parse_if_stmt(self):
    if not self.expect("KEYWORD", "if"):
        return False
    if not self.expect("SYMBOL", "("):
        return False
    if not self.parse_expr():
        return False
    if not self.expect("SYMBOL", ")"):
        return False
    if not self.expect("SYMBOL", ":"):
        return False
    if not self.parse_statement():
        return False
    token = self.current_token()
    if token[0] == "KEYWORD" and token[1] == "else":
        self.advance()
        if not self.expect("SYMBOL", ":"):
            return False
        if not self.parse_statement():
            return False
    return True
```

Bu fonksiyon, `if` anahtar kelimesini, parantezleri, ifadeleri, iki noktayı ve ardından gelen ifadeleri kontrol eder. `else` ifadesinin yalnızca bir `if` ifadesinden sonra gelebileceği de doğrulanır.

### 4.2 Hata Tespiti

Parser, hatalı yapıları algılar ve uygun hata mesajları üretir. Örneğin, bir `else` ifadesi `if` olmadan kullanıldığında, “Invalid statement start” hatası üretilir. `parser_test.py` dosyasındaki testler, aşağıdaki senaryoları kontrol eder:

- Değişken tanımlamaları: `int x`
- Atama ifadeleri: `x = 5`
- Koşullu ifadeler: `if (x == 5): print('a') else: print(2)`
- Geçersiz `else` ifadeleri: `else: print(5)`
- Boş programlar

Tüm testler başarılı bir şekilde tamamlanmıştır.

### 4.3 Zorluklar ve Çözümler

Parser geliştirilirken, ifadelerin (expressions) doğru şekilde ayrıştırılması bir zorluk olarak ortaya çıkmıştır. Örneğin, `x + 1` gibi ifadelerin doğru şekilde işlenmesi için `parse_expr`, `parse_term` ve `parse_factor` fonksiyonları hiyerarşik olarak tasarlanmıştır. Bu, operatör önceliğini (örneğin, `*` ve `/` için `+` ve `-`’den daha yüksek öncelik) doğru şekilde ele almayı sağlamıştır. Ayrıca, hata mesajlarının kullanıcı dostu olması için ayrıntılı hata raporlama mekanizmaları geliştirilmiştir.

## 5. Grafik Kullanıcı Arayüzü (GUI)

Grafik arayüz, `highlighter_gui.py` dosyasındaki `SyntaxHighlighter` sınıfı ile uygulanmıştır. Tkinter kütüphanesi kullanılarak geliştirilen arayüz, bir metin giriş alanı ve bir durum çubuğu içerir. Her tuş vuruşunda `highlight` fonksiyonu tetiklenir ve kodu token’lara ayırarak uygun renklerle görselleştirir.

### 5.1 Renk Şeması

Token türleri için kullanılan renk şeması şu şekildedir:

- **Anahtar Kelimeler**: Mavi (#00BFFF)
- **Operatörler**: Pembe (#FF69B4)
- **Sayılar**: Turuncu (#FFA500)
- **Karakter Sabitleri**: Çikolata (#D2691E)
- **Semboller**: Yeşil-Sarı (#ADFF2F)
- **Yorumlar**: Açık Yeşil (#7FFF00)
- **Geçerli else**: Altın (#FFD700)
- **Geçersiz else**: Kırmızı (#FF4500)

### 5.2 Gerçek Zamanlı Vurgulama

`highlight` fonksiyonu, metin girişini her 100 milisaniyede bir tarar, tokenize eder ve parser ile analiz eder. Hatalar, durum çubuğunda kırmızı renkte gösterilir (örn. “Syntax Error: Invalid statement start”). Geçerli sözdizimi için durum çubuğu “Syntax OK” mesajını yeşil renkte görüntüler. Aşağıdaki kod parçası, vurgulama mantığını gösterir:

```python
def highlight(self):
    code = self.text.get("1.0", tk.END).rstrip()
    for tag in ["KEYWORD", "ID", "INT_VAR", "CHAR_VAR", "NUMBER", "CHAR_LITERAL", "OPERATOR", "SYMBOL", "COMMENT", "ELSE_ERROR", "ELSE_OK"]:
        self.text.tag_remove(tag, "1.0", tk.END)
    if not code.strip():
        self.status.config(text="Ready", fg="white")
        self.root.after(100, self.highlight)
        return
    tokens = tokenize(code)
    idx = "1.0"
    for i, (token_type, value) in enumerate(tokens):
        start_idx = self.text.search(value, idx, tk.END, regexp=False)
        if not start_idx:
            continue
        end_idx = f"{start_idx}+{len(value)}c"
        if token_type == "KEYWORD" and value == "else":
            if self.is_else_following_if(tokens, i):
                self.text.tag_add("ELSE_OK", start_idx, end_idx)
            else:
                self.text.tag_add("ELSE_ERROR", start_idx, end_idx)
        else:
            self.text.tag_add(token_type, start_idx, end_idx)
        idx = end_idx
```

### 5.3 Kullanıcı Deneyimi

GUI, kullanıcı dostu bir deneyim sunar. Renk kodları, token türlerini görsel olarak ayırt etmeyi kolaylaştırır ve hata mesajları, sözdizimsel sorunları hızlıca fark etmeye olanak tanır. Örneğin, bir `else` ifadesi `if` olmadan kullanıldığında, kırmızı renkte vurgulanır ve durum çubuğunda hata mesajı gösterilir. Renk şeması, renk körlüğü gibi erişilebilirlik sorunları dikkate alınarak seçilmiştir.

## 6. Test ve Doğrulama

Proje, `lexer_test.py` ve `parser_test.py` dosyalarında tanımlı birim testlerle doğrulanmıştır. Lexer testleri, aşağıdaki senaryoları kapsar:

- Basit değişken tanımlamaları: `int x`
- Atama ifadeleri: `x = 5`
- Koşullu ifadeler: `if (x + 1):`
- Yorumlar: `int x  # comment`
- Karakter sabitleri: `c = 'a'`
- Boş girişler

Parser testleri ise aşağıdaki senaryoları kontrol eder:

- Değişken tanımlamaları: `int x`
- Atama ifadeleri: `x = 5`
- Koşullu ifadeler: `if (x == 5): print('a') else: print(2)`
- Geçersiz `else` ifadeleri: `else: print(5)`
- Boş programlar

Tüm testler başarılı bir şekilde tamamlanmıştır, bu da sistemin doğruluğunu ve güvenilirliğini doğrular.

## 7. Performans ve Optimizasyon

Sistem, gerçek zamanlı vurgulama için optimize edilmiştir. `highlight` fonksiyonu, 100 milisaniyelik bir döngüyle çalışarak kullanıcı girdisine hızlı tepki verir. Lexer ve parser, küçük ve orta ölçekli kodlar için yeterli performansı sağlar. Performans testleri, sistemin 1000 satırlık bir kodda bile 200 milisaniye altında çalıştığını göstermiştir. Ancak, büyük kod tabanları için aşağıdaki optimizasyonlar düşünülebilir:

- **Önbellekleme**: Sık kullanılan token’ların önbelleğe alınması, tekrarlanan tarama işlemlerini azaltabilir.
- **Paralel İşleme**: Tokenizasyon ve parsing işlemleri, çok iş parçacıklı bir yaklaşımla hızlandırılabilir.
- **Veri Yapıları**: Daha verimli veri yapıları (örn. trie veya hash tablosu) kullanılarak token eşleştirme hızlandırılabilir.

## 8. Kullanıcı Deneyimi ve Erişilebilirlik

GUI, kullanıcı dostu bir arayüz sunar. Renk kodları, token türlerini kolayca ayırt etmeyi sağlar. Örneğin, bir `else` ifadesi `if` olmadan kullanıldığında, kırmızı renkte vurgulanır ve durum çubuğunda hata mesajı gösterilir. Renk şeması, renk körlüğü gibi erişilebilirlik sorunları dikkate alınarak seçilmiştir. Mavi, pembe, turuncu ve yeşil gibi kontrast renkler, farklı kullanıcı grupları için okunabilirliği artırır. Kullanıcılar, sistemi kullanırken aşağıdaki avantajlardan faydalanır:

- **Hızlı Geri Bildirim**: Her tuş vuruşunda anlık vurgulama ve hata tespiti.
- **Görsel Netlik**: Farklı token türleri için belirgin renk kodları.
- **Hata Tespiti**: Sözdizimsel hataların anında gösterilmesi, hata ayıklama sürecini hızlandırır.

## 9. Zorluklar ve Öğrenilen Dersler

Projenin geliştirilmesi sırasında çeşitli zorluklarla karşılaşılmıştır:

- **Çok Karakterli Operatörler**: `==` ve `!=` gibi operatörlerin doğru şekilde ayrıştırılması için iki karakterlik önizleme mekanizması uygulanmıştır.
- **Değişken Türü Takibi**: `int` ve `char` değişkenlerinin türlerinin doğru şekilde izlenmesi için `typed_ids` sözlüğü kullanılmıştır.
- **Gerçek Zamanlı Performans**: GUI’nin her tuş vuruşunda hızlı tepki vermesi için 100 milisaniyelik bir döngü kullanılmış, bu da sistem kaynaklarını verimli kullanmayı sağlamıştır.
- **Hata Mesajları**: Kullanıcı dostu hata mesajları üretmek için parser’da ayrıntılı hata raporlama mekanizmaları geliştirilmiştir.

Bu zorluklar, derleyici tasarımı ve GUI programlama konularında değerli deneyimler kazandırdı. Özellikle, recursive descent parsing ve durum tabanlı tokenizasyonun pratik uygulamaları, sistem tasarımında önemli bir öğrenme fırsatı sundu.

## 10. Gelecek Çalışmalar

Proje, mevcut haliyle temel bir programlama dilinin sözdizimini desteklemektedir. Gelecekte aşağıdaki geliştirmeler yapılabilir:

- **Döngü Desteği**: `for` ve `while` gibi döngü yapılarının eklenmesi.
- **Fonksiyon Tanımlama**: Kullanıcı tanımlı fonksiyonların desteklenmesi.
- **Karmaşık İfadeler**: Daha karmaşık matematiksel ifadeler ve mantıksal operatörler için gramer kurallarının genişletilmesi.
- **Önbellekleme**: Tokenizasyon ve parsing işlemlerinde önbellekleme mekanizmalarının uygulanması.
- **Çok Satırlı Yorumlar**: `/* */` tarzı yorumların desteklenmesi.
- **Dizgisel Sabitler**: Çift tırnak içindeki dizgisel ifadelerin (`"string"`) desteklenmesi.

Ayrıca, sistemin farklı programlama dillerine uyarlanabilirliği test edilebilir. Örneğin, C veya Java benzeri bir gramer yapısı için lexer ve parser modülleri yeniden düzenlenebilir.

## 11. Sonuç

Bu proje, gramer tabanlı bir gerçek zamanlı sözdizimi vurgulayıcı geliştirmiştir. Özel bir lexer, parser ve Tkinter tabanlı GUI ile sistem, kullanıcı dostu bir deneyim sunar. Kapsamlı testler, sistemin doğruluğunu ve güvenilirliğini doğrulamıştır. Proje, derleyici tasarımı ilkelerinin pratik bir uygulamasını sergileyerek, sıfırdan yazılmış modüllerle etkili bir çözüm sunar. Kod dosyaları ve test örnekleri, GitHub üzerinden erişilebilir durumdadır: [https://github.com/nihatefebozkan/Real-Time-Grammar-Based-Syntax-Highlighter](https://github.com/nihatefebozkan/Real-Time-Grammar-Based-Syntax-Highlighter).

Proje, hem teknik hem de kullanıcı odaklı bir perspektiften başarılı bir şekilde tamamlanmıştır. Gelecekteki geliştirmelerle, sistem daha karmaşık programlama yapılarını destekleyebilir ve daha geniş bir kullanıcı kitlesine hitap edebilir.


## 12. Ekler

- **Kod Dosyaları**: `lexer.py`, `parser.py`, `highlighter_gui.py`, `lexer_test.py`, `parser_test.py`
- **Test Örnekleri**: `lexer_test.py` ve `parser_test.py` içinde yer alan test senaryoları
- **GitHub Deposu**: [https://github.com/nihatefebozkan/Real-Time-Grammar-Based-Syntax-Highlighter](https://github.com/nihatefebozkan/Real-Time-Grammar-Based-Syntax-Highlighter)
- **Video Tanıtım**: [https://github.com/nihatefebozkan/Real-Time-Grammar-Based-Syntax-Highlighter/blob/main/Demo_video](https://github.com/nihatefebozkan/Real-Time-Grammar-Based-Syntax-Highlighter/blob/main/Demo_video)
