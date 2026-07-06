---
name: Aniyomi/Mihon extension scaffolding requirements
description: Required abstract overrides and structure when generating a new Aniyomi animeextension module (this repo is a Kotlin/Aniyomi extensions monorepo)
---

Any class implementing `ConfigurableAnimeSource, ParsedAnimeHttpSource()` in this repo must override, even as stubs, all of: `videoFromElement`, `videoUrlParse` (both typically `throw UnsupportedOperationException()` when `videoListParse` is overridden directly), and `setupPreferenceScreen`. Missing any of these causes a Kotlin compile failure, but a `./gradlew :help` "dry run" will NOT catch it — only an actual `compileDebugKotlin` (or `assembleDebug`) run does.

**Why:** These are abstract members of `ParsedAnimeHttpSource`/`ConfigurableAnimeSource` that have no default implementation, confirmed by cross-checking multiple existing extensions in `src/ar/*` which all include these three overrides even when unused.

**How to apply:** When scaffolding/generating a brand-new extension module (e.g. via automation or a new GitHub Actions workflow), always include these overrides, and validate any generated module by actually compiling it (`./gradlew -p src :<lang>:<id>:compileDebugKotlin` with `CI=true`), not just configuring the project.

No local Python or Node runtime is available in this repl's shell (it's a pure Kotlin/Gradle/Android project) — scripts invoked from GitHub Actions (which run on `ubuntu-latest` with Python preinstalled) can't be smoke-tested locally; rely on careful manual review instead.
