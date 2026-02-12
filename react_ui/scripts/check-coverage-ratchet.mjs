import fs from 'node:fs';
import path from 'node:path';

const warnOnly = process.argv.includes('--warn-only');

const coverageSummaryPath = path.resolve('coverage', 'coverage-summary.json');
const baselinePath = path.resolve('config', 'coverage-baseline.json');

if (!fs.existsSync(coverageSummaryPath)) {
  console.error(`Coverage summary not found: ${coverageSummaryPath}`);
  console.error('Run `npm run test:coverage` first.');
  process.exit(1);
}

if (!fs.existsSync(baselinePath)) {
  console.error(`Coverage baseline not found: ${baselinePath}`);
  console.error('Create config/coverage-baseline.json before running ratchet checks.');
  process.exit(1);
}

const summary = JSON.parse(fs.readFileSync(coverageSummaryPath, 'utf8'));
const baseline = JSON.parse(fs.readFileSync(baselinePath, 'utf8'));
const totals = summary.total;

const metrics = ['statements', 'branches', 'functions', 'lines'];
const regressions = [];

for (const metric of metrics) {
  const current = Number(totals?.[metric]?.pct ?? 0);
  const required = Number(baseline?.[metric] ?? 0);

  if (current + Number.EPSILON < required) {
    regressions.push({ metric, current, required });
  }
}

if (regressions.length === 0) {
  console.log('Coverage ratchet passed.');
  for (const metric of metrics) {
    const pct = Number(totals[metric].pct).toFixed(2);
    console.log(`  ${metric}: ${pct}%`);
  }
  process.exit(0);
}

console.error('Coverage ratchet regression detected:');
for (const r of regressions) {
  console.error(`  ${r.metric}: current ${r.current.toFixed(2)}% < baseline ${r.required.toFixed(2)}%`);
}

if (warnOnly) {
  console.warn('Warn-only mode enabled; not failing process.');
  process.exit(0);
}

process.exit(1);
