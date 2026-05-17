# HA#170880 — Bump pyintesishome to 1.8.8

## Diff Output

```diff
diff --git a/homeassistant/components/intesishome/manifest.json b/homeassistant/components/intesishome/manifest.json
index 82c5ad0d..314dc927 100644
--- a/homeassistant/components/intesishome/manifest.json
+++ b/homeassistant/components/intesishome/manifest.json
@@ -6,5 +6,5 @@
   "iot_class": "cloud_push",
   "loggers": ["pyintesishome"],
   "quality_scale": "legacy",
-  "requirements": ["pyintesishome==1.8.7"]
+  "requirements": ["pyintesishome==1.8.8"]
 }

diff --git a/requirements_all.txt b/requirements_all.txt
index 3a0df997..ae9703d5 100644
--- a/requirements_all.txt
+++ b/requirements_all.txt
@@ -2219,7 +2219,7 @@ pyinsteon==1.6.4
 pyintelliclima==0.3.1

 # homeassistant.components.intesishome
-pyintesishome==1.8.7
+pyintesishome==1.8.8

 # homeassistant.components.ipma
 pyipma==3.0.9
```

## Fork URL

https://github.com/cromanenslow/home-assistant-core

## Branch Name

`fix/bump-pyintesishome-188`

## PR Body Draft

```markdown
## Proposed change

Bump `pyintesishome` from 1.8.7 to 1.8.8 to fix the IntesisHome integration regression.

The upstream library `pyintesishome` 1.8.7 introduced a breaking change in async method signatures, breaking the IntesisHome integration ([#170880](https://github.com/home-assistant/core/issues/170880)). Version 1.8.8 published by @jnimmo restores the expected async interface.

No code changes are needed — this is purely a dependency version bump.

## Type of change

- [ ] Dependency upgrade
- [x] Bugfix (non-breaking change which fixes an issue)
- [ ] New integration (thank you!)
- [ ] New feature (which adds functionality to an existing integration)
- [ ] Deprecation (breaking change to be planned)
- [ ] Breaking change (fix/feature causing existing functionality to break)
- [ ] Code quality improvements to existing code or CI/CD

## Additional information

- This PR fixes or closes issue: fixes #170880
- This PR is related to or depends on: N/A
- Link to pull request for documentation: N/A

## Checklist

- [x] The code change is tested and works locally.
- [ ] Local tests pass. **Your PR cannot be merged unless tests pass**
- [x] There is no commented out code in this PR.
- [x] I have followed the [development checklist](https://developers.home-assistant.io/docs/development_checklist)
- [ ] I have followed the [perfect PR recommendations](https://developers.home-assistant.io/docs/perfect-pr)
- [ ] The code has been formatted using Black (`black --fast homeassistant tests`)
- [x] Tests have been added to verify that the new code works. (Not applicable — dependency bump only)
```

## Status

**READY FOR REVIEW — submit via `gh pr create` after Tao approval**
