import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

RAW_NAME = os.environ["EXT_NAME"].strip()
RAW_ID = os.environ.get("EXT_ID", "").strip()
BASE_URL = os.environ["EXT_BASE_URL"].strip()
LANG = os.environ.get("EXT_LANG", "ar").strip() or "ar"
CATEGORY = os.environ.get("EXT_CATEGORY", "anime").strip() or "anime"
NSFW = os.environ.get("EXT_NSFW", "false").strip().lower() == "true"


def slugify(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "", value)
    return value.lower()


def class_name_from(value: str) -> str:
    words = re.findall(r"[a-zA-Z0-9]+", value)
    if not words:
        raise SystemExit("Extension name must contain at least one letter or digit")
    return "".join(w[:1].upper() + w[1:] for w in words)


if not RAW_NAME:
    raise SystemExit("Extension name is required")
if not BASE_URL.startswith("http://") and not BASE_URL.startswith("https://"):
    raise SystemExit("Base URL must start with http:// or https://")

ext_id = slugify(RAW_ID) if RAW_ID else slugify(RAW_NAME)
if not ext_id:
    raise SystemExit("Could not derive a valid extension id from the provided name")

class_name = class_name_from(RAW_NAME)

ext_dir = ROOT / "src" / LANG / ext_id
if ext_dir.exists():
    raise SystemExit(f"Extension folder already exists: {ext_dir.relative_to(ROOT)}")

pkg_path = f"eu/kanade/tachiyomi/animeextension/{LANG}/{ext_id}"
src_dir = ext_dir / "src" / pkg_path
src_dir.mkdir(parents=True)

res_dir = ext_dir / "res"
core_res = ROOT / "core" / "res"
for mipmap in core_res.iterdir():
    if not mipmap.is_dir():
        continue
    dest = res_dir / mipmap.name
    dest.mkdir(parents=True, exist_ok=True)
    for icon in mipmap.iterdir():
        shutil.copy(icon, dest / icon.name)

build_gradle = f"""ext {{
    extName = '{RAW_NAME}'
    extClass = '.{class_name}'
    extVersionCode = 1
}}

apply from: "$rootDir/common.gradle"
"""
(ext_dir / "build.gradle").write_text(build_gradle, encoding="utf-8")

nsfw_comment = "true" if NSFW else "false"

kotlin_source = f"""package eu.kanade.tachiyomi.animeextension.{LANG}.{ext_id}

import android.app.Application
import android.content.SharedPreferences
import androidx.preference.ListPreference
import androidx.preference.PreferenceScreen
import eu.kanade.tachiyomi.animesource.ConfigurableAnimeSource
import eu.kanade.tachiyomi.animesource.model.AnimeFilterList
import eu.kanade.tachiyomi.animesource.model.SAnime
import eu.kanade.tachiyomi.animesource.model.SEpisode
import eu.kanade.tachiyomi.animesource.model.Video
import eu.kanade.tachiyomi.animesource.online.ParsedAnimeHttpSource
import eu.kanade.tachiyomi.network.GET
import okhttp3.Request
import okhttp3.Response
import org.jsoup.nodes.Document
import org.jsoup.nodes.Element
import uy.kohesive.injekt.Injekt
import uy.kohesive.injekt.api.get

// NSFW flag for this source: {nsfw_comment}. Update AndroidManifest metadata via build.gradle if this changes.
class {class_name} : ConfigurableAnimeSource, ParsedAnimeHttpSource() {{

    override val name = "{RAW_NAME}"

    override val baseUrl = "{BASE_URL}"

    override val lang = "{LANG}"

    override val supportsLatest = true

    private val preferences: SharedPreferences by lazy {{
        Injekt.get<Application>().getSharedPreferences("source_$id", 0x0000)
    }}

    // ============================== Popular ===============================
    // TODO: عدّل المحدد (selector) ليطابق بنية صفحة الأعمال الشائعة في الموقع.
    override fun popularAnimeSelector(): String = "TODO"

    override fun popularAnimeRequest(page: Int): Request = GET(baseUrl)

    override fun popularAnimeFromElement(element: Element): SAnime {{
        return SAnime.create().apply {{
            // TODO: استخرج الرابط والعنوان والصورة المصغرة من العنصر.
            val ahref = element.selectFirst("a")!!
            setUrlWithoutDomain(ahref.attr("href"))
            title = ahref.text()
            thumbnail_url = element.selectFirst("img")?.attr("src")
        }}
    }}

    override fun popularAnimeNextPageSelector(): String? = null

    // ============================== Episodes ==============================
    // TODO: عدّل المحدد ليطابق قائمة الحلقات في صفحة العمل.
    override fun episodeListSelector(): String = "TODO"

    override fun episodeFromElement(element: Element): SEpisode {{
        return SEpisode.create().apply {{
            // TODO: استخرج رابط الحلقة ورقمها واسمها.
            setUrlWithoutDomain(element.attr("href"))
            name = element.text()
            episode_number = 1F
        }}
    }}

    // ============================ Video Links =============================
    // TODO: عدّل المحدد ليطابق قائمة روابط المشاهدة/التحميل.
    override fun videoListSelector(): String = "TODO"

    override fun videoListParse(response: Response): List<Video> = videosFromElement(response.asJsoup())

    private fun videosFromElement(document: Document): List<Video> {{
        // TODO: استخرج روابط الفيديو الفعلية من كل عنصر، وأضف مستخرِج الخادم المناسب إن لزم.
        return emptyList()
    }}

    override fun videoFromElement(element: Element): Video = throw UnsupportedOperationException()

    override fun videoUrlParse(document: Document): String = throw UnsupportedOperationException()

    // =============================== Search ================================
    // TODO: عدّل المحدد وطريقة بناء رابط البحث.
    override fun searchAnimeSelector(): String = popularAnimeSelector()

    override fun searchAnimeRequest(page: Int, query: String, filters: AnimeFilterList): Request =
        GET("$baseUrl/?s=$query")

    override fun searchAnimeFromElement(element: Element): SAnime = popularAnimeFromElement(element)

    override fun searchAnimeNextPageSelector(): String? = null

    // =============================== Latest =================================
    override fun latestUpdatesSelector(): String = popularAnimeSelector()

    override fun latestUpdatesRequest(page: Int): Request = GET(baseUrl)

    override fun latestUpdatesFromElement(element: Element): SAnime = popularAnimeFromElement(element)

    override fun latestUpdatesNextPageSelector(): String? = null

    // =============================== Details ================================
    override fun animeDetailsParse(document: Document): SAnime = SAnime.create().apply {{
        // TODO: استخرج تفاصيل العمل (الوصف، التصنيفات، الحالة) إن لزم.
        title = document.selectFirst("h1")?.text() ?: name
    }}

    // ============================== Settings ==============================
    override fun setupPreferenceScreen(screen: PreferenceScreen) {{
        // TODO: أضف تفضيلات الإضافة (جودة الفيديو، النطاق البديل، إلخ) إن لزم.
        val videoQualityPref = ListPreference(screen.context).apply {{
            key = PREF_QUALITY_KEY
            title = "الجودة المفضلة"
            entries = PREF_QUALITY_ENTRIES
            entryValues = PREF_QUALITY_ENTRIES
            setDefaultValue(PREF_QUALITY_DEFAULT)
            summary = "%s"

            setOnPreferenceChangeListener {{ _, newValue ->
                val selected = newValue as String
                val index = findIndexOfValue(selected)
                val entry = entryValues[index] as String
                preferences.edit().putString(key, entry).commit()
            }}
        }}
        screen.addPreference(videoQualityPref)
    }}

    // ============================= Utilities ==============================
    override fun List<Video>.sort(): List<Video> {{
        val quality = preferences.getString(PREF_QUALITY_KEY, PREF_QUALITY_DEFAULT)!!
        return sortedWith(compareBy {{ it.quality.contains(quality) }}).reversed()
    }}

    companion object {{
        private const val PREF_QUALITY_KEY = "preferred_quality"
        private const val PREF_QUALITY_DEFAULT = "720p"
        private val PREF_QUALITY_ENTRIES = arrayOf("1080p", "720p", "480p", "360p")
    }}
}}
"""
(src_dir / f"{class_name}.kt").write_text(kotlin_source, encoding="utf-8")

sources_md = ROOT / "SOURCES.md"
if sources_md.exists():
    lines = sources_md.read_text(encoding="utf-8").splitlines()
    category_ar = "أنمي" if CATEGORY == "anime" else "أفلام ومسلسلات"
    new_row = f"| {RAW_NAME} | {category_ar} | `{BASE_URL.split('://', 1)[-1].split('/', 1)[0]}` | 1 |"
    insert_at = None
    for i, line in enumerate(lines):
        if line.startswith("|---"):
            insert_at = i + 1
            break
    if insert_at is not None:
        lines.insert(insert_at, new_row)
        sources_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

print(f"EXT_ID={ext_id}")
print(f"CLASS_NAME={class_name}")
print(f"EXT_DIR={ext_dir.relative_to(ROOT)}")

github_output = os.environ.get("GITHUB_OUTPUT")
if github_output:
    with open(github_output, "a", encoding="utf-8") as f:
        f.write(f"ext_id={ext_id}\n")
        f.write(f"class_name={class_name}\n")
        f.write(f"ext_dir={ext_dir.relative_to(ROOT)}\n")
