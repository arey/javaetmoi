function initializeSearch(index) {
  const searchKeys = ['title', 'link', 'body', 'id', 'section', 'tags'];

  const searchPageElement = elem('#searchpage');

  const searchOptions = {
    ignoreLocation: true,
    findAllMatches: true,
    includeScore: true,
    shouldSort: true,
    keys: searchKeys,
    threshold: 0.0
  };

  index = new Fuse(index, searchOptions);

  function minQueryLen(query) {
    query = query.trim();
    const queryIsFloat = parseFloat(query);
    const minimumQueryLength = queryIsFloat ? 1 : 2;
    return minimumQueryLength;
  }

  function searchResults(results = [], query = '', passive = false) {
    let resultsFragment = new DocumentFragment();
    let showResults = elem('.search_results');
    if (passive) {
      showResults = searchPageElement;
    }
    emptyEl(showResults);

    const queryLen = query.length;
    const requiredQueryLen = minQueryLen(query);

    if (results.length && queryLen >= requiredQueryLen) {
      let resultsTitle = createEl('h3');
      resultsTitle.className = 'search_title';
      resultsTitle.innerText = quickLinks;

      let goBackButton = createEl('button');
      goBackButton.textContent = 'Go Back';
      goBackButton.className = goBackClass;
      if (passive) {
        resultsTitle.innerText = searchResultsLabel;
      }
      if (!searchPageElement) {
        results = results.slice(0, 8);
      } else {
        resultsFragment.appendChild(goBackButton);
        results = results.slice(0, 12);
      }
      resultsFragment.appendChild(resultsTitle);

      results.forEach(function(result) {
        let item = createEl('a');
        item.href = `${result.link}?query=${query}`;
        item.className = 'search_result';
        item.style.order = result.score;
        if (passive) {
          pushClass(item, 'passive');
          let itemTitle = createEl('h3');
          itemTitle.textContent = result.title;
          item.appendChild(itemTitle);

          let itemDescription = createEl('p');
          let queryInstance = result.body.indexOf(query);
          itemDescription.textContent = `${result.body.substring(queryInstance, queryInstance + 200)}`;
          item.appendChild(itemDescription);
        } else {
          item.textContent = result.title;
        }
        resultsFragment.appendChild(item);
      });
    }

    if (queryLen >= requiredQueryLen) {
      if (!results.length) {
        showResults.innerHTML = `<span class="search_result">${noMatchesFound}</span>`;
      }
    } else {
      showResults.innerHTML = `<label for="find" class="search_result">${queryLen > 1 ? shortSearchQuery : typeToSearch}</label>`;
    }

    showResults.appendChild(resultsFragment);
  }

  function search(searchTerm, scope = null, passive = false) {
    if (searchTerm.length) {
      let rawResults = index.search(searchTerm);
      rawResults = rawResults.map(function(result) {
        const score = result.score;
        const resultItem = result.item;
        resultItem.score = (parseFloat(score) * 50).toFixed(0);
        return resultItem;
      });

      if (scope) {
        rawResults = rawResults.filter(resultItem => {
          return resultItem.section == scope;
        });
      }

      passive ? searchResults(rawResults, searchTerm, true) : searchResults(rawResults, searchTerm);
    } else {
      passive ? searchResults([], '', true) : searchResults();
    }
  }

  function liveSearch() {
    const searchField = elem(searchFieldClass);

    if (searchField) {
      const searchScope = searchField.dataset.scope;
      searchField.addEventListener('input', function() {
        const searchTerm = searchField.value.trim().toLowerCase();
        search(searchTerm, searchScope);
      });

      if (!searchPageElement) {
        searchField.addEventListener('search', function() {
          const searchTerm = searchField.value.trim().toLowerCase();
          if (searchTerm.length) {
            const scopeParameter = searchScope ? `&scope=${searchScope}` : '';
            window.location.href = new URL(baseURL + `search/?query=${searchTerm}${scopeParameter}`).href;
          }
        });
      }

      const searchTerm = searchField.value.trim().toLowerCase();
      if (searchTerm.length) {
        search(searchTerm, searchScope);
      }
    }
  }

  function passiveSearch() {
    if (searchPageElement) {
      const searchTerm = findQuery();
      const searchScope = findQuery('scope');
      const searchField = elem(searchFieldClass);

      search(searchTerm, searchScope, true);

      if (searchField) {
        searchField.addEventListener('input', function() {
          const currentSearchTerm = searchField.value.trim().toLowerCase();
          search(currentSearchTerm, true);
          wrapText(currentSearchTerm, main);
        });
      }
    }
  }

  let main = elem('main');
  if (!main) {
    main = elem('.main');
  }

  if (!searchPageElement) {
    liveSearch();
  }
  passiveSearch();
}

function highlightSearchTerms(search, context, wrapper = 'mark', cssClass = '') {
  const query = findQuery();
  if (query) {
    let container = elem(context);
    if (!container) {
      return;
    }

    let reg = new RegExp('(' + search + ')', 'gi');

    function searchInNode(parentNode) {
      forEach(parentNode, function(node) {
        if (node.nodeType === 1) {
          searchInNode(node);
        } else if (
          node.nodeType === 3 &&
          reg.test(node.nodeValue)
        ) {
          let string = node.nodeValue.replace(reg, `<${wrapper} class="${cssClass}">$1</${wrapper}>`);
          let span = document.createElement('span');
          span.dataset.searched = 'true';
          span.innerHTML = string;
          parentNode.replaceChild(span, node);
        }
      });
    }

    searchInNode(container);
  }
}

function hasSearchResults() {
  const searchResults = elem('.results');
  if (searchResults) {
    const body = searchResults.innerHTML.length;
    return [searchResults, body];
  }
  return false;
}

function clearSearchResults() {
  let searchResults = hasSearchResults();
  if (searchResults) {
    searchResults = searchResults[0];
    searchResults.innerHTML = '';
    const searchField = elem(searchFieldClass);
    if (searchField) {
      searchField.value = '';
    }
  }
}

function onEscape(fn) {
  window.addEventListener('keydown', function(event) {
    if (event.code === 'Escape') {
      fn();
    }
  });
}

let searchInitialized = false;
let searchIndexPromise = null;

function getSearchIndexUrl() {
  const pageLanguage = elem('body').dataset.lang;
  const searchIndexLangSlug = pageLanguage === defaultSiteLanguage ? '' : `${pageLanguage}/`;
  let searchIndex = `${searchIndexLangSlug}index.json`;
  return new URL(`${baseURL}${searchIndex}`).href;
}

function loadSearchIndex() {
  if (searchInitialized) {
    return Promise.resolve();
  }

  if (searchIndexPromise) {
    return searchIndexPromise;
  }

  searchIndexPromise = fetch(getSearchIndexUrl())
    .then(response => response.json())
    .then(function(data) {
      data = data.length ? data : [];
      if (!searchInitialized) {
        initializeSearch(data);
        searchInitialized = true;
      }
      return data;
    })
    .catch((error) => {
      searchIndexPromise = null;
      console.error(error);
      throw error;
    });

  return searchIndexPromise;
}

function setupSearchUi() {
  highlightSearchTerms(findQuery(), '.post_body', 'mark', 'search-term');

  onEscape(clearSearchResults);

  window.addEventListener('click', function(event) {
    const target = event.target;
    const isSearch = target.closest(searchClass) || target.matches(searchClass);
    if (!isSearch && !elem('#searchpage')) {
      clearSearchResults();
    }
  });

  const searchField = elem(searchFieldClass);
  if (searchField && !elem('#searchpage')) {
    const searchScope = searchField.dataset.scope;
    searchField.addEventListener('keydown', function(event) {
      if (searchInitialized || event.key !== 'Enter') {
        return;
      }

      const searchTerm = searchField.value.trim().toLowerCase();
      if (searchTerm.length) {
        const scopeParameter = searchScope ? `&scope=${searchScope}` : '';
        window.location.href = new URL(baseURL + `search/?query=${searchTerm}${scopeParameter}`).href;
      }
    });
  }
}

function primeSearchIndex() {
  const searchField = elem(searchFieldClass);
  if (!searchField || elem('#searchpage')) {
    return;
  }

  const load = function() {
    loadSearchIndex();
  };

  searchField.addEventListener('focus', load, { once: true, passive: true });
  searchField.addEventListener('input', load, { once: true });
  searchField.addEventListener('pointerdown', load, { once: true, passive: true });
  searchField.addEventListener('touchstart', load, { once: true, passive: true });
}

function bootstrapSearch() {
  setupSearchUi();

  if (elem('#searchpage')) {
    loadSearchIndex();
    return;
  }

  primeSearchIndex();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', bootstrapSearch, { once: true });
} else {
  bootstrapSearch();
}