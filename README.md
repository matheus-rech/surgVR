# PitVQA-VR Lab v1

Multimodal VR + Video dataset generator for surgical skill modeling.

## Components
- Unity XR simulation (Quest 3)
- Telemetry + event logging
- Python dataset + ML pipeline

## Output
dataset/sessions/session_x/
  - video.mp4
  - telemetry.json
  - events.json

## Run
Unity → build to Quest  
Python → train model

## Goal
Multimodal surgical skill prediction