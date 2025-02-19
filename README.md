# m3u8_cors_helper

### GET /cors

Proxies M3U8 playlists and media segments with CORS support.

Parameters:

- `url` (required): The URL of the M3U8 playlist or media segment
- `headers` (optional): JSON string of custom headers to include in the request

Example:

```bash
# Basic usage
curl "http://localhost:8000/cors?url=https://example.com/playlist.m3u8"

# With custom headers
curl "http://localhost:8000/cors?url=https://example.com/playlist.m3u8&headers={\"Referer\":\"https://example.com\"}"
```

### GET /

Returns API usage information and documentation.

## Supported Media Types

- M3U8 Playlists (`.m3u8`)
- MPEG-2 Transport Stream (`.ts`)
- JPEG Images (`.jpg`, `.jpeg`)
- PNG Images (`.png`)
- MP4 Video (`.mp4`)
- AAC Audio (`.aac`)
- MPEG-DASH Segments (`.m4s`)
- DASH Manifests (`.mpd`)
- HTML Files (`.html`)

## Error Handling

The server returns appropriate HTTP status codes:

- 400: Invalid URL or headers
- 500: Server error or upstream request failure

## Security Considerations

- The server allows all CORS origins (`*`)
- No authentication is implemented by default
- Consider adding rate limiting for production use
- Review and adjust CORS settings based on your needs

## Example Usage

### Basic M3U8 Playlist Request

```javascript
fetch("http://localhost:8000/cors?url=https://example.com/playlist.m3u8")
  .then((response) => response.text())
  .then((data) => console.log(data));
```

### Request with Custom Headers

```javascript
const headers = JSON.stringify({
  Referer: "https://example.com",
  "User-Agent": "Custom User Agent",
});

fetch(
  `http://localhost:8000/cors?url=https://example.com/playlist.m3u8&headers=${encodeURIComponent(
    headers
  )}`
)
  .then((response) => response.text())
  .then((data) => console.log(data));
```

## Production Deployment

For production deployment, consider:

1. Adding authentication
2. Implementing rate limiting
3. Setting specific CORS origins
4. Using HTTPS
5. Adding monitoring and logging
6. Setting up proper error handling

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/name`)
3. Commit your changes (`git commit -am 'Add feature'`)
4. Push to the branch (`git push origin feature/name`)
5. Create a Pull Request
