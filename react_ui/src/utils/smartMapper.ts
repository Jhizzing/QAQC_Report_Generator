// Heuristic logic to guess column meanings
export const guessMapping = (headers: string[]): Record<string, string> => {
    const mapping: Record<string, string> = {};
    const lowerHeaders = headers.map(h => h.toLowerCase());

    // Helper to find best match
    const findMatch = (patterns: string[]) => {
        const index = lowerHeaders.findIndex(h => patterns.some(p => h.includes(p)));
        return index !== -1 ? headers[index] : undefined;
    };

    // Sample ID
    const sampleId = findMatch(['sample', 'samp_id', 'sampleid', 'id']);
    if (sampleId) mapping['sampleId'] = sampleId;

    // Sample Type
    const sampleType = findMatch(['type', 'code', 'category', 'description']);
    if (sampleType) mapping['sampleType'] = sampleType;

    // Elements (Basic heuristic: look for _ppm, _pct, %)
    // In a real app, we'd have a periodic table list
    headers.forEach(h => {
        if (h.match(/(_ppm|_pct|%|ppm|pct)$/i) || ['Au', 'Ag', 'Cu', 'Pb', 'Zn'].includes(h)) {
            mapping[h] = h; // Map to itself for now, or normalize
        }
    });

    return mapping;
};
