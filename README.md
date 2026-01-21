# khmer-space-injector-mlops
End-to-end MLOps system for deploying a Khmer word segmentation (space injection) model using FastAPI, React, Neon PostgreSQL, and Google Cloud Compute Engine.

## Project Structure

```
khmer-space-injector-mlops/
├─ .env.example
├─ .gitignore
├─ LICENSE
├─ Makefile
├─ README.md
├─ package.json
├─ package-lock.json
│
├─ .github/
│  ├─ PULL_REQUEST_TEMPLATE.md
│  └─ workflows/
│     ├─ cd.yml
│     └─ ci.yml
│
├─ apps/
│  ├─ api/
│  │  ├─ Dockerfile
│  │  ├─ alembic.ini
│  │  ├─ pyproject.toml
│  │  ├─ requirements.txt
│  │  ├─ artifacts/
│  │  │  ├─ checkpoint.pt
│  │  │  ├─ config.json
│  │  │  └─ vocab.json
│  │  ├─ app/
│  │  │  ├─ main.py
│  │  │  ├─ main_state.py
│  │  │  ├─ api/
│  │  │  │  ├─ deps.py
│  │  │  │  └─ routes/
│  │  │  │     ├─ health.py
│  │  │  │     ├─ history.py
│  │  │  │     ├─ metrics.py
│  │  │  │     ├─ records.py
│  │  │  │     └─ segment.py
│  │  │  ├─ core/
│  │  │  │  ├─ config.py
│  │  │  │  ├─ logging.py
│  │  │  │  └─ metrics.py
│  │  │  ├─ db/
│  │  │  │  ├─ session.py
│  │  │  │  └─ repo/
│  │  │  │     └─ record_repo.py
│  │  │  ├─ models/
│  │  │  │  └─ record.py
│  │  │  ├─ schemas/
│  │  │  │  ├─ history.py
│  │  │  │  ├─ record.py
│  │  │  │  └─ segment.py
│  │  │  ├─ services/
│  │  │  │  ├─ artifacts.py
│  │  │  │  ├─ net.py
│  │  │  │  ├─ normalizer.py
│  │  │  │  ├─ segmenter.py
│  │  │  │  └─ utils.py
│  │  │  └─ utils/
│  │  │     └─ time.py
│  │  └─ tests/
│  │     ├─ api/
│  │     │  ├─ conftest.py
│  │     │  ├─ test_health_route.py
│  │     │  ├─ test_history_route.py
│  │     │  └─ test_segment_route.py
│  │     ├─ integration/
│  │     │  ├─ test_db_repos.py
│  │     │  └─ test_record_repo.py
│  │     └─ unit/
│  │        ├─ test_artifacts.py
│  │        ├─ test_normalizer.py
│  │        └─ test_segmenter.py
│  │
│  └─ frontend/
│     ├─ index.html
│     ├─ package.json
│     ├─ package-lock.json
│     ├─ tsconfig.json
│     ├─ tsconfig.node.json
│     ├─ vite.config.ts
│     └─ src/
│        ├─ main.tsx
│        ├─ vite-env.d.ts
│        ├─ index.css
│        ├─ app/
│        │  ├─ App.tsx
│        │  └─ App.css
│        └─ features/
│           ├─ segment/
│           │  ├─ Segment.tsx
│           │  ├─ Segment.css
│           │  └─ segmentApi.ts
│           └─ history/
│              ├─ HistoryPage.tsx
│              ├─ HistoryPage.css
│              └─ historyApi.ts
│
├─ infra/
│  ├─ nginx/
│  │  └─ default.conf
│  ├─ scripts/
│  │  ├─ db_migrate.sh
│  │  ├─ deploy.sh
│  │  └─ provision_vm.sh
│  └─ systemd/
│     └─ fastapi.service
│
└─ packages/
   └─ shared/
      ├─ constants/
      │  ├─ limits.ts
      │  └─ routes.ts
      ├─ types/
      │  ├─ record.ts
      │  └─ segment.ts
      └─ fixtures/
         ├─ expected_segments.json
         └─ khmer_samples.json
