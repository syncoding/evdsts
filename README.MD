<p align="center">
  <img src="https://github.com/syncoding/evdsts/blob/master/docs/images/evdsts.png?raw=true" width="120"/>
</p>

<h1 align="center">evdsts</h1>

<p align="center">
  <strong>TCMB EVDS makroekonomik zaman serisi araç takımı</strong>
</p>

<p align="center">
  <a href="https://pypi.org/project/evdsts/"><img src="https://badge.fury.io/py/evdsts.svg" alt="PyPI version"></a>
  <a href="https://pypistats.org/packages/evdsts"><img src="https://img.shields.io/pypi/dm/evdsts" alt="Downloads"></a>
  <a href="https://pypi.org/project/evdsts/"><img src="https://img.shields.io/pypi/pyversions/evdsts" alt="Python Version"></a>
  <a href="https://pypi.org/project/evdsts/"><img src="https://img.shields.io/pypi/status/evdsts" alt="Status"></a>
  <a href="https://github.com/syncoding/evdsts/blob/master/LICENSE.txt"><img src="https://img.shields.io/github/license/syncoding/evdsts" alt="License"></a>
  <a href="https://github.com/syncoding/evdsts/issues"><img src="https://img.shields.io/github/issues-raw/syncoding/evdsts" alt="Issues"></a>
  <a href="https://github.com/syncoding/evdsts"><img src="https://img.shields.io/github/languages/top/syncoding/evdsts" alt="Top Language"></a>
  <a href="https://github.com/syncoding/evdsts"><img src="https://img.shields.io/github/forks/syncoding/evdsts?style=social" alt="Forks"></a>
</p>

<p align="center">
  <a href="/README_EN.md"><strong>Click here to access the English version of this document</strong></a>
</p>

---

## Amac

`evdsts` **Turkiye Cumhuriyet Merkez Bankasi** **Elektronik Veri Dagitim Sistemi** **(EVDS)** API
uzerinden makroekonomik veri alimi icin gelistirilmis bir Python uyarlamasidir. `evdsts`, verdigi
zaman serileri analizine hazir ciktilar ve diger faydali donusumleriyle; hem veri alimini hem de
zaman serileri analizlerini kolaylastirmak icin dizayn edilmistir.

## Genel Bakis

`evdsts` genel olarak **EVDS**'den alinan veriden, zaman serileri analizlerine hazir veri setleri
hazirlamak icin dizayn edilmistir. `evdsts`, gelismis ozellikleri ve veri uzerinde size verdigi
kontrol sayesinde hem veri alimini kolaylastirir hem de veri alinir alinmaz uzerinde calismaya
baslamanizi saglar.

`evdsts` iki onemli siniftan olusmaktadir:

| Sinif | Sorumluluk |
|:------|:-----------|
| **Connector** | EVDS'ye baglanti, veri indirme, isimlendirme vb. islemler. |
| **Transformator** | z-skor, kukla degisken, aykiri deger tespiti, fark alma gibi entegre donusumler. |

### Temel Ozellikler

- **Yerinde arama** -- Python'dan cikmadan anahtar kelimelerle seri arayabilirsiniz; sonuclar anlik ve lokaldir.
- **Analize hazir ciktilar** -- donen her deger uygun sayisal veya datetime turudur, asla ham string degildir.
- **Otomatik zaman serisi endeksleme** -- cekilen veriler otomatik olarak gercek pandas DatetimeIndex serilerine donusturulur (secimli).
- **Referans isimler** -- karmasik EVDS kodlarina `usdtry` veya `tufe` gibi akilda kalici takma adlar atayin; takma adlar kalici ve projeler arasi tasinabilirdir.
- **Okunabilir parametreler** -- gizemli API kodlari yerine `daily`, `quarterly`, `percent`, `diff`, `max` gibi anlamli argümanlar kullanin.
- **On dogrulama** -- bircok parametre hatasi herhangi bir ag istegi yapilmadan once yakalanir.
- **Genisletilmis donusumler** -- API tarafindan desteklenmeyen log-getiri, yuksek dereceli farklar ve diger islemler.
- **Esnek cikti** -- sonuclari `DataFrame`, `JSON` veya `dict` olarak alin; CSV, JSON veya XLSX olarak diske yazin.
- **CLI destegi** -- komut satirindan `evdsts build-index` ile lokal arama indekslerini güncelleyin.
- **Tam anotasyon** -- IDE otomatik tamamlama ve hizli yardim icin her yerde type hinting ve tum fonksiyonlar icin docstringler eklenmistir.

## Hizli Baslangic

```python
from evdsts import Connector

connector = Connector("API_ANAHTARINIZ", language="TR")

# seri arama
connector.where("tuketici fiyat endeksi")

# veri cekme
tufe = connector.get_series("TP.FE.OKTG01", start_date="01.01.2020")

# coklu seri cekme
kurlar = connector.get_series(
    "TP.DK.USD.A.YTL, TP.DK.EUR.A.YTL",
    start_date="01.01.2023",
    frequency="M",
    transformations="percent",
)
```

## CLI Kullanimi

```bash
# arama indeksini yeniden olustur
evdsts build-index -y

# tum secenekleri gor
evdsts build-index --help
```

## Dokumanlar

`evdsts`'yi nasil kullanacaginizi ve EVDS'ye baglanti icin gereken API anahtarini nasil alacaginizi
detayli olarak ogrenmek icin:

| | |
|:--|:--|
| Turkce | [**KULLANICI EL KITABI (TR)**](https://github.com/syncoding/evdsts/blob/master/docs/manuals/manual_tr.md) |
| English | [**THE USER MANUAL (EN)**](https://github.com/syncoding/evdsts/blob/master/docs/manuals/manual_en.md) |

## Ornekler [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/syncoding/evdsts/blob/master/examples/ornekler.ipynb)

Ana kullanim senaryolarini iceren [**Jupyter Notebook Uygulamasi**](https://github.com/syncoding/evdsts/blob/master/examples/)'ni indirin ya da yukaridaki *Open in Colab* linkini kullanarak uygulamayi **Google Colab** uzerinde acin.

## Kurulum

`evdsts`'nin stabil surumu GitHub, PyPI ve conda-forge uzerinde bulunur.

```bash
# PyPI
pip install evdsts

# GitHub
pip install git+https://github.com/syncoding/evdsts.git

# Conda
conda install evdsts -c conda-forge
```

## Bagimliliklar

| Paket | Surum |
|:------|:------|
| Python | >= 3.11 |
| pandas | >= 3.0.0 |
| requests | >= 2.32.5 |
| tqdm | >= 4.67.3 |

> Alinan verileri MS Excel formatinda diske kaydetmeyi dusunuyorsaniz [openpyxl](https://pypi.org/project/openpyxl/) ek olarak gereklidir.

## Baglantilar

| | |
|:--|:--|
| Kaynak Kod | [GitHub](https://github.com/syncoding/evdsts/blob/master/evdsts) |
| Degisiklik Gunlugu | [CHANGELOG.md](https://github.com/syncoding/evdsts/blob/master/CHANGELOG.md) |
| Lisans | [MIT](https://github.com/syncoding/evdsts/blob/master/LICENSE.txt) |

## Iletisim

<a href="mailto:synertic@gmail.com?"><img src="https://img.shields.io/badge/gmail-%23DD0031.svg?&style=for-the-badge&logo=gmail&logoColor=white"/></a>

[Telegram](https://t.me/synertic)
