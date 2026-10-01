// 加载首页文章
async function loadArticles() {
    const articleList = document.getElementById('article-list');
    if (!articleList) return;

    try {
        const response = await fetch('articles/index.json');
        if (!response.ok) {
            throw new Error(`文章索引请求失败：${response.status}`);
        }

        const articles = await response.json();
        if (!Array.isArray(articles) || articles.length === 0) {
            articleList.textContent = '暂无文章';
            return;
        }

        const articleFragment = document.createDocumentFragment();
        articles.slice(0, 6).forEach((article, index) => {
            const articleCard = document.createElement('article');
            articleCard.className = 'article-card';

            const articleMeta = document.createElement('div');
            articleMeta.className = 'article-meta';
            articleMeta.textContent = `${String(index + 1).padStart(2, '0')} / ${article.date}`;

            const articleTitle = document.createElement('h3');
            const articleLink = document.createElement('a');
            articleLink.href = `articles/${encodeURIComponent(article.slug)}.html`;
            articleLink.textContent = article.title;
            articleTitle.appendChild(articleLink);

            const articleArrow = document.createElement('span');
            articleArrow.className = 'article-arrow';
            articleArrow.setAttribute('aria-hidden', 'true');
            articleArrow.textContent = '→';

            articleCard.append(articleMeta, articleTitle, articleArrow);
            articleFragment.appendChild(articleCard);
        });

        articleList.replaceChildren(articleFragment);
    } catch (error) {
        console.error('无法加载文章列表：', error);
        articleList.textContent = '文章暂时无法加载，请稍后重试。';
    }
}

// 进入视口时显示内容
function initializeRevealAnimations() {
    const revealElements = document.querySelectorAll('.reveal');
    if (!revealElements.length) return;

    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        revealElements.forEach((element) => element.classList.add('is-visible'));
        return;
    }

    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach((entry) => {
            if (!entry.isIntersecting) return;
            entry.target.classList.add('is-visible');
            observer.unobserve(entry.target);
        });
    }, { threshold: 0.12 });

    revealElements.forEach((element) => revealObserver.observe(element));
}

document.addEventListener('DOMContentLoaded', async () => {
    initializeRevealAnimations();
    await loadArticles();
});
