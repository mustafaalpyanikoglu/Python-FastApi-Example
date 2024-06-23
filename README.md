# FastAPI

<img src="https://www.simplilearn.com/ice9/free_resources_article_thumb/FastAPI_b.jpg" width="1000" height="553" alt="">

## 1.1. FastAPI Nedir?

- FastAPI, web uygulamaları ve API'ler geliştirmek için kullanılan Python’a ait bir web framework'üdür.
- Express.js gibi minimal ve esnek bir yapıya sahiptir.

## 1.2. Projeye Başlangıç

- Projeyi oluşturduğumuzda üç ana dosya ile karşılaşırız:
    - `.venv / .env`: Python projeleri için sanal ortam klasörü.
    - `main.py`: Projenin başlangıç dosyası.
    - `text_main.http`: Endpoint'leri test etmek için kullanılır.

## 1.3. Projeyi Çalıştırma

- Terminal'de Uvicorn komutunu kullanarak projeyi çalıştırabiliriz:
    ```powershell
    python -m uvicorn main:app --reload
    ```
    - `main`: Python dosyasının adı.
    - `app`: FastAPI uygulamasını tanımlayan değişken.
    - `--reload`: Otomatik yeniden yükleme özelliği.

## 1.4. Path Parameters

- Path parameters, URL içinde dinamik veriler almak için kullanılır.

## 1.5. Query Parameters

- Query parameters, URL'de belirli parametreler ile veri almayı sağlar. 
- Parametreler varsayılan değerler alabilir.

## 1.6. Request Body

- Request body, API'ye gönderilen verinin JSON formatında alınmasını sağlar.
- Pydantic modelleri kullanarak veri doğrulaması yapılabilir.

## 1.7. Body - Multiple Parameters

- Birden fazla parametre, JSON gövdesinde organize edilebilir.
- `embed=True` kullanılarak JSON içinde belirli bir anahtar altında toplanabilir.

## 1.8. Body - Nested Models

- İç içe geçmiş modeller ile kompleks veri yapıları oluşturulabilir.
- `set` kullanımı ile benzersiz elemanlardan oluşan veri listeleri oluşturulabilir.

## 1.9. UUID

- Benzersiz öğeler için tanımlayıcı olarak UUID kullanılır.
- UUID, veritabanında kayıtlı öğeleri benzersiz şekilde tanımlamak için kullanılır.

## 1.10. Response Model

- Response model, API'den dönen veriyi doğrulamak ve belirli bir formatta dönmesini sağlamak için kullanılır.
- `response_model_exclude_unset` gibi parametreler ile sadece belirli alanlar döndürülebilir.

## 1.11. Request Files

- FastAPI, dosya yükleme ve işleme işlemleri için `UploadFile` ve `File` sınıflarını sağlar.
- Küçük dosyalar için `File`, büyük ve meta veriye ihtiyaç duyulan dosyalar için `UploadFile` kullanılır.

## 1.12. Exception Handler

- Özel exception sınıfları oluşturulabilir ve bu exceptionlar loglanabilir.
- Exception handler kullanılarak özel hata mesajları döndürülebilir.

## 1.13. Path Operation Configuration

- Endpoint'leri organize etmek ve açıklama eklemek için `tags` kullanılabilir.
- `deprecated` parametresi ile kullanım dışı bırakılacak endpoint'ler işaretlenebilir.

## 1.14. Dependencies

- `Depends` kullanılarak bağımlılıklar belirlenebilir ve yeniden kullanılabilir fonksiyonlar oluşturulabilir.
- Bağımlılıklar fonksiyonlar veya sınıflar ile tanımlanabilir.

## 1.15. Routers

- `APIRouter` kullanılarak endpoint'ler modüler hale getirilebilir ve kod karmaşıklığı azaltılabilir.
- Farklı dosyalara bölerek kod düzeni sağlanabilir.

## 1.16. BackgroundTasks

- BackgroundTasks kullanarak bazı işlemler arka planda yürütülebilir.
- Mail veya SMS gönderme işlemleri gibi uzun sürecek işlemler arka planda çalıştırılabilir.

# Ek Kaynaklar

- FastAPI'nin daha derinlemesine öğrenmek için [bu YouTube oynatma listesi](https://www.youtube.com/playlist?list=PLqAmigZvYxIL9dnYeZEhMoHcoP4zop8-p)'ne göz atabilirsiniz.
