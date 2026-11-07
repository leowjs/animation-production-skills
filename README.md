# Animation Production Skills

A versioned skill set for planning and building code-rendered explainers, short videos, and illustrated browser stories in **Codex** and **Claude Code**.

Use it to show an audience what a product can do, visualize an analytical result, or tell an age-appropriate story with optional choices. The entry skill recommends an animation direction and finds relevant code, style guides, or examples.

## Install

Download and extract the source archive from the [latest release](https://github.com/leowjs/animation-production-skills/releases/latest), or clone the tagged version:

```sh
git clone --branch v1.0.0 https://github.com/leowjs/animation-production-skills.git
cd animation-production-skills
```

Copy the **five folders inside `skills/`** directly into the destination for your client. Keep the folders together so their shared catalog links resolve. Choose one scope per client.

| Client | Personal skills folder | Project skills folder | Start with |
| --- | --- | --- | --- |
| Codex | `~/.agents/skills/` | `.agents/skills/` in your project | `$video-production` |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` in your project | `/video-production` |

On Windows, `~` is your user profile. Run the following PowerShell commands from the extracted or cloned repository. Use the block for your client, or both if you use both.

```powershell
# Codex
$skillDestination = Join-Path $env:USERPROFILE '.agents/skills'
New-Item -ItemType Directory -Path $skillDestination -Force | Out-Null
Copy-Item -Path './skills/*' -Destination $skillDestination -Recurse -Force

# Claude Code
$skillDestination = Join-Path $env:USERPROFILE '.claude/skills'
New-Item -ItemType Directory -Path $skillDestination -Force | Out-Null
Copy-Item -Path './skills/*' -Destination $skillDestination -Recurse -Force
```

On macOS or Linux, run the matching block from the repository root:

```sh
# Codex
mkdir -p ~/.agents/skills
cp -R skills/* ~/.agents/skills/

# Claude Code
mkdir -p ~/.claude/skills
cp -R skills/* ~/.claude/skills/
```

Start a new session in the client and select the skill. Installation copies Markdown instructions and references. Rendering dependencies are specific to the workflow and project. See the official guides for [Codex skills](https://learn.chatgpt.com/docs/build-skills) and [Claude Code skills](https://code.claude.com/docs/en/skills).

## Try it

- **Codex:** `$video-production Plan a 45-second employee showcase for an AI assistant that answers common policy questions. Recommend a style and use mock data.`
- **Claude Code:** `/video-production Create a browser story for a six-year-old about a seed finding water. Let the child make two choices.`
- **Isometric starter:** [Open the saved example prompt](skills/video-production/references/example-prompts.md#01-isometric-explainer).

## Skills and references

- [Video Production](skills/video-production/SKILL.md) handles brief, format, and style selection.
- [Stylized Motion Explainers](skills/stylized-motion-explainers/SKILL.md) covers illustrated motion and clickable stories.
- [Three.js Data Animation](skills/threejs-data-animation/SKILL.md) covers web 3D, charts, physics, and effects.
- [Blender 3D Explainers](skills/blender-3d-explainers/SKILL.md) covers editable Blender scenes and rendered explainers.
- [Animated Maths Diagrams](skills/animated-maths-diagrams/SKILL.md) covers proofs, scientific diagrams, and annotations.

The [repository catalog](skills/video-production/references/repositories.md) explains what each source does best. The [prompt catalog](skills/video-production/references/example-prompts.md) pairs all 41 source examples with independently worded adaptations.

## Updates and license

The first release is **v1.0.0**. To upgrade, download the newer release and repeat the copy steps. Review the [release notes](https://github.com/leowjs/animation-production-skills/releases) and keep any local edits in a separate copy.

See [LICENSE](LICENSE) for the original instructions and adaptations in this repository. Linked code, assets, original prompts, and media have their own terms.
