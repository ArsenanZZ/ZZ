# process_mexico_marathon.ps1
# Script to parse standalone HTML files, extract base64 webp images, and replace image references.

# Encoding settings for output files
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

# Paths
$zhStandalone = "Z:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20250831-Mexico City Marathon\0000-Web\0-Claude\files\mexico-marathon-zh-standalone.html"
$enStandalone = "Z:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20250831-Mexico City Marathon\0000-Web\0-Claude\files\mexico-marathon-en-standalone.html"
$fbStandalone = "Z:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20250831-Mexico City Marathon\0000-Web\0-Claude\files\mexico-marathon-fb-standalone.html"

$zhOut = "C:\Users\ZZ\Documents\Github\ZZ\run50\stories\chinese\mexico-marathon.html"
$enOut = "C:\Users\ZZ\Documents\Github\ZZ\run50\stories\english\mexico-marathon.html"
$fbOut = "C:\Users\ZZ\Documents\Github\ZZ\run50\facebook\mexico-marathon.html"

$imgDir = "C:\Users\ZZ\Documents\Github\ZZ\run50\stories\chinese\mexico-marathon_files"

# 1. Create images directory if not exists
if (!(Test-Path $imgDir)) {
    New-Item -ItemType Directory -Path $imgDir | Out-Null
    Write-Host "Created image directory: $imgDir"
}

# 2. Read Chinese Standalone and extract base64 images
$zhContent = [System.IO.File]::ReadAllText($zhStandalone, [System.Text.Encoding]::UTF8)
$regex = [regex]'src="data:image/webp;base64,([^"]+)"'
$matches = $regex.Matches($zhContent)

Write-Host "Found $($matches.Count) base64 images in Chinese standalone."

# Skip extraction if images are already written
$existingImages = Get-ChildItem -Path $imgDir -Filter "img-*.webp"
if ($existingImages.Count -eq $matches.Count) {
    Write-Host "All $($matches.Count) images already extracted. Skipping extraction."
} else {
    $index = 0
    foreach ($m in $matches) {
        $index++
        $base64 = $m.Groups[1].Value
        # Strip any whitespace
        $base64Clean = $base64 -replace '\s'
        $bytes = [System.Convert]::FromBase64String($base64Clean)
        $imgFile = "img-{0:D3}.webp" -f $index
        $imgPath = Join-Path $imgDir $imgFile
        [System.IO.File]::WriteAllBytes($imgPath, $bytes)
    }
    Write-Host "Extracted and wrote $index images to $imgDir"
}

# 3. Replace base64 in Chinese HTML
$global:replaceIndex = 0
$evaluatorZh = [System.Text.RegularExpressions.MatchEvaluator] {
    param($match)
    $global:replaceIndex++
    $imgFile = "img-{0:D3}.webp" -f $global:replaceIndex
    return 'src="mexico-marathon_files/' + $imgFile + '"'
}
$zhSanitized = $regex.Replace($zhContent, $evaluatorZh)

# Replace comments section in Chinese page
$chineseCommentsWidget = @"
  <section class="zz-engagement" data-zz-engagement data-locale="zh-CN" data-page-key="run50-mexico-marathon-zh">
    <div class="zz-engagement-shell">
      <div>
        <p class="zz-engagement-kicker">留言 / 访问次数</p>
        <h2>跑完也可以聊两句</h2>
        <p class="zz-engagement-note">不用注册账号即可提交留言，提交后会直接显示。</p>
        <div class="zz-engagement-stats">
          <span class="zz-engagement-stat" id="busuanzi_container_page_pv">
            <span>访问</span>
            <strong id="busuanzi_value_page_pv" data-zz-view-count>--</strong>
            <span>次</span>
          </span>
        </div>
      </div>
      <div class="zz-engagement-card">
        <div id="supabase-comments-mexico-zh" data-zz-supabase-comments></div>
        <p class="zz-engagement-status" data-zz-engagement-status>留言区加载中...</p>
      </div>
    </div>
  </section>
  <footer class="page-footer">静态整理版：正文从“前言”开始，已移除公众号导出页 the top elements，原始保存文件未修改。</footer>
  <script src="../../../assets/zz-engagement-config.js" defer></script>
  <script src="../../../assets/zz-engagement.js" defer></script>
  <link rel="stylesheet" href="../../../assets/zz-engagement.css">
"@

$commentsRegex = [regex]'(?s)<!-- COMMENT WIDGET:.*?<section class="comments">.*?</section>'
$zhSanitized = $commentsRegex.Replace($zhSanitized, $chineseCommentsWidget)

# Save Chinese page without BOM
[System.IO.File]::WriteAllText($zhOut, $zhSanitized, $Utf8NoBom)
Write-Host "Wrote Chinese sanitized HTML to $zhOut"


# 4. Replace base64 in English HTML
$enContent = [System.IO.File]::ReadAllText($enStandalone, [System.Text.Encoding]::UTF8)
$global:replaceIndex = 0
$evaluatorEn = [System.Text.RegularExpressions.MatchEvaluator] {
    param($match)
    $global:replaceIndex++
    $imgFile = "img-{0:D3}.webp" -f $global:replaceIndex
    return 'src="../chinese/mexico-marathon_files/' + $imgFile + '"'
}
$enSanitized = $regex.Replace($enContent, $evaluatorEn)

# Replace comments section in English page
$englishCommentsWidget = @"
  <section class="zz-engagement" data-zz-engagement data-locale="en" data-page-key="run50-mexico-marathon-en">
    <div class="zz-engagement-shell">
      <div>
        <p class="zz-engagement-kicker">Comments / Visits</p>
        <h2>Feel free to leave a comment</h2>
        <p class="zz-engagement-note">No registration required. Comments appear instantly after submission.</p>
        <div class="zz-engagement-stats">
          <span class="zz-engagement-stat" id="busuanzi_container_page_pv">
            <span>Visits:</span>
            <strong id="busuanzi_value_page_pv" data-zz-view-count>--</strong>
          </span>
        </div>
      </div>
      <div class="zz-engagement-card">
        <div id="supabase-comments-mexico-en" data-zz-supabase-comments></div>
        <p class="zz-engagement-status" data-zz-engagement-status>Loading comments...</p>
      </div>
    </div>
  </section>
  <footer class="page-footer">Static formatted edition: Main body starts from Preface. Original files left unchanged.</footer>
  <script src="../../../assets/zz-engagement-config.js" defer></script>
  <script src="../../../assets/zz-engagement.js" defer></script>
  <link rel="stylesheet" href="../../../assets/zz-engagement.css">
"@
$enSanitized = $commentsRegex.Replace($enSanitized, $englishCommentsWidget)

# Save English page without BOM
[System.IO.File]::WriteAllText($enOut, $enSanitized, $Utf8NoBom)
Write-Host "Wrote English sanitized HTML to $enOut"


# 5. Replace base64 in Facebook HTML
$fbContent = [System.IO.File]::ReadAllText($fbStandalone, [System.Text.Encoding]::UTF8)
$global:replaceIndex = 0
$evaluatorFb = [System.Text.RegularExpressions.MatchEvaluator] {
    param($match)
    $global:replaceIndex++
    $imgFile = "img-{0:D3}.webp" -f $global:replaceIndex
    return 'src="../stories/chinese/mexico-marathon_files/' + $imgFile + '"'
}
$fbSanitized = $regex.Replace($fbContent, $evaluatorFb)

# Replace comments section in Facebook page
$facebookCommentsWidget = @"
  <section class="zz-engagement" data-zz-engagement data-locale="en" data-page-key="run50-mexico-marathon-facebook-en">
    <div class="zz-engagement-shell">
      <div>
        <p class="zz-engagement-kicker">Comments / Views</p>
        <h2>Say something after the run</h2>
        <p class="zz-engagement-note">No account is needed to submit a comment. New comments appear right away.</p>
        <div class="zz-engagement-stats">
          <span class="zz-engagement-stat" id="busuanzi_container_page_pv">
            <span>Views</span>
            <strong id="busuanzi_value_page_pv" data-zz-view-count>--</strong>
          </span>
        </div>
      </div>
      <div class="zz-engagement-card">
        <div id="supabase-comments-mexico-facebook-en" data-zz-supabase-comments></div>
        <p class="zz-engagement-status" data-zz-engagement-status>Loading comments...</p>
      </div>
    </div>
  </section>
  <script src="../../assets/zz-engagement-config.js?v=20260604"></script>
  <script src="../../assets/zz-engagement.js?v=20260604"></script>
  <link rel="stylesheet" href="../../assets/zz-engagement.css">
"@
$fbSanitized = $commentsRegex.Replace($fbSanitized, $facebookCommentsWidget)

# Save Facebook page without BOM
[System.IO.File]::WriteAllText($fbOut, $fbSanitized, $Utf8NoBom)
Write-Host "Wrote Facebook sanitized HTML to $fbOut"
