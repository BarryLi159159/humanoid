## Big Picture (2025 → 2026)

1. **The stack converged.** A "cerebellum" (one general whole-body tracker, e.g. GMT, SONIC, HoloMotion, Humanoid-GPT) sits under a "brain" (VLA, planner, motion generator, or teleoperator). Most 2026 papers are about one of the two layers or the interface between them.
2. **The training recipe converged.** *Specialist RL experts → DAgger distillation into one (often Transformer / MoE / flow-matching) student → RL or residual finetuning for the long tail and for sim-to-real.* OmniXtreme, Athena-WBC, Humanoid-GPT, BumbleBee, UniTracker all follow variants of it.
3. **Data moved from mocap → video → robot-free devices.** AMASS-scale mocap (2025), video-reconstructed motion (HoloMotion's 2000+ h corpus, PHUMA, VideoMimic), then UMI-style robot-free humanoid data (HuMI, EgoHumanoid, BifrostUMI).
4. **The bottleneck moved up the stack.** Tracking fidelity is no longer the main blocker; *producing good, feasible, task-grounded references* (from perception, language, or VLAs) and *physical interaction* (force, objects, scenes) are.
5. **Evaluation is the weakest link.** Almost every "state of the art" claim is on a self-defined protocol, on one robot (overwhelmingly Unitree G1), with qualitative real-world videos.

**Cross-cutting open problems**

- A shared, real-robot-validated benchmark for whole-body tracking and loco-manipulation.
- Force-aware whole-body interaction with real contact sensing, beyond proprioceptive force inference.
- A principled VLA ↔ WBC interface with feasibility feedback (today the VLA does not know what the tracker can execute).
- Cross-embodiment controllers that transfer without per-robot retraining.
- Actuator-level modeling for highly dynamic motions (the real sim-to-real limit for acrobatics).
