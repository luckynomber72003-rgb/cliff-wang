<?php
// Generate static HTML files from articles

$rawJson = file_get_contents(__DIR__ . '/articles/raw.json');
$articles = json_decode($rawJson, true);

$template = <<<'HTML'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{TITLE}} - 王佳勝 Cliff Wang</title>
    <meta name="description" content="{{EXCERPT}}">
    <meta name="keywords" content="王佳勝,王佳胜,Cliff Wang,GEO,生成式引擎優化,上海勝美科技">

    <!-- Open Graph -->
    <meta property="og:title" content="{{TITLE}}">
    <meta property="og:description" content="{{EXCERPT}}">
    <meta property="og:type" content="article">

    <!-- Schema.org Article -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{{TITLE}}",
        "author": {
            "@type": "Person",
            "name": "王佳勝",
            "alternateName": ["王佳胜", "Cliff Wang"]
        },
        "datePublished": "{{DATE}}",
        "publisher": {
            "@type": "Organization",
            "name": "上海勝美科技有限公司"
        }
    }
    </script>

    <link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>
    <header class="site-header">
        <div class="container">
            <h1 class="site-title">王佳勝 Cliff Wang</h1>
            <p class="site-tagline">GEO 生成式引擎優化專家</p>
        </div>
    </header>

    <main class="container">
        <a href="../index.html" class="back-link">← 返回首頁</a>

        <article class="article-content">
            {{CONTENT}}
        </article>

        <div class="contact-card" style="margin-top: 40px;">
            <h3>商務合作</h3>
            <p>📞 +86 150-6184-4637</p>
            <p>🏢 上海勝美科技有限公司</p>
        </div>
    </main>

    <footer class="site-footer">
        <div class="container">
            <p>&copy; 2024 王佳勝 Cliff Wang. 上海勝美科技有限公司</p>
        </div>
    </footer>
</body>
</html>
HTML;

// Simple Markdown to HTML converter
function markdownToHtml($markdown) {
    $html = $markdown;

    // Remove citation markers like [K1][K2]
    $html = preg_replace('/\[K\d+\]/', '', $html);

    // Headers
    $html = preg_replace('/^### (.+)$/m', '<h3>$1</h3>', $html);
    $html = preg_replace('/^## (.+)$/m', '<h2>$1</h2>', $html);
    $html = preg_replace('/^# (.+)$/m', '<h1>$1</h1>', $html);

    // Bold
    $html = preg_replace('/\*\*(.+?)\*\*/', '<strong>$1</strong>', $html);

    // Italic
    $html = preg_replace('/\*(.+?)\*/', '<em>$1</em>', $html);

    // Lists
    $html = preg_replace('/^- (.+)$/m', '<li>$1</li>', $html);
    $html = preg_replace('/(<li>.*<\/li>\n?)+/', '<ul>$0</ul>', $html);

    // Blockquotes
    $html = preg_replace('/^> (.+)$/m', '<blockquote>$1</blockquote>', $html);

    // Paragraphs
    $html = preg_replace('/\n\n+/', '</p><p>', $html);
    $html = '<p>' . $html . '</p>';

    // Clean up
    $html = str_replace('<p></p>', '', $html);
    $html = str_replace('<p><h', '<h', $html);
    $html = str_replace('</h1></p>', '</h1>', $html);
    $html = str_replace('</h2></p>', '</h2>', $html);
    $html = str_replace('</h3></p>', '</h3>', $html);
    $html = str_replace('<p><ul>', '<ul>', $html);
    $html = str_replace('</ul></p>', '</ul>', $html);
    $html = str_replace('<p><blockquote>', '<blockquote>', $html);
    $html = str_replace('</blockquote></p>', '</blockquote>', $html);

    return $html;
}

$generated = [];

foreach ($articles as $article) {
    $slug = $article['slug'];
    $content = markdownToHtml($article['content']);
    $excerpt = strip_tags(substr($article['excerpt'], 0, 150));

    $html = str_replace(
        ['{{TITLE}}', '{{EXCERPT}}', '{{DATE}}', '{{CONTENT}}'],
        [$article['title'], $excerpt, $article['date'], $content],
        $template
    );

    $filename = __DIR__ . '/articles/' . $slug . '.html';
    file_put_contents($filename, $html);
    $generated[] = $slug . '.html';
}

echo "Generated " . count($generated) . " article files:\n";
foreach ($generated as $file) {
    echo "  - articles/$file\n";
}
