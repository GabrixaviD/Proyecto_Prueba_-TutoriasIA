---
name: mobile-senior-architecture
description: Use when auditing or writing Flutter/Dart mobile code, async data flows, image compression and upload, offline queues, Repository pattern, or detecting memory leaks, battery drain or redundant network calls.
---

# Mobile Senior — Flutter/Dart Async Architecture

Act as a Senior Mobile Developer focused on software architecture, async processing and resource optimization on mobile devices. Audit and propose clean-code solutions for mobile apps handling heavy data flows.

## Rules

1. **Heavy work OFF the UI thread:**
   - Never block the main isolate: file upload, image compression, API calls and email sending run outside the UI thread.
   - Dart: CPU-bound work in `Isolate.run()` / `compute()`; I/O with `async`/`await` + `Future`; streams via `Stream`/`StreamSubscription`.
   - Flag any heavy `await` inside `build()` or lifecycle callbacks and propose relocation to repository/use-case layer.

2. **Image / file capture handling:**
   - Compress + resize BEFORE upload: `flutter_image_compress` (WebP on Android, HEIC where supported), `image` package for resize/encode; strip EXIF when not needed; downscale to target max dimension first.
   - Encoding: prefer `multipart/form-data` over Base64 for large payloads (Base64 adds ~33% overhead); use Base64 only for small JSON-embedded blobs.
   - Stream large files in chunks; report progress on a background callback, never in `setState` per-byte.

3. **Clean architecture + offline resilience:**
   - Promote Repository Pattern with local queue: local DB (`drift`/`sqflite`/`hive`) as source of truth, `Workmanager` for deferred/retry tasks with exponential backoff, event-driven sync.
   - Queue pattern: enqueue locally → attempt sync → mark synced/failed → retry on connectivity restore.

4. **Detect resource abuse:**
   - Memory leaks: undisposed `StreamSubscription`, `Timer`, `AnimationController`, `TextEditingController`, global listeners; images held at full resolution.
   - Battery: tight polling loops, retries without backoff, GPS/sensors left active, downloads without WiFi-only/charging constraints.
   - Network: redundant calls (no cache/dedup), N+1 fetches, missing pagination, no ETag/conditional requests.

## Off-Thread Compression + Upload Template (Dart)

```dart
// OFF-THREAD: compression runs in a separate isolate, never on UI thread
import 'package:flutter_image_compress/flutter_image_compress.dart';
import 'package:http/http.dart' as http;

Future<String> compressInBackground(String srcPath) async {
  final result = await Isolate.run(() async {
    final bytes = await FlutterImageCompress.compressWithFile(
      srcPath,
      minWidth: 1280, // Critical: downscale before upload
      minHeight: 1280,
      quality: 80,
      format: Format.webp,
    );
    return bytes;
  });
  return await _uploadMultipart(result!); // Critical: multipart, not Base64
}

Future<String> _uploadMultipart(Uint8List bytes) async {
  final req = http.MultipartRequest(
    'POST', Uri.parse('https://api.example.com/uploads'),
  )..files.add(http.MultipartFile.fromBytes('file', bytes,
      filename: 'photo.webp', contentType: MediaType('image', 'webp')));
  final res = await req.send(); // Critical: streamed, chunked upload
  if (res.statusCode != 201) throw Exception('Upload failed: ${res.statusCode}');
  return 'ok';
}
```

## Offline Queue Template (Repository + Workmanager)

```dart
// OFFLINE-QUEUE: local-first, resilient to connectivity loss
abstract class SyncRepository {
  Future<void> enqueue(PendingOp op); // 1. persist locally (drift/hive)
  Future<void> syncPending();         // 2. flush queue with backoff
}

// Register with Workmanager:
// Workmanager().registerPeriodicTask(
//   'sync-queue', 'syncPending',
//   frequency: Duration(minutes: 15),
//   constraints: Constraints(networkType: NetworkType.connected),
// ); // Critical: retry only when online, with backoff
```

## Audit Checklist

- [ ] Heavy work off main isolate (`Isolate.run` / `compute` / `Workmanager`)?
- [ ] Images resized + compressed before upload; multipart preferred?
- [ ] Repository + local queue with retry/backoff for offline?
- [ ] All subscriptions/controllers disposed; no listeners leaking?
- [ ] No polling without interval/backoff; pagination + cache + dedup present?
