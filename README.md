# khmer-space-injector-mlops
End-to-end MLOps system for deploying a Khmer word segmentation (space injection) model using FastAPI, React, Neon PostgreSQL, and Google Cloud Compute Engine.

## Project Structure

```
khmer-space-injector-mlops/
├─ apps/
│  ├─ frontend/                                 # (Rattanak)
│  │  ├─ public/
│  │  ├─ src/
│  │  │  ├─ app/                               # pages/layout (router if used)
│  │  │  ├─ components/
│  │  │  ├─ features/
│  │  │  │  └─ segment/                        # textbox → call API → result
│  │  │  ├─ lib/
│  │  │  │  ├─ api.ts                          # typed fetch wrapper
│  │  │  │  └─ validators.ts                   # max length, basic checks
│  │  │  ├─ main.tsx
│  │  │  └─ vite-env.d.ts
│  │  ├─ tests/
│  │  │  └─ segment.test.tsx
│  │  ├─ index.html
│  │  ├─ package.json
│  │  ├─ tsconfig.json
│  │  └─ vite.config.ts
│  │
│  └─ api/                                      # (Virak)
│     ├─ app/
│     │  ├─ main.py                             # FastAPI entrypoint
│     │  ├─ api/
│     │  │  └─ routes/
│     │  │     ├─ health.py                     # GET /health (api+db check)
│     │  │     ├─ segment.py                    # POST /api/segment
│     │  │     └─ records.py                    # GET /api/records (optional)
│     │  ├─ core/
│     │  │  ├─ config.py                        # env + paths to artifacts
│     │  │  └─ logging.py
│     │  ├─ schemas/
│     │  │  ├─ segment.py                       # SegmentRequest/Response
│     │  │  └─ record.py                        # Record schema (db)
│     │  ├─ models/                             # SQLAlchemy models
│     │  │  └─ record.py                        # only record table
│     │  ├─ db/                                 # (Panha)
│     │  │  ├─ session.py
│     │  │  └─ repo/
│     │  │     └─ record_repo.py
│     │  └─ services/
│     │     ├─ segmenter.py                     # loads model + inference
│     │     ├─ artifacts.py                     # load config/vocab/checkpoint
│     │     ├─ normalizer.py                    # text normalization
│     │     ├─ net.py                           # model architecture
│     │     └─ utils.py                         # helper functions
│     │
│     ├─ artifacts/                             # (Seng coordinate, Virak uses)
│     │  ├─ checkpoint.pt
│     │  ├─ vocab.json
│     │  └─ config.json
│     │
│     ├─ tests/                                 # (Seng lead, Virak supports)
│     │  ├─ unit/
│     │  │  ├─ test_artifacts.py                # loading config/vocab
│     │  │  ├─ test_segmenter.py
│     │  │  └─ test_normalizer.py
│     │  ├─ api/
│     │  │  ├─ test_segment_route.py
│     │  │  └─ test_health_route.py
│     │  └─ integration/
│     │     └─ test_record_repo.py              # write/read record
│     │
│     ├─ alembic/                               # (Panha)
│     ├─ alembic.ini
│     ├─ requirements.txt
│     ├─ pyproject.toml
│     └─ Dockerfile
│
├─ packages/
│  └─ shared/                                   # (Seng)
│     ├─ constants/
│     │  ├─ routes.ts                           # "/api/segment", "/health"
│     │  └─ limits.ts                           # MAX_TEXT_LEN etc.
│     ├─ types/
│     │  ├─ segment.ts                          # SegmentRequest/Response types
│     │  └─ record.ts                           # optional for records endpoint
│     └─ fixtures/
│        ├─ khmer_samples.json
│        └─ expected_segments.json
│
├─ infra/                                       # (Seng)
│  ├─ nginx/
│  │  └─ default.conf                           # serve FE + proxy /api to FastAPI
│  ├─ scripts/
│  │  ├─ provision_vm.sh
│  │  ├─ deploy.sh
│  │  └─ db_migrate.sh
│  ├─ systemd/
│  │  ├─ fastapi.service
│  │  └─ nginx.service (optional)
│  └─ docker-compose.yml
│
├─ .github/
│  └─ workflows/                                # (Seng)
│     ├─ ci.yml                                 # lint+tests on PR
│     └─ cd.yml                                 # deploy to GCE on main
│
├─ .env.example                                 # (Panha + Seng)
├─ Makefile                                     # (Seng)
├─ README.md
└─ LICENSE

```