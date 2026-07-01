# تفاوت Dockerfile معمولی (Single-Stage) و Multi-Stage Build

## مقدمه

در Docker برای ساخت Image معمولاً از فایل **Dockerfile** استفاده می‌شود. به طور کلی دو روش برای ساخت Image وجود دارد:

- Single-Stage Build (پیاده‌سازی معمولی)
- Multi-Stage Build (پیاده‌سازی چندمرحله‌ای)

هر کدام کاربردها، مزایا و معایب خاص خود را دارند.

---

# Single-Stage Build

در این روش تمام مراحل پروژه مانند نصب وابستگی‌ها، کامپایل برنامه و اجرای آن در یک مرحله انجام می‌شود. بنابراین تمام فایل‌های موقت، ابزارهای Build و سورس کد داخل Image نهایی باقی می‌مانند.

### مزایا

- ساده و قابل فهم
- مناسب برای پروژه‌های کوچک
- پیاده‌سازی سریع

### معایب

- حجم Image زیاد است.
- ابزارهای Build در Image نهایی باقی می‌مانند.
- امنیت کمتر نسبت به Multi-Stage
- زمان انتقال و Deploy بیشتر است.

### نمونه

```dockerfile
FROM node:22

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

CMD ["npm", "start"]
```

---

# Multi-Stage Build

در این روش Dockerfile به چند مرحله تقسیم می‌شود. در مرحله اول برنامه Build می‌شود و در مرحله آخر فقط فایل‌های موردنیاز برای اجرا به Image نهایی منتقل می‌شوند.

به این ترتیب ابزارهای Build، سورس کد و فایل‌های موقت وارد Image نهایی نمی‌شوند.

### مزایا

- حجم بسیار کمتر Image
- امنیت بیشتر
- حذف فایل‌های غیرضروری
- سرعت بیشتر در Deploy
- مناسب برای محیط Production

### معایب

- Dockerfile کمی پیچیده‌تر است.
- برای پروژه‌های کوچک ممکن است تفاوت محسوسی ایجاد نکند.

### نمونه

```dockerfile
# مرحله Build
FROM node:22 AS builder

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

# مرحله نهایی
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
```

---

# مقایسه

| ویژگی | Single-Stage | Multi-Stage |
|--------|-------------|------------|
| تعداد مراحل | یک مرحله | چند مرحله |
| حجم Image | زیاد | کم |
| ابزارهای Build در Image | وجود دارد | حذف می‌شوند |
| امنیت | کمتر | بیشتر |
| سرعت Deploy | کمتر | بیشتر |
| مناسب Production | خیر | بله |
| سادگی | بیشتر | کمتر |

---

# نتیجه‌گیری

اگر هدف فقط یادگیری یا ساخت یک پروژه کوچک باشد، استفاده از **Single-Stage Build** کافی است. اما در پروژه‌های واقعی و محیط‌های Production، **Multi-Stage Build** بهترین انتخاب محسوب می‌شود؛ زیرا باعث کاهش حجم Image، افزایش امنیت، حذف فایل‌های غیرضروری و بهبود سرعت استقرار (Deployment) می‌شود. به همین دلیل امروزه اکثر پروژه‌های حرفه‌ای از Multi-Stage Build استفاده می‌کنند.