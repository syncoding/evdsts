# <img src="https://github.com/syncoding/evdsts/blob/master/docs/images/evdsts.png?raw=true" width="5%"/> evdsts

 [![PyPI version](https://badge.fury.io/py/evdsts.svg)](https://pypi.org/project/evdsts/)
 [![PyPI - Downloads](https://img.shields.io/pypi/dm/evdsts)](https://pypistats.org/packages/evdsts)
 [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/evdsts)](https://pypi.org/project/evdsts/)
 [![PyPI - Status](https://img.shields.io/pypi/status/evdsts)](https://pypi.org/project/evdsts/)
 [![GitHub - License](https://img.shields.io/github/license/syncoding/evdsts)](https://github.com/syncoding/evdsts/blob/master/LICENSE)
 [![GitHub issues](https://img.shields.io/github/issues-raw/syncoding/evdsts)](https://github.com/syncoding/evdsts/issues)
 [![GitHub top language](https://img.shields.io/github/languages/top/syncoding/evdsts)](https://github.com/syncoding/evdsts)
 [![GitHub Fork](https://img.shields.io/github/forks/syncoding/evdsts?style=social)](https://img.shields.io/github/forks/syncoding/evdsts?style=social)


### [__Click here to access the English version of this document__](/README_EN.md)
## __Amaç__

`evdsts` __Türkiye Cumhuriyet Merkez Bankası__ __Elektronik Veri Dağıtım Sistemi__ __(EVDS) API
üzerinden makroekonomik veri alımı için geliştirilmiş bir Python uyarlamasıdır. `evdsts`, verdiği
zaman serileri analizine hazır çıktılar ve diğer faydalı dönüşümleriyle; hem veri alımını hem de
zaman serileri anzlizlerini kolaylaştırmak için dizayn edilmiştir.

## __Tanıtım__

`evdsts` genel olarak __EVDS__'den alınan veriden, zaman serileri analizlerine hazır veri setleri
hazırlamak için dizayn edilmiştir. `evdsts`, gelişmiş özellikleri ve veri üzerinde size verdiği
kontrol sayesinde hem veri alımını kolaylaştırır hem de veri alınır alınmaz üzerinde çalışmaya
başlamanızı sağlar.

`evdsts` iki önemli sınıftan oluşmuştur:
1. `Connector`: EVDS'ye bağlantı, veri indirme, isimlendirme gibi süreçleri üstlenir.
2. `Transformator`: `Connector` tarafından alınan veri ile tam uyumlu çalışır ve zaman serileri
analizinde size veri hakkında ön fikirler verebilecek bazı yararlı dönüşümleri yapar.

`evdsts`'nin bazı önemli özellikleri aşağıda verilmiştir:

- `evdsts` ile alınan veri üzerinde; z-skor serisi hesaplama, kukla değişken serileri oluşturma,
dışa düşen verilerin tespiti, fark serileri oluşturma gibi bazı dönüşümleri veri alınır alınmaz
kolayca yapılabilir. Bu dönüşümlerden sorumlu olan`Transformator` sınıfı, `Connector` sınıfı
tarafından oluşturulan veri ile tam uyumlu olarak çalışması için dizayn edilmiştir.
- İndirmek istediğiniz serilerin isimlerini aramak için EVDS web sitesini ziyaret etmenize gerek
kalmadan `evdsts` içinde anahtar kelimeler ile seri tanımlarını arayabilirsiniz. Aramalar lokal
olarak (disk üzerinde) yapılır ve anında sonuç verir.
- `evdsts` geri döndürdüğü verinin başka hiçbir dönüşüme gerek kalmadan matematiksel süreçlerde
kullanılabilir olmasını sağlar. Bu, aslında bir `datetime`, `float` ya da `int` gibi  matematiksel
bir veri türünü ifade hiçbir verinin bir `string` veri olarak geri dönmemesini garanti eder.
- Alınan tüm veri otomatik olarak gerçek zaman serilerine dönüştürülür (seçimli, kapatılabilir)
- Servisten veri almak için EVDS'nin karmaşık seri etiketlerinin bilinmesine gerek yoktur. `evdsts`
size  _tüfe_, _faiz_, _gsmh_ ve _usdtry_ gibi anlamlı isimlerin seri isimleri olarak atama özgürlüğü
verir ve bu atanan isimler EVDS'den veri almak için kullanılır. Kullanıcı tarafından atanan isimler
referans isimler olarak adlandırılır ve silinmedikleri ya da değiştirilmedikleri sürece kalıcıdırlar.
Ek olarak, mevcut bir projedeki referans isimler kolayca başka bir projeye taşınabilir.
- Bütün transformasyon ve yığılma fonksiyonları ve frekansla parametreleri `daily`, `quarterly`,
`percent`, `diff`, `max`, vs. gibi anlamlı parametrelere dönüştürülmüştür. Böylece artık EVDS'nin
transformasyon ve yığılma fonksiyonları ve zaman serileri frekansları için atadığı karmaşık parametre
haritasını bilmeye gerek yoktur.
- `evdsts`, EVDS'ye bağlantı yapılmadan önce bir çok hatayı tespit edebilir ve sizi uyarabilir. Bu,
niçin verilen parametrelere veri alınamayacağını ya da verilen parametrelerin niçin belirsizlik
yarattığını bilmenize olanak tanır.
- `evdsts`, veri üzerinde log-return serileri ya da 2., 3., n. seviye fark serileri gibi API
tarafından desteklenmeyen fakat zaman seri analizlerinde sıklıkla kullanılan dönüşümleri yapabilmenizi
sağlar.
- Alınan tüm veriler `DataFrame`, `JSON` ya da `dict` sınıfları olarak isteğe bağlı biçimde geri
döndürülebilir.
- Alınan tüm veriler daha sonra kullanılmak üzere saklanmak ya da; R, EViews, SAS ya da RATS gibi
diger analiz uygulamarında kullanılmak üzere `JSON`, `CSV` ve `XLS` formatında diske yazılabilir.
- Tüm fonksiyon ve sınıf metotlarının anotasyonu yapılmıştır. Bu sayede;  Spyder IDE, Pycharm,
VS Code ya da Jupyter üzerinde kullanmak istediğiniz herhangi bir fonksiyon hakkında anlık yardım
alabilirsiniz.
- Geliştiricilerin kaynak kod üzerinde çalışmasını kolaylaştırmak için kaynak kod içinde tüm değişken
tiplerinin anotasyonu (gerekli yorumlarla birlikte) yapılmıştır.

## __Dökümanlar__

`evdsts`'yi nasıl kullanacağınızı ve EVDS'ye bağlantı için gereken API anahtarını nasıl alacağınızı
detaylı olarak öğrenmek için:  
[__KULLANICI EL KITABI (TR)__](https://github.com/syncoding/evdsts/blob/master/docs/manuals/manual_tr.md) ya da
[__THE USER MANUAL (EN)__](https://github.com/syncoding/evdsts/blob/master/docs/manuals/manual_en.md)
dökümanlarına göz atın.

## __Örnekler__ [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/syncoding/evdsts/blob/master/examples/ornekler.ipynb)

Ana kullanım senaryolarını içeren [__Jupyter Notebook Uygulaması__](https://github.com/syncoding/evdsts/blob/master/examples/)'nı indirin ya da yukarıdaki _Open in Colab_ linkini kullanarak uygulamayı __Google Colab__ üzerinde açın.


## __Gereklilikler__

`evdsts` bir __Python 3__ projesidir ve aşağıda sıralananlar gereklidir:

1. cpython >= 3.6.15 (ya da eşdeğer PyPy sürümü)
1. pandas >= 0.25.3
2. requests >= 2.12.5

## __Ek Gereklilikler__

Alınan verileri MS Excel formatında diske kaydetmeyi düşünüyorsanız [__openpyxl__](https://pypi.org/project/openpyxl/)
paketi gereklidir. Eğer MS Excel dosyaları ile çalışmayı düşünmüyorsanız openpyxl bağımlılığı yoktur.

## __Kurulum__

`evdsts`'nin stabil sürümü GitHub, PyPI ve conda-forge üzerinde bulunur ve aşağıdaki yollardan
herhangi biri kullanılarak kurulum gerçekleştirilebilir.

### __PyPI__

```
pip install evdsts
```

### __GitHub__

```
pip install git+https://github.com/syncoding/evdsts.git
```

### __Conda__

```
conda install evdsts -c conda-forge
```

## __Kaynak Kod__

[GitHub](https://github.com/syncoding/evdsts/evdsts)

## __Versiyon Değişiklik Günlüğü__
[__Changelog__](https://github.com/syncoding/evdsts/blob/master/CHANGELOG.md)

## __Lisans__

[__MIT__](https://github.com/syncoding/evdsts/blob/master/LICENSE.txt)

## __İletişim__

<a href="mailto:synertic@gmail.com?"><img src="https://img.shields.io/badge/gmail-%23DD0031.svg?&style=for-the-badge&logo=gmail&logoColor=white"/></a>

[Telegram](https://t.me/synertic)

