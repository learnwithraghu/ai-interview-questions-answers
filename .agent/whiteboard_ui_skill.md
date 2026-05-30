# Whiteboard UI Skill

## Purpose

Use this skill when creating or updating standalone HTML learning pages for the AI Engineer Interview Bootcamp.

The goal is visual-first learning: teach the idea through slide-based diagrams, short labels, arrows, simple motion, and small examples before adding detail. Do not turn the answer markdown into a long HTML article.

## PaperBanana-Inspired Workflow

Use a lightweight creative loop inspired by PaperBanana:

1. **Extract:** Read the matching answer file and identify the one concept the learner must remember.
2. **Plan:** Pick a visual metaphor before writing HTML.
3. **Visualize:** Build the diagram as a full-screen slide deck with sparse text.
4. **Critique:** Check whether the page can be understood at a glance without reading paragraphs.
5. **Refine:** Remove text, simplify shapes, and improve placement until the visual carries the lesson.

## Source Discipline

- Use only the matching file in `answers/` as the source of truth.
- Rephrase and compress the answer for visual teaching.
- Do not add facts, examples, libraries, APIs, or claims that are not present in the source answer.
- Keep each page focused on one interview concept.

## Page Requirements

Every generated HTML file must be standalone and include:

- Valid `<!doctype html>`, `html`, `head`, and `body` structure.
- `<meta name="viewport" content="width=device-width, initial-scale=1.0">`.
- Self-contained CSS in a `<style>` tag.
- Self-contained JavaScript in a `<script>` tag only when needed for slide navigation.
- No external image, font, script, or CSS dependencies.
- A full-screen `.deck` layout with one active slide at a time.
- Exactly four slides:
  1. The original interview question from the matching answer markdown file.
  2. A visual explanation slide with 50-75 words of explanation.
  3. A second visual explanation slide with 50-75 words of explanation.
  4. The interview-ready answer from `### 4. This is how I would answer this`.
- Left and right arrow buttons.
- Keyboard navigation for `ArrowLeft` and `ArrowRight`.
- Compact slide progress text or dots.
- Bounded navigation: the deck must not wrap from the final slide back to slide 1.
- A small end note on slide 4 explaining that forward navigation stops there and the learner can use the left arrow to go back.
- A right-side LinkedIn logo link using inline SVG:

```html
<a class="linkedin-mark" href="https://www.linkedin.com/in/raghunandana-krishnamurthy-664264b7/" target="_blank" rel="noopener" aria-label="Built by Raghunandana KrishnaMurthy Sanur on LinkedIn">
  <svg viewBox="0 0 24 24" aria-hidden="true">
    <path d="M4.98 3.5C4.98 4.88 3.86 6 2.5 6S0 4.88 0 3.5 1.12 1 2.5 1s2.48 1.12 2.48 2.5zM.5 8h4V24h-4V8zm7.5 0h3.8v2.2h.06c.53-1 1.84-2.2 3.79-2.2C19.7 8 20.45 10.67 20.45 14.14V24h-4v-8.74c0-2.08-.04-4.76-2.9-4.76-2.9 0-3.35 2.27-3.35 4.61V24h-4V8z"/>
  </svg>
</a>
```

## Responsive Layout Rules

Design for every screen size first. Nothing should overlap, clip, or require page scrolling.

- Use `height: 100dvh` and `overflow: hidden` for the deck.
- Use `box-sizing: border-box` globally.
- Use grid or flexbox inside each slide. Avoid text-heavy absolute-positioned elements.
- Use `clamp()` for type, spacing, diagram nodes, and controls.
- Keep each slide's visible text short enough to fit on mobile without vertical scrolling.
- Keep slide 2 and slide 3 explanation copy between 50 and 75 words each.
- Place slide 2 and slide 3 explanation copy inside the main visual box, below or beside the diagram. Do not float the explanation outside the board.
- Prefer annotation chips, labels, callout bubbles, or mini decision cards over a single paragraph. The explanation should read like part of the diagram.
- Use `minmax(0, 1fr)`, `max-width`, and percentage widths instead of fixed screen assumptions.
- Use `overflow-wrap: anywhere` for code-like labels and long URLs.
- Keep controls in safe zones: arrows at horizontal edges, progress at bottom center, LinkedIn mark at right center.
- On small screens, shrink controls and diagram nodes instead of adding page scroll.

## Creator Credit Placement

The LinkedIn credit must be a right-side logo, not a text footer.

- Use an inline SVG LinkedIn `in` logo.
- Place it on the right side of the viewport, vertically centered.
- Keep it above the background but outside the main diagram focus area.
- Add an accessible label: `Built by Raghunandana KrishnaMurthy Sanur on LinkedIn`.
- Never use a bottom text footer for the credit in slide decks.

## Visual Style

Prefer a clean academic-illustration aesthetic:

- Light background with a subtle dot grid.
- Rounded diagram nodes with crisp outlines.
- A small palette of marker-like colors.
- Short labels, SVG arrows, loops, meters, lanes, and strong visual grouping.
- Friendly language that feels like a quick teaching board.
- A clear visual hierarchy: title, main diagram, tiny caption, controls.

Avoid:

- Dense paragraph dumps.
- Caption-like explanation paragraphs that simply sit under the diagram.
- Tiny text.
- Large blocks copied from the markdown answer.
- Decorative elements that reduce readability.
- Long vertical pages.
- More than one paragraph on a slide.
- Complex animations that distract from the concept.

## Suggested Page Pattern

```html
<main class="deck" data-deck>
  <a class="linkedin-mark" href="https://www.linkedin.com/in/raghunandana-krishnamurthy-664264b7/" target="_blank" rel="noopener" aria-label="Built by Raghunandana KrishnaMurthy Sanur on LinkedIn">
    <!-- inline SVG logo -->
  </a>

  <section class="slide active" data-slide>
    <p class="eyebrow">Question 01</p>
    <h1>What is the difference between a system prompt, a user prompt, and an assistant response?</h1>
  </section>

  <section class="slide" data-slide>
    <h2>Visual explanation</h2>
    <div class="board explain-board">
      <div class="diagram"><!-- visual metaphor first --></div>
      <div class="explain" data-explain>
        <span><strong>Signal:</strong> short annotation chip.</span>
        <span><strong>Rule:</strong> another scan-friendly chip.</span>
      </div>
    </div>
  </section>

  <section class="slide" data-slide>
    <h2>Visual explanation</h2>
    <div class="board explain-board">
      <div class="diagram"><!-- second visual angle --></div>
      <div class="explain" data-explain>
        <span><strong>Watch:</strong> visual callout.</span>
        <span><strong>Fix:</strong> visual callout.</span>
      </div>
    </div>
  </section>

  <section class="slide" data-slide>
    <h2>Say it</h2>
    <p class="say-line">...</p>
    <p class="end-note">End: this deck stops here. Use the left arrow to review earlier slides.</p>
  </section>

  <button class="nav prev" type="button" aria-label="Previous slide">‹</button>
  <button class="nav next" type="button" aria-label="Next slide">›</button>
  <div class="progress" aria-live="polite">1 / 4</div>
</main>
```

## Grid Layout Rules

When using CSS Grid for flow diagrams (boxes + arrows in a row):

- Count every child element, including arrow divs. A 4-box + 3-arrow flow has **7 children**, not 4.
- The `grid-template-columns` definition must match the exact child count. `repeat(4,1fr)` for 7 children will wrap and break the diagram.
- Use an explicit mixed template for flow diagrams: `1fr auto 1fr auto 1fr` (or extend the pattern). Arrow columns are `auto`; content columns are `1fr`.
- Never use `repeat(N, 1fr)` for a flow that contains arrow divs — it gives arrow divs the same width as content boxes and causes wrapping when children exceed N.
- **Maximum 4 boxes in a single horizontal flow row.** If the concept has 5 or more steps, use the two-phase split pattern instead (see below).
- When diagrams and explain chips share a board, the diagram must be visually lean — title-only labels, short subtitles, no paragraphs inside diagram nodes. All explanatory text goes in the chips below.
- Limit explain chips to 4 per slide so diagram + chips fit without overflow inside the board.

## Arrow and Connector Rules

- Always use the Unicode right arrow `→` (not ASCII `->` or HTML entity `-&gt;`) for horizontal flow connectors.
- Always use the Unicode down arrow `↓` for vertical flow connectors.
- In the CSS, arrow columns must be `auto` width — never `1fr`. This keeps arrows narrow and lets content boxes take the available space.
- Arrow font size: `clamp(1rem, 2.2vw, 1.8rem)` — do not scale arrows as large as headings.
- On mobile when a horizontal flow collapses to a single column, add `transform: rotate(90deg)` on the `.flow-arrow` so horizontal `→` visually becomes `↓`.

## Two-Phase Layout Pattern (for 5+ step concepts)

When a concept has a "model decides / your code acts" boundary, or any natural 2-phase split, use a stacked two-phase layout instead of a single horizontal row:

```html
<div class="two-phase">
  <div><span class="phase-label" style="background:#dbeafe;color:#1d4ed8">Phase 1 label</span></div>
  <div class="phase-row-sm">
    <!-- 2–3 boxes + arrows for phase 1 -->
  </div>
  <div class="handoff">↓ &nbsp; transition label &nbsp; ↓</div>
  <div><span class="phase-label" style="background:#dcfce7;color:#15803d">Phase 2 label</span></div>
  <div class="phase-row">
    <!-- 3 boxes + arrows for phase 2 -->
  </div>
</div>
```

CSS for the two-phase pattern:
```css
.two-phase { width: min(820px, 100%); display: grid; gap: clamp(6px, 1.2vw, 10px); }
.phase-label { font-size: clamp(.7rem, 1.3vw, .82rem); font-weight: 900; letter-spacing: .1em; text-transform: uppercase; padding: 3px 10px; border-radius: 999px; display: inline-block; width: fit-content; }
.phase-row  { display: grid; grid-template-columns: 1fr auto 1fr auto 1fr; gap: clamp(6px, 1.2vw, 10px); align-items: center; }
.phase-row-sm { display: grid; grid-template-columns: 1fr auto 1fr; gap: clamp(6px, 1.2vw, 10px); align-items: center; }
.handoff { text-align: center; font-size: clamp(.72rem, 1.3vw, .85rem); font-weight: 900; color: var(--muted); padding: clamp(4px, 0.8vw, 6px) 0; border-top: 2px dashed #cbd5e1; border-bottom: 2px dashed #cbd5e1; margin: 2px 0; }
.flow-box { border: 3px solid var(--line); border-radius: 14px; padding: clamp(8px, 1.5vw, 13px); text-align: center; font-weight: 900; font-size: clamp(.7rem, 1.4vw, .88rem); box-shadow: 3px 3px 0 rgba(15,23,42,.06); }
.flow-arrow { text-align: center; font-size: clamp(1rem, 2vw, 1.6rem); font-weight: 900; padding: 0 2px; }
```

Mobile override: collapse both phase rows to single column and rotate arrows.

## Nav Button Rules

Navigation buttons must always use single-chevron characters, never angle brackets:

- **Correct:** `&lsaquo;` (renders as `‹`) and `&rsaquo;` (renders as `›`)
- **Wrong:** `&lt;` / `&gt;` (renders as `<` and `>` — looks like HTML markup, not navigation)

```html
<button class="nav prev" type="button" aria-label="Previous slide">&lsaquo;</button>
<button class="nav next" type="button" aria-label="Next slide">&rsaquo;</button>
```

## Validation Checklist

Before finishing HTML learning pages:

- **Count grid children vs columns:** for every grid-based diagram, verify the `grid-template-columns` column count exactly matches the number of direct children.
- **Arrow characters:** every flow connector div uses `→` (Unicode) not `->` or `-&gt;`. Vertical connectors use `↓`.
- **Arrow CSS columns:** arrow divs sit in `auto`-width columns, never `1fr` — confirm no `repeat(N,1fr)` template contains arrow divs.
- **Flow row length:** no single horizontal flow row has more than 4 content boxes. If 5+ steps needed, the two-phase layout pattern is used.
- **Nav buttons:** prev/next buttons use `&lsaquo;` / `&rsaquo;`, not `&lt;` / `&gt;`.
- Open every page at mobile, tablet, laptop, and wide desktop widths.
- Confirm there is no horizontal overflow.
- Confirm no text overlaps another element.
- Confirm the document does not require vertical page scrolling.
- Confirm the LinkedIn logo is visible on the right side and not overlaying controls or the main diagram.
- Confirm arrow buttons and keyboard arrows change slides.
- Confirm the right arrow stops on slide 4 instead of wrapping to slide 1.
- Confirm the left arrow can navigate back from slide 4.
- Confirm slide 2 and slide 3 each have 50-75 words of explanation.
- Confirm slide 2 and slide 3 explanations are inside the bordered visual box, split into visual annotation chips, and do not overlap the diagram.
- Confirm slide 4 includes a small end note.
- Confirm the page works without network access.
- Confirm each page uses only details from its matching answer markdown file.
