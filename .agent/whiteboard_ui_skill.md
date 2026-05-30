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

## Validation Checklist

Before finishing HTML learning pages:

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
