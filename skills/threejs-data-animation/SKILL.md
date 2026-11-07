---
name: threejs-data-animation
description: Build browser-based 3D data charts, product spins, flythroughs, physics reveals, or glow effects with Three.js and compatible React extensions. Use when the user needs a scene in browser 3D or a video rendered from that scene.
---

# Three.js Data Animation

Read the [repository catalog](../video-production/references/repositories.md), the matching [example prompt](../video-production/references/example-prompts.md), and the relevant [production checks](../video-production/references/production-checks.md).

- **Three.js first for a 3D data chart.** Use scene geometry, camera, and materials to guide attention. Fix one scale and baseline, preserve magnitudes, and show units and values. Check that the final camera view keeps the comparison readable. Sample data should be visibly marked.
- **React Three Rapier for a domino reveal or Galton board.** Use it when the project already supports React Three Fiber and collisions should drive the result. Use a fixed time step and seeded inputs, or precompute the trajectories for stable frame capture.
- **React Postprocessing for Glow Atom.** In React Three Fiber, use it for bloom or a deliberate focus pull. Keep labels readable after the effect. A shell diagram should be labelled as a simplified model.
- **Three.js also supports product spins and flythroughs.** Check the exact subject, materials, camera path, and whether the ending needs to loop.

Drive the scene from an explicit timeline. Keep the camera testable separately from data and simulation. Deliver a browser preview or export according to the brief, and inspect the actual video if one was requested.
