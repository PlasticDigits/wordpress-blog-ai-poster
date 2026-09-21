# ADR 0001: Remove catch-all CODEOWNERS

## Status

Proposed ([#3](https://git.cl8y.com/code/wordpress-blog-ai-poster/issues/3)).
Not accepted by this design-author pass. Do not call this tip accepted until
independent review says so. Keywords in the issue body are not architecture
approval. Ordinary design is not a founder card.

If this SHA (or a later vehicle-retarget successor) is independently
accepted, **keep `Status: Proposed` on `main`**. Acceptance lives in that
review comment (it names the SHA). A Status-only successor that flips this
line to Accepted is **allowed** but **not required** for land. Implementers
must not guess: copy the two `docs/` files byte-identical to the named SHA,
including this Proposed line, unless review accepted a Status-only SHA
instead.

Tracker `#3` is the closed occupying PR (issues URL and pull share one
number). Remaining S0+S2 work needs a **new iid**. See architecture
[Land vehicle](../architecture.md#land-vehicle) — that paragraph is the
single occupancy/successor rule.

Copy onto the successor tip with a **path-limited** checkout of the two
docs files from **the independently accepted SHA**. `cac-design-issue-3` is
never the merge vehicle. Land criterion for docs: those two files on the
successor tip are byte-identical to that SHA (Proposed status included,
unless a Status-only SHA was accepted).

Overview (merge gate, GET contract, product tree, land vehicle):
[`architecture.md`](../architecture.md). Do not copy that table here. Local
invariant IDs are **H3-*** (this ticket). `code/hello` architecture **H15**
is the canary’s copy of the same flags, not this repo’s issue number.

This ADR does not authorize deploy, spend, custody rotation, WordPress
publish, or Forgejo protection PATCH
([agent-control #297](https://git.cl8y.com/PlasticDigits/cl8y-agent-control/issues/297)).

## Outcome

Delete the catch-all `CODEOWNERS` so this tree no longer supplies the
planting file. **S1 is already on `main`** (merge of
[#3](https://git.cl8y.com/code/wordpress-blog-ai-poster/pulls/3) at
`2a81aac` / `4a77cb8`; four-path `test ! -e` holds). Official plant-stop on
later PRs is leftover-complete (test 4 / S3), not close of `#3` (already
closed) and not merge of the successor. Merge to `main` stays: pull
request, Woodpecker context `ci/woodpecker/pr/woodpecker`, SHA-pinned
`Do: merge`, no direct push, no `force_merge`.

**Remaining land** is **S0+S2 only**: this ADR, `docs/architecture.md`, and
a README pointer, on a new branch from current `origin/main`. Vehicle is a
**new iid + new PR** (architecture **Land vehicle**). Merging that
successor does **not** close `#3`. Design branch `cac-design-issue-3` is
review/transport only; it is **not** merged as a docs-only PR, is **not**
the successor PR, and still carries root `CODEOWNERS`.

This is a product-tree copy of the pattern named by
[cl8y-forgejo#48](https://git.cl8y.com/PlasticDigits/cl8y-forgejo/issues/48).
The canary is `code/hello`
[#15](https://git.cl8y.com/code/hello/issues/15), not this repo. Protection
on `code/wordpress-blog-ai-poster` `main` already matches that ticket
(`block_on_official_review_requests=false` **H3-8**, `required_approvals=0`
**H3-9**, `enable_push=false` **H3-2**). Remaining work does not re-roll
protection, does not implement CAC autoland, and does not publish to
WordPress.

Author-attested live protection (authenticated GET, 2026-09-21,
design-author session) on `main`: `enable_push=false`,
`enable_status_check=true` with `status_check_contexts` equal
`["ci/woodpecker/pr/woodpecker"]`, `required_approvals=0`,
`block_on_official_review_requests=false`, `block_on_rejected_reviews=true`,
`updated_at=2026-09-21T07:29:31Z`. Pin one path:
`GET /api/v1/repos/code/wordpress-blog-ai-poster/branch_protections`
(pick `rule_name == "main"`). Anonymous GET on that path returns 401
(`token is required`). Independent review of this SHA cannot re-verify
those flags without a token. If live flags differ from this attestation,
stop and escalate to forge owners. Do not PATCH protection from this repo.
This ADR does **not** treat the GET as implement write permission. Five-flag
GET is leftover-complete item 1, not a successor land close criterion.

## Context

`ca6a1f7` (2026-09-02) added root `CODEOWNERS`:

```
.* @code/maintainers
```

Forgejo uses Go regular expressions, not GitHub globs. Runtime search
(first existing blob wins) is `CODEOWNERS`, `docs/CODEOWNERS`,
`.gitea/CODEOWNERS`, then `.forgejo/CODEOWNERS`. Gitea’s list is root /
`docs/` / `.gitea/`; Forgejo added `.forgejo/` without dropping `.gitea/`.
User docs often omit `.gitea/`; the runtime list does not. Combined with
historical `block_on_official_review_requests`, every non-WIP PR requested
team **maintainers** (CODEOWNERS line `@code/maintainers`; PR JSON
`requested_reviewers_teams[].name` is `maintainers`, org `code`). That
team’s only member is the usual PR author, so self-approve is 422 and merge
is 405. CAC `RECOMMEND: ACCEPT` is not a Forgejo `APPROVED` review.
[cl8y-agent-control#388](https://git.cl8y.com/PlasticDigits/cl8y-agent-control/issues/388)
skipped the deadlock; it did not remove the file or the protection.
CODEOWNERS is evaluated from the **base** branch of the PR, not the tip.

[#1](https://git.cl8y.com/code/wordpress-blog-ai-poster/pulls/1) proved
Woodpecker can go green under the required context
(`NO_CI_MISSING_WOODPECKER` compileall stub). [cl8y-forgejo ADR
0003](https://git.cl8y.com/PlasticDigits/cl8y-forgejo/src/branch/main/docs/adr/0003-community-forge-and-woodpecker.md)
item 8 (“CODEOWNERS plus protected `main`”) is amended on the forge repo
for the **official-review** half only. This tree’s README is the WordPress
CLI usage guide; `origin/main` still has no merge-gate pointer. The
successor PR must add a pointer at **H3** without rewriting
generation/SEO/publish instructions. The issue body links cl8y-forgejo
`docs/INVARIANTS.md`; that file is not in this tree. Do not invent a local
copy.

S1 is **done**: `4a77cb80a43b34671a43904d8bbb7178f9a891e1` deleted the
six-line file; `2a81aac` merged it via occupying `#3`. Live `GET /pulls/3`
is `merged: true`. `origin/main` has no `CODEOWNERS` and no `docs/`. That
delete-only merge did not land standing docs or the README pointer.

Historical plant proof (disqualified as leftover-complete evidence): while
open, [#3](https://git.cl8y.com/code/wordpress-blog-ai-poster/pulls/3) had
`official: true` `REQUEST_REVIEW` from team `maintainers`;
`requested_reviewers_teams` was that team.
[#2](https://git.cl8y.com/code/wordpress-blog-ai-poster/pulls/2) (Renovate)
still lists the same team. Protection GET on `main` has `updated_at`
2026-09-21T07:29:31Z and official-review **block** off (**H3-8**), so
leftover requests must not be treated as merge blockers.

This branch (`cac-design-issue-3`) is design transport only. It still has
root `CODEOWNERS` (`.* @code/maintainers`). Whole-tree copy of a transport
SHA would re-plant that file onto a tip whose `main` ancestor already
deleted it.

`origin/main` has no `docs/` tree. Relative README links to ADR 0001 /
architecture 404 unless those two files land on the **same merged tip** as
the README pointer. `.gitignore` does not ignore `docs/` (unlike Foundry
`docs/` on `code/BASE_Buster`); do not add `docs/*` exceptions.

No in-repo issue dependencies. Merged
[#1](https://git.cl8y.com/code/wordpress-blog-ai-poster/issues/1) already
put `.woodpecker.yml` on `main`. Closed `#3` is not a remaining-work
dependency. Open
[#2](https://git.cl8y.com/code/wordpress-blog-ai-poster/pulls/2)
(`renovate/configure`) is unrelated.

## Non-goals

- Forgejo protection JSON / `apply_repo_policy.py` / migrate
  `_ensure_codeowners` / templates
  ([cl8y-forgejo#48](https://git.cl8y.com/PlasticDigits/cl8y-forgejo/issues/48)
  / [pulls/50](https://git.cl8y.com/PlasticDigits/cl8y-forgejo/pulls/50)).
- CAC autoland predicates, occupying jobs, or `DrainSkip::OfficialReview`
  cleanup
  ([cl8y-agent-control#429](https://git.cl8y.com/PlasticDigits/cl8y-agent-control/issues/429),
  leftover of #388).
- Dismissing reviewers from the controller (forbidden substitute in #388),
  including leftovers on closed `#3` and open `#2`.
- Path-specific CODEOWNERS, a second maintainer, or `required_approvals: 1`.
- Weakening or expanding Woodpecker (keep the existing `python` /
  `compileall` step; no scanner upgrade; no Alpine `apk add` / `rg`; no
  `scripts/`; no fake commit statuses), adding `force_merge`, enabling
  direct `main`, or adding a required push context on PR tips.
- Coolify, UUID/token changes, WordPress publish, OpenAI/Tavily spend, or
  flipping auto-deploy
  ([agent-control #297](https://git.cl8y.com/PlasticDigits/cl8y-agent-control/issues/297)).
- Renovate config
  ([#2](https://git.cl8y.com/code/wordpress-blog-ai-poster/pulls/2)),
  rewriting `wp_ai_poster.py` / `blog_*.py` / `wp_add_meta.py` /
  `Context_*.md`, or a local `docs/INVARIANTS.md`.
- Editing `autonomy.rs` / HMAC, self-approval, or a founder card for this
  ordinary design.
- Open `cac-design-issue-3` as a PR, merge that transport ref to `main`,
  `git checkout <sha> -- .`, or `git reset --hard` to the design branch.
- Reopen or update closed occupying `#3`; put `Fixes #3` on the successor.
- Copying Foundry `docs/*` `.gitignore` exceptions; this tree does not
  ignore `docs/`.

## Decision

1. **Delete** root `CODEOWNERS`. Do not leave an empty or comments-only file
   (Forgejo still parses it). **Already done on `main`.** The successor must
   not restore it.
2. **Do not add** `docs/CODEOWNERS`, `.gitea/CODEOWNERS`, or
   `.forgejo/CODEOWNERS`. After land, `test ! -e` succeeds on all four
   paths. None of those paths may contain a reviewer rule for any pattern
   (not only `.*`). Same sentence as **H3-1**, test 1, and land close
   (tree).
3. **Keep** the merge gate in [`architecture.md`](../architecture.md)
   **H3**. On the successor PR, keep the WordPress CLI README and insert
   the pointer specified here. Do not claim maintainers review every
   change. Do not expand generation, SEO, or publish instructions.
   Architecture-only is **not** sufficient. Do not merge a README that
   points at those paths until they exist on that tip. The two `docs/`
   files on the successor tip must be byte-identical to the independently
   accepted SHA (see Status).

   **README insertion (S2, implementable):** after the title paragraph
   (`A Python script that uses OpenAI…WordPress.`), before `## Features`,
   insert a short section. Leave Installation / Usage / CLI flags
   untouched. Use hrefs that resolve on the same tip:

   ```markdown
   ## Merge gate

   Merge to `main` is a pull request plus Woodpecker context
   `ci/woodpecker/pr/woodpecker`. CODEOWNERS is not a merge gate. See
   [ADR 0001](docs/adr/0001-remove-catchall-codeowners.md) and
   [architecture — Merge gate (H3)](docs/architecture.md#merge-gate-h3).
   ```

   The architecture heading slug is `#merge-gate-h3`, not `#H3`.
4. **Successor PR (new iid).** Remaining land is S0+S2 only. Vehicle is
   architecture [Land vehicle](../architecture.md#land-vehicle): new branch
   from current `origin/main`; new iid + new PR; diff is ADR 0001 +
   architecture + README pointer. Do not reopen `#3`. `cac-design-issue-3`
   is transport; do not merge it to `main` (it still has root
   `CODEOWNERS`).
5. **Leave** already-planted official requests on open PRs (including
   leftover on closed `#3` and open `#2`). They are non-blocking under
   **H3-8** / **H3-9**. Do not dismiss them from CAC. Human dismiss is
   optional leftover, not AC. They do not count as “no new plant.”
6. **Do not** PATCH branch protection from this repository.

## Component / state / interface changes

| Surface | Change |
| --- | --- |
| `CODEOWNERS` (root) | Already removed on `main` (S1). Successor must not restore it. If a path-limited copy mistake re-adds it, delete it before ready. |
| `docs/CODEOWNERS`, `.gitea/CODEOWNERS`, `.forgejo/CODEOWNERS` | Must remain absent (no empty file). Do not add `.gitea/CODEOWNERS`. |
| `docs/adr/0001-remove-catchall-codeowners.md`, `docs/architecture.md` | Path-limited copy from the independently accepted SHA onto the successor PR (`git checkout <accepted-sha> -- docs/adr/0001-remove-catchall-codeowners.md docs/architecture.md`). Byte-identical. Standing H3 contract lands with the README pointer. |
| Forgejo PR review interface | Planting file is already gone from `main`. Official team requests on **new** non-WIP PRs against `main` are leftover-complete evidence (test 4 / S3), not a successor close gate. `requested_reviewers_teams` from this file is expected empty for those new PRs. Forgejo skips CODEOWNERS on WIP/draft — a draft is not proof. |
| Branch protection API | No write from this ticket. Operator GET must still match architecture **GET-required** (**H3-2**, **H3-3**, **H3-5**, **H3-8**, **H3-9**) for leftover-complete. Observed rows are do-not-touch. In-repo CI cannot perform that GET. Independent review of a design SHA cannot re-GET (401). |
| `.gitignore` | Unchanged (`.env`, `__pycache__`). Do not add `docs/*` exceptions. |
| `.woodpecker.yml` | Unchanged. Keep the existing `python` / `compileall` step. No secrets on `pull_request`. |
| README | Mandatory on the successor PR: insert the **Merge gate** section from decision 3 after the title paragraph. CLI usage stays. Do not rewrite CLI usage. |
| `wp_ai_poster.py` / `blog_*.py` / `wp_add_meta.py` / `Context_*.md` | Unchanged. |
| CAC / Coolify / org team `code/maintainers` | Unchanged. The team may keep existing; it simply is not planted as official review. |

No runtime contract, schema, or HTTP API change.

Forgejo CODEOWNERS lookup is root, `docs/`, `.gitea/`, or `.forgejo/`
(Go-regexp, not GitHub globs). Outcome 1 / **H3-1** is **no file** at those
four paths (already true on `main`).

## Affected invariants

| ID | Kind | Rule |
| --- | --- | --- |
| **H3-1** | Non-GET | None of the four Forgejo search paths exist on `main` (`test ! -e CODEOWNERS`, `test ! -e docs/CODEOWNERS`, `test ! -e .gitea/CODEOWNERS`, `test ! -e .forgejo/CODEOWNERS`). Same sentence as test 1 and land close (tree). File line `@code/maintainers` / JSON team `maintainers` is the leftover plant this absence stops. |
| **H3-2** | GET-required | `enable_push=false` on `main`. |
| **H3-3** | GET-required | `enable_status_check=true` and `status_check_contexts` **equal** `["ci/woodpecker/pr/woodpecker"]`. |
| **H3-4** | Non-GET | Merge is SHA-pinned `Do: merge`. Never document or use `force_merge`. Not a protection field; omit from GET matching. |
| **H3-5** | GET-required | `block_on_rejected_reviews` stays true. An explicit REJECT still blocks. |
| **H3-6** | Non-GET | No Coolify/Woodpecker secrets on `pull_request`. This tree does not grow a deploy step from the successor. WordPress publish and OpenAI/Tavily spend stay #297. |
| **H3-7** | Non-GET | This tree does not expand CAC merge/deploy/spend/custody policy. |
| **H3-8** | GET-required | `block_on_official_review_requests=false`. Leftover official requests on closed #3 / open #2 are non-blocking. |
| **H3-9** | GET-required | `required_approvals=0`. |

GET-observed flags (`block_on_outdated_branch`, `dismiss_stale_approvals`,
`apply_to_admins`) are listed in architecture only. They have no land or
leftover IDs. The successor must not PATCH them.

Do not weaken cl8y-forgejo protection invariants **2–10** and **13** from
product commits. CAC #388 stays: skip official-review deadlock; never
`force_merge`; drain does not delete CODEOWNERS. Product land (S1 already
on `main`) makes the skip class stop firing **for this repo** once new PRs
have no plant.

Python generation behavior is unchanged. There is no local
`docs/invariants.md` / typed product invariant file to rewrite.

## Alternatives

| Option | Why not |
| --- | --- |
| Keep file, rely on `block_on_official_review_requests=false` | Requests still plant on every non-WIP PR; drain noise; Renovate/agent PRs look like they need a human stamp; templates can re-teach the old gate. (File already deleted on `main`; do not restore.) |
| Replace `.*` with path owners | No second reviewer exists; same 405/422 if official-review is ever turned on; out of scope. Outcome 1 forbids the file. |
| Add a second maintainer | Founder ops, not this implement. |
| Dismiss official requests from CAC | Forbidden by #388 as a substitute for policy reversal. |
| Direct-push remaining docs to `main` | Violates **H3-2**. S0+S2 go through a new PR. |
| Empty or comments-only CODEOWNERS | Forgejo still parses it. Absence is the contract. |
| Wait for `code/hello` canary merge before this delete | Sister pattern, not a local iid. This repo’s protection is already rolled; S1 is already on `main`. Copying hello `#15`’s frozen canary is not a land procedure for remaining docs. |
| Leave ADR only on `cac-design-issue-3` | Standing docs never reach `main`; later agents re-add `.* @code/maintainers`. |
| Reopen or update occupying `#3` for S0+S2 | Occupancy on that number is done; the tracker is closed. Remaining work requires a new iid. |
| Merge `cac-design-issue-3` to `main` | That ref still has root `CODEOWNERS`; it is not a valid Outcome 1 tip. Transport only. |
| Whole-tree `git checkout <sha> -- .` or `reset --hard` to the design branch | Re-plants root `CODEOWNERS` onto a tip whose `main` already deleted it. Path-limited copy only. |
| Close leftover-complete only after a later PR proves no new plant, treating that as `#3` close | `#3` is already closed; S3 is a follow-up iid / operator attestation. |
| Add Alpine `test ! -f` / `scripts/` / `rg` to Woodpecker | Out of scope; keep compileall. Absence is test 1 on `main`, not a new CI image. |
| Copy BASE_Buster `docs/*` gitignore exceptions | This tree does not ignore `docs/`; those lines would hide standing docs. |
| Wait on open `#2` or re-do merged `#1` | Unrelated / already on `main`. |
| Required approvals = 1 | Same self-approve deadlock with a one-person team. |

## Complexity added / removed

**Removed:** catch-all official-review robot on every diff (S1 on `main`);
operator dismiss step; risk that later agents re-teach “CODEOWNERS is the
trusted-PR gate” once S0+S2 land.

**Added:** a small standing doc (this ADR + architecture **H3**) plus a
README pointer so later agents do not re-add `.* @code/maintainers` as a
merge requirement. No new services, jobs, flags, scanners, or `.gitignore`
carve-out. No runtime change.

## Migration

1. Protection is already migrated (forge #48 execute on this repo,
   `updated_at` 2026-09-21T07:29:31Z).
2. S1 is already on `main` (occupying `#3` merged). Four-path `test ! -e`
   holds.
3. Remaining: combine S0+S2 onto a **new** branch from current
   `origin/main`, then merge a **new** PR (see slices). Design branch
   `cac-design-issue-3` is **not** that PR. Merging the successor does
   **not** close `#3`.
4. Leftover-complete (S3) is a **follow-up** that survives close of `#3`
   (new iid or operator attestation). Do not reopen `#3` to hold S3.
5. Open PRs created while the file existed (`#2`; leftover on closed `#3`)
   may still show an official team `maintainers` request. Non-blocking
   under **H3-8**. No bulk dismiss required. Disqualified as
   leftover-complete evidence.
6. Do not restore the file from `docs/templates/CODEOWNERS` in
   cl8y-forgejo; that template is owned by #48.

## Observability

Relative reads. Do not log tokens, hosts, WordPress credentials, or
protection-script inventories. Do not add a Forgejo admin token to
Woodpecker.

**Protection (operator).** Repo admin attests dated JSON of the five
GET-required flags for the `main` rule. Path:
`GET /api/v1/repos/code/wordpress-blog-ai-poster/branch_protections`, pick
`rule_name == "main"`. Unauthenticated GET is 401. Independent review of
this design SHA cannot re-GET. A green `compileall` run does not satisfy
this read. In-repo CI cannot perform this GET. If flags differ from the
author attestation above, escalate; do not PATCH from here. This read is
**leftover-complete item 1**, not successor land close.

**Plant signal (fail-closed pair).** Do **not** match
`team.name == "code/maintainers"` (that string is the CODEOWNERS target, not
the live JSON). Do **not** require `team.organization` on the reviews GET.

Known-plant sample: PR
[#3](https://git.cl8y.com/code/wordpress-blog-ai-poster/pulls/3) while it
was open (must **fail** this predicate; not S3 evidence).

`GET /api/v1/repos/code/wordpress-blog-ai-poster/pulls/3` fragment:

```json
{
  "draft": false,
  "requested_reviewers_teams": [
    {
      "id": 4,
      "name": "maintainers",
      "organization": { "id": 4, "name": "code" }
    }
  ]
}
```

`GET /api/v1/repos/code/wordpress-blog-ai-poster/pulls/3/reviews` fragment:

```json
[
  {
    "id": 218,
    "official": true,
    "state": "REQUEST_REVIEW",
    "team": { "id": 4, "name": "maintainers", "organization": null }
  }
]
```

Pass iff `(requested_reviewers_teams // []) | length == 0` **and** no review
with `official == true && state == "REQUEST_REVIEW" && team.name ==
"maintainers"` (optional extra pin: `team.id == 4`). `official` alone means
assigned/write-access, not “planted by CODEOWNERS”; the conjunction is the
plant signal. `REQUEST_REVIEW` is `state`, not a sibling key.

Recipe for leftover-complete is Tests item 4. `{n}` is a **dedicated**
plant-check PR opened **after** the delete is on `main` (S1 already is).
GET both endpoints **immediately after open**. If either plant signal is
present, fail. If both signals are empty, wait once **30 seconds** and
re-GET both before pass; pass only if the second pair is still empty. PR
GET must have `draft == false`. Title must not contain `WIP`
(case-insensitive). Record `{n}` **and** the two JSON bodies (the pair used
for the pass decision) on the leftover issue, then **close without merge**.
PR `#3`’s own official request does not pass. `#2` does not pass. “The next
natural PR” does not pass.

**CI.** Woodpecker context `ci/woodpecker/pr/woodpecker` on PRs; push
pipeline on `main` (`compileall`). Drain comments such as
`drain skip: no occupying job…` and `default autoland requires tip ACCEPT
(#77)` are **#429** / CAC, not a successor failure. If autoland waits on
#429, an operator still SHA-pins `Do: merge` (**H3-4**).

## Failure modes

| Mode | Handling |
| --- | --- |
| README links ADR/architecture but those files are not on the same tip | 404 after merge. Land fails docs+README. Vehicle: path-limited copy both files onto the successor PR before merging README. |
| Copy left in `docs/`, `.gitea/`, or `.forgejo/` (including empty/comments-only) | Forgejo still loads the first existing path and may plant. Land fails **H3-1**; delete those paths too (none exist on current `main`). Standing `docs/adr/` and `docs/architecture.md` are not CODEOWNERS. `.gitea/CODEOWNERS` is absent today; a later catch-all there would plant while a three-path check still passed. |
| Whole-tree copy of a `cac-design-issue-3` SHA (`git checkout <sha> -- .`, `reset --hard` to the design branch, or merging that ref) | Re-plants root `CODEOWNERS`. Forbidden. Use the path-limited copy in the combine step. |
| `CODEOWNERS` reappears after the path-limited copy | Delete it before ready. Land fails **H3-1** until gone. |
| Reopen or update occupying `#3` for remaining docs | Occupancy on that number is done. Open a new iid. |
| Merge `cac-design-issue-3` to `main` | Leaves the plant; contradicts Outcome 1. Transport only. |
| cl8y-forgejo migrate/apply re-copies a template | Sister-repo race ([cl8y-forgejo#48](https://git.cl8y.com/PlasticDigits/cl8y-forgejo/issues/48) `_ensure_codeowners`). Out of this slice. If a later apply re-adds the file, leftover-complete is **not** done: delete again via PR, then one new dated leftover comment with all leftover-complete items, **H3-1 last**. A GET or plant-check from before a re-copy does not count. Never direct-push `main`. |
| Official request leftover on closed #3 or open #2 | Non-blocking (**H3-8** / **H3-9**). Optional human dismiss. Not a rollback signal. Not leftover-complete evidence. If CAC later skips `OfficialReview` on that leftover, operators use SHA-pinned `Do: merge`. Never `force_merge`. |
| Treating merge of `#3` as leftover-complete | `#3` closed after S1 only. Use a new iid / operator attestation. |
| Treating merge of the successor as close of `#3` | `#3` is already closed; the successor must not use `Fixes #3`. |
| Plant-check is draft (`draft != false` on PR GET), title contains `WIP` (case-insensitive), has no changed file, or reviewers were requested in the UI / `POST .../requested_reviewers` | False pass (CODEOWNERS skipped or would not have planted) or false fail (manual team request). Recipe fails closed; open a new probe. |
| Operator matches `team.name == "code/maintainers"` or requires `team.organization` on reviews GET | Misses the live plant (`team.name == "maintainers"`, `team.organization == null` on reviews). Use the Observability fail-closed pair. |
| Merging the plant-check PR | Unnecessary `main` push. **Close without merge.** |
| Protection silently reverted to official-review true | Merge 405 returns. Out of this repo; re-apply via forge policy, do not `force_merge`. Not proven by compileall. |
| `enable_push` flipped true | **H3-2** regression. Refuse. |
| Re-adding CODEOWNERS “for safety” in a follow-up | Violates **H3-1**. Reviewers must reject unless a new ADR allowlists path owners. |
| Implement PATCHes protection or edits CAC | Out of authority / wrong repo. |
| `force_merge` to land the successor | Forbidden. Wait for ACCEPT + Woodpecker PR context + SHA-pinned `Do: merge`. |
| Drop or skip `compileall` while landing docs | Weakens the merge gate; keep the existing `python` step. |
| Whole-tree `git grep` for `.* @code/maintainers` | This ADR quotes that string and would false-fail. Pathspec the four Forgejo paths only. Extra lint must pass under `set -e` when files are missing. |
| Copy BASE_Buster `docs/*` gitignore | Standing docs become untracked. Do not. |

## Ordered implementation slices

| Slice | Work | Mergeable? | Depends on |
| --- | --- | --- | --- |
| **S0** | This design on `cac-design-issue-3` (ADR 0001 + architecture **H3**). Transport only. Path-limited copy of **the independently accepted SHA** (this SHA or a successor) onto the successor tip; do not call this tip accepted until independent review says so. | No. Do not open or merge as the successor PR. | None in `code/wordpress-blog-ai-poster`. |
| **S1** | Delete root `CODEOWNERS`. Confirm the other three paths are absent. | **Already on `main`** (`2a81aac` / `4a77cb8`). Do not reopen `#3`. | None remaining. |
| **S2** | New branch from current `origin/main`: standing docs (byte-identical to the independently accepted SHA via path-limited copy) + README pointer (decision 3). No Woodpecker / Python runtime / `.gitignore` / `.env.example` edits. | Yes, as the successor PR (new iid). | S0 accepted; S1 already on `main`. |
| **Successor PR** | **New iid + new PR** from current `origin/main` whose `git diff origin/main...HEAD` is ADR 0001 + architecture + README pointer. Merging this PR does **not** close `#3`. | Yes, once S0+S2 are on the head, rebased, Woodpecker green. | S0 accepted; S1 on `main`. |
| **S3** | Leftover-complete “no new plant” (tests item 4). New iid **or** operator attestation. Not a close gate for `#3` (closed) and not a close gate for the successor. S1-on-`main` is sufficient to run the plant-check. | N/A | S1 on `main` (already). |

The successor ships **S0+S2**. S1 is not part of that diff.

Sister repos (not slices of remaining work, not local `DEPS`): forge #48
protection+templates; CAC #429 autoland occupying job; `code/hello` canary
docs.

### Combine step (S0+S2 onto the successor vehicle)

Do this on a **new branch from current `origin/main`**, not on
`cac-design-issue-3`, and not by updating closed occupying `#3`:

1. `git fetch origin && git checkout -b <new-branch> origin/main`.
2. Fetch the published design: `origin/cac-design-issue-3` at **the
   independently accepted SHA**.
3. Path-limited copy only:

   ```
   git checkout <accepted-sha> -- docs/adr/0001-remove-catchall-codeowners.md docs/architecture.md
   ```

   **Forbid** `git checkout <accepted-sha> -- .`, `git reset --hard` to the
   design branch, and merging `cac-design-issue-3`. Those restore root
   `CODEOWNERS`.
4. If `CODEOWNERS` exists after the copy, delete it before ready.
5. Edit README only as specified in decision 3 (Merge gate section after
   the title paragraph; CLI usage stays).
6. Rebase onto current `origin/main` if needed (`block_on_outdated_branch`
   is observed-true; do not PATCH it off). Push the new branch. Open a
   **new** PR (new iid). Do not reopen `#3`. Do not put `Fixes #3`.
7. Ready the PR only when `git diff origin/main...HEAD` is exactly the
   three-part docs/README diff (test 6). Then merge with SHA-pinned
   `Do: merge`.

## Tests

In-repo CI cannot GET branch protection. `compileall` is unrelated to file
absence and must not be rewritten for this ticket. The existing `python`
step must still pass on the successor PR.

1. **Absence / H3-1** (on `main` / successor tip). Same sentence as land
   close (tree): none of the four Forgejo search paths exist
   (`test ! -e CODEOWNERS`, `test ! -e docs/CODEOWNERS`,
   `test ! -e .gitea/CODEOWNERS`, `test ! -e .forgejo/CODEOWNERS`). Grep is
   extra catch-all lint, not the definition of **H3-1** (an empty,
   comment-only, or non-`.*` owner file still fails `test ! -e`). Do not
   `git grep` the whole tree (this ADR quotes `.* @code/maintainers` and
   would false-fail).

   ```
   test ! -e CODEOWNERS
   test ! -e docs/CODEOWNERS
   test ! -e .gitea/CODEOWNERS
   test ! -e .forgejo/CODEOWNERS
   # pass: all four succeed. This *is* H3-1 / land close (tree).

   # extra lint, not H3-1. Missing paths and no-match must pass under
   # set -e (do not treat grep exit 1 as the pass signal).
   fail=0
   for p in CODEOWNERS docs/CODEOWNERS .gitea/CODEOWNERS .forgejo/CODEOWNERS; do
     if test -e "$p" && grep -qE '^\.\* @' "$p"; then
       echo "fail: catch-all owner line in $p" >&2
       fail=1
     fi
   done
   test "$fail" -eq 0
   ```

   Do **not** whole-tree `git grep` (the escaped form
   `git grep -n '^\\.\\* @'` matches nothing even while the catch-all file
   exists; the unescaped `git grep -nE '^\.\* @'` hits this ADR after a
   correct delete).

2. **PR pipeline.** Existing Woodpecker `python` / `compileall` step succeeds
   on the successor PR. No secrets on the PR event. Do not add a second
   image for absence.

3. **Protection (operator read; leftover-complete item 1, not land close).**
   `GET /api/v1/repos/code/wordpress-blog-ai-poster/branch_protections`,
   pick `rule_name == "main"`, still equals **H3-2**, **H3-3**, **H3-5**,
   **H3-8**, **H3-9**. Fail if `enable_push` is true, official-review block
   is true, `required_approvals` is not 0, reject-block is false, or
   `status_check_contexts` is not **equal**
   `["ci/woodpecker/pr/woodpecker"]`. Do **not** treat observed flags or
   **H3-4** as GET-match fields. Unauthenticated GET is 401; attestation is
   operator-only. Independent review of this SHA cannot re-GET. Not inferred
   from a green `compileall`.

4. **No new plant** (leftover-complete; **not** a `#3` close gate and
   **not** a successor close gate). After S1 is on `main` (already true):

   1. CODEOWNERS is evaluated from the **base** branch. Opening a non-WIP
      PR into `main` after the file is gone from `main` is the plant
      mechanism. A tip without `CODEOWNERS` is extra, not what Forgejo reads
      for planting.
   2. Open a **dedicated** plant-check PR into `main`. PR GET must have
      `draft == false`. Title must not contain `WIP` (case-insensitive). At
      least one changed file (any path matches Go `.*`).
   3. Do not request users or teams in the UI or via
      `POST .../requested_reviewers`.
   4. GET `.../pulls/{n}` and `.../pulls/{n}/reviews` **immediately after
      open**.
   5. Pass iff Observability’s fail-closed pair holds. If either plant
      signal is present, fail. If both signals are empty, wait once
      **30 seconds** and re-GET both; pass only if the second pair is still
      empty.
   6. Record `{n}` **and** the two JSON bodies (the pair used for the pass
      decision), then **close without merge**.

   Fail if `draft != false`, if the title contains `WIP` (case-insensitive),
   if the PR has no changed file, if reviewers were requested manually, or
   if either GET signal is present after the wait. Do not use `#3`. Do not
   use `#2`. Do not use “the next natural PR.” Who opens the PR: anyone who
   can create a PR on `code/wordpress-blog-ai-poster`. Who GETs protection
   (item 3): repo admin; not Woodpecker.

   Leftover-complete attest order is Integration: **H3-1 last**. Do not
   treat a passing GET or plant-check from before a later
   `_ensure_codeowners` apply as done.

5. **Reject still blocks (doc-level).** Do not turn off
   `block_on_rejected_reviews` to “make autoland easier.”

6. **Preflight.** Refuse merge unless `git diff origin/main...HEAD` is
   exactly the three-part docs/README diff (ADR 0001 + architecture +
   README pointer). No `CODEOWNERS` add. No `.gitignore` edit. No
   Woodpecker edit. No Python runtime edit.

Do not add a pytest harness solely for file absence. `compileall` is not
the merge-plane oracle.

Human / review (not Woodpecker): product docs must not recommend enabling
`force_merge`. If a docs grep is used at all, match `force_merge:\s*true` as
**advice**, not any occurrence of `force_merge` (this ADR names the
forbidden API).

## Rollout

- Merge vehicle: **new iid + new PR** from current `origin/main`, after
  the combine step. Diff must be ADR 0001 + architecture + README pointer.
  Design-only `cac-design-issue-3` must not be opened or merged as the
  successor PR (it still carries root `CODEOWNERS`). Do not reopen `#3`.
  Merging the successor does **not** close `#3`.
- Order: protection already live → S1 already on `main` → path-limited
  copy of S0 files from the independently accepted SHA + S2 README on a
  new branch → rebase → Woodpecker green → `Do: merge`. Then
  leftover-complete test 4 on a new iid or operator attestation (S1-on-main
  is enough to run the plant-check).
- Canary: `code/hello` may land the same pattern first; this ADR does not
  merge that repo and does not block on it.
- [#297](https://git.cl8y.com/PlasticDigits/cl8y-agent-control/issues/297):
  no deploy, spend, custody, or CAC policy expansion. Landing the successor
  does not authorize WordPress publish, OpenAI/Tavily spend, Coolify, or
  autonomy changes.

Chat/issue cannot set protection flags.

## Rollback

Restore the previous `CODEOWNERS` **via PR**, not direct `main`. That
re-plants official requests. It does **not** by itself re-enable merge-block
(`block_on_official_review_requests`); restoring the 405 gate is a
forge-policy revert, founder-scoped, and is not a wordpress-blog-ai-poster
rollback step.

File-only rollback that leaves this ADR and architecture on `main` (still
saying CODEOWNERS must be absent) is **intended**: standing docs keep
telling later agents not to treat the restored file as a merge gate. Do not
delete the docs as part of restoring the file unless a new ADR reverses this
decision. If S0 docs need revert, revert via PR together with README so
relative links do not 404.

Woodpecker / Python runtime rollback is unused: those files are untouched.

## Integration completion criteria

### Land (S0+S2) — merge of the successor PR (new iid)

Merging the successor does **not** close
[#3](https://git.cl8y.com/code/wordpress-blog-ai-poster/issues/3). Close the
**new** tracker when all of the following are true at that merge:

1. **Tree.** None of the four Forgejo search paths exist on `main`
   (`test ! -e CODEOWNERS`, `test ! -e docs/CODEOWNERS`,
   `test ! -e .gitea/CODEOWNERS`, `test ! -e .forgejo/CODEOWNERS`). Same
   sentence as **H3-1** and test 1. Already true after S1; the successor
   must not restore any of those paths.
2. **Docs + README.** Merged tip contains
   `docs/adr/0001-remove-catchall-codeowners.md` and
   `docs/architecture.md` **byte-identical** to the independently accepted
   SHA (this SHA or a successor; not this tip until independent review;
   `Status: Proposed` stays unless a Status-only SHA was accepted). README
   has the Merge gate section from decision 3 after the title paragraph;
   relative links resolve on that tip. CLI usage remains. Architecture-only
   is not sufficient. Do not merge a README that points at those paths until
   they exist on that tip.
3. **Woodpecker.** Context `ci/woodpecker/pr/woodpecker` succeeded on that
   successor PR; no deploy secrets ran on that PR event; existing `python`
   / `compileall` step remains.
4. **Authority.** No `force_merge`, no direct `main`, no CAC dismiss-as-merge,
   no Coolify/HMAC/`autonomy.rs`/WordPress-publish edits, and no `#297`
   expansion in the successor diff.

Green Woodpecker on the successor PR is necessary for merge. It is
sufficient for the CI item. Five-flag protection GET is **not** a land
close criterion (leftover-complete item 1).

### Leftover-complete (S3) — follow-up; `#3` is already closed

Require **one dated leftover comment** with all three items, **H3-1 last**
(or all three timestamps in one attest). A GET or plant-check from before a
later `_ensure_codeowners` apply does not count; re-delete via PR and write
a new comment.

1. Protection GET five flags: repo admin attests dated JSON:
   `GET /api/v1/repos/code/wordpress-blog-ai-poster/branch_protections`,
   pick `rule_name == "main"`, equals the five architecture
   **GET-required** flags (**H3-2**, **H3-3**, **H3-5**, **H3-8**,
   **H3-9**). Not the Merge API row. Not inferred from a green
   `compileall`. Independent review of a design SHA cannot re-GET (401).
2. Plant-check `{n}` + JSON: a **dedicated** plant-check PR following Tests
   item 4 and Observability’s fail-closed pair. Record `{n}` and the two
   JSON bodies, then close without merge. `#3`’s own official request does
   not count. `#2` does not count. “The next natural PR” does not count.
3. **H3-1 last:** `test ! -e` succeeds on `CODEOWNERS`, `docs/CODEOWNERS`,
   `.gitea/CODEOWNERS`, and `.forgejo/CODEOWNERS`. Recorded after items 1
   and 2 (same comment or later timestamp in the same attest).

Forgejo#50, CAC#429, and wordpress-blog-ai-poster #2 may stay open; they are
not land or leftover gates for this tree.

Live Grafana/CAC leftover cleanup is not a completion criterion here.

## Requirement-to-test mapping

See **Tests**. Implement keeps the mapping next to the four-path `test ! -e`
block (that block *is* **H3-1**).

## Authority

[cl8y-agent-control#297](https://git.cl8y.com/PlasticDigits/cl8y-agent-control/issues/297):
this design does not grant deploy, spend, custody, or agent-permission
expansion. Relaxing official-review as a **forge merge gate** is already
executed on this repo by #48; this ADR only records the in-tree delete
(S1 on `main`) and remaining standing docs. Independent review of this
proposal is a later gate. Design author must not write `DESIGN: APPROVE`.

## Cross-links

- [#3](https://git.cl8y.com/code/wordpress-blog-ai-poster/issues/3) (closed occupying PR; S1)
- [cl8y-forgejo#48](https://git.cl8y.com/PlasticDigits/cl8y-forgejo/issues/48)
- [cl8y-forgejo INVARIANTS](https://git.cl8y.com/PlasticDigits/cl8y-forgejo/src/branch/main/docs/INVARIANTS.md)
- [cl8y-agent-control#388](https://git.cl8y.com/PlasticDigits/cl8y-agent-control/issues/388)
- [cl8y-agent-control#297](https://git.cl8y.com/PlasticDigits/cl8y-agent-control/issues/297)
- [`architecture.md`](../architecture.md)
- [code/hello#15](https://git.cl8y.com/code/hello/pulls/15) (canary delete)
