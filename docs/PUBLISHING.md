# Publishing: YouTube, archive.org and the feed

The runbook for putting a finished set online, as done for WeatherDreamer (Nov 17, 2026: 2 videos, 5 shorts,
episode 30). Agents do this with Claude in Chrome in the owner's browser. Publishing is public and outward-facing:
get the owner's explicit go-ahead first (a permission check blocked the first Publish click until they gave it), and
publish in this order: archive.org, then YouTube, then the feed (the feed links to the archive.org file).

## Files bigger than the browser tool's 10.4 MB limit

The extension's `file_upload` rejects anything over ~10 MB. Instead, serve the files locally and hand them to the
page's own file input:

```sh
# a folder of symlinks + meta.json (titles/descriptions), served with CORS on 127.0.0.1:8765
python3 serve.py <folder>      # SimpleHTTPRequestHandler + 'Access-Control-Allow-Origin: *'
```
```js
// in the page (javascript_tool): fetch -> File -> DataTransfer -> the input -> 'change'
const b = await fetch('http://127.0.0.1:8765/loop.mp4').then(r => r.blob());
const dt = new DataTransfer(); dt.items.add(new File([b], 'name.mp4', {type: 'video/mp4'}));
inp.files = dt.files; inp.dispatchEvent(new Event('change', {bubbles: true}));
```
If the call times out on a big file (archive.org did), start the fetch without awaiting it, store the result in a
`window.__status` variable, and read that variable in a second call.

## YouTube Studio (The AIGS Pod)

- **Channel:** Studio may open on the owner's personal channel. Avatar → Switch account → **The AIGS Pod** (@aigspod,
  "You're a manager", under the owner's own Google account).
- **Upload:** upload icon → `ytcp-uploads-dialog input[type=file]` (accepts several files). Each becomes a private
  draft; open each from the progress panel's pencil or Content → "Edit draft".
- **Details:** title and description are `ytcp-uploads-dialog #textbox` (0 and 1): focus, `execCommand('selectAll')`,
  `execCommand('insertText', ...)`. Descriptions can't contain `<` or `>`. Thumbnail: `#file-loader`.
  Radios by name: `VIDEO_MADE_FOR_KIDS_NOT_MFK`; click "Show more", then `VIDEO_PAID_PRODUCT_PLACEMENT_NO` and
  `VIDEO_HAS_ALTERED_CONTENT_NO` (the owner's confirmed settings: public, not for kids, no paid promotion, altered
  content No).
- **Captions** (`captions.srt` from `out/narrated/`): `#next-button` → Video elements → Subtitles "Add" (for long
  videos it is the first "Add"; for **shorts the first "Add" is Related video**, Subtitles is the second) → click
  "Upload file". A "With timing / Without timing" modal appears: **don't click Continue** (it opens a native file
  picker the tool can't drive). The hidden `#captions-file-loader` input exists once the modal is up: set the SRT on
  it and dispatch `change`, then click **Done**. Check the dialog says "English by you".
  - Shorts sometimes open the subtitle editor in plain-text mode with a transcript already filled in. Use the editor's
    ⋮ menu → "Upload file" to reach the same modal, then set `#captions-file-loader` as above.
  - If the row still says "English by YouTube (automatic)", open Languages → Edit subtitles: if it shows our timed
    lines, it's saved.
- **Publish:** `#next-button` until the Visibility step, click radio `PUBLIC`, then the Publish button (a real click).
  The "Video published" dialog shows the youtu.be / youtube.com/shorts link: record it in the topic's `AGENTS.md`.

## archive.org (the podcast MP3)

- Signed in as **AIGROUP ESSM** (`aigroupe3sm`), the owner's account; if it isn't signed in, the owner logs in
  themselves.
- `archive.org/upload/` → `#file_input_initial` (via the local server; see above; check the file list for a
  duplicate if a timed-out call also succeeded).
- Metadata follows the earlier items (`archive.org/metadata/epiplexity-pod/metadata`): title "<Topic> Pod", page URL
  `<topic>-pod`, description "podcast", subject tag "podcast", collection Community audio. Wait for the identifier
  check to finish before "Upload and Create Your Item".
- Verify: `curl -sIL https://archive.org/download/<topic>-pod/<File>.mp3` → 200, `audio/mpeg`, the right length.

## The feed (`aigspod.github.io`)

- Add an `<item>` above the newest one in `feed.xml`, modelled on it: question-style `<title>`, description (an aigs pod
  extra / journal-club line, "Narrated by a synthetic voice (Kokoro, "Bella")", the paper link), enclosure URL and exact
  byte `length`, `guid` `aigspod-epNNN-<topic>`, `pubDate`, `itunes:image` `images/epNNN.png` (1400 × 1400, from the
  episode's `cover.py`, with "the aigs pod · episode NN"), `itunes:duration`, summary, `itunes:episode` NN.
- `images/thumbs/epNNN.jpg` is the same art at 640 px (`sips -s format jpeg -Z 640`).
- **An aigs pod extra (not a journal-club paper) must stay off the /mull/ desk**, which lists every feed episode by
  itself: add its keys to `NOT_ON_DESK` in `mull/index.html`, both the paper link and `ep<N>` (the desk keys an episode
  by the URL right after "Paper:" in its description, else by `ep<N>`; ours start "Paper: Authors, ..."). Check the
  page locally (`python3 -m http.server`, open `/mull/`) before pushing.
- **Shorts point to their full video:** set each short's Related video (Studio, the short's details page, "Related
  video" pencil; or Video elements → Related video at upload) and put `▶ The full story (N-minute video): <link>` on the
  first line of its description. Link the long video that answers the short's question.
- Check `feed.xml` parses (`python3 -c "import xml.dom.minidom; xml.dom.minidom.parse('feed.xml')"`), commit on `main`
  ("Add episode NN: <title>"), push.

## After publishing

Record links and ids in the topic's `AGENTS.md` files (see `projects/epiplexity/videos/AGENTS.md` "Published"), then
commit the aiglainer branch.
