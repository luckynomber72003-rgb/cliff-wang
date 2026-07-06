// Load articles on homepage
document.addEventListener('DOMContentLoaded', function() {
    const articleList = document.getElementById('article-list');
    if (!articleList) return;

    // Fetch article index
    fetch('articles/index.json')
        .then(response => response.json())
        .then(articles => {
            if (articles.length === 0) {
                articleList.innerHTML = '<p style="color: var(--text-light);">暂无文章</p>';
                return;
            }

            articleList.innerHTML = articles.map(article => `
                <div class="article-card">
                    <h3><a href="articles/${article.slug}.html">${article.title}</a></h3>
                    <div class="article-meta">
                        <span>📅 ${article.date}</span>
                    </div>
                </div>
            `).join('');
        })
        .catch(() => {
            articleList.innerHTML = '<p style="color: var(--text-light);">文章加载中...</p>';
        });
});
