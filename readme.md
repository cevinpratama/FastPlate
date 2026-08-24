# 🚘 License Plate Detection & OCR API

API berbasis **Python dan FastAPI** untuk melakukan **deteksi plat nomor kendaraan dan Optical Character Recognition (OCR)** secara otomatis.

Project ini menggabungkan model **YOLO** yang telah dilatih menggunakan sekitar **12.000 gambar** untuk mendeteksi lokasi plat nomor, kemudian menggunakan **PaddleOCR** untuk membaca dan mengenali karakter yang terdapat pada plat tersebut.

> 🚧 **Project Status: Under Development**
>
> Project ini bersifat **open public** dan masih dalam tahap pengembangan. Arsitektur, model, preprocessing, serta sistem OCR masih akan terus dikembangkan untuk meningkatkan akurasi dan reliability sebelum digunakan dalam skala production maupun komersial.

---

## 🎯 Visi

Membangun sebuah **API deteksi plat nomor kendaraan yang cepat, akurat, mudah digunakan, dan siap diintegrasikan** ke berbagai sistem seperti:

* Sistem parkir otomatis
* Gerbang tol
* Sistem keamanan
* Monitoring kendaraan
* Smart city
* Automatic Number Plate Recognition (ANPR)
* Sistem manajemen kendaraan
* Aplikasi pencatatan kendaraan

Dalam jangka panjang, project ini ditujukan untuk berkembang menjadi sebuah **layanan ANPR yang reliable dan production-ready**, dengan tingkat akurasi yang tinggi serta dapat digunakan oleh developer maupun perusahaan.

---

## 🚀 Misi

Project ini dikembangkan dengan beberapa misi utama:

1. **Membangun API ANPR yang mudah digunakan**

   Menyediakan endpoint yang sederhana sehingga developer dapat mengintegrasikan deteksi plat nomor ke dalam aplikasi mereka.

2. **Meningkatkan akurasi deteksi plat**

   Mengembangkan dan melakukan fine-tuning terhadap model YOLO agar mampu mendeteksi plat nomor dalam berbagai kondisi.

3. **Meningkatkan kemampuan OCR**

   Mengoptimalkan preprocessing gambar dan PaddleOCR agar karakter pada plat dapat dibaca dengan lebih akurat.

4. **Membangun sistem yang scalable**

   Mengembangkan API menggunakan FastAPI sehingga nantinya dapat digunakan untuk kebutuhan dengan traffic dan workload yang lebih besar.

5. **Open Development**

   Membuka project ini kepada publik sehingga developer lain dapat mencoba, memberikan feedback, menemukan bug, dan ikut berkontribusi.

6. **Menuju Production & Commercial Ready**

   Setelah model dan pipeline mencapai tingkat akurasi serta reliability yang memadai, project akan dikembangkan lebih lanjut agar dapat digunakan untuk kebutuhan production dan berpotensi dipasarkan sebagai layanan komersial.

---

# 🧠 Cara Kerja

Pipeline utama project ini adalah:

```text
                Input Image
                     │
                     ▼
              ┌─────────────┐
              │   FastAPI   │
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │    YOLO     │
              │   Detection │
              └──────┬──────┘
                     │
               License Plate
                  Bounding Box
                     │
                     ▼
              ┌─────────────┐
              │   Cropping  │
              │    Image    │
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │ Preprocess  │
              │   Image     │
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │ PaddleOCR   │
              │ OCR Engine  │
              └──────┬──────┘
                     │
                     ▼
              Detected Plate
                  Text
```

Secara sederhana:

**Image → YOLO → Plate Detection → Crop → Image Preprocessing → PaddleOCR → Plate Number**

---

# 🔬 Model

## YOLO

Project ini menggunakan model **YOLO** untuk melakukan object detection terhadap plat nomor kendaraan.

Model telah melalui proses training menggunakan sekitar:

**12.000 gambar**

Dataset tersebut digunakan untuk melatih model agar dapat mengenali lokasi plat nomor pada gambar kendaraan.

Output dari YOLO berupa bounding box:

```json
{
  "x1": 100,
  "y1": 150,
  "x2": 400,
  "y2": 250
}
```

Bounding box tersebut kemudian digunakan untuk melakukan cropping terhadap area plat sebelum diproses oleh OCR.

---

# 🔤 OCR

Setelah plat nomor berhasil dideteksi oleh YOLO, gambar plat diproses menggunakan **PaddleOCR**.

Pipeline preprocessing saat ini meliputi:

1. Convert image menjadi RGB
2. Convert RGB → BGR
3. Upscaling gambar hingga **4x**
4. Interpolation menggunakan `INTER_CUBIC`
5. Penambahan padding putih
6. OCR menggunakan PaddleOCR
7. Penggabungan karakter
8. Filtering karakter non-alphanumeric
9. Conversion menjadi uppercase

Contoh:

```text
Input:
        b 1234 abc

Output:
        B1234ABC
```

---

# ⚡ Technology Stack

| Technology | Purpose                    |
| ---------- | -------------------------- |
| Python     | Programming language       |
| FastAPI    | REST API framework         |
| YOLO       | License plate detection    |
| PaddleOCR  | Character recognition      |
| OpenCV     | Image processing           |
| Pillow     | Image handling             |
| NumPy      | Numerical/image processing |

---

# 📁 Project Architecture

Contoh struktur project yang direkomendasikan:

```text
license-plate-ocr/
│
├── app/
│   ├── main.py
│   ├── models/
│   │   └── yolov11s_fold3.pt
│   │
│   ├── services/
│   │   ├── detector.py
│   │   ├── ocr.py
│   │   └── preprocessing.py
│   │
│   └── utils/
│
├── debug/
│   └── debug_paddle.jpg
│
├── requirements.txt
├── README.md
└── .gitignore
```

> Struktur di atas merupakan struktur yang direkomendasikan. Struktur aktual repository dapat berbeda selama project masih dalam tahap pengembangan.

---

# 🛠️ Installation

Clone repository:

```bash
git clone <repository-url>
cd <repository-folder>
```

Buat virtual environment:

```bash
python -m venv venv
```

Aktifkan environment.

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependency:

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the API

Jalankan FastAPI menggunakan Uvicorn:

```bash
uvicorn main:app --reload
```

Jika aplikasi berada di dalam package `app`:

```bash
uvicorn app.main:app --reload
```

API secara default dapat diakses melalui:

```text
http://127.0.0.1:8000
```

Dokumentasi Swagger tersedia di:

```text
http://127.0.0.1:8000/docs
```

---

# 📡 API Endpoint

## `POST /plat`

Endpoint untuk mendeteksi plat nomor dan melakukan OCR.

### Request

Kirim gambar menggunakan `multipart/form-data`.

Parameter:

```text
file: image
```

Contoh menggunakan cURL:

```bash
curl -X POST "http://127.0.0.1:8000/plat" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@car.jpg"
```

---

## Response

Contoh response:

```json
{
  "Pesan": "Terdeteksi plat dengan jumlah 1",
  "Jumlah": 1,
  "Hasil OCR": [
    {
      "teks_plate": "B1234ABC",
      "confidence_yolo": 0.96,
      "koordinat": {
        "x1": 100,
        "y1": 150,
        "x2": 400,
        "y2": 250
      }
    }
  ]
}
```

### Response Fields

| Field             | Description                              |
| ----------------- | ---------------------------------------- |
| `Pesan`           | Informasi jumlah plat yang terdeteksi    |
| `Jumlah`          | Jumlah bounding box plat yang terdeteksi |
| `Hasil OCR`       | Hasil pemrosesan masing-masing plat      |
| `teks_plate`      | Hasil pembacaan karakter plat            |
| `confidence_yolo` | Confidence dari model YOLO               |
| `koordinat`       | Bounding box plat pada gambar            |

---

# 🧪 Current Development

Saat ini pipeline utama telah berhasil menggabungkan:

```text
FastAPI
   ↓
YOLO
   ↓
License Plate Detection
   ↓
Image Cropping
   ↓
OpenCV Preprocessing
   ↓
PaddleOCR
   ↓
Plate Number
```

Namun project masih berada dalam tahap **research & development**.

Beberapa kondisi seperti:

* gambar blur
* pencahayaan rendah
* glare/reflection
* sudut kamera ekstrem
* plat kotor
* karakter yang terlalu kecil
* resolusi rendah
* kendaraan bergerak
* occlusion
* format plat yang berbeda

masih dapat mempengaruhi hasil deteksi maupun OCR.

---

# 🗺️ Roadmap

## Phase 1 — Initial Prototype

* [x] FastAPI API
* [x] YOLO license plate detection
* [x] Training menggunakan dataset ±12.000 gambar
* [x] License plate cropping
* [x] Image preprocessing
* [x] PaddleOCR integration
* [x] OCR text normalization
* [x] JSON API response

## Phase 2 — Accuracy Improvement

* [ ] Fine-tuning YOLO
* [ ] Optimasi dataset
* [ ] Data augmentation
* [ ] Optimasi image preprocessing
* [ ] Fine-tuning OCR pipeline
* [ ] Character-level post-processing
* [ ] Validasi hasil OCR berdasarkan format plat
* [ ] Benchmark accuracy

## Phase 3 — Production Optimization

* [ ] Docker support
* [ ] Model optimization
* [ ] GPU inference support
* [ ] CPU inference optimization
* [ ] Batch inference
* [ ] Async/background processing
* [ ] Logging
* [ ] Monitoring
* [ ] Automated testing
* [ ] API authentication
* [ ] Rate limiting

## Phase 4 — Commercial Ready

* [ ] Production-grade API
* [ ] Versioned API
* [ ] Deployment infrastructure
* [ ] Scalability improvements
* [ ] SLA & monitoring
* [ ] Usage analytics
* [ ] API key management
* [ ] Documentation untuk developer
* [ ] Commercial API/service

---

# 📊 Future Evaluation

Salah satu fokus utama pengembangan adalah melakukan evaluasi model secara terukur.

Metric yang akan digunakan antara lain:

### Object Detection

* Precision
* Recall
* mAP50
* mAP50-95
* IoU

### OCR

* Character Accuracy
* Exact Match Accuracy
* Character Error Rate
* Plate Recognition Accuracy

Target akhirnya bukan hanya **plat berhasil ditemukan**, tetapi:

> **Plat ditemukan dengan benar → karakter terbaca dengan benar → hasil akhir sesuai dengan plat sebenarnya.**

---

# ⚠️ Disclaimer

Project ini masih dalam tahap pengembangan dan **belum dapat dianggap sebagai sistem ANPR production-ready**.

Hasil deteksi dan OCR dapat berbeda tergantung pada:

* kualitas gambar
* kamera
* kondisi pencahayaan
* sudut pengambilan gambar
* ukuran plat pada gambar
* kondisi fisik plat
* jenis kendaraan
* kondisi lingkungan

Model dan pipeline akan terus dikembangkan untuk meningkatkan akurasi dan robustness.

---

# 🤝 Contributing

Project ini bersifat **open public** dan kontribusi sangat terbuka.

Jika Anda menemukan:

* bug
* hasil OCR yang salah
* kasus gambar yang gagal diproses
* masalah API
* ide optimasi
* improvement model
* improvement preprocessing

silakan membuat **Issue** atau mengirimkan **Pull Request**.

Kontribusi berupa dataset, benchmark, preprocessing technique, model improvement, dan testing juga sangat terbuka.

---

# 🔮 Long-Term Vision

Project ini tidak berhenti pada sekadar membuat endpoint untuk membaca plat nomor.

Tujuan jangka panjangnya adalah membangun sebuah **platform License Plate Recognition / ANPR** yang dapat digunakan oleh berbagai aplikasi dan sistem di dunia nyata.

Pengembangan akan berfokus pada:

```text
Prototype
    ↓
Research
    ↓
Fine-Tuning
    ↓
Accuracy Improvement
    ↓
Benchmark
    ↓
Production API
    ↓
Scalable Infrastructure
    ↓
Commercial ANPR Platform
```

Dengan pengembangan model, dataset, OCR pipeline, dan infrastructure secara berkelanjutan, project ini diharapkan dapat berkembang dari sebuah **open-source research project** menjadi sebuah **reliable license plate recognition service** yang siap digunakan pada skenario dunia nyata.

---

# 📜 License

Tambahkan lisensi sesuai tujuan distribusi project.

Contoh:

```text
MIT License
```

> Pastikan lisensi yang digunakan juga kompatibel dengan lisensi model, dataset, dan dependency pihak ketiga yang digunakan dalam project.

---

## ⭐ Project Status

**🚧 Active Development**

Project ini masih terus dikembangkan.
Feedback, testing, issue report, dan contribution sangat diterima.

Jika project ini bermanfaat, silakan ⭐ repository ini dan ikut berkontribusi dalam pengembangannya.
