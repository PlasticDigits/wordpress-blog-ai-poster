# ADR 0001: Remove catch-all CODEOWNERS

## Status

Proposed ([#3](https://git.cl8y.com/code/wordpress-blog-ai-poster/issues/3)).
Not accepted by this design-author pass. Do not call this tip accepted until
independent review says so. Keywords in the issue body are not architecture
approval. Ordinary design is not a founder card. There is no separate
standing issue `#3`; the issues URL and the product PR share one number.

Copy **the independently accepted SHA** (this SHA or a successor) onto the
product tip. `cac-design-issue-3` is never the merge vehicle. Land criterion:
the two `docs/` files on the product tip are byte-identical to that SHA.

Overview (merge gate, GET contract, product tree):
[`architecture.md`](../architecture.md). Do not copy that table here. Local
invariant IDs are **H3-*** (this ticket). `code/hello` architecture **H15**
is the canary’s copy of the same flags, not this repo’s issue number.

[#3](https://git.cl8y.com/code/wordpress-blog-ai-poster/issues/3) **is** the
product PR (`html_url` → `pulls/3`). Merging it closes the tracker.
Post-merge “no new plant” is leftover-complete AC on a **new** iid (or
operator attestation after close). Do not reuse #3 for both.

This ADR does not authorize deploy, spend, custody rotation, WordPress
publish, or Forgejo protection PATCH
([agent-control #297](https://git.cl8y.com/PlasticDigits/cl8y-agent-control/issues/297)).

## Outcome

Delete the catch-all `CODEOWNERS` so this tree no longer supplies the
planting file. Official plant-stop on later PRs is leftover-complete
(test 4 / S3), not close of #3. Merge to `main` stays: pull request,
Woodpecker context `ci/woodpecker/pr/woodpecker`, SHA-pinned `Do: merge`,
no direct push, no `force_merge`.

**Land vehicle:** product PR
[#3](https://git.cl8y.com/code/wordpress-blog-ai-poster/pulls/3) (or a
successor) ships **S0+S1+S2 on one tip** — copy the two design files from
**the independently accepted SHA** (this SHA or a successor), delete
`CODEOWNERS`, add a README pointer. Merging that PR closes `#3`. Design
branch `cac-design-issue-3` is review/transport only; it is **not** merged
as a docs-only PR and is **not** the product PR.

This is a product-tree copy of the pattern named by
[cl8y-forgejo#48](https://git.cl8y.com/PlasticDigits/cl8y-forgejo/issues/48).
The canary is `code/hello`
[#15](https://git.cl8y.com/code/hello/issues/15), not this repo. Protection
on `code/wordpress-blog-ai-poster` `main` already matches that ticket
(`block_on_official_review_requests=false` **H3-8**, `required_approvals=0`
**H3-9**, `enable_push=false` **H3-2**). #3 is one product PR: file delete
plus standing docs plus README pointer. It does not re-roll protection, does
not implement CAC autoland, and does not publish to WordPress.

Author-attested live protection (authenticated GET, 2026-09-21,
design-author session) on `main`: `enable_push=false`,
`enable_status_check=true` with `status_check_contexts` equal
`["ci/woodpecker/pr/woodpecker"]`, `required_approvals=0`,
`block_on_official_review_requests=false`, `block_on_rejected_reviews=true`,
`updated_at=2026-09-21T07:29:31Z`. Anonymous
`GET /repos/code/wordpress-blog-ai-poster/branch_protections` returns 401
(`token is required`). Independent review cannot re-verify those flags
without a token. If live flags differ from this attestation, stop and
escalate to forge owners. Do not PATCH protection from this repo. This ADR
does **not** treat the GET as implement write permission.

## Context

`ca6a1f7` (2026-09-02) added root [`CODEOWNERS`](../../CODEOWNERS):

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
CLI usage guide; it does not currently name a merge gate. The product PR
must add a pointer at **H3** without rewriting generation/SEO/publish
instructions. The issue body links cl8y-forgejo `docs/INVARIANTS.md`; that
file is not in this tree. Do not invent a local copy.

Live proof that the file still plants requests (re-checked this pass):
[#3](https://git.cl8y.com/code/wordpress-blog-ai-poster/pulls/3) has
`official: true` `REQUEST_REVIEW` from team `maintainers` on open;
`requested_reviewers_teams` is that team.
[#2](https://git.cl8y.com/code/wordpress-blog-ai-poster/pulls/2) (Renovate)
still lists the same team. Those leftovers are **disqualified** as “no new
plant” evidence. Protection GET on `main` has `updated_at`
2026-09-21T07:29:31Z and official-review **block** off (**H3-8**), so
leftover requests must not be treated as merge blockers.

Draft implementation (not this design commit):
`4a77cb80a43b34671a43904d8bbb7178f9a891e1` on
`chore/remove-catchall-codeowners` deletes the six-line file and nothing
else. Live `draft` is currently `false`. Woodpecker
`ci/woodpecker/pr/woodpecker` succeeded on that SHA (pipeline 6). That head
is **not landable** until standing docs and the README pointer are on the
**same** branch. This branch (`cac-design-issue-3`) is design transport
only; it is not the product PR.

`origin/main` has no `docs/` tree. Relative README links to ADR 0001 /
architecture 404 unless those two files land on the **same merged tip** as
the README pointer. `.gitignore` does not ignore `docs/` (unlike Foundry
`docs/` on `code/BASE_Buster`); do not add `docs/*` exceptions.

No in-repo issue dependencies. Merged
[#1](https://git.cl8y.com/code/wordpress-blog-ai-poster/issues/1) already
put `.woodpecker.yml` on `main`. Open
[#2](https://git.cl8y.com/code/wordpress-blog-ai-poster/pulls/2)
(`renovate/configure`) is unrelated occupancy.

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
  including leftovers on `#3` and `#2`.
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
- Open `cac-design-issue-3` as a PR, or merge that transport ref to `main`.
- Sibling PR `issue/3` while `#3` is open (occupancy).
- Copying Foundry `docs/*` `.gitignore` exceptions; this tree does not
  ignore `docs/`.

## Decision

1. **Delete** root `CODEOWNERS`. Do not leave an empty or comments-only file
   (Forgejo still parses it).
2. **Do not add** `docs/CODEOWNERS`, `.gitea/CODEOWNERS`, or
   `.forgejo/CODEOWNERS`. After land, `test ! -e` succeeds on all four
   paths. None of those paths may contain a reviewer rule for any pattern
   (not only `.*`). Same sentence as **H3-1**, test 1, and close criterion 1.
3. **Keep** the merge gate in [`architecture.md`](../architecture.md)
   **H3**. On the product PR, keep the WordPress CLI README and add one or
   two sentences plus relative links to this ADR and architecture **H3**.
   Do not claim maintainers review every change. Do not expand generation,
   SEO, or publish instructions. Architecture-only is **not** sufficient.
   Do not merge a README that points at those paths until they exist on
   that tip. The two `docs/` files on the product tip must be
   byte-identical to the independently accepted SHA.
4. **One product PR** whose diff is: delete `CODEOWNERS` + ADR 0001 +
   architecture + README pointer. `cac-design-issue-3` is transport; do not
   merge it to `main` and do not open it as the product PR.
5. **Leave** already-planted official requests on open PRs (including #3
   and #2). They are non-blocking under **H3-8** / **H3-9**. Do not dismiss
   them from CAC. Human dismiss is optional leftover, not AC. They do not
   count as “no new plant.”
6. **Do not** PATCH branch protection from this repository.

## Component / state / interface changes

| Surface | Change |
| --- | --- |
| `CODEOWNERS` (root) | Remove file. |
| `docs/CODEOWNERS`, `.gitea/CODEOWNERS`, `.forgejo/CODEOWNERS` | Must remain absent (no empty file). Do not add `.gitea/CODEOWNERS`. |
| `docs/adr/0001-remove-catchall-codeowners.md`, `docs/architecture.md` | Copy from the independently accepted SHA onto the product PR so the merged tip is S0+S1+S2 (byte-identical). Standing H3 contract lands with the delete. |
| Forgejo PR review interface | Removes the planting file. Official team requests on **new** non-WIP PRs against `main` after land are leftover-complete evidence (test 4 / S3), not a #3 close gate. `requested_reviewers_teams` from this file is expected empty for those new PRs. Forgejo skips CODEOWNERS on WIP/draft — a draft is not proof. |
| Branch protection API | No write from this ticket. Operator GET must still match architecture **GET-required** (**H3-2**, **H3-3**, **H3-5**, **H3-8**, **H3-9**). Observed rows are do-not-touch. In-repo CI cannot perform that GET. |
| `.gitignore` | Unchanged (`.env`, `__pycache__`). Do not add `docs/*` exceptions. |
| `.woodpecker.yml` | Unchanged. Keep the existing `python` / `compileall` step. No secrets on `pull_request`. |
| README | Mandatory on the product PR: one or two sentences — merge gate is **H3** (PR + Woodpecker + no direct `main`); CODEOWNERS is not a gate. Relative links to ADR 0001 / architecture, which exist on that same tip. Do not rewrite CLI usage. |
| `wp_ai_poster.py` / `blog_*.py` / `wp_add_meta.py` / `Context_*.md` | Unchanged. |
| CAC / Coolify / org team `code/maintainers` | Unchanged. The team may keep existing; it simply is not planted as official review. |

No runtime contract, schema, or HTTP API change.

Forgejo CODEOWNERS lookup is root, `docs/`, `.gitea/`, or `.forgejo/`
(Go-regexp, not GitHub globs). Outcome 1 / **H3-1** is **no file** at those
four paths.

## Affected invariants

| ID | Kind | Rule |
| --- | --- | --- |
| **H3-1** | Non-GET | None of the four Forgejo search paths exist on `main` (`test ! -e CODEOWNERS`, `test ! -e docs/CODEOWNERS`, `test ! -e .gitea/CODEOWNERS`, `test ! -e .forgejo/CODEOWNERS`). Same sentence as test 1 and close criterion 1. File line `@code/maintainers` / JSON team `maintainers` is the leftover plant this absence stops. |
| **H3-2** | GET-required | `enable_push=false` on `main`. |
| **H3-3** | GET-required | `enable_status_check=true` and `status_check_contexts` **equal** `["ci/woodpecker/pr/woodpecker"]`. |
| **H3-4** | Non-GET | Merge is SHA-pinned `Do: merge`. Never document or use `force_merge`. Not a protection field; omit from GET matching. |
| **H3-5** | GET-required | `block_on_rejected_reviews` stays true. An explicit REJECT still blocks. |
| **H3-6** | Non-GET | No Coolify/Woodpecker secrets on `pull_request`. This tree does not grow a deploy step from #3. WordPress publish and OpenAI/Tavily spend stay #297. |
| **H3-7** | Non-GET | This tree does not expand CAC merge/deploy/spend/custody policy. |
| **H3-8** | GET-required | `block_on_official_review_requests=false`. Leftover official requests on #3/#2 are non-blocking. |
| **H3-9** | GET-required | `required_approvals=0`. |

GET-observed flags (`block_on_outdated_branch`, `dismiss_stale_approvals`,
`apply_to_admins`) are listed in architecture only. They have no
close-criterion IDs. #3 must not PATCH them.

Do not weaken cl8y-forgejo protection invariants **2–10** and **13** from
product commits. CAC #388 stays: skip official-review deadlock; never
`force_merge`; drain does not delete CODEOWNERS. Product land makes the
skip class stop firing **for this repo** once new PRs have no plant.

Python generation behavior is unchanged. There is no local
`docs/invariants.md` / typed product invariant file to rewrite.

## Alternatives

| Option | Why not |
| --- | --- |
| Keep file, rely on `block_on_official_review_requests=false` | Requests still plant on every non-WIP PR; drain noise; Renovate/agent PRs look like they need a human stamp; templates can re-teach the old gate. |
| Replace `.*` with path owners | No second reviewer exists; same 405/422 if official-review is ever turned on; out of scope. Outcome 1 forbids the file. |
| Add a second maintainer | Founder ops, not this implement. |
| Dismiss official requests from CAC | Forbidden by #388 as a substitute for policy reversal. |
| Direct-push the delete to `main` | Violates **H3-2**. File deletes go through a PR (already [#3](https://git.cl8y.com/code/wordpress-blog-ai-poster/pulls/3)). |
| Empty or comments-only CODEOWNERS | Forgejo still parses it. Absence is the contract. |
| Wait for `code/hello` canary merge before this delete | Sister pattern, not a local iid. This repo’s protection is already rolled; the file still plants. |
| Leave ADR only on `cac-design-issue-3` | Standing docs never reach `main`; later agents re-add `.* @code/maintainers`. |
| Merge live #3 as delete-only (`4a77cb8`, S1 without S2) | **H3-1** true, standing docs / README pointer false; later agents have no “do not re-add” contract; README links 404. |
| Merge `cac-design-issue-3` to `main` | That ref still has root `CODEOWNERS`; it is not a valid Outcome 1 tip. Transport only. |
| Open `issue/3` beside `#3` | Occupancy violation. |
| Close #3 only after a later PR proves no new plant | Merge of #3 closes the tracker; waiting for the follow-up before merge never produces it. |
| Add Alpine `test ! -f` / `scripts/` / `rg` to Woodpecker | Out of scope; keep compileall. Absence is test 1 on the product tip, not a new CI image. |
| Copy BASE_Buster `docs/*` gitignore exceptions | This tree does not ignore `docs/`; those lines would hide standing docs. |
| Wait on open `#2` or re-do merged `#1` | Unrelated / already on `main`. |
| Required approvals = 1 | Same self-approve deadlock with a one-person team. |

## Complexity added / removed

**Removed:** catch-all official-review robot on every diff; operator dismiss
step; risk that later agents re-teach “CODEOWNERS is the trusted-PR gate.”

**Added:** a small standing doc (this ADR + architecture **H3**) plus a
README pointer so later agents do not re-add `.* @code/maintainers` as a
merge requirement. No new services, jobs, flags, scanners, or `.gitignore`
carve-out. No runtime change.

## Migration

1. Protection is already migrated (forge #48 execute on this repo,
   `updated_at` 2026-09-21T07:29:31Z).
2. Before merging the product PR, treat leftover-complete (S3) as a
   **follow-up** that survives close of `#3` (new iid or operator
   attestation after merge). Merging [#3](https://git.cl8y.com/code/wordpress-blog-ai-poster/pulls/3)
   closes that number; S3 must not live only there.
3. Combine onto the existing product head, then merge **one** PR (see
   slices). Design branch `cac-design-issue-3` is **not** that PR.
4. Open PRs created while the file existed (#3, #2) may still show an
   official team `maintainers` request. Non-blocking under **H3-8**. No
   bulk dismiss required to close #3. Disqualified as leftover-complete
   evidence.
5. Do not restore the file from `docs/templates/CODEOWNERS` in
   cl8y-forgejo; that template is owned by #48.

Title/body of `#3` need no extra `Fixes #3` (the pull **is** iid 3).

## Observability

Relative reads. Do not log tokens, hosts, WordPress credentials, or
protection-script inventories. Do not add a Forgejo admin token to
Woodpecker.

**Protection (operator).** Repo admin attests dated JSON of the five
GET-required flags for the `main` rule. Unauthenticated GET is 401. A green
`compileall` run does not satisfy this read. In-repo CI cannot perform this
GET. If flags differ from the author attestation above, escalate; do not
PATCH from here.

**Plant signal (fail-closed pair).** Do **not** match
`team.name == "code/maintainers"` (that string is the CODEOWNERS target, not
the live JSON). Do **not** require `team.organization` on the reviews GET.

Known-plant sample: PR
[#3](https://git.cl8y.com/code/wordpress-blog-ai-poster/pulls/3) (must
**fail** this predicate; not S3 evidence).

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
plant-check PR opened **after** the delete is on `main`. GET both endpoints
**immediately after open**. If either plant signal is present, fail. If both
signals are empty, wait once **30 seconds** and re-GET both before pass;
pass only if the second pair is still empty. PR GET must have
`draft == false`. Title must not contain `WIP` (case-insensitive). Record
`{n}` **and** the two JSON bodies (the pair used for the pass decision) on
the leftover issue, then **close without merge**. PR `#3`’s own official
request does not pass. `#2` does not pass. “The next natural PR” does not
pass.

**CI.** Woodpecker context `ci/woodpecker/pr/woodpecker` on PRs; push
pipeline on `main` (`compileall`). Drain comments such as
`drain skip: no occupying job…` and `default autoland requires tip ACCEPT
(#77)` are **#429** / CAC, not a #3 failure. If autoland waits on #429, an
operator still SHA-pins `Do: merge` (**H3-4**).

## Failure modes

| Mode | Handling |
| --- | --- |
| File deleted on a branch but still on `main` | New non-WIP PRs keep planting official review until the product PR merges. Expected until land. |
| README links ADR/architecture but those files are not on the same tip | 404 after merge. Land fails criterion 2. Vehicle: copy both files onto the product PR before merging README. |
| Copy left in `docs/`, `.gitea/`, or `.forgejo/` (including empty/comments-only) | Forgejo still loads the first existing path and may plant. Land fails **H3-1**; delete those paths too (none exist on current `main`). Standing `docs/adr/` and `docs/architecture.md` are not CODEOWNERS. `.gitea/CODEOWNERS` is absent today; a later catch-all there would plant while a three-path check still passed. |
| Merge live #3 (`4a77cb8`) without S0 files and S2 | **H3-1** true, standing docs / README pointer false. Forbidden. Convert #3 to draft until the complete diff is on the head. |
| Merge `cac-design-issue-3` to `main` | Leaves the plant; contradicts Outcome 1. Transport only. |
| Sibling PR `issue/3` | Occupancy violation. Update `#3` only. |
| cl8y-forgejo migrate/apply re-copies a template | Sister-repo race ([cl8y-forgejo#48](https://git.cl8y.com/PlasticDigits/cl8y-forgejo/issues/48) `_ensure_codeowners`). Out of this slice. If a later apply re-adds the file, leftover-complete is **not** done: delete again via PR, then one new dated leftover comment with all leftover-complete items, **H3-1 last**. A GET or plant-check from before a re-copy does not count. Never direct-push `main`. |
| Official request leftover on #3 or #2 | Non-blocking (**H3-8** / **H3-9**). Optional human dismiss. Not a rollback signal. Not leftover-complete evidence. If CAC later skips `OfficialReview` on that leftover, operators use SHA-pinned `Do: merge`. Never `force_merge`. |
| Treating merge of `#3` as leftover-complete | Merge closes `#3` before S3. Use a new iid / operator attestation. |
| Plant-check is draft (`draft != false` on PR GET), title contains `WIP` (case-insensitive), has no changed file, or reviewers were requested in the UI / `POST .../requested_reviewers` | False pass (CODEOWNERS skipped or would not have planted) or false fail (manual team request). Recipe fails closed; open a new probe. |
| Operator matches `team.name == "code/maintainers"` or requires `team.organization` on reviews GET | Misses the live plant (`team.name == "maintainers"`, `team.organization == null` on reviews). Use the Observability fail-closed pair. |
| Merging the plant-check PR | Unnecessary `main` push. **Close without merge.** |
| Protection silently reverted to official-review true | Merge 405 returns. Out of this repo; re-apply via forge policy, do not `force_merge`. Not proven by compileall. |
| `enable_push` flipped true | **H3-2** regression. Refuse. |
| Re-adding CODEOWNERS “for safety” in a follow-up | Violates **H3-1**. Reviewers must reject unless a new ADR allowlists path owners. |
| Implement PATCHes protection or edits CAC | Out of authority / wrong repo. |
| `force_merge` to land `#3` | Forbidden. Wait for ACCEPT + Woodpecker PR context + SHA-pinned `Do: merge`. |
| Drop or skip `compileall` while landing docs | Weakens the merge gate; keep the existing `python` step. |
| Whole-tree `git grep` for `.* @code/maintainers` | This ADR quotes that string and would false-fail. Pathspec the four Forgejo paths only. |
| Copy BASE_Buster `docs/*` gitignore | Standing docs become untracked. Do not. |

## Ordered implementation slices

| Slice | Work | Mergeable? | Depends on |
| --- | --- | --- | --- |
| **S0** | This design on `cac-design-issue-3` (ADR 0001 + architecture **H3**). Transport only. Copy **the independently accepted SHA** (this SHA or a successor) onto the product tip; do not call this tip accepted until independent review says so. | No. Do not open or merge as a product PR. | None in `code/wordpress-blog-ai-poster`. |
| **S1** | Delete root `CODEOWNERS`. Confirm the other three paths are absent. Live head `4a77cb8` on `chore/remove-catchall-codeowners`. | **Draft-only** until S2 is on the same branch. Not a landable slice. Convert live #3 to `draft` (it is currently `draft: false`) before any merge. | S0 files present on the **same product-PR tip** (not “S0 accepted” alone). |
| **S2** | Same branch as S1: standing docs (byte-identical to the independently accepted SHA) + README pointer (CLI usage kept; one/two sentences + relative links). No Woodpecker / Python runtime / `.gitignore` / `.env.example` edits. | Only as the **combined** product PR with S1. | S0 files on the same tip as S1. Same PR as S1. |
| **Product PR** | **One** PR: [#3](https://git.cl8y.com/code/wordpress-blog-ai-poster/pulls/3) (`chore/remove-catchall-codeowners`) whose `git diff origin/main...HEAD` is delete + ADR 0001 + architecture + README pointer. Merging this PR **closes #3**. | Yes, once S1+S2 are on the head, rebased, Woodpecker green. | S0 accepted; S1+S2 combined. |
| **S3** | Leftover-complete “no new plant” (tests item 4). New iid **or** operator attestation **after** #3 is closed. Not a close gate for #3. | N/A | Product PR merged to `main`. |

PR `#3` (or successor) ships **S0+S1+S2**. S2 depends on S0 files being on
the same tip, not only on S1.

Sister repos (not slices of #3, not local `DEPS`): forge #48
protection+templates; CAC #429 autoland occupying job; `code/hello` canary
docs.

### Combine step (S1+S2 onto the product vehicle)

Do this on `chore/remove-catchall-codeowners`, not on `cac-design-issue-3`:

1. Mark [#3](https://git.cl8y.com/code/wordpress-blog-ai-poster/pulls/3)
   **draft** so delete-only `4a77cb8` cannot land.
2. Fetch published design: `origin/cac-design-issue-3` (this ADR,
   `docs/architecture.md`) at **the independently accepted SHA**.
3. Copy those two files onto `chore/remove-catchall-codeowners` so they are
   byte-identical to that SHA (keep the CODEOWNERS delete from `4a77cb8`).
   The cherry-pick / copy must not restore `CODEOWNERS`.
4. Edit README only as specified in decision 3 (one/two sentences + relative
   links; CLI usage stays).
5. Rebase onto current `origin/main` (`block_on_outdated_branch` is
   observed-true; do not PATCH it off). Push the product branch.
6. Ready the PR only when `git diff origin/main...HEAD` is exactly the
   four-part product diff (test 6). Then merge with SHA-pinned `Do: merge`.

## Tests

In-repo CI cannot GET branch protection. `compileall` is unrelated to file
absence and must not be rewritten for this ticket. The existing `python`
step must still pass on the product PR.

1. **Absence / H3-1** (on the product tip / after land). Same sentence as
   close criterion 1: none of the four Forgejo search paths exist on `main`
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
   # pass: all four succeed. This *is* H3-1 / close criterion 1.

   git grep -nE '^\.\* @' -- CODEOWNERS docs/CODEOWNERS .gitea/CODEOWNERS .forgejo/CODEOWNERS
   # extra lint, not H3-1: pass is grep exit 1 (no matches / no files)
   ```

   Do **not** whole-tree `git grep` (the escaped form
   `git grep -n '^\\.\\* @'` matches nothing even while the catch-all file
   exists; the unescaped `git grep -nE '^\.\* @'` hits this ADR after a
   correct delete).

2. **PR pipeline.** Existing Woodpecker `python` / `compileall` step succeeds
   on the **combined** product PR. No secrets on the PR event. Do not add a
   second image for absence.

3. **Protection (operator read).** Same list as close criterion 4: GET
   `main` still equals **H3-2**, **H3-3**, **H3-5**, **H3-8**, **H3-9**. Fail
   if `enable_push` is true, official-review block is true,
   `required_approvals` is not 0, reject-block is false, or
   `status_check_contexts` is not **equal**
   `["ci/woodpecker/pr/woodpecker"]`. Do **not** treat observed flags or
   **H3-4** as GET-match fields. Unauthenticated GET is 401; attestation is
   operator-only. Not inferred from a green `compileall`.

4. **No new plant** (leftover-complete; **not** a #3 close gate). After
   S1+S2 are on `main`:

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
   exactly the four-part product diff (delete `CODEOWNERS` + ADR 0001 +
   architecture + README pointer). No `.gitignore` edit. No Woodpecker edit.
   No Python runtime edit.

Do not add a pytest harness solely for file absence. `compileall` is not
the merge-plane oracle.

Human / review (not Woodpecker): product docs must not recommend enabling
`force_merge`. If a docs grep is used at all, match `force_merge:\s*true` as
**advice**, not any occurrence of `force_merge` (this ADR names the
forbidden API).

## Rollout

- Merge vehicle: **one** PR, existing
  [#3](https://git.cl8y.com/code/wordpress-blog-ai-poster/pulls/3), after
  the combine step. Diff must be delete + ADR 0001 + architecture + README
  pointer. Design-only `cac-design-issue-3` must not be opened or merged as
  the product PR.
- Order: protection already live → convert #3 to draft → copy S0 files from
  the independently accepted SHA + keep S1 delete + S2 README on that tip →
  rebase → Woodpecker green → `Do: merge` → **#3 closes**. Then
  leftover-complete test 4 on a new iid or operator attestation.
- Canary: `code/hello` may land the same pattern first; this ADR does not
  merge that repo and does not block on it.
- [#297](https://git.cl8y.com/PlasticDigits/cl8y-agent-control/issues/297):
  no deploy, spend, custody, or CAC policy expansion. Landing #3 does not
  authorize WordPress publish, OpenAI/Tavily spend, Coolify, or autonomy
  changes.

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

### Land (S0+S1+S2) — merge of PR `#3` or successor

Merging the product PR (complete S1+S2 diff) **is** close of
[#3](https://git.cl8y.com/code/wordpress-blog-ai-poster/issues/3). Close when
all of the following are true at that merge (not after a later iid):

1. None of the four Forgejo search paths exist on `main`
   (`test ! -e CODEOWNERS`, `test ! -e docs/CODEOWNERS`,
   `test ! -e .gitea/CODEOWNERS`, `test ! -e .forgejo/CODEOWNERS`). Same
   sentence as **H3-1** and test 1.
2. Merged tip contains `docs/adr/0001-remove-catchall-codeowners.md` and
   `docs/architecture.md` **byte-identical** to the independently accepted
   SHA (this SHA or a successor; not this tip until independent review).
   README relative links to those paths resolve. Do not merge a README that
   points at those paths until they exist on that tip. Architecture-only is
   not sufficient.
3. README states the **H3** gate and does not imply CODEOWNERS is what makes
   merge trusted. CLI usage remains. No stub escape.
4. Woodpecker `ci/woodpecker/pr/woodpecker` succeeded on that combined
   product PR; no deploy secrets ran on that PR event; existing `python` /
   `compileall` step remains.
5. Protection GET still matches **H3-2**, **H3-3**, **H3-5**, **H3-8**,
   **H3-9** (same list as test 3; operator attestation; not inferred from a
   green `compileall`; not **H3-4**; not observed flags).
6. No `force_merge`, no direct `main`, no CAC dismiss-as-merge, no
   Coolify/HMAC/`autonomy.rs`/WordPress-publish edits in the #3 diff.

Green Woodpecker on the **combined** product PR is necessary for merge. It
is sufficient for #3’s CI item. Draft `4a77cb8` is incomplete without S0
files and S2.

### Leftover-complete (S3) — follow-up; survives merge of `#3`

Require **one dated leftover comment** with all three items, **H3-1 last**
(or all three timestamps in one attest). A GET or plant-check from before a
later `_ensure_codeowners` apply does not count; re-delete via PR and write
a new comment.

1. Protection GET five flags: repo admin attests dated JSON: `GET
   .../branch_protections` `main` rule equals the five architecture
   **GET-required** flags (**H3-2**, **H3-3**, **H3-5**, **H3-8**, **H3-9**).
   Not the Merge API row. Not inferred from a green `compileall`.
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
executed on this repo by #48; this ADR only removes the in-tree file that
plants requests. Independent review of this proposal is a later gate.
Design author must not write `DESIGN: APPROVE`.

## Cross-links

- [#3](https://git.cl8y.com/code/wordpress-blog-ai-poster/issues/3)
- [cl8y-forgejo#48](https://git.cl8y.com/PlasticDigits/cl8y-forgejo/issues/48)
- [cl8y-forgejo INVARIANTS](https://git.cl8y.com/PlasticDigits/cl8y-forgejo/src/branch/main/docs/INVARIANTS.md)
- [cl8y-agent-control#388](https://git.cl8y.com/PlasticDigits/cl8y-agent-control/issues/388)
- [cl8y-agent-control#297](https://git.cl8y.com/PlasticDigits/cl8y-agent-control/issues/297)
- [`architecture.md`](../architecture.md)
- [code/hello#15](https://git.cl8y.com/code/hello/pulls/15) (canary delete)
