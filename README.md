# Earnies Production

A glassy little studio for your beats, projects and collaborations. It installs on iPhone and PC as an app.

**Open it:** https://ernstemileggummyrvang-sketch.github.io/earnies-production/

- **iPhone:** open the link in Safari, tap Share, then **Add to Home Screen**.
- **PC or Mac:** open it in Chrome or Edge and click the install icon in the address bar.

Everything you add is stored on that device (browser storage), and the app works offline.

## Cloud sync (Backblaze B2)

Tap **Transfer › Cloud sync › Set up** and follow the steps: a free Backblaze account, a private bucket, an application key, and one Terminal command on the Mac that lets the app talk to the bucket (it sets the bucket's CORS rules). Then tap **Connect** and paste the code it gives you into the iPhone. From then on every device syncs on open and after each change. The library lives in `earnies/library.json` in your bucket, audio and art under `earnies/files/`. The key is stored only on your own devices.

## Moving beats between devices without an account

Tap **Transfer** at the top. **Export** saves your whole library (beats, songs, projects, collaborators, folders and cover art, with WAVs untouched) into one `.earnies` file. Send it to the other device, for example with AirDrop from the Mac's Downloads folder, then tap **Transfer › Import** there and pick the file. Beats that are already on that device are matched by name and length, and you choose to replace them, skip them or keep both.

## Editing

Edit `src/earnies-production.html`, then run `python3 build.py` to regenerate `index.html`, `manifest.webmanifest` and `sw.js`.
