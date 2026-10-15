document.addEventListener('DOMContentLoaded', () => {
    // 1. Set current year in footer
    const yearSpan = document.getElementById('year');
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }

    // 2. Dynamically load content grids
    loadManifest('posts/post-list.json', 'posts-grid', 'posts');
    loadManifest('tools/tool-list.json', 'tools-grid', 'tools');
});

async function loadManifest(manifestPath, gridId, type) {
    const gridContainer = document.getElementById(gridId);
    if (!gridContainer) return;

    try {
        const response = await fetch(manifestPath);
        if (!response.ok) throw new Error(`Failed to load manifest: ${manifestPath}`);
        
        const items = await response.json();
        
        // Clear fallback static HTML
        gridContainer.innerHTML = '';

        if (items.length === 0) {
            gridContainer.innerHTML = '<p class="card-excerpt">Nothing here yet. Check back soon!</p>';
            return;
        }

        items.forEach(item => {
            const article = document.createElement('article');
            article.className = 'card';
            
            if (type === 'posts') {
                const formattedDate = formatDate(item.date);
                article.innerHTML = `
                    <div class="card-meta">
                        <time datetime="${item.date}">${formattedDate}</time>
                        <span class="tag">${item.tag}</span>
                    </div>
                    <h3 class="card-title"><a href="posts/${item.slug}">${item.title}</a></h3>
                    <p class="card-excerpt">${item.excerpt}</p>
                `;
            } else if (type === 'tools') {
                article.innerHTML = `
                    <div class="card-meta">
                        <span class="tag">${item.tag}</span>
                    </div>
                    <h3 class="card-title"><a href="tools/${item.slug}">${item.title}</a></h3>
                    <p class="card-excerpt">${item.excerpt}</p>
                `;
            }
            
            gridContainer.appendChild(article);
        });

    } catch (error) {
        console.error(`Error loading ${type}:`, error);
        gridContainer.innerHTML = '<p class="card-excerpt">Could not load items at this time.</p>';
    }
}

function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric', timeZone: 'UTC' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}
