import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const root = path.dirname(fileURLToPath(import.meta.url));
const workspace = path.join(root, 'virtual-workspace');
const cliRoot = '/home/alanrichard/.local/lib/node_modules/@tiendanube/cli';
const cliSource = await fs.readFile(path.join(cliRoot, 'dist/cli.js'), 'utf8');
const expected = new Map([
  ['sections/hero.tpl', '06dded46e359d68648c05253eff315e5c124e9c1d30313b0ea0b8e2c7ac7062c'],
  ['snippets/image.tpl', '447a9b23e2cbe7ac752f804a754d8e99ad87cd32449c41aa658fa919e18a32b5'],
]);
const require = createRequire(path.join(cliRoot, 'package.json'));
const { readdirpPromise } = require('readdirp');
const prefixes = ['blocks', 'config', 'custom', 'layouts', 'sections', 'snippets', 'static', 'templates', 'translations', 'manifest.json'];
const shouldSync = relativePath => {
  const norm = relativePath.replaceAll('\\', '/');
  const parts = path.normalize(relativePath).split(/[\\/]/).filter(Boolean);
  const hidden = parts.some(s => s.startsWith('.') && s !== '.' && s !== '..');
  return !hidden && prefixes.some(prefix => norm === prefix || norm.startsWith(`${prefix}/`));
};

const scanned = await readdirpPromise(workspace, {
  alwaysStat: true,
  directoryFilter: entry => shouldSync(entry.path),
  fileFilter: entry => shouldSync(entry.path),
});
const paths = scanned.map(entry => path.relative(workspace, entry.fullPath).replaceAll('\\', '/')).sort();
assert.deepEqual(paths, [...expected.keys()].sort(), 'workspace scan includes exactly the two authorized candidate files');

const fileEvidence = [];
for (const [relative, expectedSha] of expected) {
  const content = await fs.readFile(path.join(workspace, relative));
  const actualSha = crypto.createHash('sha256').update(content).digest('hex');
  assert.equal(actualSha, expectedSha, `${relative} SHA256 matches frozen candidate`);
  fileEvidence.push({ path: relative, sha256: actualSha, bytes: content.length });
}

const checkStart = cliSource.indexOf('var ThemeApiCheckCommand = class');
const checkEnd = cliSource.indexOf('// src/category/theme/api/commands/', checkStart + 1);
const checkCommand = cliSource.slice(checkStart, checkEnd > checkStart ? checkEnd : checkStart + 4000);
assert.ok(checkCommand.includes('const files = [...diff.toCreate, ...diff.toUpdate]'), 'theme check validates only local creates/updates');
assert.ok(!checkCommand.includes('diff.toDelete'), 'theme check does not send remote deletions to validation');
assert.ok(checkCommand.includes('validateThemeFiles({') && checkCommand.includes('files,'), 'check passes its exact file list to validation');

const planStart = cliSource.indexOf('async function buildThemeDiffPlan');
const planEnd = cliSource.indexOf('// src/category/theme/api/theme-api-file-validation.ts', planStart);
const diffPlan = cliSource.slice(planStart, planEnd);
assert.ok(diffPlan.includes('readdirpPromise(cwd'), 'CLI walks the current directory');
assert.ok(diffPlan.includes('directoryFilter: (entry) => shouldSync(entry.path)'), 'CLI applies its sync filter to directories');
assert.ok(diffPlan.includes('fileFilter: (entry) => shouldSync(entry.path)'), 'CLI applies its sync filter to files');
assert.ok(diffPlan.includes('client.getInstallation(themeId)') && diffPlan.includes('client.getFileHashes(themeId)'), 'preflight uses installation metadata and file hashes');

const requestStart = cliSource.indexOf('async request(url, init, { retry = true } = {})');
const requestEnd = cliSource.indexOf('async requestJson(', requestStart);
const request = cliSource.slice(requestStart, requestEnd);
assert.ok(request.includes('const maxAttempts = retry ? THEME_API_MAX_ATTEMPTS_FOR_REQUESTS : 1'), 'CLI request path retries unless caller disables it');
assert.ok(request.includes('fetch(url, {') && !request.slice(request.indexOf('fetch(url, {'), request.indexOf('});', request.indexOf('fetch(url, {'))).includes('redirect:'), 'request path leaves redirect handling at fetch default');
assert.ok(cliSource.includes('THEME_API_MAX_ATTEMPTS_FOR_REQUESTS = 6'), 'installed CLI default allows six attempts');
assert.ok(cliSource.includes('THEME_API_REQUEST_TIMEOUT_MS = 12e4'), 'installed CLI timeout is 120 seconds per attempt');
assert.ok(cliSource.includes('TIENDANUBE_CLI_TELEMETRY_ENABLED'), 'telemetry can be disabled by environment for future run');
assert.ok(cliSource.includes('TELEMETRY_DISABLED'), 'CLI has a disabled telemetry decision');

const validateStart = cliSource.indexOf('async validateFiles(installationId, upsert)');
const validateEnd = cliSource.indexOf('getMaxParallel()', validateStart);
const validateMethod = cliSource.slice(validateStart, validateEnd);
assert.ok(validateMethod.includes('method: "POST"') && validateMethod.includes('files/validate'), 'only server-validation path is the intended POST in this command path');
assert.ok(validateMethod.includes('body: JSON.stringify({ upsert: chunks[i] })'), 'POST body is an upsert-only validation payload');

const report = {
  kind: 'offline-native-check-preflight',
  no_network: true,
  cli_invoked: false,
  production_requests: 0,
  workspace: 'virtual-workspace',
  candidate_files_seen_by_cli_scan: paths,
  files: fileEvidence,
  source_verified: {
    cli_check_uses_current_working_directory: true,
    validation_files_are_only_local_create_or_update: true,
    remote_delete_list_is_not_validated_or_sent: true,
    validation_endpoint_method: 'POST',
    installation_metadata_endpoint_method: 'GET',
    file_hashes_endpoint_method: 'GET',
    retries_default_attempts: 6,
    timeout_ms_per_attempt: 120000,
    redirect_policy_explicitly_disabled: false,
    telemetry_disable_env_available: true,
  },
  limitations: [
    'Remote hashes were not read; the future CLI diff can submit either of these files only if its remote hash differs. A fail-closed body guard must require both paths and exact content hashes before allowing the POST.',
    'The CLI itself does not expose a retry-off or redirect-off flag. A future execution needs a verified request guard that allows only exact endpoints, one network attempt per request, redirect:error, and rejects all other methods/hosts.',
    'No HTML rendering, resolve_media execution, currentSrc, browser behavior, CLS, or production validation is performed by theme check.',
  ],
};
await fs.writeFile(path.join(root, 'offline-preflight-results.json'), JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify(report, null, 2));
