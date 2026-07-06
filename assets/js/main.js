// Load articles on homepage
document.addEventListener('DOMContentLoaded', function() {
    const articleList = document.getElementById('article-list');
    if (!articleList) return;

    // Fetch article index
    fetch('articles/index.json')
        .then(response => response.json())
        .then(articles => {
            if (articles.length === 0) {
                articleList.innerHTML = '<p style="color: var(--text-muted);">暂无文章</p>';
                return;
            }

            articleList.innerHTML = articles.slice(0, 8).map(article => `
                <div class="article-card">
                    <div>
                        <h3><a href="articles/${article.slug}.html">${article.title}</a></h3>
                        <div class="article-meta">${article.date}</div>
                    </div>
                    <span class="article-arrow">→</span>
                </div>
            `).join('');
        })
        .catch(() => {
            articleList.innerHTML = '<p style="color: var(--text-muted);">文章加载中...</p>';
        });
});

// Add subtle mouse parallax effect to glow elements
document.addEventListener('mousemove', (e) => {
    const glows = document.querySelectorAll('.bg-glow');
    const x = e.clientX / window.innerWidth;
    const y = e.clientY / window.innerHeight;

    glows.forEach((glow, i) => {
        const factor = (i + 1) * 20;
        glow.style.transform = `translate(${x * factor}px, ${y * factor}px)`;
    });
});
