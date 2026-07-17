# prose-lint.ps1 — deterministic AI-prose backstop for site articles.
#
# Wired as a PostToolUse hook on Write|Edit|MultiEdit. Reads the hook JSON
# from stdin, and only acts when the edited file is an article output page
# (research/ , reviews/ , ir-reports/  ...  /index.html). Scans for the two
# things a human pass reliably misses: em dashes and the RULES.md §1 banned
# phrases. Findings are advisory — exit 2 feeds them back to Claude so the
# next action can fix them or run /humanizer. It never blocks or reverts.
#
# Advisory by design: a banned word inside a code block or quote is a false
# positive, so this only surfaces line numbers, it does not fail the edit.

$ErrorActionPreference = 'Stop'

try {
    $raw = [Console]::In.ReadToEnd()
    if ([string]::IsNullOrWhiteSpace($raw)) { exit 0 }
    $data = $raw | ConvertFrom-Json
    $fp = $data.tool_input.file_path
    if ([string]::IsNullOrWhiteSpace($fp)) { exit 0 }
} catch { exit 0 }

# Only lint article output pages.
$norm = ($fp -replace '\\', '/')
if ($norm -notmatch '/(research|reviews|ir-reports)/[^/]+/index\.html$') { exit 0 }
if (-not (Test-Path -LiteralPath $fp)) { exit 0 }

$lines = Get-Content -LiteralPath $fp
$findings = New-Object System.Collections.Generic.List[string]

# RULES.md §1 banned phrases (case-insensitive, .NET regex).
$phrases = @(
    "it'?s worth noting", "it is important to note", "it should be noted",
    "keep in mind that", "delve", "a testament to", "at its core",
    "in today'?s", "ever-evolving", "in the realm of", "when it comes to",
    "that said,", "moving forward", "in conclusion", "to summarize",
    "in order to", "this allows you to", "game-?changer", "seamless",
    "\bleverage\b", "\butilize\b", "not only .+ but also", "not just .+ but\b"
)

for ($i = 0; $i -lt $lines.Count; $i++) {
    $ln = $lines[$i]
    $n = $i + 1
    if ($ln -match '—') { $findings.Add("L${n}: em dash (U+2014) in body text") }
    foreach ($p in $phrases) {
        if ($ln -match "(?i)$p") { $findings.Add("L${n}: banned phrase /$p/") }
    }
}

if ($findings.Count -gt 0) {
    [Console]::Error.WriteLine("[prose-lint] $norm has AI-prose tells (RULES.md). Fix these or run /humanizer:")
    foreach ($f in $findings) { [Console]::Error.WriteLine("  $f") }
    exit 2
}
exit 0
