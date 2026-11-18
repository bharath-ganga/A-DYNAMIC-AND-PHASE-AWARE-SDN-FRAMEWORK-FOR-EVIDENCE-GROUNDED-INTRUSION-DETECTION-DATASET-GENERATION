$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech
$story = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'narration-story.json') -Raw | ConvertFrom-Json
$audioDirectory = Join-Path $PSScriptRoot '.narration-work'
New-Item -ItemType Directory -Path $audioDirectory -Force | Out-Null
$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer
$speaker.SelectVoice('Microsoft Zira Desktop')
$speaker.Rate = 0
$speaker.Volume = 100
try {
 for ($sceneIndex = 0; $sceneIndex -lt $story.Count; $sceneIndex++) {
  for ($sentenceIndex = 0; $sentenceIndex -lt $story[$sceneIndex].sentences.Count; $sentenceIndex++) {
   $audioPath = Join-Path $audioDirectory ('{0:D2}-{1:D2}.wav' -f $sceneIndex, $sentenceIndex)
   $speaker.SetOutputToWaveFile($audioPath)
   $speaker.Speak([string]$story[$sceneIndex].sentences[$sentenceIndex])
   $speaker.SetOutputToNull()
  }
  Write-Output ('Narrated chapter {0}/{1}' -f ($sceneIndex + 1), $story.Count)
 }
} finally { $speaker.Dispose() }
