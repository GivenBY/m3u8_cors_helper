from fastapi import FastAPI, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from urllib.parse import urljoin, urlparse
import m3u8
import json

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

CONTENT_TYPES = {
    'm3u8': 'application/vnd.apple.mpegurl',
    'ts': 'video/MP2T',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'mp4': 'video/mp4',
    'aac': 'audio/aac',
    'm4s': 'video/iso.segment',
    'mpd': 'application/dash+xml',
    'html': 'text/html'
}

DEFAULT_HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate',
    'connection': 'keep-alive',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': 'Linux'
}

EXCLUDED_HEADERS = {
    "content-security-policy", "cross-origin-opener-policy", "cross-origin-embedder-policy",
    "cross-origin-resource-policy", "cross-origin-embedder-policy-report-only",
    "cross-origin-resource-policy-report-only", "content-encoding", "transfer-encoding"
}

@app.get("/cors")
async def cors(url: str, headers: str = None):
    if not all([urlparse(url).scheme, urlparse(url).netloc]):
        raise HTTPException(status_code=400, detail="Invalid URL")

    try:
        request_headers = DEFAULT_HEADERS.copy()
        if headers:
            request_headers.update(json.loads(headers))
        
        response = requests.get(url, headers=request_headers)
        response.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    response_headers = {k: v for k, v in response.headers.items() 
                       if k.lower() not in EXCLUDED_HEADERS}

    if url.endswith('.m3u8'):
        try:
            playlist = m3u8.loads(response.text)
            base_url = urljoin(response.url, ".")
            
            for item in (playlist.iframe_playlists + playlist.segments + 
                        (playlist.playlists if playlist.is_variant else [])):
                item.uri = f"/cors?url={urljoin(base_url, item.uri)}"
            
            content = playlist.dumps()
            content_type = CONTENT_TYPES['m3u8']
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"M3U8 parsing error: {e}")
    else:
        content = response.content
        content_type = CONTENT_TYPES.get(url.split('.')[-1].lower(), 'application/octet-stream')

    response_headers.update({
        'Content-Type': content_type,
        'Content-Length': str(len(content.encode('utf-8') if isinstance(content, str) else content)),
        'Content-Disposition': f'inline; filename="{urlparse(url).path.split("/")[-1] or "file"}"'
    })

    return Response(content=content, headers=response_headers, media_type=content_type)

@app.get("/")
def root():
    return {
        "message": "M3U8 CORS Provider",
        "usage": {
            "basic": "/cors?url={url_path}",
            "with_headers": "/cors?url={url_path}&headers={headers}"
        }
    }