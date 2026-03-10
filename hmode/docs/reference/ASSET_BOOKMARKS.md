# Asset Bookmarks SOP

**Rule:** When ANY asset is published to a URL, create a bookmark shortcut file.

**Location:** `/bookmarks/` directory

## Structure

```
bookmarks/
├── index.html              # Master index of all published assets
├── dossiers/               # Person research dossiers
│   ├── andrew-hopper.url
│   └── mark-oreta.url
├── deliveries/             # Customer deliveries
├── presentations/          # Published presentations
└── microsites/             # Published microsites
```

## URL Shortcut Format (.url files)

```ini
[InternetShortcut]
URL=https://bucket.s3.region.amazonaws.com/path/to/asset.html
```

## SOP Steps

1. After successful S3 publish, extract the URL
2. Create `.url` file in appropriate `/bookmarks/` subfolder
3. Filename = descriptive name (e.g., `andrew-hopper.url`)
4. Update `/bookmarks/index.html` with new entry
5. Commit changes

**Automation:** S3 publish scripts SHOULD auto-generate bookmark files.
