#requires -Version 7.0
<#
.SYNOPSIS
    Creates prompt-history entries and rebuilds their monthly indexes.

.DESCRIPTION
    Layout: docs/prompts-history/<YYYY>/<MM>/<YYYY-MM-DDTHHmmss+HHMM>_<step>_<slug>.md

    -Action new          write one entry for a single request/response turn
    -Action consolidate  create the current month folder and rebuild every INDEX.md

.EXAMPLE
    pwsh scripts/prompt-log.ps1 -Action new -Step step002 -Title "Add cost kill-switch" `
        -RequestText "..." -ResponseText "..."

.EXAMPLE
    pwsh scripts/prompt-log.ps1 -Action consolidate
#>
[CmdletBinding()]
param(
    [ValidateSet('new', 'consolidate')]
    [string]$Action = 'consolidate',

    [string]$Step,
    [string]$Title,
    [string]$Slug,
    [string]$Tags = '',
    [string]$RequestFile,
    [string]$RequestText,
    [string]$ResponseFile,
    [string]$ResponseText,
    [datetimeoffset]$When = [datetimeoffset]::Now
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$RepoRoot = Split-Path -Parent $PSScriptRoot
$HistoryRoot = Join-Path $RepoRoot 'docs/prompts-history'

function Get-Stamp {
    param([datetimeoffset]$Value)
    return $Value.ToString('yyyy-MM-ddTHHmmss') + $Value.ToString('zzz').Replace(':', '')
}

function ConvertTo-Slug {
    param([string]$Value, [int]$MaxLength = 60)
    $slug = ($Value.ToLowerInvariant() -replace '[^a-z0-9]+', '-').Trim('-')
    if ($slug.Length -gt $MaxLength) { $slug = $slug.Substring(0, $MaxLength).Trim('-') }
    if ([string]::IsNullOrWhiteSpace($slug)) { $slug = 'entry' }
    return $slug
}

function Read-TextSource {
    param([string]$File, [string]$Text, [string]$What)
    if ($File) {
        if (-not (Test-Path -LiteralPath $File)) { throw "$What file not found: $File" }
        return (Get-Content -LiteralPath $File -Raw).TrimEnd()
    }
    if ($null -ne $Text -and $Text.Trim().Length -gt 0) { return $Text.TrimEnd() }
    return $null
}

function Get-FrontMatterValue {
    param([string[]]$Lines, [string]$Name)
    $inside = $false
    foreach ($line in $Lines) {
        if ($line.Trim() -eq '---') {
            if ($inside) { break } else { $inside = $true; continue }
        }
        if (-not $inside) { continue }
        if ($line -match ('^' + [regex]::Escape($Name) + ':\s*(.+?)\s*$')) {
            return $Matches[1].Trim().Trim('"').Trim("'")
        }
    }
    return ''
}

function New-Entry {
    if (-not $Step) { throw 'Action new requires -Step (for example step002).' }
    if (-not $Title) { throw 'Action new requires -Title.' }

    $requestBody = Read-TextSource -File $RequestFile -Text $RequestText -What 'Request'
    $responseBody = Read-TextSource -File $ResponseFile -Text $ResponseText -What 'Response'
    if (-not $requestBody) { throw 'Action new requires -RequestText or -RequestFile.' }

    $year = $When.ToString('yyyy')
    $month = $When.ToString('MM')
    $monthDir = Join-Path (Join-Path $HistoryRoot $year) $month
    New-Item -ItemType Directory -Path $monthDir -Force | Out-Null

    $slug = if ($Slug) { ConvertTo-Slug $Slug } else { ConvertTo-Slug $Title }
    $stamp = Get-Stamp $When
    $fileName = "${stamp}_${Step}_${slug}.md"
    $path = Join-Path $monthDir $fileName
    if (Test-Path -LiteralPath $path) { throw "Entry already exists: $path" }

    $tagLine = if ($Tags) { '[' + (($Tags -split ',' | ForEach-Object { $_.Trim() } | Where-Object { $_ }) -join ', ') + ']' } else { '[]' }

    $builder = [System.Text.StringBuilder]::new()
    [void]$builder.AppendLine('---')
    [void]$builder.AppendLine("step: $Step")
    [void]$builder.AppendLine("timestamp: $($When.ToString('yyyy-MM-ddTHH:mm:sszzz'))")
    [void]$builder.AppendLine('project: amtocsoft-megagent')
    [void]$builder.AppendLine("tags: $tagLine")
    [void]$builder.AppendLine('---')
    [void]$builder.AppendLine()
    [void]$builder.AppendLine("# $Step - $Title")
    [void]$builder.AppendLine()
    [void]$builder.AppendLine('## Request')
    [void]$builder.AppendLine()
    [void]$builder.AppendLine('```text')
    [void]$builder.AppendLine($requestBody)
    [void]$builder.AppendLine('```')
    [void]$builder.AppendLine()
    [void]$builder.AppendLine('## Response')
    [void]$builder.AppendLine()
    if ($responseBody) { [void]$builder.AppendLine($responseBody) } else { [void]$builder.AppendLine('_Not recorded._') }
    [void]$builder.AppendLine()
    [void]$builder.AppendLine('## Follow-ups')
    [void]$builder.AppendLine()
    [void]$builder.AppendLine('- none')

    Set-Content -LiteralPath $path -Value $builder.ToString() -Encoding utf8NoBOM
    Write-Output $path
}

function Write-MonthIndex {
    param([string]$MonthDir)

    $entries = @(Get-ChildItem -LiteralPath $MonthDir -File -Filter '*.md' |
        Where-Object { $_.Name -ne 'INDEX.md' } |
        Sort-Object Name)

    $label = '{0}/{1}' -f (Split-Path -Leaf (Split-Path -Parent $MonthDir)), (Split-Path -Leaf $MonthDir)
    $lines = [System.Collections.Generic.List[string]]::new()
    $lines.Add("# $label")
    $lines.Add('')
    $lines.Add(('{0} entries. Generated by `scripts/prompt-log.ps1 -Action consolidate`; do not edit by hand.' -f $entries.Count))
    $lines.Add('')

    if ($entries.Count -eq 0) {
        $lines.Add('_No entries yet._')
    }
    else {
        $lines.Add('| Timestamp | Step | Title | Entry |')
        $lines.Add('| --- | --- | --- | --- |')
        foreach ($entry in $entries) {
            $head = Get-Content -LiteralPath $entry.FullName -TotalCount 20
            $step = Get-FrontMatterValue -Lines $head -Name 'step'
            $title = Get-FrontMatterValue -Lines $head -Name 'title'
            if (-not $title) {
                $bodyTitle = $head | Where-Object { $_ -match '^#\s+(.+)$' } | Select-Object -First 1
                if ($bodyTitle -match '^#\s+(.+)$') {
                    $title = ($Matches[1] -replace '^step\d+\s*[-\u2013\u2014]\s*', '').Trim()
                }
            }
            if (-not $title) { $title = (Split-Path -LeafBase $entry.Name) }
            $title = $title.Replace('|', '\|')

            if ($entry.Name -match '^(\d{4}-\d{2}-\d{2})T(\d{2})(\d{2})(\d{2})') {
                $display = '{0} {1}:{2}' -f $Matches[1], $Matches[2], $Matches[3]
            }
            else { $display = $entry.Name }

            $lines.Add(('| {0} | {1} | {2} | [{3}]({3}) |' -f $display, $step, $title, $entry.Name))
        }
    }

    Set-Content -LiteralPath (Join-Path $MonthDir 'INDEX.md') -Value ($lines -join [Environment]::NewLine) -Encoding utf8NoBOM
    return $entries.Count
}

function Invoke-Consolidate {
    $yearDir = Join-Path $HistoryRoot $When.ToString('yyyy')
    $monthDir = Join-Path $yearDir $When.ToString('MM')
    New-Item -ItemType Directory -Path $monthDir -Force | Out-Null

    $rows = [System.Collections.Generic.List[string]]::new()
    $total = 0

    foreach ($year in Get-ChildItem -LiteralPath $HistoryRoot -Directory | Where-Object Name -match '^\d{4}$' | Sort-Object Name) {
        foreach ($month in Get-ChildItem -LiteralPath $year.FullName -Directory | Where-Object Name -match '^\d{2}$' | Sort-Object Name) {
            $count = Write-MonthIndex -MonthDir $month.FullName
            $total += $count
            $rows.Add(('| [{0}/{1}]({0}/{1}/INDEX.md) | {2} |' -f $year.Name, $month.Name, $count))
        }
    }

    $root = [System.Collections.Generic.List[string]]::new()
    $root.Add('# Prompt history index')
    $root.Add('')
    $root.Add(('{0} entries across {1} month folders. Generated file; do not edit by hand.' -f $total, $rows.Count))
    $root.Add('')
    if ($rows.Count -eq 0) {
        $root.Add('_No entries yet._')
    }
    else {
        $root.Add('| Month | Entries |')
        $root.Add('| --- | --- |')
        foreach ($row in $rows) { $root.Add($row) }
    }
    Set-Content -LiteralPath (Join-Path $HistoryRoot 'INDEX.md') -Value ($root -join [Environment]::NewLine) -Encoding utf8NoBOM

    Write-Output (('Consolidated: {0} entries, {1} month folder(s), current month {2}.' -f $total, $rows.Count, $When.ToString('yyyy/MM')))
}

try {
    switch ($Action) {
        'new' { $created = New-Entry; Invoke-Consolidate | Out-Null; Write-Output "Entry: $created" }
        'consolidate' { Invoke-Consolidate }
    }
}
catch {
    Write-Error $_.Exception.Message
    exit 1
}
