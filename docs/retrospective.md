# Final Retrospective — AquaFlow / Garbusa Capstone
**Date**: 2026-10-08
**Team**: Bukidnon / Northern Mindanao Group
**Focus**: Blameless — learning, not blame

---

## ✅ What Went Well

### Technical
- Fast recovery from critical issues: `package.json` syntax error diagnosed and fixed within the same session ✅
- Git workflow learned end-to-end: branch → fix → PR → review → merge → sync ✅
- Codespaces environment consistent across team members
- Optional chaining (`?.`) adopted early — prevented multiple crash scenarios on loading states
- Refactoring done cleanly: extracted `StationCard` component — removed duplication without breaking anything ✅
- All merges resolved; no work permanently lost or stranded

### Process & Collaboration
- Immediate communication when stuck — no multi-hour blockers
- Clear task separation: P0 (blocker) → P1 (feature/crash) → Tech Debt → Documentation
- PR descriptions thorough enough to review without re-reading code
- Local-first then push pattern followed consistently
- Everyone contributed to troubleshooting — shared knowledge grew fast

### Personal & Team
- Kept going through confusing moments — divergence conflicts, untracked files, wrong-paste errors all solved together
- Adapted to different tools: terminal, Codespaces, GitHub web editor
- Maintained positive tone — errors framed as learning opportunities

---

## ⚠️ What Didn't Go Smoothly

### Git & Workflow Pain Points
- Divergent branches happened repeatedly — local commits existed before pulling remote changes → `git pull` stalled without a strategy
- Untracked folders (`docs/pr-logs/`) conflicted with remote additions → merge state got tangled
- Pasting code directly into terminal caused syntax errors — mix-up between "where to type commands" vs "where to edit files"
- No agreed `pull.rebase` default → every merge needed extra flags

### Communication & Clarity
- File paths unclear early — searching for `src/` when actual code lived in `aquaflo-dashboard/src/` wasted time
- Naming inconsistency across branches: `fix/p1-loading-state-crash`, `feature/update-station-header`, `refactor/extract-station-card` — good names, but no single template
- Review process manual — no automated checks ran locally before push → CI caught issues later

### Technical & Scope Creep
- "While I'm here" urge appeared — early attempts to rewrite unrelated code alongside fixes
- No local test command run habit — `npm run test` / `npm run build` only checked after PR opened
- Commit messages sometimes vague — "fix stuff" instead of specific changes

---

## 🔄 What We'd Change Next Time

### Workflow & Setup
- **Set Git defaults on day one**:
  ```bash
  git config --global pull.rebase false   # merge strategy clear for everyone
