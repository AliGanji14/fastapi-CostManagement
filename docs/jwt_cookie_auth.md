
## نکات امنیتی

- `HttpOnly` باعث می شود JavaScript مرورگر نتواند مقدار توکن را بخواند؛ این موضوع خطر دزدیده شدن توکن در حملات XSS را کمتر می کند.
- `Secure` باعث می شود cookie فقط روی HTTPS ارسال شود. برای تست محلی می توان `COOKIE_SECURE=False` گذاشت، اما در محیط واقعی بهتر است `True` باشد.
- `SameSite=Lax` کمک می کند cookie در بسیاری از درخواست های cross-site ارسال نشود و خطر CSRF کمتر شود.
- اگر پروژه در آینده frontend جداگانه داشت و درخواست های cross-site لازم شد، بهتر است علاوه بر SameSite از CSRF token هم استفاده شود.
- مقدار `JWT_SECRET_KEY` باید طولانی و محرمانه باشد و در کد واقعی نباید داخل گیت قرار بگیرد.

## مدیریت خطاهای توکن

- اگر access token وجود نداشته باشد، endpoint های هزینه خطای `401` برمی گردانند.
- اگر access token منقضی یا نامعتبر باشد، کاربر باید `POST /users/refresh-token` را صدا بزند.
- اگر refresh token معتبر باشد، سیستم بدون ورود دوباره access token و refresh token جدید داخل cookie قرار می دهد.
- اگر refresh token هم منقضی یا نامعتبر باشد، کاربر باید دوباره login کند.
- در logout هر دو cookie پاک می شوند تا نشست کاربر تمام شود.

## مزیت cookie نسبت به Authorization header

وقتی توکن در `Authorization` header نگهداری شود، معمولا frontend باید آن را در جایی مثل `localStorage` ذخیره کند. اگر سایت XSS داشته باشد، JavaScript مخرب می تواند به `localStorage` دسترسی پیدا کند. اما cookie با `HttpOnly` توسط JavaScript خوانده نمی شود.

البته cookie به تنهایی جلوی CSRF را کامل نمی گیرد، چون مرورگر cookie را خودکار همراه درخواست می فرستد. برای همین از `SameSite=Lax` استفاده شده و در پروژه های واقعی بهتر است CSRF token هم اضافه شود.


