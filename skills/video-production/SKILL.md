---
name: video-production
description: Choose a format, animation style, and production workflow for a visual explainer, product showcase, short film, or interactive browser story. Use for a new video brief when the user wants a recommendation, storyboard, or finished production.
---

# Video Production

1. Identify the audience, one thing they should understand or do afterward, source material, and requested deliverable. Distinguish a treatment, an editable animation, an exported video, and an interactive browser story. When the user wants a child to make choices and the format is unclear, distinguish pause-and-discuss moments in a video from clickable choices in a browser story.
2. Treat format, visual style, and renderer as separate decisions. Honor an explicit compatible style. For an open brief, recommend one direction and give up to two genuinely different options if the choice changes the experience or tooling. Say which repo to consult first and why. Ask only for choices that would materially change the output.
3. Read the matching workflow below as Markdown. Use the [repository catalog](references/repositories.md) to select sources and the [example prompts](references/example-prompts.md) to start the storyboard. Inspect only the examples, source files, or APIs relevant to the brief. Read [production checks](references/production-checks.md) for the selected deliverable.

| Brief | Workflow |
| --- | --- |
| Isometric process, hand-drawn story, pixel explainer, glass mosaic, or clickable illustrated story | [Stylized motion explainers](../stylized-motion-explainers/SKILL.md) |
| Browser-based 3D data chart, product spin, flight, physics, or postprocessing | [Three.js data animation](../threejs-data-animation/SKILL.md) |
| Editable Blender scene, exploded assembly, spatial explanation, or studio render | [Blender 3D explainers](../blender-3d-explainers/SKILL.md) |
| Proof, equation, or line-art teaching diagram where correctness drives the motion | [Animated maths diagrams](../animated-maths-diagrams/SKILL.md) |

For an internal AI showcase, show a familiar problem, the verified action the AI performs, and what the employee can do with the result. Base claims on supplied product evidence. Mark illustrative screens or data where viewers can see the distinction. For a child's story, tune vocabulary, scene length, and the number of choices to the child's age.

Make the storyboard before building. If the user asks for production and the format, renderer, and content are clear, proceed to a small preview and then the requested deliverable. Use the existing project stack when it can achieve the selected style. If required tooling is unavailable, state the dependency and offer a feasible option or a storyboard. Use the checks for the actual output.

For a rendered video, consider [Remotion](references/repositories.md#remotion) when you need a reusable React composition with animated maps or captions. When the video needs generated narration or captions from a recording, consider [VibeVoice](references/repositories.md#microsoft-vibevoice). Preview a representative scene with its final audio and captions before rendering the full video.
