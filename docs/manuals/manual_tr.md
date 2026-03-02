# <img src="https://github.com/syncoding/evdsts/blob/master/docs/images/evdsts.png?raw=true" width="5%"/> evdsts

## KULLANIM KILAVUZU - TR - V.1.R.0

- ## [__EVDS'den API Anahtarı Alma__](#getting-an-api-key-from-edds)
- ## [__Connector Temelleri__](#the-basics-1)
    - ### [__Connector'ı İçe Aktarma ve Bir Örnek Oluşturma__](#importing-connector)
    - ### [__API Anahtarınızı Gelecekteki Kullanım İçin Kaydetme__](#save-the-key)
    - ### [__EVDS Seri Adı Tanımları İçin Veritabanında Arama Yapma__](#searching-into-database)
    - ### [__EVDS'deki Ana Veri Kategorilerini Listeleme__](#listing-main-cat)
    - ### [__Ana Kategorilerdeki Alt Kategorileri Listeleme__](#listing-sub-cat)
    - ### [__Alt Kategorilere Ait Grupları Listeleme__](#listing-groups)
    - ### [__Tekli Zaman Serisi Çekme__](#getting-singular)
    - ### [__Çok Boyutlu Zaman Serisi Çekme__](#getting-multi)
- ## [__Gelişmiş Özellikler__](#the-advanced-1)
    - ### [__Zaman Serisi Endeksleme__](#ts-indexing)
    - ### [__İstenen Zaman Serisi İçin Farklı Frekans Seçme__](#selecting-different-frequency)
    - ### [__İstenen Zaman Serisi İçin Dönüşüm Fonksiyonu Seçme__](#selecting-transformation)
    - ### [__İstenen Zaman Serisi İçin Toplama Fonksiyonu Seçme__](#selecting-aggregation)
    - ### [__Ham Veriyi JSON Formatında Alma__](#retrieving-raw-data)
    - ### [__Çekilen Zaman Serilerine Yeni İsimler Atama__](#assigning-new-names)
        - ### [__Sade Seri İstekleri İçin Yeni İsim Atama__](#assigning-new-names-bare)
        - ### [__Dönüştürülmüş veya Toplanmış Seri İstekleri İçin Yeni İsim Atama__](#assigning-new-names-transagg)
    - ### [__Serileri Diske Yazma__](#writing-series)
    - ### [__Yerel Arama İndeksini Güncelleme__](#updating-index)
- ## [__Referans İsimlerle Zaman Serisi Çekme__](#using-reference-names)
    - ### [__Zaman Serisi Çekerken Referans İsim Kaydetme__](#saving-reference-name)
    - ### [__Referans İsimleri Doğrudan Kaydetme__](#saving-names-directly)
    - ### [__Referans İsimleri Diğer Projelere Aktarma__](#transferring-reference-names)
- ## [__Transformator__](#the-transformator-1)
    - ### [__Transformator ile Seri İsimlerini Yeniden Adlandırma__](#rename-series)
    - ### [__Transformator ile Kayan Noktalı Sayı Hassasiyetini Ayarlama__](#trans-precision)
    - ### [__Fark Alma: D(y<sub>t</sub>, i) = y<sub>t</sub> - y<sub>t-i</sub> = (1-L)<sup>i</sup>y<sub>t</sub>__](#regular-diff)
    - ### [__Doğal Logaritmik Dönüşüm: ln(y<sub>t</sub>)__](#log-transform)
    - ### [__Logaritmik Fark (LogGetiri): D(ln(y<sub>t</sub>), i) = ln(y<sub>t</sub>) - ln(y<sub>t-i</sub>) = (1-L)<sup>i</sup>ln(y<sub>t</sub>)__](#logaritmic-diff)
    - ### [__Deterministik Trend: y<sub>t</sub> = β<sub>0</sub> + β<sub>1</sub>Trend + β<sub>2</sub>Trend<sup>2</sup> + ... β<sub>n</sub>Trend<sup>n</sup> + ε<sub>t</sub>__](#deterministic-trend)
    - ### [__Ayrıştırma: y<sub>t</sub> - (β<sub>0</sub> + β<sub>1</sub>Trend + β<sub>2</sub>Trend<sup>2</sup> + ... β<sub>n</sub>Trend<sup>n</sup> + ε<sub>t</sub>)__](#de-trend)
    - ### [__Basit Hareketli Ortalama: MA<sub>t</sub> = (y<sub>t</sub> + y<sub>t-1</sub> ... y<sub>t-n</sub>) / n__](#smooth-sma)
    - ### [__Üstel Hareketli Ortalama: EMA<sub>t</sub> = αy<sub>t</sub> + (1-α)EMA<sub>t-1</sub>__](#smooth-ema)
    - ### [__Kayan Varyans: ROLVAR<sub>t</sub> = σ<sup>2</sup>(y<sub>t</sub>, y<sub>t-1</sub> ... y<sub>t-n</sub>)__](#detect-rollvar)
    - ### [__Kayan Korelasyon: ROLCORR<sub>t</sub> = ρ(y<sub>t-n</sub>, x<sub>t-n</sub>)__](#detect-rollcorr)
    - ### [__Kümülatif Toplam: Cusum<sub>t</sub> = 𝚺(y<sub>t</sub>, y<sub>t-1</sub> ... y<sub>t-n</sub>)__](#get-cusum)
    - ### [__Z-Skoru: Z<sub>t</sub> = (y<sub>t</sub> - ȳ) / σ<sub>y</sub>__](#get-z-score)
    - ### [__Medyan Mutlak Sapma: MAD<sub>t</sub> = median(|y<sub>t</sub> - median(y<sub>t</sub>)|)__](#get-mad)
    - ### [__Normalize Edilmiş Seriler: y<sub>t, normal</sub> = F(y<sub>t</sub>)__](#get-normalized)
    - ### [__Kukla Değişken Serileri: D<sub>n</sub>__](#get-dummies)
    - ### [__Gecikmeli Seriler: y<sub>t-1</sub>, y<sub>t-2</sub> ... y<sub>t-n</sub>__](#get-laggeds)
    - ### [__Korelasyon Katsayıları: ρ(y<sub>t</sub>, x<sub>t</sub>)__](#get-corr)
    - ### [__Otokorelasyon Katsayıları: AUTOCORR<sub>t</sub> = ρ<sub>t, t-n</sub>__](#get-auto-corr)
    - ### [__Seri Korelasyon Katsayıları: SERIALCORR<sub>t</sub> = ρ<sub>t, x-n</sub>__](#get-serial-corr)
    - ### [__Aykırı Değerler__](#get-outliers)
    - ### [__Düzleştirilmiş Seriler__](#get-smoothed)
## [__Connector ve Transformator Metotlarını Birleştirme__](#joining-methods)
## [__Tanımlı İstisnalar (Exceptions)__](#defined-exceptions-1)


<a id="getting-an-api-key-from-edds"></a>

### __EVDS'den API Anahtarı Alma__

EVDS'ye bağlanmak için gereken API anahtarını edinmek üzere aşağıdaki adımları izleyin:


1. EVDS web sitesini açın. [__EVDS__](https://evds2.tcmb.gov.tr/index.php?/evds/login)
2. Sağ üst çubuktan __`TR`__'ye tıklayarak dili değiştirebilirsiniz.
3. Mevcut sayfadaki __`KAYIT OL`__ düğmesine tıklayın.
4. İstenen bilgileri doldurarak kaydolun.
5. EVDS üyeliği için kullandığınız e-posta adresine gelen kutusundan gelen e-postayı kontrol edin ve e-posta adresinizi doğrulayın.
6. Aynı sayfayı açarak hesabınıza giriş yapın.
7. Kullanıcı adınıza tıklayın ve açılan menüden __`Profil`__'e tıklayın.
8. Yeni açılan sayfada __`API Anahtarı`__'na tıklayarak anahtarınızı alabilirsiniz.


<a id="the-basics-1"></a>

## __Connector Temelleri__

`evdsts` iki önemli sınıftan oluşur:
1. __`Connector`__: EVDS'ye bağlanma ve zaman serisi çekmekten sorumludur.
2. __`Transformator`__: Çekilen veriler üzerinde faydalı dönüşümler ve diğer manipülasyonları yapmaktan sorumludur.

Burada `evdsts` ile temel veri çekme ve ilgili işlemleri ele alacağız, dolayısıyla `Connector` sınıfını inceleyeceğiz.


<a id="importing-connector"></a>

### [__Connector'ı İçe Aktarma ve Bir Örnek Oluşturma__](#connector-instance)
### [__API Anahtarınızı Gelecekteki Kullanım İçin Kaydetme__](#save-the-key)
### [__EVDS Seri Adı Tanımları İçin Veritabanında Arama Yapma__](#searching-into-database)
### [__EVDS'deki Ana Veri Kategorilerini Listeleme__](#listing-main-cat)
### [__Ana Kategorilerdeki Alt Kategorileri Listeleme__](#listing-sub-cat)
### [__Alt Kategorilere Ait Grupları Listeleme__](#listing-groups)
### [__Tekli Zaman Serisi Çekme__](#getting-singular)
### [__Çok Boyutlu Zaman Serisi Çekme__](#getting-multi)


<a id="connector-instance"></a>

### __Connector'ı İçe Aktarma ve Bir Örnek Oluşturma__

EVDS'den zaman serisi çekmek için `evdsts`'den __`Connector`__ sınıfını projenize aktarmanız gerekmektedir.

```python
from evdsts import Connector
```
ardından API anahtarınızı kullanarak aşağıdaki gibi bir `Connector` örneği oluşturabilirsiniz:

```python
connector = Connector('API_ANAHTARINIZ', language='TR')  # Varsayılan dil TR'dir
```
`Connector` sınıfını oluştururken çeşitli ek parametreler kullanılabilir. Sınıfın tam başlatma seçenekleri aşağıda verilmiştir:

```python
def __init__(
                key: Optional[str] = None,
                language: str = "TR",
                show_links: bool = False,
                proxy_servers: Optional[Dict[str, str]] = None,
                verify_certificates: bool = True,
                jupyter_mode: bool = False,
                precision: Optional[int] = None
) -> None:

```

1. `key`: __EVDS__ tarafından sağlanan API anahtarı
2. `language`: Arayüz dili (mevcutsa).
    - Desteklenen diller:
        - Türkçe: `TUR`, `tur`, `TR`, `tr`
        - İngilizce: `ENG`, `eng`, `EN`, `en`
    Varsayılan: `TR`
3. `show_links`: Bağlanılacak URL'yi gösterir. Varsayılan: `False`
4. `proxy_servers`: Proxy sunucusu arkasından bağlanmak isteyen kullanıcılar için.
Proxy sunucuları `dict` tipinde verilmelidir:
`{"http": "127.0.0.1", "https": "127.0.0.1"}`
Varsayılan: `None`
5. `verify_certificates`: Bağlantı sırasında sunucunun SSL güvenlik sertifikasının doğrulanmasını Etkinleştirme/Devre Dışı Bırakma. Varsayılan: `True`
6. `jupyter_mode`: Ekranda daha iyi gösterim için `Jupyter Notebook` modunu Etkinleştirir/Devre Dışı Bırakır.
    - `True`:
        - ekran kayan nokta hassasiyeti: __2__
        (bu yalnızca ekran gösteriminin hassasiyetini etkiler. Dahili işlem hassasiyeti ya EVDS servisinden geldiği gibidir ya da `precision` parametresi ile sabit hassasiyet verilmişse kullanıcının belirlediği hassasiyete eşittir.)
        - Ekranda gösterilecek maksimum pandas `DataFrame` nesne sütunu: __6__
    - `False`: Ekran gösterim optimizasyonu yapılmaz.
    Varsayılan: `None`
7. `precision`: Kayan noktalı sayıların işlem hassasiyeti.
    - tam sayı değeri: kayan nokta hassasiyetleri verilen değere ayarlanır. Örneğin:
    `1907.72231162012281817`, hassasiyet `2` verildiğinde `1907.72`'ye kesilir veya `72.1907`,
    hassasiyet `0` verildiğinde `72`'ye kesilir.
    - None: hassasiyet, EVDS'den dönen orijinal hassasiyete ayarlanır.
    Varsayılan: `None`

__Örnekler__:

```python
# basit başlatma
connector = Connector('API_ANAHTARINIZ', language='TR')

# bağlantı URL'sini gösterir
connector = Connector('API_ANAHTARINIZ', language='TR', show_links=True)

# proxy arkasından bağlantı
proxies = {"http": "127.0.0.1", "https": "127.0.0.1"}
connector = Connector('API_ANAHTARINIZ', language='TR', proxy_server=proxies)

# sunucu SSL sertifika doğrulamasını devre dışı bırakır
connector = Connector('API_ANAHTARINIZ', language='TR', verify_certificates=False)

# Jupyter'da daha iyi ekran gösterimi için Jupyter Notebook modu
connector = Connector('API_ANAHTARINIZ', language='TR', jupyter_mode=True)

# tüm çekilen seriler için hassasiyeti 2 olarak ayarlar
connector = Connector('API_ANAHTARINIZ', language='TR', precision=2)
```


<a id="save-the-key"></a>

### __API Anahtarınızı Gelecekteki Kullanım İçin Kaydetme__

Uygulamanızı her başlattığınızda API Anahtarınızı kullanmanıza gerek yoktur. API anahtarınızı diske kaydederek gelecekteki `Connector` başlatmalarında kullanmak zorunda kalmazsınız. Anahtarınızı diske kaydetmek için `save_key()` metodunu kullanabilirsiniz.

```python
connector = Connector('API_ANAHTARINIZ', language='TR')
connector.save_key()  # artık mevcut projeniz için API anahtarınızı kullanmanıza gerek yok.
```

anahtarınızı diske kaydettikten sonra API anahtarı kullanmadan bir `Connector` örneği oluşturabilirsiniz.

```python
connector = Connector(language='TR')  # anahtarınız diskten okunur.
```


<a id="searching-into-database"></a>

### __EVDS Seri Adı Tanımları İçin Veritabanında Arama Yapma__

Çekmek istediğiniz serinin EVDS'deki adı tanımını bulmak için EVDS web sitesini ziyaret etmenize gerek yoktur. `where()` metodu sayesinde `evdsts`'den ayrılmadan anahtar kelimelerle seri adlarını arayabilirsiniz.

`where()` metodunun imzası:

```python
def where(keyword: str, n: int = 100, verbose: bool = True) -> Dict[str, str]
```

1. `keyword`: aranacak kelimeler (örneğin: tüketici fiyat endeksi)
2. `verbose`: `True` ise sonuçları ekranda gösterir. Varsayılan: `True`.
3. `n`: Döndürülecek maksimum ilgili sonuç sayısı. Varsayılan: `100`.


__Örnekler (TR)__:

```python
connector = Connector()                   # API Anahtarınızı daha önce kaydettiğinizi varsayarak.
connector.where("tüketici fiyat endeksi") # arama yaklaşık 0.5 saniye sürer.
```

Yukarıdaki arama şu çıktıyı verir:

```
5 most relevant results for 'tüketici fiyat endeksi' are shown below.

                                                 Search Results                                                 
----------------------------------------------------------------------------------------------------------------
Series Code          Series Name                                                     Frequency        Start Date 
----------------------------------------------------------------------------------------------------------------
TP.FE.OKTG01         Tüketici Fiyat Endeksi (Genel)                                  AYLIK            01-01-2003 
TP.MK.F.BILESIK.TUM  (FİYAT) BİST Tüm-100 Endeksi (XTUMY), Kapanış Fiyatlarına Göre  İŞ GÜNÜ          02-01-2009 
TP.MK.F.HIZMET       (FİYAT) BİST Hizmet Endeksi (XUHIZ), Kapanış Fiyatlarına Göre ( İŞ GÜNÜ          02-01-1997 
TP.MK.F.TEKNOLOJI    (FİYAT) BİST Teknoloji Endeksi (XUTEK), Kapanış Fiyatlarına Gör İŞ GÜNÜ          30-06-2000 
TP.TUFE1YI.T1        1.Yurt İçi Üretici Fiyat Endeksi                                AYLIK            01-01-1982 
----------------------------------------------------------------------------------------------------------------
```

Bu çıktı, sonuçlar üzerinde herhangi bir kesim yapılmadan `Dict` olarak döndürülür ve bir değişkene atanabilir.

```python
# tüm arama sonuçları herhangi bir kesim yapılmadan 'tum_sonuclar' değişkenine atanır.
# Dict[Seri Kodu, List[Seri Adı, Seri Frekansı, Seri Başlangıç Tarihi]] şeklinde bir sözlüktür.
tum_sonuclar = connector.where("tüketici fiyat endeksi")
```

__Örnekler (EN)__:

```python
connector = Connector(language="EN")    # API Anahtarınızı daha önce kaydettiğinizi varsayarak.
connector.where("consumer price index") # arama yaklaşık 0.5 saniye sürer.
```

Yukarıdaki arama şu çıktıyı verir:

```
5 most relevant results for 'consumer price index' are shown below.

                                                 Search Results                                                 
----------------------------------------------------------------------------------------------------------------
Series Code          Series Name                                                     Frequency        Start Date 
----------------------------------------------------------------------------------------------------------------
TP.FE.OKTG01         Consumer Price Index                                            MONTHLY          01-01-2003 
TP.MK.F.BILESIK      (PRICE INDICES) BIST-100 (XU100), According to Closing Price (J BUSINESS DAILY   01-02-1986 
TP.MK.F.BILESIK.TUM  (PRICE INDICES) BIST All Shares-100 Index (XTUMY), According to BUSINESS DAILY   02-01-2009 
TP.FG.T63            Istanbul Wholesale Price Index (1963=100)(ICC)                  MONTHLY          01-01-1963 
TP.FG.T68            Istanbul Wholesale Price Index (1968=100)(ICC)                  MONTHLY          01-01-1968 
----------------------------------------------------------------------------------------------------------------
```

> Seri adlarını ararken varsayılan olarak en yakın __5__ sonuç gösterilir, ancak `n` en yakın sonucu görmek
> için `n` parametresini ayarlayabilirsiniz. Örneğin; `connector.where("tüketici fiyat endeksi", 10)`
> _tüketici fiyat endeksi_ ifadesi için en yakın 10 sonucu gösterir.

> `where()` metodu ayrıca yapılan aramanın tüm sonuçlarını herhangi bir kesim olmadan içeren bir
> `dict` nesnesi döndürür.

```python
# tüm arama sonuçları herhangi bir kesim yapılmadan 'tum_sonuclar' değişkenine atanır.
# Dict[Seri Kodu, List[Seri Adı, Seri Frekansı, Seri Başlangıç Tarihi]] şeklinde bir sözlüktür.
tum_sonuclar = connector.where("consumer price index")
```

<a id="listing-main-cat"></a>

### __EVDS'deki Ana Veri Kategorilerini Listeleme__

EVDS veritabanında saklanan tüm verilerin ana veri kategorilerini almak için `get_main_categories()` metodunu kullanabilirsiniz. Dönen tür varsayılan olarak pandas `DataFrame`'dir, ancak isterseniz ana kategorileri `dict` veya `json` formatında da alabilirsiniz.

`get_main_categories` metodunun imzası:

```python
def get_main_categories(
                        as_dict: bool = False,
                        raw: bool = False,
) -> Union[pd.DataFrame, JSONType, Dict]:
```

1. `as_dict`: Ana kategorileri {CATEGORY_ID: kategori_adı} şeklinde sözlük olarak döndürür.
Varsayılan: False.
2. `raw`: İşlenmiş türler yerine EVDS Servisinden alınan ham `JSON` nesnesini döndürür.
Varsayılan: `False`

__Örnekler__:

```python
ana_kategoriler = connector.get_main_categories()
print(ana_kategoriler)

# bu size aşağıdaki tabloyu temsil eden bir pandas DataFrame nesnesi verir.
```

|Index| KATEGORİ ID|                       BAŞLIK                                                    |
|:---: |:---:       |-----------------------------------------------------------------------------|
|0	   |     10	    | BEKLENTİ VE EĞİLİM ANKETLERİ                                               |
|1	   |     1001   | BANKA KREDİLERİ EĞİLİM ANKETİ (TCMB)                                       |
|2	   |     1002   | FİNANSAL HİZMETLER ANKETİ (TCMB)                                           |
|...   |     ...    | ...                                                                         |
|11    |     15	    | BÜYÜME, İSTİHDAM, KAMU MALİYESİ                                            |
|...   |     ...    | ...                                                                         |
|16    |     25	    | DÖVİZ KURLARI VE KIYMETLİ MADENLER                                         |
|17    |     2502   | ALTIN İSTATİSTİKLERİ                                                        |
|18    |     2503   | DİĞER EMTİA VERİLERİ                                                       |
|19    |     2504   | REEL EFEKTİF DÖVİZ KURLARI (TCMB)                                          |
|20    |     2501   | TCMB DÖVİZ KURLARI                                                         |
|21    |     20	    | FİYAT ENDEKSLERİ                                                           |
|...   |     ...    | ...                                                                         |
|26    |     30	    | MERKEZ BANKASI BİLANÇO VE PİYASA VERİLERİ                                  |
|...   |     ...    | ...                                                                         |
|29    |     35	    | ÖDEME SİSTEMLERİ VE EMİSYON                                                |
|...   |     ...    | ...                                                                         |
|33    |     40	    | ÖDEMELER DENGESİ VE DIŞ İSTATİSTİKLER                                      |
|...   |     ...    | ...                                                                         |
|49    |     45	    | PARASAL VE FİNANSAL İSTATİSTİKLER                                          |
|...   |     ...    | ...                                                                         |
|76    |     50	    | REEL SEKTÖR İSTATİSTİKLERİ                                                  |
|...   |     ...    | ...                                                                         |
|91    |     55	    | ULUSLARARASI İSTATİSTİKLER                                                  |
|...   |     ...    | ...                                                                         |
|95    |     0	    | ARŞİV                                                                       |
|...   |     ...    | ...                                                                         |

> Not: API artık hiyerarşik bir kategori yapısı döndürmektedir. Yukarıdaki tablo kısaltılmıştır.
> Tam liste için `get_main_categories()` metodunu kullanarak tüm kategorileri ve alt kategorileri görüntüleyebilirsiniz.


Ana kategoriler ayrıca işlenmiş Python sözlükleri veya JSON dizileri olarak da istenebilir. Çekilen veriyi `Dict` türünde almak için `as_dict` bayrağını `True` olarak ayarlayabilir veya benzer şekilde ana kategorileri JSON dizisi olarak almak için `raw` bayrağını kullanabilirsiniz.

```python
# sözlük
ana_sozluk = connector.get_main_categories(as_dict=True)

# JSON dizisi
ana_ham = connector.get_main_categories(raw=True)
```


<a id="listing-sub-cat"></a>

### __Ana Kategorilerdeki Alt Kategorileri Listeleme__

`get_sub_categories()` metoduna ana kategori ID'leri veya ana kategori adları verilerek alt kategoriler listelenebilir. Alt kategoriler varsayılan ayarında pandas `DataFrame` olarak döner, ancak isterseniz `dict` veya `json` formatında da alabilirsiniz.

`get_sub_categories()` metodunun imzası:

```python
def get_sub_categories(
                        main_category: Union[int, str],
                        as_dict: bool = False,
                        raw: bool = False,
                        verbose: bool = False,
) -> Union[pd.DataFrame, JSONType, Dict]:
```

1. `main_category`: Ana kategori ID'si veya gerçek ana kategori adı olabilir.
        - tam sayı: verilen değerin ana kategori ID'sine karşılık gelen alt kategorileri döndürür.
        - metin: verilen ana kategori adına ait alt kategorileri döndürür.
2. `as_dict`: {veri_grubu_kodu: veri_grubu_adı} şeklinde sözlük döndürür.
Varsayılan: `False`
3. `raw`: İşlenmiş türler yerine EVDS Servisinden alınan ham JSON nesnesini döndürür.
Varsayılan: `False`
4. `verbose`: Çekilen verinin detaylı versiyonu. Varsayılan: `False`.

__Örnekler__:

```python
# (2501 = TCMB DÖVİZ KURLARI) ana kategoriler tablosundaki Kategori ID bölümüne göre.
doviz_kurlari_alt = connector.get_sub_categories(2501)

```

Bu size aşağıdaki tabloyu temsil eden bir `DataFrame` verir:

|DATAGROUP_CODE  | CATEGORY_ID  |...    |START_DATE	|END_DATE   |
|----------------|--------------|-------|-----------|-----------|
|	bie_dkkurbil  |	    2501    |...	|2013-03-01	|2025-10-31 |
|	bie_dkefkytl  |	    2501    |...	|1990-01-02	|2010-12-30 |
|	bie_dkdovytl  |	    2501    |...	|1959-09-01	|2025-12-31 |

> Not: Yukarıdaki tablo daha fazla sütun içermektedir ancak ekrana sığması için kısaltılmıştır.

veya alternatif olarak aynı alt kategori verilerini almak için ana kategori adlarını kullanabilirsiniz.

```python
doviz_kurlari_alt = connector.get_sub_categories("TCMB DÖVİZ KURLARI")

```
> __İşlemin büyük/küçük harfe duyarlı olduğunu, bu nedenle kategori adlarının ana kategorilerde__
> __göründüğü şekliyle tam olarak kullanılması gerektiğini lütfen unutmayın.__

Alt kategoriler `dictionary` nesneleri, ham `JSON` veya `DataFrame` tablosunun detaylı versiyonu olarak döndürülebilir.

```python
# sözlük olarak
alt_sozluk = connector.get_sub_categories("REEL SEKTÖR İSTATİSTİKLERİ", as_dict=True)

# ham JSON olarak
alt_ham = connector.get_sub_categories("REEL SEKTÖR İSTATİSTİKLERİ", raw=True)

# DataFrame'in daha detaylı versiyonu
alt_detayli = connector.get_sub_categories("REEL SEKTÖR İSTATİSTİKLERİ", verbose=True)

# yukarıdakilerin birleşik versiyonu
kurlar_tumu = connector.get_sub_categories("TCMB DÖVİZ KURLARI", as_dict=True, verbose=True)
```


<a id="listing-groups"></a>

### __Alt Kategorilere Ait Grupları Listeleme__

Alt kategorilere ait gruplar, ilgili alt kategori adı `get_groups()` metoduna parametre olarak verilerek çağrılabilir. Gruplar varsayılan ayarında pandas `DataFrame` olarak döner, ancak isterseniz `dict` veya `json` formatında da alabilirsiniz.

`get_groups()` metodunun imzası:

```python
def get_groups(
                data_group_code: str,
                as_dict: bool = False,
                raw: bool = False,
                verbose: bool = False,
                parse_dt: bool = False
) -> Union[pd.DataFrame, JSONType, Dict]:
```

1. `data_group_code`: Verinin istendiği alt kategorinin kodu.
2. `as_dict`: {seri_kodu: seri_adı} şeklinde sözlük döndürür.
Varsayılan: `False`
3. `raw`: İşlenmiş türler yerine EVDS Servisinden alınan ham JSON nesnesini döndürür.
Varsayılan: `False`
4. `verbose`: Grup verisinin çok detaylı versiyonu.
Varsayılan: False.
5. `parse_dt`: Tarih-saat alanlarının gösterim seçeneği.
    - `True`: döndürülen sözlükteki tarih alanları Python date nesnesine dönüştürülür.
    - `False`: döndürülen sözlükteki tarih alanları olduğu gibi (metin) döndürülür.
Varsayılan: `False`

__Örnekler__:

```python
grup_efektifler = connector.get_groups("bie_dkdovytl")
```

|SERIE_NAME                         |SERIE_CODE	    |FREQUENCY_STR    |START_DATE   |END_DATE  |
|-----------------------------------|---------------|-----------------|-------------|----------|
|(USD) ABD Doları (Döviz Alış)	    |TP.DK.USD.A.YTL|	GÜNLÜK	      |1950-01-02	|2026-03-02|
|(USD) ABD Doları (Döviz Satış)	    |TP.DK.USD.S.YTL|	GÜNLÜK	      |1950-01-02	|2026-03-02|
|(EUR) Euro (Döviz Alış)	        |TP.DK.EUR.A.YTL|	GÜNLÜK	      |1999-01-04	|2026-03-02|
|(EUR) Euro (Döviz Satış)	        |TP.DK.EUR.S.YTL|	GÜNLÜK	      |1999-01-04	|2026-03-02|

> Not: Yukarıdaki tablo daha fazla satır içermektedir ancak ekrana sığması için kısaltılmıştır.

Gruplar `dict` türü nesneler veya `JSON` türü ham veri olarak da istenebilir. Ayrıca `verbose` bayrağı ile gruplara ait daha detaylı veri alınabilir.

```python
# sözlük olarak
gruplar_sozluk = connector.get_groups("bie_dkdovytl", as_dict=True)

# JSON olarak
gruplar_ham = connector.get_groups("bie_dkdovytl", raw=True)

# verbose bayrağı ile daha detaylı grup verisi istenebilir.
detayli_gruplar = connector.get_groups("bie_dkdovytl", verbose=True)

# hem verbose hem de as_dict bayrakları birlikte verilerek detaylı sözlük istenebilir.
detayli_sozluk = connector.get_groups("bie_dkdovytl", as_dict=True, verbose=True)
```


<a id="getting-singular"></a>

### __Tekli Zaman Serisi Çekme__

Tekli zaman serisi verisi çekmek `get_series()` metodu ile yapılır:

> `evdsts`, döndürülen tüm verilerin matematiksel işlemler için anında kullanılabilmesini sağlar. Bu, çekilen veriye kullanıcıya döndürülmeden önce bir dizi dönüşüm uygulanarak garanti altına alınır. Başka bir deyişle, `evdsts` asla gerçekte kayan noktalı sayı veya tam sayıyı temsil eden `string` (veya pandas'ın terimiyle `object`) türü veri döndürmez. Tüm `kayan` veriler döndürülmeden önce `float32` türüne dönüştürülür. Gerçek sayıları temsil etmeyen `string`'ler ise matematiksel bütünlüğü bozmayan `NaN`'lara dönüştürülür. Bu yaklaşım pratikte büyük avantaj sağlar çünkü `evdsts`'den dönen tüm seriler herhangi bir ek işleme gerek kalmadan matematiksel işlemler için anında kullanılabilir.

`get_series()` metodunun imzası:

```python
def get_series(
                series: Union[str, Sequence[str]],
                start_date: Optional[Union[str, datetime]] = None,
                end_date: Optional[Union[str, datetime, pd.Timestamp]] = None,
                period: Optional[str] = None,
                aggregations: Optional[Union[str, List[str], Tuple[str]]] = None,
                transformations: Optional[Union[str, List[str], Tuple[str]]] = None,
                keep_originals: bool = True,
                frequency: Optional[Union[str, int]] = None,
                new_names: Optional[Sequence[str]] = None,
                keep_references: bool = False,
                time_series: bool = True,
                ascending: bool = True,
                raw: bool = False,
                as_dict: bool = False,
                convert_to_bd: bool = True
) -> Union[pd.DataFrame, JSONType, Dict]:
```

1. `series`: EVDS API sunucusundan istenen zaman serisi adları.
    - Seri adları orijinal EVDS servis adları veya daha önce referans adı olarak kaydedilmiş isimlerle verilebilir.
        - adlar birkaç şekilde verilebilir:
            - Virgülle ayrılmış metin: "usdtry, eurtry"
            - Boşlukla ayrılmış metin: "usdtry eurtry"
            - Liste veya Tuple gibi bir Sequence türü içinde: ["usdtry", "eurtry"] veya ("usdtry", "eurtry")
2. `start_date`: Zaman serisi verilerinin başlangıç tarihi. Varsayılan: `None`
    - `None` veya belirtilmemiş: `start_date` güncel tarihe ayarlanır.
    - `dd-mm-YYYY`, `dd.mm.YYYY`, `dd/mm/YYYY` formatında metin olarak verilebilir.
    - Python `datetime` nesnesi olarak verilebilir.
    - Pandas `TimeStamp` nesnesi olarak verilebilir.
3. `end_date`: İstenen zaman serisi için son gözlem tarihi. Varsayılan: `None`
    - `None` veya belirtilmemiş: `end_date` güncel tarihe ayarlanır.
    - `dd-mm-YYYY`, `dd.mm.YYYY`, `dd/mm/YYYY` formatında metin olarak verilebilir.
    - Python `datetime` nesnesi olarak verilebilir.
    - Pandas `TimeStamp` nesnesi olarak verilebilir.
4. `period`: Güncel tarihten itibaren bir dönemi temsil eden dönem metni. Varsayılan: `None`.
    - dönem metinleri bir sayı ve bir tarih tanımlayıcı kısımdan oluşur. Sayı kısmı herhangi bir tam sayı, tarih kısmı ise gün, hafta, ay ve yılı yansıtan bir harftir. Harfler Türkçe ve İngilizce dönem tanımlayıcılarının ilk harfleridir. `period`, `start_date` veya `end_date` ile birlikte kullanılamaz.
    - `1d` veya `1g` -> şu dönemi temsil eder: 1 gün öncesinden bugüne, örnekler: `2d`, `7d`, `30d`
    - `1w` veya `1h` -> şu dönemi temsil eder: 1 hafta öncesinden bugüne, örnekler: `2w`, `7w`, `30w`
    - `1m` veya `1a` -> şu dönemi temsil eder: 1 ay öncesinden bugüne, örnekler: `2m`, `7m`, `12m`
    - `1y` -> şu dönemi temsil eder: 1 yıl öncesinden bugüne, örnekler: `2y`, `7y`, `30y`
5. `aggregations`: Zaman serilerine döndürülmeden önce uygulanacak toplama fonksiyonları. Varsayılan: `None`
    - `None` veya belirtilmemiş: Zaman serilerine toplama fonksiyonu uygulanmaz.
    - `string` olarak verildiğinde: Aynı toplama fonksiyonu tüm serilere uygulanır.
    - `List` veya `Tuple` olarak verildiğinde: Farklı toplama fonksiyonları serilere sırasıyla uygulanır.
        - Mevcut toplama fonksiyonları:
            - Ortalama: `avg`
            - Minimum: `min`
            - Maksimum: `max`
            - İlk: `first`
            - Son: `last`
            - Kümülatif Toplam: `sum`
6. `transformations`: Zaman serilerine döndürülmeden önce uygulanacak dönüşüm fonksiyonları. Varsayılan: `None`
    - `None` veya belirtilmemiş: Zaman serilerine dönüşüm uygulanmaz.
    - `string` olarak verildiğinde: Aynı dönüşüm tüm serilere uygulanır.
    - `List` veya `Tuple` olarak verildiğinde: Farklı dönüşümler serilere sırasıyla uygulanır.
        - Mevcut dönüşüm fonksiyonları:
            - Düzey: `level`
            - Yüzde Değişim: `percent`
            - Fark: `diff`
            - Yıllık Yüzde Değişim: `ypercent`
            - Yıllık Fark: `ydiff`
            - Yılbaşından İtibaren Yüzde Değişim: `ytdpercent`
            - Yılbaşından İtibaren Fark: `ytddiff`
            - Hareketli Ortalama: `mov`
            - Hareketli Toplam: `movsum`
7. `keep_originals` (bool, opsiyonel): Bir toplama veya dönüşüm fonksiyonu uygulandığında orijinal serilerin durumunu belirler. Varsayılan: `True`
    - `True`: Dönüşüm fonksiyonu uygulandığında orijinal serileri koru.
    - `False`: Dönüşüm fonksiyonu uygulandığında orijinal serileri çıkar.
8. `frequency`: İstenen zaman serisinin frekansı. Varsayılan: `None` (olduğu gibi)
    - Mevcut frekanslar:
        - Günlük: `daily` veya `D`
        - İş Günü: `bdaily` veya `B`
        - Haftalık: `weekly` veya `W`
        - Yarı Aylık: `semimonthly` veya `SM`
        - Aylık: `monthly` veya `M`
        - Üç Aylık: `quarterly` veya `Q`
        - Altı Aylık: `semiyearly` veya `6M`
        - Yıllık: `yearly` veya `Y`
9. `new_names`: Oluşturulan `DataFrame` sütun adlarını verilenlerle değiştirir. Varsayılan: `None`
10. `keep_references`: Verilen yeni sütun adlarını (verilmişse) EVDS API servisindeki gerçek seri adlarına referans olarak kaydeder. Referans adlar, bir dönüşüm veya toplama fonksiyonu uygulandığında kaydedilemez. Varsayılan: `False`.
11. `time_series`: Metin tarihlerini döndürülen zaman serisinin frekansına karşılık gelen DateRange'lere dönüştürmeye çalışır. Bu özellikle zaman serisi analizi için faydalıdır (ve çoğunlukla gereklidir) çünkü metin tarihler sıralanabilir, indekslenebilir, dilimlendirilebilir, farkı alınabilir gerçek tarihlere dönüştürülür. Varsayılan: `True`
12. `ascending`: İndeksin sıralama yönü.
    - `True`: En eski veri önce.
    - `False`: En yeni veri önce. Varsayılan: `True`
13. `raw`: Çekilen `JSON` verisini dokunulmamış olarak döndürür. Varsayılan: `False`
14. `as_dict`: Çekilen veriyi sözlük türünde döndürür. Varsayılan: `False`
15. `convert_to_bd`: start_date ve end_date'i kontrol eder ve herhangi biri hafta sonuna denk gelirse en yakın iş gününü döndürür. Varsayılan: `True`.


__Örnekler__:

```python
usdtry = connector.get_series("TP.DK.USD.A.YTL")
```
Bir seri adı herhangi bir parametre verilmeden `get_series()` metoduna sağlandığında sonuç, verinin en güncel değeridir. Dönen tür, aksi istenmediği sürece varsayılan olarak pandas `DataFrame` nesnesidir. İstenen seriler için başlangıç ve bitiş tarihleri `get_series()` metodunun `start_date` ve `end_date` parametreleri aracılığıyla verilir. Herhangi biri sağlanmadığında tarih güncel tarihe eşitlenir. Sadece başlangıç tarihi verildiğinde istenen zaman serisi verileri verilen başlangıç tarihinden güncel tarihe kadar çekilir.

`start_date` (ve ileride bahsedilen `end_date`) aşağıdaki formatlarda verilebilir.

1. `g.a.y` -> 01.07.2022 veya 1.7.2022
2. `g-a-y` -> 01-07-2022 veya 1-7-2022
3. `g/a/y` -> 01/07/2022 veya 1/7/2022
4. Python'un `datetime` türü -> datetime(2022, 7, 1)
5. pandas'ın `Timestamp` türü -> pd.Timestamp(2002, 7, 1)

```python
# aşağıdaki tüm örneklerde 'end_date' verilmediği için güncel tarihe eşitlenir.

# metin tarihler
usdtry = connector.get_series("TP.DK.USD.A.YTL", start_date="1.7.2022")  # OK
usdtry = connector.get_series("TP.DK.USD.A.YTL", start_date="1-7-2022")  # OK
usdtry = connector.get_series("TP.DK.USD.A.YTL", start_date="1/7/2022")  # OK

# datetime sınıfları
from datetime import datetime
from pandas import Timestamp

# datetime örnekleri
d_tarih = datetime(2022, 7, 1)
p_tarih = Timestamp(2022, 7, 1)

usdtry = connector.get_series("TP.DK.USD.A.YTL", start_date=d_tarih)  # OK
usdtry = connector.get_series("TP.DK.USD.A.YTL", start_date=p_tarih)  # OK
```

`end_date`, istenen zaman serisinin son verisinin hangi tarihte biteceğini belirlemek için aynı tür tarih girişlerini kabul eder. Hiçbir şey verilmediğinde `end_date` güncel tarihe eşitlenir.

```python
# end_date parametresi sağlanmadığı için otomatik olarak güncel tarihe atanır.
usdtry = connector.get_series("TP.DK.USD.A.YTL", start_date="1.7.2022")

# 2022 Haziran dönemine ait günlük USDTRY serisi.
usdtry = connector.get_series("TP.DK.USD.A.YTL", start_date="01.06.2022", end_date="30.06.2022")
```

Alternatif olarak, güncel tarihten itibaren bir zaman dilimini belirtmek için `get_series()` metodunun `period` parametresini kullanabilirsiniz. `period`, çekmek istediğiniz dönemi tanımlamak için bir dönem metni alır.

Dönem metni iki kısımdan oluşur; birincisi bir tam sayı, ikincisi ise gün, hafta, ay ve yıl gibi bir tarih dönemidir.

|dönem tanımlayıcı  | örnek parametre   | anlamı                                |
|-------------------|-------------------|---------------------------------------|
| `d` veya `g`      |    `27d` veya `27g`| bugünden 27 gün öncesi - bugün       |
| `w` veya `h`      |   `19w` veya `19h` | bugünden 19 hafta öncesi - bugün     |
| `m` veya `a`      |   `2m` veya `2a`   | bugünden 2 ay öncesi - bugün         |
| `y`               |   `27y`            | bugünden 27 yıl öncesi - bugün       |

> `start_date` veya `end_date`, `period` ile birlikte kullanılamaz çünkü belirsiz bir istek oluşturur.
> Bu parametreleri birlikte kullanmaya çalışırsanız bir istisna fırlatılır.


<a id="getting-multi"></a>

### __Çok Boyutlu Zaman Serisi Çekme__

Çok boyutlu veri çekmek aşağıdaki yollardan biri ile yapılabilir:

1. seriler `get_series()` metoduna `List` veya `Tuple` gibi bir sequence türü içinde metin olarak verilebilir.
2. seriler `get_series()` metoduna virgülle ayrılmış `string`'ler olarak verilebilir.
3. seriler `get_series()` metoduna boşlukla ayrılmış `string`'ler olarak verilebilir.

__Örnekler__:

```python
# liste veya tuple
seriler = ["TP.DK.USD.A.YTL", "TP.DK.EUR.A.YTL"]
doviz_kurlari = connector.get_series(seriler,                              # OK
                                     start_date="01.06.2022",
                                     end_date="07.06.2022")

# virgülle ayrılmış metinler
doviz_kurlari = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",  # OK
                                     start_date="01.06.2022",
                                     end_date="07.06.2022")

# boşlukla ayrılmış metinler
doviz_kurlari = connector.get_series("TP.DK.USD.A.YTL TP.DK.EUR.A.YTL",   # OK
                                     start_date="01.06.2022",
                                     end_date="07.06.2022")
```


<a id="the-advanced-1"></a>

## __Gelişmiş Özellikler__

Burada `evdsts`'nin bazı gelişmiş özelliklerini inceleyeceğiz;

### [__Zaman Serisi Endeksleme__](#ts-indexing)
### [__İstenen Zaman Serisi İçin Farklı Frekans Seçme__](#selecting-different-frequency)
### [__İstenen Zaman Serisi İçin Dönüşüm Fonksiyonu Seçme__](#selecting-transformation)
### [__İstenen Zaman Serisi İçin Toplama Fonksiyonu Seçme__](#selecting-aggregation)
### [__Ham Veriyi JSON Formatında Alma__](#retrieving-raw-data)
### [__Çekilen Zaman Serilerine Yeni İsimler Atama__](#assigning-new-names)
### [__Serileri Diske Yazma__](#writing-series)
### [__Yerel Arama İndeksini Güncelleme__](#updating-index)


<a id="ts-indexing"></a>

### __Zaman Serisi Endeksleme__

`evdsts`, EVDS servisinden çekilen tüm serileri gerçek zaman serilerine dönüştürür. Bu davranış `get_series()` metodunun `time_series` bayrağı ile kontrol edilir ve `True` veya `False` olarak ayarlanabilir. Varsayılan: `True`.

__Örnekler__:

```python
# bu çağrı zaman serisi endekslemesi olmadan bir DataFrame döndürür.
usdtry = connector.get_series("TP.DK.USD.A.YTL",
                              start_date="01.06.2022",
                              end_date="30.06.2022",
                              time_series=False)
```

> __Zaman serisi endekslemesini devre dışı bırakmak birçok faydalı özelliğin kaybedilmesine neden olur.__
> __Bu nedenle, belirli bir ihtiyaç ortaya çıkmadıkça etkin tutulması daha iyidir.__

Zaman serisi endeksleme aşağıdaki gibi dilimler almamızı sağlar.

`usdtry`'den 1 Haziran 2022 - 7 Haziran 2022 aralığını kapsayan bir dilim alalım

```python
usdtry = connector.get_series("TP.DK.USD.A.YTL",
                              start_date="01.06.2022",
                              end_date="30.06.2022")

usdtry_dilim = usdtry.loc["2022-06-01": "2022-06-07"]
```

Burada zaman serisi endekslemenin avantajlarından birini görüyoruz: 01-07 Haziran aralığını, hangi orijinal indeks numarasına (EVDS serileri orijinal olarak 0'dan n'e indekslenerek döndürür) karşılık geldiğini bilmeden elde edebildik.

Benzer şekilde, `usdtry` serimiz için yapısal kırılma başlangıcı olabileceğinden şüphelendiğimiz bir tarih (15.06.2022) olduğunu varsayalım.

```python
yapisal_kirilma = datetime(2022, 6, 15)
usdtry_kirilma_sonrasi = usdtry.loc[usdtry.index > yapisal_kirilma]
usdtry_kirilma_oncesi = usdtry.loc[usdtry.index <= yapisal_kirilma]
```

Zaman serisi endeksleme sayesinde seriyi kırılma öncesi ve sonrası olarak kolayca bölebildik.

Veya modelimiz için `Pazartesi` günlerini temsil eden bir kukla değişkene ihtiyacımız olduğunu varsayalım. Zaman serisi endekslemesi kullanmasaydık mevcut aralıkta hangi günlerin Pazartesi'ye denk geldiğini bilmemiz gerekirdi, ancak zaman serisi endeksleme sayesinde aşağıdaki gibi kolayca yeni bir seri oluşturabiliriz.

```python

# haftanın günü -> Pazartesi: 0 - Pazar: 6
import pandas as pd

usdtry = connector.get_series("TP.DK.USD.A.YTL",
                              start_date="01.06.2022",
                              end_date="30.06.2022")

usdtry_pazartesileri = usdtry.loc[usdtry.index.day_of_week == 0]

kukla_pazartesi = pd.DataFrame(index=usdtry.index)
kukla_pazartesi = kukla_pazartesi.combine_first(usdtry_pazartesileri)
kukla_pazartesi = kukla_pazartesi.fillna(0)
kukla_pazartesi[kukla_pazartesi > 0] = 1

```

Başka bir örnek olarak çektiğimiz seriden yıllık dilimler alalım:

```python
usdtry = connector.get_series("TP.DK.USD.A.YTL",
                              start_date="01.01.2020",
                              end_date="31.12.2021")

# belki sadece 2020'ye ait veriye ihtiyacımız var.
usd_20 = usdtry.loc["2020"]

# veya belki 2020 ile 2021 arasına.
usd_21_22 = usdtry.loc["2020": "2021"]
```

Yukarıda `evdsts`'nin zaman serisi dönüşümlerinin bazı avantajlarını gördük, ancak bunlar gerçek zaman serileri üzerinde çalışırken elde edebileceklerinizin sadece küçük bir kısmıydı. Zaman serileri ile çalışma hakkında daha fazla bilgi almak için [Pandas Zaman Serileri](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html) sayfasını ziyaret edebilirsiniz.


<a id="selecting-different-frequency"></a>

### __İstenen Zaman Serisi İçin Farklı Frekans Seçme__

`get_series()` metodunun `frequency` parametresi, API servisinden istediğiniz zaman serisinin frekansını seçmek için kullanılır. Tanımlı frekansları görmek için `Connector` örneğinin `show_frequency_references()` metodunu kullanabilirsiniz.

```python
connector.show_frequency_references()
```

```python
                 References Table                 
--------------------------------------------------
Reference Name Represents -> Original Frequency Names on EVDS
--------------------------------------------------
default or level or 0   ---> 
daily or D or 1         ---> 1
bdaily or B or 2        ---> 2
weekly or W or 3        ---> 3
semimonthly or SM or 4  ---> 4
monthly or M or 5       ---> 5
quarterly or Q or 6     ---> 6
semiyearly or 6M or 7   ---> 7
yearly or Y or 8        ---> 8
--------------------------------------------------
```
Orijinal olarak günlük frekansta gözlemlenen `usdtry` serisini iş günü frekansında çekelim. Yukarıdaki tabloya göre bunu yapmak için `frequency` parametresine `bdaily`, `B` veya `2` verebilirsiniz.

```python
usdtry = connector.get_series("TP.DK.USD.A.YTL",
                              start_date="01.01.2020",
                              end_date="31.12.2021",
                              frequency="bdaily")
```

Frekansı iş günü olarak ayarladığınızda, döndürülen seri indeksinde Cumartesi ve Pazarlarına karşılık gelen tarihler artık yer almamalıdır.

> Not: Bu frekansta hafta sonuna denk gelmeyen resmi tatiller `NaN` olarak temsil edilir.


<a id="selecting-transformation"></a>

### __İstenen Zaman Serisi İçin Dönüşüm Fonksiyonu Seçme__

Seriler servisten çekilmeden önce bir dizi tanımlı dönüşüm fonksiyonu uygulanabilir. Bu tanımlı fonksiyonlar `get_series()` metodunun `transformations` parametresi ile belirlenir. Tüm EVDS servisinde önceden tanımlanmış fonksiyonları görmek için `Connector` örneğinin `show_transformation_references()` metodunu kullanabilirsiniz.

__Örnekler__:

```python
connector.show_transformation_references()
```

```python
                 References Table                 
--------------------------------------------------
Reference Name Represents -> Original Transformation Function Names on EVDS
--------------------------------------------------
level or 0              ---> 0
percent or 1            ---> 1
diff or 2               ---> 2
ypercent or 3           ---> 3
ydiff or 4              ---> 4
ytdpercent or 5         ---> 5
ytddiff or 6            ---> 6
mov or 7                ---> 7
movsum or 8             ---> 8
--------------------------------------------------
```

Yukarıdaki tabloda verilen dönüşüm fonksiyonlarının tanımları:

|   parametre       |   açıklama                                               |
|:-----------------:|-----------------------------------------------------------|
| `level`           |    _Düzey Serisi_                                         |
| `percent`         |    _Yüzde Değişim (getiri) Serisi_                       |
| `diff`            |    _Fark Serisi_                                          |
| `ypercent`        |    _Yıllık Yüzde Değişim (getiri) Serisi_                |
| `ydiff`           |    _Yıllık Fark Serisi_                                   |
| `ytdpercent`      |    _Yılbaşından İtibaren Yüzde Değişim (getiri) Serisi_  |
| `ytddiff`         |    _Yılbaşından İtibaren Fark Serisi_                    |
| `mov`             |    _Hareketli Ortalama Serisi_                           |
| `movsum`          |    _Hareketli Toplam Serisi_                             |

Orijinal olarak günlük gözlemlenen zaman serimizi haftalık seriye dönüştürelim ve ardından bu seriye yüzde değişim (getiri) serisini ekleyelim.

```python
usdtry = connector.get_series("TP.DK.USD.A.YTL",
                              start_date="01.01.2021",
                              end_date="31.12.2021",
                              frequency="W",
                              transformations="percent")

# dönen veri: USDTRY ve USDTRY% haftalık frekansta.
# USDTRY% = (USDTRY-USDTRY(t-1)) / USDTRY(t-1)
```

Çok boyutlu seriler istendiğinde dönüşümler iki farklı şekilde uygulanabilir.

1. Sadece bir fonksiyon verildiğinde, verilen dönüşüm fonksiyonu istenen tüm serilere uygulanır. Örneğin, `s1` ve `s2` serileri için sadece `t` fonksiyonu verilirse, dönüştürülmüş seriler `t(s1)` ve `t(s2)` olur.
2. Her seri için ayrı ayrı dönüşüm fonksiyonları verildiğinde, verilen fonksiyonlar sırasıyla serilere uygulanır. Örneğin, `s1` ve `s2` serileri için `t1` ve `t2` fonksiyonları verilirse, dönüştürülmüş seriler `t1(s1)` ve `t2(s2)` olur.

```python
doviz_kurlari = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                     start_date="01.01.2021",
                                     end_date="31.12.2021",
                                     frequency="W",
                                     transformations="percent")

# dönen veri; USDTRY, EURTRY, USDTRY% ve EURTRY% olacaktır çünkü her iki seri için
# tek bir dönüşüm fonksiyonu (percent) verilmiştir.
```

> Aksi açıkça istenmedikçe, dönüşüm veya toplama fonksiyonları uygulandığında orijinal seriler korunur ve çerçevede döndürülür. Bu davranış `get_series()` metodunun `keep_originals` bayrağı ile kontrol edilir ve varsayılan olarak `True`'dur. Dönüştürülmüş serilerle birlikte orijinal serilerin döndürülmesini istemiyorsanız çağırırken `False` olarak ayarlayabilirsiniz.

```python
doviz_kurlari = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                     start_date="01.01.2021",
                                     end_date="31.12.2021",
                                     frequency="W",
                                     transformations="percent",
                                     keep_originals=False)

# dönen veri USDTRY% ve EURTRY% olacaktır çünkü 'keep_originals' bayrağı 'False' olarak ayarlanmıştır.
```

Aşağıdaki örnekte ise, iki istenen zaman serisi için iki ayrı dönüşüm fonksiyonu verildiği için `percent` TP.DK.USD.A.YTL (USDTRY)'ye ve `diff` TP.DK.EUR.A.YTL (EURTRY)'ye sırasıyla uygulanır.

```python
doviz_kurlari = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                     start_date="01.01.2021",
                                     end_date="31.12.2021",
                                     frequency="W",
                                     transformations="percent, diff")

# dönen veri; USDTRY, EURTRY, USDTRY% ve D(EURTRY) zaman serileri olacaktır.
# USDTRY% = (USDTRY-USDTRY(t-1)) / USDTRY(t-1)
# D(EURTRY) = (EURTRY(t) - EURTRY(t-1))
```

Bireysel dönüşüm fonksiyonları aşağıda gösterilen farklı yollarla verilebilir:

1. virgülle ayrılmış `string` ile
2. boşlukla ayrılmış `string` ile
3. `List` veya `Tuple` gibi bir sequence türü içinde bireysel metinlerle

```python
donusumler = ["percent", "diff"]

doviz_kurlari = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                     start_date="01.01.2022",
                                     transformations=donusumler)          # OK

doviz_kurlari = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                     start_date="01.01.2022",
                                     transformations="percent, diff")     # OK

doviz_kurlari = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                     start_date="01.01.2022",
                                     transformations="percent diff")      # OK
```


<a id="selecting-aggregation"></a>

### __İstenen Zaman Serisi İçin Toplama Fonksiyonu Seçme__

Seriler servisten çekilmeden önce bir dizi tanımlı toplama fonksiyonu uygulanabilir. Bu tanımlı fonksiyonlar `get_series()` metodunun `aggregations` parametresi ile belirlenir. Tüm EVDS servisinde önceden tanımlanmış fonksiyonları görmek için `Connector` örneğinin `show_aggregation_references()` metodunu kullanabilirsiniz.

__Örnekler__:

```python
connector.show_aggregation_references()
```

```python
                 References Table                 
--------------------------------------------------
Reference Name Represents -> Original Aggregation Function Names on EVDS
--------------------------------------------------
avg or 1                ---> avg
min or 2                ---> min
max or 3                ---> max
first or 4              ---> first
last or 5               ---> last
sum or 6                ---> sum
--------------------------------------------------
```

Yukarıdaki tabloda verilen toplama fonksiyonlarının tanımları:

|   parametre   |   açıklama                                       |
|:--------------|--------------------------------------------------|
| `avg`         |seçilen frekanstaki ortalama (mean) değer          |
| `min`         |seçilen frekanstaki minimum değer                  |
| `max`         |seçilen frekanstaki maksimum değer                 |
| `first`       |seçilen frekanstaki ilk değer                      |
| `last`        |seçilen frekanstaki son değer                      |
| `sum`         |seçilen frekanstaki değerlerin toplamı              |

```python
usdtry = connector.get_series("TP.DK.USD.A.YTL",
                              start_date="01.01.2021",
                              end_date="31.12.2021",
                              frequency="W",
                              aggregations="max")

# çıktı USDTRY ve (01.01.2021 - 31.12.2021) aralığında verilen bir haftadaki
# USDTRY için gözlemlenen maksimum değerler olacaktır.
# diğer bir deyişle, USDTRY ve max(USDTRY, W)'ye eşittir.
```

Çok boyutlu seriler istendiğinde toplamalar iki farklı şekilde uygulanabilir.

1. Sadece bir fonksiyon verildiğinde, verilen toplama fonksiyonu istenen tüm serilere uygulanır.
2. Her seri için ayrı ayrı toplama fonksiyonları verildiğinde, verilen fonksiyonlar sırasıyla serilere uygulanır.

```python
doviz_kurlari = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                     start_date="01.01.2021",
                                     end_date="31.12.2021",
                                     frequency="W",
                                     aggregations="max")

# dönen veri; USDTRY, EURTRY, max(USDTRY, W) ve max(EURTRY, W) olacaktır çünkü
# tüm seriler için tek bir toplama fonksiyonu verilmiştir.
```

> Orijinal zaman serileri, `keep_originals` bayrağı varsayılan olarak `True` olduğundan toplanmış serilerle birlikte korunur ve döndürülür.

Aşağıdaki örnekte ise, iki zaman serisi için iki ayrı toplama fonksiyonu verildiği için `max` TP.DK.USD.A.YTL (USDTRY)'ye ve `min` TP.DK.EUR.A.YTL (EURTRY)'ye sırasıyla uygulanır.

```python
doviz_kurlari = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                     start_date="01.01.2021",
                                     end_date="31.12.2021",
                                     frequency="W",
                                     aggregations="max, min")

# çıktı USDTRY, EURTRY, (01.01.2021 - 31.12.2021) aralığında verilen bir haftadaki
# USDTRY için gözlemlenen maksimum değerler ve EURTRY için gözlemlenen minimum değerler olacaktır.
# diğer bir deyişle, USDTRY, EURTRY, max(USDTRY, W), min(EURTRY, W)'ye eşittir.
```

Bireysel toplama fonksiyonları aşağıda gösterilen farklı yollarla verilebilir:

1. virgülle ayrılmış `string` ile
2. boşlukla ayrılmış `string` ile
3. `List` veya `Tuple` gibi bir sequence türü içinde bireysel metinlerle

```python
toplamalar = ["max", "min"]

doviz_kurlari = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                     start_date="01.01.2022",
                                     aggregations=toplamalar)             # OK

doviz_kurlari = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                     start_date="01.01.2022",
                                     aggregations="min, max")             # OK

doviz_kurlari = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                     start_date="01.01.2022",
                                     aggregations="min max")              # OK
```

> __Belirsizliği önlemek için `evdsts`, dönüşüm ve toplama fonksiyonlarının serilere aynı anda__
> __uygulanmasına izin vermez.__


<a id="retrieving-raw-data"></a>

### __Ham Veriyi Diğer Formatlarda Alma__

API servisinden dönen dokunulmamış JSON verisini almak için `get_series()` metodunun `raw` bayrağını kullanabilirsiniz.

```python
doviz_kurlari = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                     start_date="01.01.2020",
                                     end_date="31.12.2021",
                                     frequency="Y",
                                     transformations="percent",
                                     raw=True)
```

benzer şekilde, veriyi `Dict` nesnesi olarak almak için `as_dict` parametresini kullanabilirsiniz.

```python
doviz_kurlari = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                     start_date="01.01.2020",
                                     end_date="31.12.2021",
                                     frequency="Y",
                                     transformations="percent",
                                     as_dict=True)
```


<a id="assigning-new-names"></a>

### __Çekilen Zaman Serilerine Yeni İsimler Atama__

`get_series()` metodunun `new_names` parametresi ile çekilen serilere yeni sütun adları atayabilirsiniz. `DataFrame` sütunları için yeni adlar istenen seriler sırasıyla atanır.

### [__Sade Seri İstekleri İçin Yeni İsim Atama__](#assigning-new-names-bare)
### [__Dönüştürülmüş veya Toplanmış Seri İstekleri İçin Yeni İsim Atama__](#assigning-new-names-transagg)


<a id="assigning-new-names-bare"></a>

### __Sade Seri İstekleri İçin Yeni İsim Atama__

Aşağıdaki örnek çekilen seriler için nasıl yeni isim verileceğini gösterir. İsimler sırasıyla verilir: `TP.DK.USD.A.YTL = USDTRY` ve `TP.DK.EUR.A.YTL = EURTRY`, bu nedenle döndürülen `DataFrame`'in sütun adları `TP.DK.USD.A.YTL` ve `TP.DK.EUR.A.YTL` yerine `USDTRY` ve `EURTRY` olur.

__Örnekler__:

```python
doviz_kurlari = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                     start_date="01.01.2021",
                                     end_date="31.12.2021",
                                     frequency="W",
                                     new_names="USDTRY, EURTRY")
```

Yeni seri adları aşağıda gösterilen farklı yollarla verilebilir:

1. virgülle ayrılmış `string` ile
2. boşlukla ayrılmış `string` ile
3. `List` veya `Tuple` gibi bir sequence türü içinde bireysel metinlerle

```python
yeni_isimler = ["USDTRY", "EURTRY"]

doviz_kurlari = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                     start_date="01.01.2021",
                                     end_date="31.12.2021",
                                     frequency="W",
                                     new_names=yeni_isimler)               # OK

doviz_kurlari = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                     start_date="01.01.2021",
                                     end_date="31.12.2021",
                                     frequency="W",
                                     new_names="USDTRY, EURTRY")           # OK

doviz_kurlari = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                     start_date="01.01.2021",
                                     end_date="31.12.2021",
                                     frequency="W",
                                     new_names="USDTRY EURTRY")            # OK
```


<a id="assigning-new-names-transagg"></a>

### __Dönüştürülmüş veya Toplanmış Seri İstekleri İçin Yeni İsim Atama__

Orijinal zaman serileri dönüştürülmüş veya toplanmış serilerle birlikte isteniyorsa, yani `keep_originals = True` ise, yeni isimler aşağıdaki sırada verilmelidir:

__`orijinal seriler için isimler ardından dönüştürülmüş/toplanmış seriler için isimler`__

Dolayısıyla, örneğin; USDTRY `percent` dönüşümü ile isteniyorsa, döndürülen `DataFrame` hem `USDTRY` hem de `USDTRY%` serilerini içerdiği için (`keep_originals` varsayılan olarak `True` olduğundan) yeni isimler aşağıdaki gibi verilmelidir.

```python
usdtry = connector.get_series("TP.DK.USD.A.YTL",
                              start_date="01.01.2021",
                              end_date="31.12.2021",
                              frequency="W",
                              transformations="percent",
                              new_names="USDTRY, P_USDTRY")

# döndürülen dataframe USDTRY, USDTRY%'den oluştuğu için ('keep_originals' = True varsayılan)
# yeni isimler USDTRY, P_USDTRY olarak verilmiştir.
```

> İpucu: Eşleşmeyen sayıda yeni isim verdiğinizde `UnmatchingFieldSizeException` hatası fırlatılır
> ve hata mesajından kaç tane yeni isim vermeniz gerektiğini anlayabilirsiniz.

Orijinal seriler döndürülen veride istenmiyorsa (`keep_originals = False`) yeni isimler sadece dönüştürülmüş veya toplanmış seriler için verilir.

```python
usdtry = connector.get_series("TP.DK.USD.A.YTL",
                              start_date="01.01.2021",
                              end_date="31.12.2021",
                              frequency="W",
                              transformations="percent",
                              keep_originals=False,
                              new_names="USDTRY_P")

# döndürülen veri keep_originals bayrağı False olduğu için sadece USDTRY% içerdiğinden
# yeni isim olarak sadece USDTRY verilmiştir
```

benzer şekilde,

```python
doviz_kurlari = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                     start_date="01.01.2021",
                                     end_date="31.12.2021",
                                     frequency="6M",
                                     aggregations="max, min",
                                     new_names="USDTRY, EURTRY, USDTRY_MAX, EURTRY_MIN")

# döndürülen veri USDTRY, EURTRY, max(USDTRY), min(EURTRY) içerdiğinden
# yeni isimler buna göre verilmiştir.
```

ve,

```python
doviz_kurlari = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                     start_date="01.01.2021",
                                     end_date="31.12.2021",
                                     frequency="6M",
                                     aggregations="max, min",
                                     new_names="USDTRY_MAX, EURTRY_MIN",
                                     keep_originals=False)

# döndürülen veri sadece max(USDTRY) ve min(EURTRY) içerdiğinden
# yeni isimler buna göre verilmiştir.
```


<a id="writing-series"></a>

### __Serileri Diske Yazma__

`evdsts`'den dönen tüm veriler `Connector` örneğinin `to_file()` metodu ile diske yazılabilir. Verileri daha sonra kullanmak üzere saklamak için `JSON`, `CSV` veya `XLS` (`openpyxl` paketi gerektirir) formatlarında yazabilirsiniz.

`to_file()` metodu iki önemli parametre alır:

a. `data`: diske yazılacak verinin kendisi
b. `data_format`: `csv`, `json`, `xls` gibi çıktı formatını belirler

`to_file()` metodunun imzası:

```python
def to_file(
            data: Optional[Union[pd.DataFrame, JSONType, Dict]] = None,
            data_format: str = "csv",
            filename: Optional[str] = None,
            delimiter: str = ";",
) -> None:
```

1. `data`: Diske yazılacak veri.
    - Pandas `DataFrame` olarak verilebilir
    - `JSONType` ham veri olarak verilebilir
    - Python `Dict` olarak verilebilir.
2. `data_format`: Çıktı formatı. Varsayılan: `csv`
    - csv dosya formatı için: `csv`
    - Excel formatı için: `excel`, `xls` veya `xlsx`
    - ham format için: `raw` veya `json`
3. `filename`: Çıktı dosya adı. Varsayılan: `None`
    - Çıktı için yalın dosya adı. Çıktı dosyası her zaman mevcut çalışma dizinine kaydedilir.
    Bu nedenle verilen dosya adı sadece "cppi" veya "issizlik" gibi yalın bir dosya adı olmalıdır.
        - verilmezse çıktı dosya adı şu şekilde ayarlanır: `data_yil_ay_gun_saat_dakika_saniye`
4. `delimiter`: csv formatı için alan ayırıcı. Varsayılan: `;`

__Örnekler__:

Ana kategorileri diske yazalım:

```python

ana_sozluk = connector.get_main_categories()
connector.to_file(data=ana_sozluk, data_format='csv')

```
```python
Given data have been written on g:\My Drive\Dev\Active\evdsts\data_2022_07_19_213945.csv
```

Benzer şekilde,

```python
alt_kategoriler_df = connector.get_sub_categories("TCMB DÖVİZ KURLARI")
connector.to_file(data=alt_kategoriler_df, data_format='json')

```
```python
Data is written on g:\My Drive\Dev\Active\evdsts\data_2022_08_12_214320.json
```

> `evdsts` tüm `dict`, `JSON` ve `DataFrame` türü verileri verilen formatlarda diske yazabilir.


<a id="updating-index"></a>

### __Yerel Arama İndeksini Güncelleme__

`evdsts`, EVDS'de seri adlarını aramak için yerel bir indeks kullanır. Yerel indeks, EVDS'de yapılan seri güncellemeleri nedeniyle oluşturulma tarihinden birkaç ay sonra güncelliğini yitirebilir. Yerel indeksi EVDS ile senkronize tutmak için birkaç ayda bir güncelleyebilirsiniz.

__Komut Satırı ile (Önerilen)__:

Arama indeksini yeniden oluşturmanın en kolay yolu `evdsts` komut satırı aracıdır:

```bash
# Türkçe indeksi yeniden oluştur (varsayılan)
evdsts build-index

# İngilizce indeksi yeniden oluştur
evdsts build-index --language ENG

# onay istemini atla
evdsts build-index -y

# API anahtarını doğrudan ver
evdsts build-index --key API_ANAHTARINIZ --language TR -y

# API istekleri arasındaki bekleme süresini ayarla (varsayılan: 5 saniye, minimum: 5)
evdsts build-index --wait 7
```

__Python ile__:

İndeksi `IndexBuilder` sınıfını kullanarak programatik olarak da yeniden oluşturabilirsiniz:

```python
from evdsts import IndexBuilder

# bir builder örneği oluşturun
builder = IndexBuilder('API_ANAHTARINIZ', language="TR")

# yerel indeksin gün cinsinden ne kadar eski olduğunu kontrol edin
print(builder.index_age_in_days)

# indeksi yeniden oluşturun
builder.build_index()
```

> __Yerel arama indeksini yeniden oluşturmanın yaklaşık 60 dakika sürdüğünü lütfen unutmayın çünkü builder,__
> __API servisini yoğun isteklerle aşırı yüklememek için kurduğu her yeni bağlantı arasında__
> __makul bir süre (min. 5 sn.) bekler.__


<a id="using-reference-names"></a>

## __Referans İsimlerle Zaman Serisi Çekme__

EVDS veritabanındaki serilerle çalışırken verimliliği olumsuz etkileyen en önemli neden, EVDS'nin karmaşık seri adı tanımlamalarıdır. Bu durum, servisten veri almak istediğinizde her seferinde EVDS'deki orijinal seri adlarını bulmanıza neden olur. `evdsts`, servisten veri çekerken EVDS veritabanındaki gerçek seri adları için vekil isimler olarak kullanılabilecek referans isimleri tanıtarak bu sorunu çözer.

Referans isimler iki farklı şekilde verilebilir:

1. Sadece orijinal seriler istendiğinde, yani ne dönüşüm ne de toplama fonksiyonu istendiğinde, `keep_references` bayrağını kullanarak serilere yeni isimler verebilir ve referans isim olarak kaydedebilirsiniz.
2. Referans isimleri doğrudan kaydetmek için `Connector` örneğinin `save_name_references()` metodunu kullanabilirsiniz.

### [__Zaman Serisi Çekerken Referans İsim Kaydetme__](#saving-reference-name)
### [__Referans İsimleri Doğrudan Kaydetme__](#saving-names-directly)
### [__Referans İsimleri Diğer Projelere Aktarma__](#transferring-reference-names)


<a id="saving-reference-name"></a>

### __Zaman Serisi Çekerken Referans İsim Kaydetme__

Referans isimleri kaydetmenin ilk yolu aşağıdaki blokta gösterilmiştir. İstenen seriler için ne dönüşüm ne de toplama fonksiyonu uygulanmadığından `keep_references` bayrağını kullanabilirsiniz. `usdtry` referans adı kalıcı olarak `usdtry -> TP.DK.USD.A.YTL` şeklinde kaydedilir.

__Örnekler__:

```python
usdtry = connector.get_series("TP.DK.USD.A.YTL",
                              start_date="01.01.2021",
                              end_date="31.12.2021",
                              frequency="Q",
                              new_names="usdtry",
                              keep_references=True)
```

Bir seri için referans isim kaydettiğinizde ekranda bir bildirim gösterilir. Bu, bundan sonra veri çekerken bu referans ismi kullanabileceğiniz anlamına gelir.

```python
Below references map have been created for further use. You can use reference series names instead of original ones
when retrieving data from the EVDS API service. Reference names are permanent unless this reference mapping is deleted
or changed.

                 References Table                 
--------------------------------------------------
Reference Name Represents -> Original Series Names on EVDS
--------------------------------------------------
usdtry          ---> TP.DK.USD.A.YTL
--------------------------------------------------
```

Şimdi aynı isteği yapalım.

```python
usdtry = connector.get_series("usdtry",
                              start_date="01.01.2021",
                              end_date="31.12.2021",
                              frequency="Q")
# artık orijinal seri adını bilmenize veya vermenize gerek yok!
```

Tek bir çağrıda birden fazla referans isim kaydedelim.

```python
doviz_kurlari = connector.get_series("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
                                     start_date="01.01.2021",
                                     end_date="31.12.2021",
                                     frequency="Q",
                                     new_names="usdtry, eurtry",
                                     keep_references=True)
```

Mevcut projeniz için verdiğiniz tüm referans isimleri `show_name_references()` metodu ile görebilirsiniz.

```python
connector.show_name_references()
```

Referans isimlerle çok boyutlu zaman serisi çekelim.

```python
doviz_kurlari = connector.get_series("usdtry, eurtry",
                                     start_date="01.01.2021",
                                     end_date="31.12.2021",
                                     frequency="Q")
```

Referans isimleri bu yöntemle aşağıdaki gibi değiştirebilirsiniz:

```python
doviz_kurlari = connector.get_series("usdtry, eurtry",
                                     start_date="01.01.2021",
                                     end_date="31.12.2021",
                                     frequency="Q",
                                     new_names="dolar_tl, euro_tl",
                                     keep_references = True)
# eski referans isimleri 'usdtry' ve 'eurtry', 'dolar_tl' ve 'euro_tl' ile değiştirilir
```

> İstenen serilerden herhangi birine referans isim verilmişse, döndürülen `DataFrame` sütunları otomatik olarak referans isimlerle adlandırılır. Bu nedenle, referans isimleri zaten atanmış seriler için sütunları yeniden adlandırmak üzere `new_names` parametresini kullanmanıza gerek yoktur.


<a id="saving-names-directly"></a>

### __Referans İsimleri Doğrudan Kaydetme__

İkinci yol olarak, `Connector` örneğinin `save_name_references()` metodunu kullanarak referans isimleri doğrudan kaydedebilirsiniz.

`save_name_references()` metodunun imzası:

```python
def save_name_references(
                         series_names: Union[str, Sequence[str]],
                         reference_names: Union[str, Sequence[str]],
                         old_reference_names: Optional[List[str]] = None,
                         verbose: bool = True,
                         check_names: bool = True
) -> None:
```

1. `series_names`: EVDS API'deki orijinal seri adları veya şu anda referans olarak kaydedilmiş adlar.
    - Tek bir seri için metin olarak veya `List` ya da `Tuple` gibi bir Sequence türünde verilebilir.
2. `reference_names`: Seriler için referans adlar.
    - Tek bir seri için metin olarak veya `List` ya da `Tuple` gibi bir Sequence türünde verilebilir.
    - Referans adlar standart `Latin` karakterler `[A-Za-z]`, rakamlar `[0-9]` ve alt çizgi (`_`) karakterinden oluşmalıdır.
3. `old_reference_names`: Çoğunlukla dahili kullanım içindir. Varsayılan: `None`
4. `verbose`: Sonuç için metin çıktısı verir. Varsayılan: `True`.
5. `check_names`: Verilen seri adlarının EVDS API sunucusunda doğru tanımlayıcılar olup olmadığını kontrol eder. Varsayılan: `True`


__Örnekler__:

```python
connector.save_name_references('TP.FE.OKTG01', 'tufe')
```

veya bir kerede birden fazla referans isim kaydedebilirsiniz;

```python
connector.save_name_references('TP.FE.OKTG01, TP.DK.USD.A.YTL', 'tufe, usdtry')
```

Referans isimleri farklı yollarla kaydedebilirsiniz:

1. virgülle ayrılmış `string` ile
2. boşlukla ayrılmış `string` ile
3. `List` veya `Tuple` gibi bir sequence türü içinde bireysel metinlerle

```python
seriler = ["TP.DK.USD.A.YTL", "TP.DK.EUR.A.YTL"]
referanslar = ["usdtry", "eurtry"]

connector.save_name_references("TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL", "usdtry, eurtry", verbose=False)  # OK
connector.save_name_references("TP.DK.USD.A.YTL TP.DK.EUR.A.YTL", "usdtry eurtry", verbose=False)    # OK
connector.save_name_references(seriler, referanslar, verbose=False)                                    # OK

# verbose ekran çıktısını kontrol eder
```
> İpucu: Sonuçların ekran gösterimini etkinleştirmek veya devre dışı bırakmak için hemen hemen her fonksiyonda `verbose` bayrağını kullanabilirsiniz.

Eski referans isimlerini yenileriyle de değiştirebilirsiniz. Daha önce `usdtry` olarak atadığımız referans adını `usdlira` olarak değiştirmek istediğimizi varsayalım.

```python
connector.save_name_references("usdtry", "usdlira")
```


<a id="transferring-reference-names"></a>

### __Referans İsimleri Diğer Projelere Aktarma__

`evds_series_references.json` dosyasını projelerin mevcut çalışma dizinlerine aktararak referans isimlerinizi projeler arasında transfer edebilirsiniz.

_Mevcut referans isimleri dosyası nerede?_

```python
print(connector.references_file)

# 'g:\\My Drive\\Dev\\Active\\evdsts\\evds_series_references.json' verir
```

veya diğer detaylarla birlikte referans dosya konumunu görmek için `Connector` örneğini `print` edin.

```python
print(connector)
```

_Bu isimleri şu anda üzerinde çalıştığım yeni projeye nasıl aktarabilirim?_

1. Yeni projenizde yeni bir `Connector` örneği oluşturun. Diyelim, `connector`
2. Diğer projeden aldığınız referans isim dosya yolunu vererek `import_name_references()` metodunu kullanın.

`import_name_references()` metodunun imzası:

```python
def import_name_references(source: Union[str, Path]) -> None:
```

1. `source`: referans isimleri dosyasının mutlak yolu.

__Örnekler__:

```python
connector.import_name_references('g:\\My Drive\\Dev\\Active\\evdsts\\evds_series_references.json')
```


<a id="the-transformator-1"></a>

## __Transformator__

`Transformator`, çekilen verileri zaman serisi analiz sürecini kolaylaştırmak amacıyla manipüle etmekten sorumlu olan `evdsts`'nin ikinci önemli bileşenidir. Tanımlı dönüşümleri gerçekleştirmek için `Transformator` sınıfından bir örnek oluşturmanız gerekmektedir.

> __`Transformator` metotlarının çoğunun '_zaman serisi endekslemesi_' ve '_artan sıralama_'ya bağlı__
> __olduğunu lütfen unutmayın. Bu zaten `Connector`'ın varsayılan dönüş değeridir, ancak `Connector`'ın__
> __`get_series()` metodu ile veri çekerken;__
> __`time_series = False`__ ve/veya
> __`ascending = False`__
> __bayraklarını kullanırsanız sonuçların bütünlüğü garanti edilmez.__

`Transformator` sınıfının imzası:

```python
def __init__(global_precision: Optional[int] = None) -> None:
```

1. `global_precision`: Tüm dönüşüm fonksiyonları tarafından döndürülen kayan noktalı sayılar için global hassasiyet belirler. Varsayılan: `None`
    - `None` verilirse: Global hassasiyet ayarlanmaz. Her dönüşüm fonksiyonu, `precision=n` parametresi ile açık bir hassasiyet verilmezse kendi varsayılan hassasiyetini kullanır.
    - tam sayı verilirse: Her dönüşüm fonksiyonu için global varsayılan hassasiyet verilen değere ayarlanır. Bu, `precision=n` parametresi ile açık bir hassasiyet verilmezse fonksiyonların kendi bireysel varsayılanları yerine bu global varsayılan hassasiyeti kullanacağı anlamına gelir.

    - Notlar:
        - Herhangi bir dönüşüm fonksiyonu çağrılırken `precision=n` parametresi ile açıkça verilen hassasiyet, her zaman `global_precision` ve fonksiyonun kendi varsayılan hassasiyetini geçersiz kılar.
        - `precision=n` parametresi ile açık bir hassasiyet verilmezse, `global_precision` fonksiyonun kendi varsayılan hassasiyetini geçersiz kılar.

__Örnekler__:

`Transformator` sınıfından aşağıdaki gibi bir örnek oluşturabilirsiniz;

Öncelikle `evdsts`'den `Transformator` sınıfını içe aktarmanız gerekir

```python
from evdsts import Transformator
```

ardından sınıftan aşağıdaki gibi bir örnek oluşturabilirsiniz;

```python
transformator = Transformator()
```

veya tüm `Transformator` metotları tarafından varsayılan olarak kullanılacak global kayan noktalı sayı hassasiyeti tanımlayabilirsiniz. Aşağıdaki `transformator` nesnesinin kayan noktalı sayı hassasiyeti örnek olarak `4` olarak ayarlanmıştır.

```python
transformator = Transformator(4)  # Bu, tüm metotlar için varsayılan kayan noktalı sayı hassasiyetini 4 olarak ayarlar.
```


<a id="rename-series"></a>

### __Transformator ile Seri İsimlerini Yeniden Adlandırma__

`Transformator` tarafından otomatik olarak atanan seri isimlerini kullanmak istemiyorsanız `rename()` fonksiyonunu kullanarak yeniden adlandırabilirsiniz.

`rename()` fonksiyonunun imzası:

```python
def rename(
            self,
            series: pd.DataFrame,
            names: Union[str, Sequence[str]],
            inplace: bool = False
) -> Union[pd.DataFrame, None]:
```

1. `series`: Serilerden oluşan bir DataFrame nesnesi.
2. `names`: Orijinallerle aynı sırada serilerin yeni adları.
    - virgülle ayrılmış metin olarak verilebilir: `"usdtry, eurtry, corr_usdtry, corr_eurtry"`
    - Tuple olarak verilebilir: `("usdtry", "eurtry", "corr_usdtry", "corr_eurtry")`
    - List olarak verilebilir: `["usdtry", "eurtry", "corr_usdtry", "corr_eurtry"]`
3. `inplace`: `True` ise verilen seriyi doğrudan değiştirir. Varsayılan: `False`

__Kullanılabilirlik__:
Tekli (ör: usdtry) veya çok boyutlu (ör: usdtry ve eurtry içeren doviz_kurlari) seriler için kullanılabilir.

__Örnekler__:

```python
connector = Connector(language="TR")  # API Anahtarınızı zaten diske kaydettiğinizi varsayarak.
transformator = Transformator()

# referans isimlerle seri çek
seriler = connector.get_series("usdtry, eurtry",
                              start_date="01.01.2021",
                              end_date="31.12.2021",
                              frequency="M")

lag_2s = transformator.laggeds(seriler, "1, 2")

# bu, lag_2s'deki tüm serileri yeniden adlandıran bir kopya döndürür
lag_2s_renamed = transformator.rename(lag_2s, "utr, eutr, utrl1, eutrl1, utrl2, eutrl2")

# Bu, lag_2s'nin kendisini yeniden adlandırır ve hiçbir şey döndürmez.
transformator.rename(lag_2s, "utr, eutr, utrl1, eutrl1, utrl2, eutrl2", inplace=True)
```


<a id="trans-precision"></a>

### __Transformator ile Kayan Noktalı Sayı Hassasiyetini Ayarlama__

Verilerinizdeki kayan noktalı sayıları istediğiniz zaman `set_precision()` metodu ile kesebilirsiniz.

`set_precision()` fonksiyonunun imzası:

```python
def set_precision(
                    series: pd.DataFrame,
                    precision: int,
                    inplace: bool = False
) -> Union[pd.DataFrame, None]:
```

1. `series`: Sayısal serilerden oluşan bir DataFrame.
2. `precision`: Kayan noktalı sayıların sabitleneceği hassasiyet.
3. `inplace`: `True` ise verilen seriyi doğrudan değiştirir. Varsayılan: `False`

__Örnekler__:

```python
connector = Connector(language="TR")
transformator = Transformator()

eurtry = connector.get_series("eurtry",
                              start_date="01.06.2022",
                              end_date="30.06.2022",
                              frequency="B")

# döviz kuru hassasiyetleri 2'ye sabitlenmiş yeni bir seri döndürür
eurtry_p4 = transformator.set_precision(eurtry, 2)

# 'eurtry' değişkeninin kendisini kayan nokta hassasiyetlerini 2'ye sabitleyerek değiştirir
transformator.set_precision(eurtry, 2, inplace=True)
```


<a id="regular-diff"></a>

### __Fark Alma: Δ(y<sub>t</sub>, i) = y<sub>t</sub> - y<sub>t-i</sub> = (1-L)<sup>i</sup>y<sub>t</sub>__

Verilen serilerin fark serilerini almak için `Transformator`'un `diff()` metodunu kullanabilirsiniz. Fark serileri genellikle durağan olmayan serilerden durağan seriler elde etmek için kullanılır. Bu işlemdeki en önemli uyarı, fark serileriyle modellemenin değişkenlerle uzun dönemli ilişkileri temsil edemeyeceğidir çünkü fark alma işlemi serilerin uzun dönemli hafızalarını kaybetmesine neden olur.

`diff()` metodunun imzası:

```python
def diff(
        series: pd.DataFrame,
        order: int = 1,
        precision: Optional[int] = None,
        keep_originals: bool = True,
        rename: bool = True
) -> pd.DataFrame:
```

1. `series`: İşlenecek serileri içeren bir `DataFrame`.
2. `order`: Fark operatörünün derecesi. Varsayılan: `1` (1. Fark).
3. `precision`: Döndürülen değerlerin hassasiyeti. Varsayılan: `None`
4. `keep_originals`: `True` ise döndürülen DataFrame'e orijinal serileri dahil eder. Varsayılan: `True`
5. `rename`: sütun adlarını uygun şekilde yeniden adlandırır. Varsayılan: `True`

__Örnekler__:

```python
connector = Connector(language="TR")
transformator = Transformator(4)

usdtry = connector.get_series("usdtry",
                              start_date="01.06.2022",
                              end_date="30.06.2022",
                              frequency="B")

# bu size usdtry ve usdtry'nin birinci farkını bir çerçevede verir
fark_orijinallerle = transformator.diff(usdtry)
```

Fark serileri varsayılan olarak orijinal serilerle birlikte döndürülür. Orijinal serilerin fark alınmış serilerle birlikte döndürülmesini istemiyorsanız `keep_originals` bayrağını kullanabilirsiniz. Ayrıca 2., 3., 4.,...n. farkı almak için `order` parametresini kullanabilirsiniz.

```python
# Bu size sadece usdtry'nin 2. farkını verir
sadece_fark_2 = transformator.diff(usdtry, order=2, keep_originals=False)
```


<a id="log-transform"></a>

### __Doğal Logaritmik Dönüşüm: ln(y<sub>t</sub>)__

Verilen serilerin doğal logaritmalarını almak için `ln()` metodunu kullanabilirsiniz. Log dönüşümü, yüksek seri varyanslarından kaynaklanan modelleme problemlerini kolaylaştırabilir.

`ln()` metodunun imzası:

```python
def ln(
       series: pd.DataFrame,
       precision: Optional[int] = None,
       keep_originals: bool = True,
       rename: bool = True
) -> pd.DataFrame:
```

__Örnekler__:

```python
usd_ve_ln_usd = transformator.ln(usdtry)   # bu size usdtry ve ln(usdtry) verir

ln_usd = transformator.ln(usdtry, keep_originals=False)   # bu size sadece ln(usdtry) verir
```


<a id="logaritmic-diff"></a>

### __Logaritmik Fark (LogGetiri): Δ(ln(y<sub>t</sub>), i) = ln(y<sub>t</sub>) - ln(y<sub>t-i</sub>) = (1-L)<sup>i</sup>ln(y<sub>t</sub>)__

Serilerin logaritmik farklarını (log getirileri) almak için `lndiff()` metodunu kullanabilirsiniz. Bu simetrik bir getiri serisidir; t zamanında `0.2` ln fark ve t+1 zamanında `-0.2` ln fark elde ederseniz, başladığınız yere geri dönersiniz, yani toplam etkisi `0`'dır.

`lndiff()` metodunun imzası:

```python
def lndiff(
           series: pd.DataFrame,
           order: int = 1,
           precision: Optional[int] = None,
           keep_originals: bool = True,
           rename: bool = True
) -> pd.DataFrame:
```

__Örnekler__:

```python
usd_log_getiri = transformator.lndiff(usdtry)           # 1. logaritmik farkları (log getiri) verir
usd_2_lndiff = transformator.lndiff(usdtry, order=2)    # 2. logaritmik farkları verir
sadece_log_getiri = transformator.lndiff(usdtry, keep_originals=False)  # sadece log getiriyi verir
```


<a id="deterministic-trend"></a>

### __Deterministik Trend: y<sub>t</sub> = β<sub>0</sub> + β<sub>1</sub>Trend + β<sub>2</sub>Trend<sup>2</sup> + ... β<sub>n</sub>Trend<sup>n</sup> + ε<sub>t</sub>__

Verilen seriler için deterministik trend modelinden elde edilen tahmin serisini almak için `deterministic_trend()` metodunu kullanabilirsiniz.

Deterministik trend, σ<sup>2</sup>y<sub>t</sub> = σ<sup>2</sup> koşulunu sağlayan, yani trendin varyansının zamanla değişmediği bir olgudur. Böyle bir süreç _trend durağan_ süreç olarak adlandırılır ve durağanlık o trendi orijinal seriden çıkararak sağlanabilir.

`deterministic_trend()` metodunun imzası:

```python
def deterministic_trend(
                        series: pd.DataFrame,
                        degree: int = 1,
                        precision: Optional[int] = None,
                        keep_originals: bool = True,
                        rename: bool = True
) -> pd.DataFrame:
```

__Örnekler__:

```python
# doğrusal trend modelinin tahminlerini verir
dt_tahmin = transformator.deterministic_trend(usdtry)

# ikinci derece trend modelinin tahminlerini verir
dt_ikinci_tahmin = transformator.deterministic_trend(usdtry, degree=2)
```

> Yüksek dereceli polinomlar, verilen serinin iyi bir temsilcisi değillerse aşırı salınım yapabilirler.


<a id="de-trend"></a>

### __Ayrıştırma: y<sub>t</sub> - (β<sub>0</sub> + β<sub>1</sub>Trend + β<sub>2</sub>Trend<sup>2</sup> + ... β<sub>n</sub>Trend<sup>n</sup> + ε<sub>t</sub>)__

Çekilen serileri `decompose()` metodu ile ayrıştırabilirsiniz (trendden arındırabilirsiniz). Orijinal serilerden zamana bağlı deterministik trendleri çıkarmak, durağan olmayan (veya trend durağan) serilerden durağan seriler elde etmenin iyi bir yoludur.

Ayrıştırma aşağıdaki yollardan biriyle yapılabilir;

- Deterministik trend çıkarma
    - çıkarma (subtract)
    - bölme (divide)
- Basit/Üstel Hareketli Ortalamaları çıkarma
    - çıkarma (subtract)
    - bölme (divide)

`decompose()` metodunun imzası:

```python
def decompose(
              series: pd.DataFrame,
              degree: int = 1,
              source: str = "trend",
              method: str = "subtract",
              precision: Optional[int] = None,
              keep_originals: bool = True,
              rename: bool = True
) -> pd.DataFrame:
```

1. `series`: Trendden arındırılacak serilerden oluşan DataFrame
2. `degree`: Deterministik trendin derecesi veya (e/s)ma için pencere. Varsayılan: `1`.
3. `source`: Trendden arındırma kaynağı. Varsayılan: `trend`.
    - `trend`: trendden arındırılmış seri = seri (- veya /) trend(seri, verilen_derece)
    - `sma`: trendden arındırılmış seri = seri (- veya /) sma(seri, pencere=derece)
    - `ema`: trendden arındırılmış seri = seri (- veya /) ema(seri, pencere=derece)
4. `method`: Trendden arındırma operatörü olarak kullanılacak yöntem. Varsayılan: `subtract`
    - `subtract`: `seri` - `kaynak`
    - `divide`: `seri` / `kaynak`

__Örnekler__:

```python
# [usdtry - (usdtry_tahmin = b0 + b1Trend*usdtry)] verir
det_usdtry = transformator.decompose(usdtry, degree=1, source='trend', method='subtract')

# [usdtry - sma(usdtry, pencere=2)] verir
det_usdtry_sma = transformator.decompose(usdtry, degree=2, source='sma', method='subtract')

# [usdtry - ema(usdtry, pencere=2)] verir
det_usdtry_ema = transformator.decompose(usdtry, degree=2, source='ema', method='subtract')
```


<a id="smooth-sma"></a>

### __Basit Hareketli Ortalama: MA<sub>t</sub>(n) = (y<sub>t</sub> + y<sub>t-1</sub> ... y<sub>t-n</sub>) / n__

_Basit Hareketli Ortalama_ düzleştirilmiş serilerini `Transformator`'un `sma()` metodu ile alabilirsiniz. Hareketli Ortalamalar genel olarak, beklenen değerler etrafındaki yüksek frekanslı salınımları (gürültü olarak görülebilir) göz ardı ederek serilerdeki ana akımları gözlemlemek için iyidir. __SMA__ verilen zaman penceresi için gözlemlere eşit ağırlık verir.

`sma()` metodunun imzası:

```python
def sma(
        series: pd.DataFrame,
        window: Union[int, str],
        precision: Optional[int] = None,
        keep_originals: bool = True,
        rename: bool = True
) -> pd.DataFrame:
```

1. `series`: Zaman serilerinden oluşan bir DataFrame.
2. `window`: Ortalama alma işlemi için pencere (sabit dönem veya zamana dayalı).
    - gözlemlere sabitlenebilir: `5`, zamandan bağımsız olarak tam olarak 5 gözlem anlamına gelir.
    - zamana sabitlenebilir: `5d`, tam olarak `5` günü kapsayan gözlemler anlamına gelir.

__Örnekler__:

```python
# sma(5) verir
usdtry_sma5 = transformator.sma(usdtry, window=5)
```


<a id="smooth-ema"></a>

### __Üstel Hareketli Ortalama: EMA<sub>t</sub>(n) = αy<sub>t</sub> + (1-α)EMA<sub>t-1</sub>__

_Üstel Hareketli Ortalama_ düzleştirilmiş serilerini `Transformator`'un `ema()` metodu ile alabilirsiniz. __EMA__ verilen zaman penceresi için son gözlemlere daha fazla ağırlık verir ve bu nedenle zamandaki aşırı son değer sapmalarına duyarlı bir süreç olarak görülebilir. Bu, rejim kaymaları veya yapısal değişiklikleri SMA'dan daha erken tespit etmeye yardımcı olabilir.

`ema()` metodunun imzası:

```python
def ema(
        series: pd.DataFrame,
        window: Optional[float]= None,
        alpha: Optional[float] = None,
        precision: Optional[int] = None,
        keep_originals: bool = True,
        rename: bool = True
) -> pd.DataFrame:
```

1. `series`: Zaman serilerinden oluşan bir DataFrame.
2. `window`: Ortalama alma için pencere (veya span), sabit dönem olarak.
3. `alpha`: Doğrudan verilen düzleştirme faktörü. (0, +1) aralığında olmalıdır.

__Örnekler__:

```python
usdtry_ema5 = transformator.ema(usdtry, window=5)        # ema(5) verir
usdtry_ema5 = transformator.ema(usdtry, alpha=0.333)     # bu da ema(5) verir çünkü alpha = 2 / (1 + n)
```


<a id="detect-rollvar"></a>

### __Kayan Varyans: ROLVAR<sub>t</sub>(n) = σ<sup>2</sup>(y<sub>t</sub>, y<sub>t-1</sub> ... y<sub>t-n</sub>)__

Sabit bir zaman diliminde (pencere) _Kayan Varyanslar_, serilerdeki rejim veya yapısal değişikliklerin iyi bir göstergesi olabilir. `rolling_var()` metodu ile kayan varyansları alabilirsiniz.

```python
def rolling_var(
                series: pd.DataFrame,
                window: int,
                precision: Optional[int] = None,
                keep_originals: bool = True,
                rename: bool = True
) -> pd.DataFrame:
```

__Örnekler__:

```python
# 10 günlük dönem için kayan varyansları verir.
usdtry_rolvar_10 = transformator.rolling_var(usdtry, window=10)
```


<a id="detect-rollcorr"></a>

### __Kayan Korelasyon: ROLCORR<sub>t</sub>(n) = ρ(y<sub>t</sub>, y<sub>t-1</sub> ... y<sub>t-n</sub>)__

Bir zaman diliminde (pencere) _Kayan Korelasyonlar_, serilerdeki kararsız veya sahte ilişkilerin iyi bir göstergesi olabilir. Kayan korelasyonlar özellikle verilen serilerdeki uzun dönemli doğrusal ilişkilerden sapmaları gözlemlemek için faydalıdır. `rolling_corr()` metodu ile kayan korelasyonları alabilirsiniz.

```python
def rolling_corr(
                 series: pd.DataFrame,
                 window: int,
                 precision: Optional[int] = None,
                 keep_originals: bool = True,
                 rename: bool = True
) -> pd.DataFrame:
```

__Örnekler__:

```python
kurlar = connector.get_series("usdtry, eurtry",
                             start_date="01.06.2022",
                             end_date="30.06.2022",
                             frequency="B")

# 10 günlük dönem için usdtry ve eurtry arasındaki kayan korelasyonları verir.
kurlar_rolcorr_10 = transformator.rolling_corr(kurlar, window=10)
```


<a id="get-cusum"></a>

### __Kümülatif Toplam: Cusum<sub>t</sub> = 𝚺(y<sub>t</sub>, y<sub>t-1</sub> ... y<sub>t-n</sub>)__

Serilerin kümülatif toplamlarını almak için `cusum()` metodunu kullanabilirsiniz.


<a id="get-z-score"></a>

### __Z-Skoru: Z<sub>t</sub> = (y<sub>t</sub> - ȳ) / σ<sub>y</sub>__

_Z-Skoru_, bir ham skorun ortalamadan ne kadar uzakta olduğunu standart sapma birimleri cinsinden tanımlar. Z-Skoru, normal dağılıma sahip y:~N(μ, σ) bir seri için beklenen değerlerden sapmaları tespit etmek için iyi bir ölçüdür. Seriler normal dağılıma sahip olmasa bile büyük örneklem varsayımı altında `+3`'ten büyük veya `-3`'ten küçük z-skorları gözlemlemek, ilgili değerin şüpheli bir aykırı değer olduğunun iyi bir göstergesi olabilir.

```python
def z_score(
            series: pd.DataFrame,
            precision: Optional[int] = None,
            keep_originals: bool = True,
            rename: bool = True
) -> pd.DataFrame:
```

__Örnekler__:

```python
usdtry_z = transformator.z_score(usdtry, precision=2)
```


<a id="get-mad"></a>

### __Medyan Mutlak Sapma: median(|y<sub>t</sub> - median(y<sub>t</sub>)|)__

_Medyan Mutlak Sapma_ (__MAD__), bir medyan skorun medyandan ne kadar uzakta olduğunu mutlak olarak tanımlar. Aykırı değerlere sahip serilerin değişkenliğini tanımlamak için çok faydalıdır. MAD, normal olmayan popülasyonlardan çekilen veriler için bile sağlam bir istatistiktir ve sapmaları ölçmek için z-skoru yerine kullanılabilir.

```python
def mad(
        series: pd.DataFrame,
        precision: Optional[int] = None,
        keep_originals: bool = True,
        rename: bool = True
) -> pd.DataFrame:
```

__Örnekler__:

```python
usdtry_mad = transformator.mad(usdtry, precision=2)
```


<a id="get-normalized"></a>

### __Normalize Edilmiş Seriler: y<sub>t, normal</sub> = F(y<sub>t</sub>)__

Verilen serilerin normalize edilmiş halini makine öğrenimi algoritmaları gibi diğer süreçlere girdi olarak kullanmak için `normalize()` metodunu kullanabilirsiniz.

6 normalizasyon yöntemi tanımlanmıştır:

|Yöntem        | Tanım                                                   | Aralık        |
|:-------------|:--------------------------------------------------------|:--------------|
|`simple`      |  x / (max(x) + 1)                                       | [0, +1)       |
| `min - max`  | (x - min(x)) / (max(x) - min(x))                        | (0, 1]        |
| `mean`       | (x - x̄) / (max(x) + 1)                                  | [-1, +1)      |
| `median`     | (x - median(x)) / (max(x) + 1)                          | [-1, +1)      |
| `mad`        | (x - median(x)) / (median(\|(x - median(x)\|)) * 1.4826 | (-inf, +inf)  |
| `z`          | (x- x̄) / σ<sub>x</sub>                                  | (-inf, +inf)  |

```python
def normalize(
              series: pd.DataFrame,
              method: str = "mad",
              precision: Optional[int] = None,
              keep_originals: bool = True,
              rename: bool = True
) -> pd.DataFrame:
```

__Örnekler__:

```python
usdtry_normalize = transformator.normalize(usdtry, method="z")
```


<a id="get-dummies"></a>

### __Kukla Değişken Serileri: D<sub>n</sub>__

Verilen koşullara uygun kukla seriler oluşturmak için `dummy()` metodunu kullanabilirsiniz. Kukla seriler, yapısal/rejim değişikliklerini veya kırılmaları ve aykırı değerleri modellemek için çok faydalıdır.

```python
def dummy(
            series: pd.DataFrame,
            condition: str,
            threshold: Union[float, str, int, Sequence[Union[float, str, int]]],
            fill_true: float = 1,
            fill_false: float = 0,
            precision: Optional[int] = None,
            keep_originals: bool = True,
            rename: bool = True
) -> pd.DataFrame:
```

Koşullar:

| koşul   | açıklama                                                                                      |
|:-------:|-----------------------------------------------------------------------------------------------|
| `>`     | eşik değerden büyük                                                                           |
| `>=`    | eşik değerden büyük veya eşit                                                                 |
| `<`     | eşik değerden küçük                                                                            |
| `<=`    | eşik değerden küçük veya eşit                                                                  |
| `()`    | alt sınırdan büyük ve üst sınırdan küçük (kapalı sınırlar)                                    |
| `[]`    | alt sınıra eşit veya büyük ve üst sınıra eşit veya küçük (açık sınırlar)                     |

__Örnekler__:

```python
# usdtry'de bir değer 9'dan büyükse 1, aksi halde 0 olan kukla seri
usdtry_gt9 = transformator.dummy(usdtry, ">", 9)

# kapalı sınırlar: 8 < x < 10
usdtry_g8_l10 = transformator.dummy(usdtry, "()", "8, 10")

# açık sınırlar: 8 <= x <= 10
usdtry_g8_l10 = transformator.dummy(usdtry, "[]", "8, 10")
```


<a id="get-laggeds"></a>

### __Gecikmeli Seriler: y<sub>t-1</sub>, y<sub>t-2</sub> ... y<sub>t-n</sub>__

Verilen serilerin gecikmeli serilerini almak için `laggeds()` metodunu kullanabilirsiniz.

```python
def laggeds(
            series: pd.DataFrame,
            range_lags: Optional[int] = None,
            lags: Optional[Union[int, Sequence, str]] = None,
            precision: Optional[int] = None,
            keep_originals=True
) -> pd.DataFrame:
```

1. `range_lags`: Aralık olarak gecikmeleri gösteren bir tam sayı. Varsayılan: `None`
2. `lags`: Gecikmeler.
    - verilen `n` sadece n. gecikmeyi ifade eder. Örneğin; `5`: y<sub>t-5</sub>
    - `(3, 6, 9, 12)` veya `[3, 6, 9, 12]` gibi bir `Sequence` içinde verilebilir
    - `"3, 4"` gibi virgülle ayrılmış metin olarak verilebilir

__Örnekler__:

```python
# sadece usdtry(t-2) verir
usdtry_l2 = transformator.laggeds(usdtry, lags=2)

# usdtry(t-1), usdtry(t-3) ve usdtry(t-5) verir
usdtry_135 = transformator.laggeds(usdtry, lags="1, 3, 5")

# usdtry(t-1), usdtry(t-2), usdtry(t-3) verir
usdtry_3 = transformator.laggeds(usdtry, range_lags=3)

# usdtry(t-1), usdtry(t-2), usdtry(t-6), usdtry(t-12) verir
usdtry_12612 = transformator.laggeds(usdtry, range_lags=2, lags="6, 12")
```


<a id="get-corr"></a>

### __Korelasyon Katsayıları: ρ(y<sub>t</sub>, x<sub>t</sub>)__

Verilen seriler arasındaki korelasyon katsayılarını almak için `corr()` metodunu kullanabilirsiniz. Bu, düşünülen modeldeki olası çoklu doğrusal bağlantı (multicollinearity) sorununu tespit etmek için özellikle önemlidir. `Pearson Doğrusal`, `Kendall Tau` ve `Spearman Sıralama` korelasyon katsayılarını alabilirsiniz.

```python
def corr(
         series: pd.DataFrame,
         method: str = "pearson",
         precision: Optional[int] = None,
         rename: bool = True
) -> pd.DataFrame:
```

__Örnekler__:

```python
seriler = connector.get_series("usdtry, eurtry",
                              start_date="01.01.2021",
                              end_date="31.12.2021",
                              frequency="M")

# Pearson doğrusal korelasyon katsayısını verir
korelasyonlar = transformator.corr(seriler)

# Spearman sıralama korelasyon katsayılarını verir
korelasyonlar_sp = transformator.corr(seriler, method='spearman')
```


<a id="get-auto-corr"></a>

### __Otokorelasyon Katsayıları: AUTOCORR<sub>t</sub> = ρ<sub>t, t-n</sub>__

Orijinal seriler ile verilen gecikmeleri arasındaki otokorelasyonları almak için `autocorr()` metodunu kullanabilirsiniz. Otokorelasyonlar, verilen serilerin durağanlık durumu hakkında çok hızlı bir fikir sağlayabilir. Seri ile gecikmeleri arasındaki anlamlı korelasyonlar (`ρ > 0.6` veya `ρ < -0.6`), gözlemlerin zamandaki önceki değerlerine yüksek oranda bağımlı olduğunu ve dolayısıyla serinin ortalamasının zamana bağlı olarak değiştiğini (olası bir stokastik trend işareti) gösterebilir.

```python
def autocorr(
            series: pd.DataFrame,
            range_lags: Optional[int] = None,
            lags: Optional[Union[int, Sequence, str]] = None,
            method: str = 'pearson',
            column: Optional[Union[str, int]] = None,
            precision: Optional[int] = None
) -> pd.DataFrame:
```

__Örnekler__:

```python
# usdtry ile usdtry(t-1), usdtry(t-2), usdtry(t-3) arasındaki otokorelasyonları verir
otokorelasyonlar = transformator.autocorr(usdtry, range_lags=3)

# usdtry ile usdtry(t-1), usdtry(t-3), usdtry(t-5) arasındaki otokorelasyonları verir
otokorelasyonlar = transformator.autocorr(usdtry, lags="1, 3, 5")

# çok boyutlu serilerde column parametresi ile belirli bir seriyi seçebilirsiniz
kurlar = connector.get_series("usdtry, eurtry",
                              start_date="01.01.2020",
                              end_date="01.01.2022",
                              frequency="Q")

eurtry_otokorr = transformator.autocorr(kurlar, column='EURTRY', range_lags=4, precision=4)
```


<a id="get-serial-corr"></a>

### __Seri Korelasyon Katsayıları: SERIALCORR<sub>t</sub> = ρ<sub>t, x-n</sub>__

Sabit ile diğerleri arasındaki korelasyon vektörünü almak için `serial_corr()` metodunu kullanabilirsiniz. Vektör, sabit bir seri ile gecikmeleri dahil diğerleri arasındaki doğrusal ilişkiler hakkında çok hızlı bir fikir sağlayabilir.

```python
def serial_corr(
                series: pd.DataFrame,
                hold: Union[str, int],
                range_lags: Optional[int] = None,
                lags: Optional[Union[int, Sequence, str]] = None,
                method: str = 'pearson',
                precision: Optional[int] = None
) -> pd.DataFrame:
```

__Örnekler__:

```python
seriler = connector.get_series("usdtry, eurtry",
                              start_date="01.01.2014",
                              end_date="31.12.2021",
                              frequency="M")

# usdtry'yi sabit tutarak korelasyon vektörünü verir
sk_vektor = transformator.serial_corr(seriler, hold="usdtry", range_lags=4, lags=12)
```


<a id="get-outliers"></a>

### __Aykırı Değerler__

Verilen serilerde tespit edilen aykırı değerler için kukla seriler oluşturmak üzere `outliers()` metodunu kullanabilirsiniz.

```python
def outliers(
            series: pd.DataFrame,
            method: str = 'mad',
            critical_upper: float = 3.0,
            critical_lower: float = -3.0,
            precision: Optional[int] = None,
            keep_originals: bool = True,
            rename: bool = True
) -> pd.DataFrame:
```

1. `method`: Aykırı değer tespit yöntemi. Varsayılan: `mad`.
    - `mad`: aykırı değerler _medyan mutlak sapma_ kullanılarak tespit edilir. Normal dağılıma sahip olmayan seriler için tercih edilen yöntemdir.
    - `z`: aykırı değerler __standart normal dağılımdan__ sapmalara göre tespit edilir. Normal dağılıma sahip seriler için tercih edilebilir.
2. `critical_upper`: Sapmalar için üst kritik değer. Varsayılan: `3.0`
3. `critical_lower`: Sapmalar için alt kritik değer. Varsayılan: `-3.0`

Döndürülen kukla seriler `0` ve `1`'lerden oluşur:
- `1`: ilgili tarihte bir aykırı değer tespit edildi.
- `0`: değer beklentiler dahilinde.

__Örnekler__:

```python
# mad ve -3, +3 kritik değer sınırlarına göre tespit edilen aykırı değerleri verir.
usdtry_outliers = transformator.outliers(usdtry)

# z-skoru ve -3, +3 kritik değer sınırlarına göre tespit edilen aykırı değerleri verir.
usdtry_outliers = transformator.outliers(usdtry, method="z")
```


<a id="get-smoothed"></a>

### __Düzleştirilmiş Seriler__

Verilen aykırı değer tespit kriterlerine göre aykırı değerlere karşı düzleştirilmiş seriler almak için `smooth()` metodunu kullanabilirsiniz. Aykırı değerleri düzleştirerek çıkarmak ve düzleştirilmiş serileri orijinallerin yerine kullanmak, kesin tahmin yerine değişkenler arasındaki genel davranışları modellemek için iyi bir yoldur.

```python
def smooth(
           series: pd.DataFrame,
           method: str = 'mad',
           critical_upper: float = 3.0,
           critical_lower: float = -3.0,
           smooth_method: str = 'ema',
           smooth_window: int = 2,
           precision: Optional[int] = None,
           keep_originals: bool = True,
           rename: bool = True
) -> pd.DataFrame:
```

1. `method`: Aykırı değer tespit yöntemi. Varsayılan: `mad`.
2. `critical_upper`: Sapmalar için üst kritik değer. Varsayılan: `3.0`
3. `critical_lower`: Sapmalar için alt kritik değer. Varsayılan: `-3.0`
4. `smooth_method`: Tespit edilen aykırı değerleri düzleştirmek için kullanılacak yöntem. Varsayılan: `ema`
    - `sma` veya `ema` kullanılabilir
5. `smooth_window`: e(ma) penceresi (düzleştirme için kaç değer kullanılacağı) Varsayılan: `2`

Döndürülen seriler:
- Düzleştirilmiş Değerler: Tespit edilen aykırı değerler için.
- Orijinal Gözlemler: Sınırlar dahilindeki değerler için.

__Örnekler__:

```python
seriler = connector.get_series("usdtry, eurtry",
                              start_date="01.01.2014",
                              end_date="31.12.2021",
                              frequency="M")

# mad sınırlarına (-3.0, +3.0) göre tespit edilen aykırı değerlerin sma(seri, 5) ile düzleştirildiği serileri verir
duzlestirilmis_mad = transformator.smooth(seriler, smooth_method='sma', smooth_window=5)

# z-skoru sınırlarına (-1.96, +1.96) göre tespit edilen aykırı değerlerin ema(seri, 2) ile düzleştirildiği serileri verir
duzlestirilmis_z = transformator.smooth(seriler, method="z", critical_upper=1.96, critical_lower=-1.96)
```


<a id="joining-methods"></a>

## __Connector ve Transformator Metotlarını Birleştirme__

İsterseniz hem `Connector` hem de `Transformator` sınıf metotlarını zincirleyebilirsiniz.

__Örnekler__:

```python

connector = Connector()          # API Anahtarınızı zaten diske kaydettiğinizi varsayarak.
transformator = Transformator()

# aşağıdaki örnekler referans isimleri zaten kaydettiğinizi varsayar:
# usdtry -> 'TP.DK.USD.A.YTL'
# eurtry -> 'TP.DK.EUR.A.YTL'


# düzleştirilmiş usdtry ve eurtry verir
duzlestirilmis_kurlar = (
    transformator
    .smooth(
            connector
            .get_series("usdtry, eurtry", start_date="01.01.2014", end_date="31.12.2021", frequency="M")
    )
)

# Bu da düzleştirilmiş usdtry ve eurtry verir
duzlestirilmis_kurlar = transformator.smooth(
    connector.get_series("usdtry, eurtry", start_date="01.01.2014", end_date="31.12.2021", frequency="M")
)

# z_skoru sınırlarına (-1.96, +1.96) göre düzleştirilmiş usdtry ve eurtry verir,
# ancak 'keep_originals' bayrağı False olduğundan orijinal seriler döndürülen veride yer almaz
duzlestirilmis_kurlar = (
    transformator
    .smooth(
            series=connector.get_series("usdtry, eurtry", start_date="01.01.2014", end_date="31.12.2021", frequency="M"),
            method="z", critical_lower=-1.96, critical_upper=1.96, keep_originals=False
    )
)

# sma(usdtry, 3), sma(eurtry, 3) ve 2 kukla seri verir
kurlar_sma_3_kukla = (
    transformator
     .dummy(
        transformator
         .sma(
            connector
                .get_series("usdtry, eurtry", start_date="01.01.2014", end_date="31.12.2021", frequency="M")
         , window=3, keep_originals=False)
     , condition="()", threshold=(10, 12)
     )
)

```

<a id="defined-exceptions-1"></a>

## __Tanımlı İstisnalar (Exceptions)__

Aşağıda tanımlı özel istisnaları ve fırlatılma koşullarını bulabilirsiniz.

|İstisna                               | Açıklama
|--------------------------------------|--------------------------------------------------------------------------------|
|`AmbiguousFunctionMappingException` |Dönüşüm ve toplama fonksiyonları aynı anda uygulandığında fırlatılır              |
|`AmbiguousFunctionParameterException`|Bir fonksiyon belirsiz parametre seti aldığında fırlatılır                        |
|`AmbiguousOutputTypeException` |Ham ve sözlük türleri aynı anda istendiğinde fırlatılır                            |
|`APIServiceConnectionException` |API anahtarı, API Sunucusu, API İsteği ve ağ tabanlı istisnalar oluştuğunda fırlatılır|
|`GroupNotFoundException` |Bir alt kategori grubu bulunamadığında fırlatılır                                    |
|`InsufficientSampleSizeException` |Bir işlem sağlanandan daha büyük örneklem boyutuna ihtiyaç duyduğunda fırlatılır |
|`OptionalPackageRequiredException` |Gerekli opsiyonel bir paket ortamda bulunamadığında fırlatılır                    |
|`SeriesNotFoundException` |Bir seri bulunamadığında fırlatılır                                                 |
|`SubCategoryNotFoundException` |Bir alt kategori bulunamadığında fırlatılır                                       |
|`UndefinedAggregationFunctionException` |Tanımsız bir toplama fonksiyonu parametre olarak verildiğinde fırlatılır      |
|`UndefinedFrequencyException` |Verilen veya API'den dönen zaman serisi frekansı tanımlanamadığında fırlatılır     |
|`UndefinedTransformationFunctionException` |Tanımsız bir dönüşüm fonksiyonu parametre olarak verildiğinde fırlatılır |
|`UnknownTimeSeriesIdentifierException` |Verilen seri adı API sunucusunda bulunamadığında fırlatılır                |
|`UnmatchingFieldSizeException` |Verilen seri adı sayısı API'den dönen seri sayısından farklı olduğunda fırlatılır |
|`UnmatchingParameterSizeException` |Verilen parametre boyutları birbiriyle eşleşmediğinde fırlatılır              |
|`WrongAPIKeyException` |Kullanılan EVDS API Anahtarı yanlış olduğunda fırlatılır                            |
|`WrongDateFormatException` |Verilen tarih formatı tanımlanamadığında fırlatılır                              |
|`WrongDateRangeException` |Verilen tarih aralık dışında olduğunda fırlatılır                                 |
