# إضافات Aniyomi العربية

مستودع Kotlin/Android جاهز للبناء والنشر يضم **14 إضافة عربية** لـ Aniyomi: أنمي، أفلام، مسلسلات، ودراما آسيوية. لا يحتوي المستودع على APKs مجهولة المصدر؛ كل APK يُبنى من الشفرة الموجودة هنا بواسطة GitHub Actions.

> هذا مشروع مجتمعي غير تابع لـ Aniyomi أو للمواقع المدرجة. توفر المواقع وبنية صفحاتها يتغيران باستمرار، وقد تتوقف إضافة عن العمل رغم نجاح بنائها. استخدم المصادر التي يحق لك الوصول إلى محتواها والتزم بالقوانين وشروط المواقع في بلدك.

## الإضافات

راجع [SOURCES.md](SOURCES.md) للقائمة الكاملة والتصنيف وعناوين المواقع، و[STATUS.md](STATUS.md) لنتيجة فحص الوصول إلى النطاقات، و[BUILD_VERIFICATION.md](BUILD_VERIFICATION.md) لإثبات بناء 14/14 APK. المستودع يضم جميع الإضافات العربية الموجودة في لقطة المصدر المجتمعي المعتمدة بتاريخ 12 مايو 2026؛ عبارة «كل المواقع العربية» لا يمكن ضمانها حرفيًا لأن المواقع تظهر وتختفي وتتغير نطاقاتها باستمرار.

## رفع المشروع إلى GitHub

بعد فك ملف ZIP، أنشئ مستودعًا فارغًا في GitHub ثم نفّذ:

```bash
git init
git add .
git commit -m "Initial Arabic Aniyomi extensions repository"
git branch -M main
git remote add origin https://github.com/USERNAME/REPOSITORY.git
git push -u origin main
```

سيعمل Workflow باسم `CI` تلقائيًا ويجمع كل الإضافات بصيغة Debug للتحقق من سلامة الشفرة.

## إضافة موقع جديد عبر GitHub Actions

يمكنك توليد سقالة (scaffold) لإضافة جديدة مباشرة من GitHub دون الحاجة للكتابة يدويًا:

1. افتح تبويب `Actions` في المستودع على GitHub.
2. اختر workflow باسم **Add extension** من القائمة الجانبية.
3. اضغط `Run workflow` وعبّئ الحقول:
   - **اسم الموقع/الإضافة**: مثل `My Site`.
   - **معرّف مختصر (اختياري)**: بالإنجليزية فقط، يُستخدم لاسم المجلد والحزمة؛ يُشتق تلقائيًا من الاسم إن تُرك فارغًا.
   - **رابط الموقع الأساسي**: يجب أن يبدأ بـ `http://` أو `https://`.
   - **نوع المحتوى**: أنمي أو أفلام/مسلسلات.
   - **رمز اللغة**: `ar` افتراضيًا.
   - **هل الموقع للبالغين؟**
4. شغّل الـ workflow. سيقوم تلقائيًا بـ:
   - إنشاء مجلد إضافة جديد داخل `src/<lang>/<id>/` يحوي `build.gradle` وأيقونة افتراضية وصنف Kotlin مبدئي يمتد من `ParsedAnimeHttpSource`.
   - إضافة صف جديد في [SOURCES.md](SOURCES.md).
   - التأكد من أن الوحدة الجديدة تُصرَّف بنجاح (compile) قبل المتابعة.
   - فتح Pull Request يحتوي التغييرات لمراجعتها ودمجها.
5. الشفرة الناتجة سقالة أولية فقط تحمل تعليقات `TODO` في المحددات (selectors)؛ يجب على مطوّر مراجعتها وإكمال منطق الاستخراج (الأعمال الشائعة، الحلقات، روابط الفيديو، البحث) ليطابق بنية الموقع الفعلية قبل نشرها، مع رفع `extVersionCode` عند كل تعديل لاحق.

## نشر مستودع قابل للإضافة داخل Aniyomi

يلزم توقيع APKs بنفس المفتاح في كل تحديث. أنشئ المفتاح مرة واحدة واحفظ نسخة احتياطية آمنة منه:

```bash
keytool -genkeypair -v -keystore signingkey.jks -alias extensions -keyalg RSA -keysize 4096 -validity 10000
```

أضف أسرار GitHub التالية من `Settings > Secrets and variables > Actions`:

- `SIGNING_KEY`: محتوى `signingkey.jks` مشفرًا Base64 كسطر واحد.
- `ALIAS`: اسم alias، مثل `extensions`.
- `KEY_STORE_PASSWORD`: كلمة مرور ملف المفتاح.
- `KEY_PASSWORD`: كلمة مرور المفتاح.

لإنشاء قيمة `SIGNING_KEY` على PowerShell:

```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("signingkey.jks")) | Set-Clipboard
```

أول مرة فقط، افتح `Actions > Publish extension repository > Run workflow` يدويًا. سيُنشأ فرع `repo` تلقائيًا، ورابط المستودع الذي تضيفه داخل Aniyomi هو:

```text
https://raw.githubusercontent.com/drnopoh2810-spec/anime-repo/repo/index.min.json
```

هذا الرابط **مُفعّل حاليًا ويعمل** (تم تشغيله وتوقيعه بنجاح، ويضم الإضافات الـ14).

### التحديث التلقائي للرابط

workflow **Publish extension repository** يعمل الآن تلقائيًا أيضًا (بدون تدخل يدوي) في كل مرة يصل فيها تعديل إلى مجلد `src/` على فرع `main` — سواء بدمج Pull Request لموقع جديد (من workflow **Add extension**) أو برفع `extVersionCode` لموقع موجود. أي إضافة أو تحديث جديد يُدمج في `main` سيُبنى ويُوقّع تلقائيًا ويُضاف إلى نفس الرابط أعلاه خلال دقائق، دون الحاجة لتشغيل الـ workflow يدويًا في كل مرة. لا يزال بالإمكان تشغيله يدويًا من تبويب Actions عند الحاجة (مثلًا لإعادة التوقيع بعد تغيير الأسرار).

## البناء محليًا

المتطلبات: JDK 17، وAndroid SDK، ومتغير `ANDROID_HOME` صحيح.

```bash
./gradlew -p src assembleDebug
```

على Windows:

```powershell
.\gradlew.bat -p src assembleDebug
```

توجد ملفات APK الناتجة داخل مجلد `build/outputs/apk/` الخاص بكل إضافة.

## الصيانة

- عند تعديل إضافة، ارفع `extVersionCode` في `src/ar/<extension>/build.gradle`.
- لا تغيّر package name أو source ID لإضافة منشورة؛ وإلا ستظهر كتطبيق منفصل.
- لا تضع keystore أو كلمات المرور أو APKs غير الموثوقة في Git.
- افحص النطاقات والمحددات وواجهات API دوريًا؛ نجاح Gradle لا يضمن أن الموقع ما زال يعمل.

## الترخيص والنسب

الشفرة مرخصة وفق Apache License 2.0. راجع [LICENSE](LICENSE) و[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
