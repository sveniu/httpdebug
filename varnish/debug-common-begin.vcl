if (req.http.x-debug-key && req.http.x-debug-key != "mydebugkey") {
    /* Remove debug headers due to key mismatch */
    remove req.http.x-debug-level;
    remove req.http.x-debug-key;
}
if (req.http.x-debug-level) {
