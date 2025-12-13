// Global data storage
let papersData = null;
let categoriesData = null;

// Load papers data
async function loadData() {
    try {
        const response = await fetch('data/papers.json');
        const data = await response.json();
        papersData = data.papers;
        categoriesData = data.categories;
        return data;
    } catch (error) {
        console.error('Error loading data:', error);
        return null;
    }
}

// Load categories for homepage
async function loadCategories() {
    const data = await loadData();
    if (!data) return;
    
    const grid = document.getElementById('categoriesGrid');
    const dropdown = document.getElementById('categoryDropdown');
    
    if (grid) {
        grid.innerHTML = '';
        for (const [code, name] of Object.entries(data.categories)) {
            const card = document.createElement('div');
            card.className = 'category-card';
            
            const paperCount = data.papers.filter(p => p.category === code).length;
            
            card.innerHTML = `
                <h3>${code}</h3>
                <p>${name}</p>
                <p>${paperCount} paper${paperCount !== 1 ? 's' : ''}</p>
                <a href="category.html?category=${code}">Browse Papers →</a>
            `;
            
            grid.appendChild(card);
        }
    }
    
    if (dropdown) {
        dropdown.innerHTML = '';
        for (const [code, name] of Object.entries(data.categories)) {
            const link = document.createElement('a');
            link.href = `category.html?category=${code}`;
            link.textContent = `${code} - ${name}`;
            dropdown.appendChild(link);
        }
    }
}

// Load papers for category page
async function loadPapers(category = null) {
    const data = await loadData();
    if (!data) return;
    
    const list = document.getElementById('papersList');
    const titleEl = document.getElementById('categoryTitle');
    const descEl = document.getElementById('categoryDescription');
    
    if (!list) return;
    
    // Filter papers by category
    let papers = data.papers;
    if (category) {
        papers = papers.filter(p => p.category === category);
        if (titleEl) titleEl.textContent = `${category} Papers`;
        if (descEl) descEl.textContent = data.categories[category] || '';
    } else {
        if (titleEl) titleEl.textContent = 'All Papers';
        if (descEl) descEl.textContent = 'Showing all recent submissions across CS fields';
    }
    
    // Sort by date (newest first)
    papers.sort((a, b) => new Date(b.submitted) - new Date(a.submitted));
    
    // Display papers
    list.innerHTML = '';
    papers.forEach(paper => {
        const card = createPaperCard(paper);
        list.appendChild(card);
    });
}

// Create paper card element
function createPaperCard(paper) {
    const card = document.createElement('div');
    card.className = 'paper-card';
    
    const date = new Date(paper.submitted).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
    
    card.innerHTML = `
        <div class="paper-meta">
            <span class="paper-category">${paper.category}</span>
            <span>${date}</span>
            <span>arXiv:${paper.id}</span>
        </div>
        <h2 class="paper-title">
            <a href="paper.html?id=${paper.id}">${paper.title}</a>
        </h2>
        <p class="paper-authors">${paper.authors.join(', ')}</p>
        <p class="paper-abstract">${paper.abstract}</p>
    `;
    
    return card;
}

// Filter papers by date
function filterByDate() {
    const dateFilter = document.getElementById('dateFilter');
    const selectedDate = dateFilter.value;
    
    const urlParams = new URLSearchParams(window.location.search);
    const category = urlParams.get('category');
    
    const list = document.getElementById('papersList');
    if (!list || !papersData) return;
    
    let papers = papersData;
    
    // Filter by category
    if (category) {
        papers = papers.filter(p => p.category === category);
    }
    
    // Filter by date
    if (selectedDate) {
        papers = papers.filter(p => p.submitted === selectedDate);
    }
    
    // Sort and display
    papers.sort((a, b) => new Date(b.submitted) - new Date(a.submitted));
    
    list.innerHTML = '';
    papers.forEach(paper => {
        const card = createPaperCard(paper);
        list.appendChild(card);
    });
}

// Load paper details
async function loadPaperDetails(paperId) {
    const data = await loadData();
    if (!data) return;
    
    const paper = data.papers.find(p => p.id === paperId);
    if (!paper) {
        document.getElementById('paperDetail').innerHTML = '<p>Paper not found.</p>';
        return;
    }
    
    const detailDiv = document.getElementById('paperDetail');
    
    const date = new Date(paper.submitted).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
    
    detailDiv.innerHTML = `
        <div class="paper-meta">
            <span class="paper-category">${paper.category}</span>
            <span>${date}</span>
            <span>arXiv:${paper.id}</span>
        </div>
        <h1>${paper.title}</h1>
        
        <div class="detail-section">
            <h2>Authors</h2>
            <p class="authors-list">${paper.authors.join(', ')}</p>
            <p style="color: #666; font-size: 0.9rem;">${paper.affiliations.join(', ')}</p>
        </div>
        
        <div class="detail-section">
            <h2>Abstract</h2>
            <p>${paper.abstract}</p>
        </div>
        
        <div class="detail-section">
            <h2>Links</h2>
            <a href="${paper.pdf_url}" class="btn btn-primary pdf-link" target="_blank">View PDF</a>
            <a href="${paper.arxiv_url}" class="btn btn-secondary pdf-link" target="_blank">arXiv Page</a>
        </div>
    `;
    
    // Generate citations
    generateCitations(paper);
}

// Generate citations
function generateCitations(paper) {
    const year = new Date(paper.submitted).getFullYear();
    const authorsLastNames = paper.authors.map(a => a.split(' ').pop());
    
    // BibTeX
    const bibtex = `@article{${authorsLastNames[0].toLowerCase()}${year}${paper.id.split('.')[1]},
  title={${paper.title}},
  author={${paper.authors.join(' and ')}},
  journal={arXiv preprint arXiv:${paper.id}},
  year={${year}}
}`;
    
    document.getElementById('bibtexCitation').textContent = bibtex;
    
    // Standard citation
    const standardCitation = `${paper.authors.join(', ')}. "${paper.title}." arXiv preprint arXiv:${paper.id} (${year}).`;
    
    document.getElementById('standardCitation').textContent = standardCitation;
}

// Copy citation to clipboard
function copyCitation(type) {
    let text = '';
    
    if (type === 'bibtex') {
        text = document.getElementById('bibtexCitation').textContent;
    } else if (type === 'standard') {
        text = document.getElementById('standardCitation').textContent;
    }
    
    navigator.clipboard.writeText(text).then(() => {
        alert('Citation copied to clipboard!');
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

// Initialize dropdowns on all pages
document.addEventListener('DOMContentLoaded', function() {
    loadCategories();
});