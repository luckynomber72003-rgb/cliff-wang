// Load articles on homepage
document.addEventListener('DOMContentLoaded', function() {
    const articleList = document.getElementById('article-list');
    if (!articleList) return;

    // Fetch article index
    fetch('articles/index.json')
        .then(response => response.json())
        .then(articles => {
            if (articles.length === 0) {
                articleList.innerHTML = '<p>暫無文章</p>';
                return;
            }

            articleList.innerHTML = articles.map(article => `
                <div class="article-card">
                    <h3><a href="articles/${article.slug}.html">${article.title}</a></h3>
                    <p class="article-meta">${article.date} · ${article.category}</p>
                </div>
            `).join('');
        })
        .catch(() => {
            articleList.innerHTML = '<p>文章加載中...</p>';
        });
});
