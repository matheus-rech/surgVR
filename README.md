# PitVQA-VR Lab v1

Multimodal VR + Video dataset generator for surgical skill modeling.

## Components
- Unity XR simulation (Quest 3)
- Telemetry + event logging
- Python dataset + ML pipeline

## Output
`Application.persistentDataPath` (on-device session output)
  - `${sessionId}/telemetry.json`
  - `${sessionId}/events.json`

## Run
Unity → build to Quest  
Python → `python python/train.py`

The repository includes `dataset/sessions/demo_session/` so the Python pipeline can be exercised end to end from a fresh clone. If PyTorch is unavailable, `python/train.py` automatically runs a lightweight standard-library fallback so the demo still works.

## Goal
Multimodal surgical skill prediction
