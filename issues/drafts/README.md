# Drafts for publishing (nothing has been published)

Local repo: `..\..\miminet` (clone of mimi-net/miminet, remote `upstream`, no push done).
Each branch = one PR, based on upstream main `24c36f3`; all 9 branches merge together cleanly
(checked: merged into a temp branch → ruff clean, 86 browser-free tests pass, all live checks pass).

| Order | Branch | Draft | Closes |
|---|---|---|---|
| 1 | `fix/524-preview-white-background-front` | [pr-524.md](pr-524.md) | #524 |
| 2 | `fix/404-declare-port-variable-front` | [pr-404.md](pr-404.md) | #404 |
| 3 | `fix/506-stop-printing-jwt-tokens-front` | [pr-506-tokens.md](pr-506-tokens.md) | refs #506 |
| 4 | `fix/542-keep-admin-author-front` | [pr-542.md](pr-542.md) | #542 |
| 5 | `fix/543-hide-heavy-section-fields-front` | [pr-543.md](pr-543.md) | #543 |
| 6 | `fix/412-db-connection-resilience-front` | [pr-411-412.md](pr-411-412.md) | #411, #412 |
| 7 | `fix/531-set-russian-document-lang-front` | [pr-531.md](pr-531.md) | refs #531 |
| 8 | `refactor/506-print-to-logging` | [pr-506-logging.md](pr-506-logging.md) | #506 |
| 9 | `fix/539-yandex-avatar-and-example-network-front` | [pr-539.md](pr-539.md) | #539 |
| — | (no code yet) | [issue-535-comment.md](issue-535-comment.md) | #535: comment first |

Each draft's first line holds the branch and PR title.

## When you decide to publish (your account, your call)
```bash
gh repo fork mimi-net/miminet --clone=false          # once
cd miminet
git remote add origin https://github.com/<you>/miminet.git
git push -u origin fix/524-preview-white-background-front
gh pr create -R mimi-net/miminet --base main --head <you>:fix/524-preview-white-background-front \
  --title "fix(front): render network preview on white background (#524)" --body-file ../issues/drafts/pr-524.md
```
Before opening a PR it is polite to comment in the issue that you are taking it.
Drafts are in Russian like most PRs in the repo; remove the first `<!-- ... -->` line or keep it (it is an HTML comment and won't render).

## New findings without an issue (open issues first if you want to fix them)
- Default avatar `empty.jpg` → `<img src="/avatar/empty.jpg">` → 404 on production (users without an avatar likely see a broken image).
- Yandex sign-up: `email=""` vs unique `User.email` → IntegrityError for a second user without email; no linking by email (VK does it).
- ~30 implicit globals in front JS + latent `const edges` vs Ctrl+Z (`RestoreNetworkObject`).
